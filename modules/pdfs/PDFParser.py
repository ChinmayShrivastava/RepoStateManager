from modules.images.ImageReader import ImageReader
from pdf2image import convert_from_path
import logging
import tqdm

class PDFParser(ImageReader):

    def __init__(
            self,
            pdf_path,
            device: str = 'cpu',
            verbose: bool = True,
            ):
        self.verbose = verbose
        if self.verbose:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)
        self.pdf_path = pdf_path
        self.file_name = self.pdf_path.split('/')[-1]
        self.device = device
        self.pdf = convert_from_path(self.pdf_path)
        self.pdf_width, self.pdf_height = self.pdf[0].size
        self.pdf_pixels = self.pdf[0].load()
        self.pdf_pages = len(self.pdf)
        self.pdf_images = []
        for i in tqdm.tqdm(range(self.pdf_pages)):
            image = self.pdf[i].convert("RGB")
            self.pdf_images.append(ImageReader(PIL_image=image, device=device, verbose=self.verbose))
        self.tables_by_page = []
        self.tables_by_page_structure = []
        self.tables_by_page_data = []
        self.chunks = []
        # log
        logging.info('PDFParser initialized.')

    def __str__(self) -> str:
        _str = f"PDFParser for {self.pdf_path}"
        return _str
    
    def _get_chunks(
            self,
            chunk_size: int = 512,
            paragraph_separator: str = '\n\n',
            chunk_overlap: int = 128,
            ):
        from llama_index import SimpleDirectoryReader
        from llama_index.node_parser import SentenceSplitter
        reader = SimpleDirectoryReader(input_files=[self.pdf_path])
        documents = reader.load_data()
        splitter = SentenceSplitter(chunk_size=chunk_size, paragraph_separator=paragraph_separator, chunk_overlap=chunk_overlap)
        nodes = splitter.get_nodes_from_documents(documents)
        # self.chunks = [x.text for x in nodes]
        self.chunks = [
            {
                "text": x.text,
                "metadata": {
                    "page_no": x.metadata["page_label"],
                    "file_type": x.metadata["file_type"],
                    "chunk_no": i,
                }
            } for i, x in enumerate(nodes)
        ]
        return self.chunks
    
    def get_chunks(self):
        return self._get_chunks()