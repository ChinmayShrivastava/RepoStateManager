from modules.pdfs.PDFParser import PDFParser
from modules.images.ImageReader import ImageReader
from transformers import AutoModelForObjectDetection, TableTransformerForObjectDetection
import torch
import logging
import numpy as np
import csv
import easyocr
from tqdm.auto import tqdm
from .base import BaseTableReader

def get_cell_coordinates_by_row(table_data):
    # Extract rows and columns
    rows = [entry for entry in table_data if entry['label'] == 'table row']
    columns = [entry for entry in table_data if entry['label'] == 'table column']

    # Sort rows and columns by their Y and X coordinates, respectively
    rows.sort(key=lambda x: x['bbox'][1])
    columns.sort(key=lambda x: x['bbox'][0])

    # Function to find cell coordinates
    def find_cell_coordinates(row, column):
        cell_bbox = [column['bbox'][0], row['bbox'][1], column['bbox'][2], row['bbox'][3]]
        return cell_bbox

    # Generate cell coordinates and count cells in each row
    cell_coordinates = []

    for row in rows:
        row_cells = []
        for column in columns:
            cell_bbox = find_cell_coordinates(row, column)
            row_cells.append({'column': column['bbox'], 'cell': cell_bbox})

        # Sort cells in the row by X coordinate
        row_cells.sort(key=lambda x: x['column'][0])

        # Append row information to cell_coordinates
        cell_coordinates.append({'row': row['bbox'], 'cells': row_cells, 'cell_count': len(row_cells)})

    # Sort rows from top to bottom
    cell_coordinates.sort(key=lambda x: x['row'][1])

    return cell_coordinates

def get_cell_coordinates_by_column(table_data):
    # Extract rows and columns
    rows = [entry for entry in table_data if entry['label'] == 'table row']
    columns = [entry for entry in table_data if entry['label'] == 'table column']

    # Sort rows and columns by their Y and X coordinates, respectively
    rows.sort(key=lambda x: x['bbox'][1])
    columns.sort(key=lambda x: x['bbox'][0])

    # Function to find cell coordinates
    def find_cell_coordinates(row, column):
        cell_bbox = [column['bbox'][0], row['bbox'][1], column['bbox'][2], row['bbox'][3]]
        return cell_bbox

    # Generate cell coordinates and count cells in each row
    cell_coordinates = []

    for column in columns:
        column_cells = []
        for row in rows:
            cell_bbox = find_cell_coordinates(row, column)
            column_cells.append({'row': row['bbox'], 'cell': cell_bbox})

        # Sort cells in the row by X coordinate
        column_cells.sort(key=lambda x: x['row'][1])

        # Append row information to cell_coordinates
        cell_coordinates.append({'column': column['bbox'], 'cells': column_cells, 'cell_count': len(column_cells)})

    # Sort rows from top to bottom
    cell_coordinates.sort(key=lambda x: x['column'][0])

    return cell_coordinates

def apply_ocr(cell_coordinates, cropped_table, reader):
    # let's OCR row by row
    data = dict()
    max_num_columns = 0
    for idx, row in enumerate(tqdm(cell_coordinates)):
      row_text = []
      for cell in row["cells"]:
        # crop cell out of image
        cell_image = np.array(cropped_table.crop(cell["cell"]))
        # apply OCR
        result = reader.readtext(np.array(cell_image))
        if len(result) > 0:
          # print([x[1] for x in list(result)])
          text = " ".join([x[1] for x in result])
          row_text.append(text)

      if len(row_text) > max_num_columns:
          max_num_columns = len(row_text)

      data[idx] = row_text

    print("Max number of columns:", max_num_columns)

    # pad rows which don't have max_num_columns elements
    # to make sure all rows have the same number of columns
    for row, row_data in data.copy().items():
        if len(row_data) != max_num_columns:
          row_data = row_data + ["" for _ in range(max_num_columns - len(row_data))]
        data[row] = row_data

    return data

def objects_to_crops(img, tokens, objects, class_thresholds, padding=10):
    """
    Process the bounding boxes produced by the table detection model into
    cropped table images and cropped tokens.
    """

    table_crops = []
    for obj in objects:
        if obj['score'] < class_thresholds[obj['label']]:
            continue

        cropped_table = {}

        bbox = obj['bbox']
        bbox = [bbox[0]-padding, bbox[1]-padding, bbox[2]+padding, bbox[3]+padding]

        cropped_img = img.crop(bbox)

        table_tokens = [token for token in tokens if iob(token['bbox'], bbox) >= 0.5]
        for token in table_tokens:
            token['bbox'] = [token['bbox'][0]-bbox[0],
                             token['bbox'][1]-bbox[1],
                             token['bbox'][2]-bbox[0],
                             token['bbox'][3]-bbox[1]]

        # If table is predicted to be rotated, rotate cropped image and tokens/words:
        if obj['label'] == 'table rotated':
            cropped_img = cropped_img.rotate(270, expand=True)
            for token in table_tokens:
                bbox = token['bbox']
                bbox = [cropped_img.size[0]-bbox[3]-1,
                        bbox[0],
                        cropped_img.size[0]-bbox[1]-1,
                        bbox[2]]
                token['bbox'] = bbox

        cropped_table['image'] = cropped_img
        cropped_table['tokens'] = table_tokens

        table_crops.append(cropped_table)

    return table_crops

class TableReader(PDFParser, BaseTableReader):

    def __init__(
            self,
            pdf_path,
            verbose: bool = True,
            ):
        self.verbose = verbose
        self.model = AutoModelForObjectDetection.from_pretrained("microsoft/table-transformer-detection", revision="no_timm")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.srmodel = TableTransformerForObjectDetection.from_pretrained("microsoft/table-structure-recognition-v1.1-all")
        self.ocrreader = easyocr.Reader(['en'])
        # self.model.eval()
        # log
        logging.info('TableReader initialized.')
        super().__init__(pdf_path=pdf_path,
                         device=self.device,
                         verbose=self.verbose)

    def __str__(self) -> str:
        _str = f"{self.model.config.id2label}"
        return _str
    
    def _forward_pass_on_image(
            self,
            pixel_values,
            model
        ):
        with torch.no_grad():
            outputs = model(pixel_values)
        logging.info("outputs.logits.shape: ", end="")
        logging.info(outputs.logits.shape)
        return outputs
    
    # for output bounding box post-processing
    def _box_cxcywh_to_xyxy(self, x):
        x_c, y_c, w, h = x.unbind(-1)
        b = [(x_c - 0.5 * w), (y_c - 0.5 * h), (x_c + 0.5 * w), (y_c + 0.5 * h)]
        return torch.stack(b, dim=1)


    def _rescale_bboxes(self, out_bbox, size):
        img_w, img_h = size
        b = self._box_cxcywh_to_xyxy(out_bbox)
        b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
        return b
    
    def _update_id2label(self, id2label, model):
        id2label = model.config.id2label
        id2label[len(model.config.id2label)] = "no object"
        return id2label
    
    def _outputs_to_objects(self, outputs, img_size, model):
        id2label = self._update_id2label(model.config.id2label, model)
        m = outputs.logits.softmax(-1).max(-1)
        pred_labels = list(m.indices.detach().cpu().numpy())[0]
        pred_scores = list(m.values.detach().cpu().numpy())[0]
        pred_bboxes = outputs['pred_boxes'].detach().cpu()[0]
        pred_bboxes = [elem.tolist() for elem in self._rescale_bboxes(pred_bboxes, img_size)]

        objects = []
        for label, score, bbox in zip(pred_labels, pred_scores, pred_bboxes):
            class_label = id2label[int(label)]
            if not class_label == 'no object':
                objects.append({'label': class_label, 'score': float(score),
                                'bbox': [float(elem) for elem in bbox]})
                
        logging.info("objects: ")
        logging.info(objects)
        return objects
    
    def _crop_table_from_image(self, image, objects) -> list:
        class_thresholds = {'table': 0.5, 'table rotated': 0.5, "no object": 10}
        tokens = []
        table_crops = objects_to_crops(image, tokens, objects, class_thresholds, padding=10)
        return table_crops
    
    def _extract_tables_from_pdf_page_index(self, page_index):
        page = self.pdf_images[page_index]
        outputs = self._forward_pass_on_image(page.pixel_values, self.model)
        objects = self._outputs_to_objects(outputs, page.image.size, self.model)
        table_crops = self._crop_table_from_image(page.image, objects)
        return table_crops
    
    def extract_tables_from_pdf_page(self, page_number):
        return self._extract_tables_from_pdf_page_index(page_number-1)
    
    def _extract_all_tables(self):
        for page in range(self.pdf_pages):
            table_crops = self._extract_tables_from_pdf_page_index(page)
            self.tables_by_page.append([ImageReader(PIL_image=x['image'], device=self.device, is_structure=True) for x in table_crops])
        return self.tables_by_page
    
    def _extract_structure_from_table(self, table_crop: ImageReader):
        outputs = self._forward_pass_on_image(table_crop.pixel_values, self.srmodel)
        cells = self._outputs_to_objects(outputs, table_crop.image.size, self.srmodel)
        logging.info("cells: ")
        logging.info(cells)
        return cells
    
    def _extract_structure_from_all_pdf(self):
        for page in range(self.pdf_pages):
            tables = self.tables_by_page[page]
            _structure = []
            for table in tables:
                cells = self._extract_structure_from_table(table)
                _structure.append(cells)
            self.tables_by_page_structure.append(_structure)
        return self.tables_by_page_structure
    
    def _extract_data_from_table(self, table_crop: ImageReader, cells):
        cell_coordinates = get_cell_coordinates_by_column(cells)
        data = apply_ocr(cell_coordinates, table_crop.image, self.ocrreader)
        return data
    
    def extract_all_data(self):
        self._extract_all_tables()
        self._extract_structure_from_all_pdf()
        for page in range(self.pdf_pages):
            tables = self.tables_by_page[page]
            _data = []
            for table in tables:
                cells = self.tables_by_page_structure[page][tables.index(table)]
                data = self._extract_data_from_table(table, cells)
                _data.append(data)
            self.tables_by_page_data.append(_data)
        return self.tables_by_page_data