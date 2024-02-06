from modules.pdfs.PDFParser import PDFParser
from .base import BaseTableReader
import camelot
import logging
import tqdm
from img2table.ocr import EasyOCR
from img2table.document import PDF
from .conversion.df2graph import Dataframe2Graph
import networkx as nx

class TextTableReader(PDFParser, BaseTableReader):

    def __init__(
            self,
            pdf_path,
            extract_using: str = 'img2table', # camelot or img2table
            confidence: float = 55.0, # percentage of whitespace in a table
            G: nx.Graph = nx.DiGraph(),
            verbose: bool = True,
            ):
        self.verbose = verbose
        if self.verbose:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)
        self.extract_using = extract_using
        self._extraction_dispatcher = {
            'camelot': self._extract_all_data_camelot,
            'img2table': self._extract_all_tables_img2table,
        }
        if extract_using == 'img2table':
            self.ocr = EasyOCR()
        else:
            self.ocr = None
        self.confidence = confidence
        self.G = G
        super().__init__(pdf_path=pdf_path, verbose=self.verbose)
        # log
        logging.info('TextTableReader initialized.')

    def __str__(self) -> str:
        _str = f"TextTableReader for {self.pdf_path}"
        return _str
    
    def _extract_all_data_camelot(self):
        for i in tqdm.tqdm(range(self.pdf_pages)):
            pg_no = i + 1
            logging.info(f'Extracting tables from page {pg_no}...')
            tables = camelot.read_pdf(self.pdf_path, pages=str(pg_no), flavor='lattice') # flavor='lattice'
            table_data = []
            # for each table in page, make a pandas df and append to table_data
            for table in tables:
                if table.parsing_report['whitespace'] < self.confidence:
                    table_data.append({
                        "page": pg_no,
                        "confidence": 100-int(table.parsing_report['whitespace']),
                        "accuracy": table.parsing_report['accuracy'],
                        "title": None, # to implement for camelot still, img2table has this
                        "dataframe": table.df})
            self.tables_by_page_data.append(table_data)
            self.tables_by_page_structure.append(tables)
        return
    
    def _extract_all_tables_img2table(self):
        doc = PDF(self.pdf_path)
        extracted_tables = doc.extract_tables(ocr=self.ocr,
                            implicit_rows=False,
                            borderless_tables=False,
                            min_confidence=self.confidence)
        for page_no in extracted_tables.keys():
            tables = extracted_tables[page_no]
            table_data = []
            for table in tables:
                table_data.append({
                    "page": page_no,
                    "confidence": 'UNKNOWN', # to implement for img2table still, camelot has this
                    "accuracy": 'UNKNOWN', # to implement for img2table still, camelot has this
                    "title": table.title,
                    "dataframe": table.df})
            self.tables_by_page_data.append(table_data)
            self.tables_by_page_structure.append(tables)
        return
    
    def _extract_all_data(self):
        self._extraction_dispatcher[self.extract_using]()
        for page in self.tables_by_page_data:
            for table in page:
                if self.extract_using == 'camelot':
                    df2g = Dataframe2Graph.from_camelot_extracted_table(table['dataframe'], table['title'], G=self.G, verbose=self.verbose)
                elif self.extract_using == 'img2table':
                    df2g = Dataframe2Graph.from_img2table_extracted_table(table['dataframe'], table['title'], G=self.G, verbose=self.verbose)
                self.G = df2g()
        self.get_chunks()
        return
    
    def extract_all_data(self):
        self._extract_all_data()
        logging.info(f'Extracted all data from {self.pdf_path}.')
        return
    
    def _extract_all_tables(self):
        pass

    def _extract_structure_from_all_pdf(self):
        pass

    def _extract_data_from_all_pdf(self):
        pass

    def _extract_data_from_all_pdf_csv(self):
        pass

    def extract_tables_from_pdf_page(self, page_number):
        pass
    
    def extract_structure_from_pdf_page(self, page_number):
        pass
    
    def extract_data_from_pdf_page(self, page_number):
        pass
    
    def extract_data_from_pdf_page_csv(self, page_number):
        pass
    
    def extract_all_tables(self):
        pass
    
    def extract_all_structure(self):
        pass