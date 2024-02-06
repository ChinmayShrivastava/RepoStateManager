from abc import ABC, abstractmethod
# from llama_index.llms.openai import OpenAI

class BaseTableReader(ABC):
    def __init__(
            self, 
            pdf_path, 
            verbose: bool = True,
            # llm: OpenAI = OpenAI(model="gpt-3.5-turbo"),
            ):
        self.verbose = verbose
        self.pdf_path = pdf_path

    @abstractmethod
    def _extract_all_tables(self):
        pass

    @abstractmethod
    def _extract_structure_from_all_pdf(self):
        pass

    @abstractmethod
    def _extract_data_from_all_pdf(self):
        pass

    @abstractmethod
    def _extract_data_from_all_pdf_csv(self):
        pass

    @abstractmethod
    def extract_tables_from_pdf_page(self, page_number):
        return self.tables_by_page[page_number-1]
    
    @abstractmethod
    def extract_structure_from_pdf_page(self, page_number):
        return self.tables_by_page_structure[page_number-1]
    
    @abstractmethod
    def extract_data_from_pdf_page(self, page_number):
        return self.tables_by_page_data[page_number-1]
    
    @abstractmethod
    def extract_data_from_pdf_page_csv(self, page_number):
        return self.tables_by_page_data_csv[page_number-1]
    
    @abstractmethod
    def extract_all_tables(self):
        return self.tables_by_page
    
    @abstractmethod
    def extract_all_structure(self):
        return self.tables_by_page_structure
    
    @abstractmethod
    def _extract_all_data(self):
        pass

    @abstractmethod
    def extract_all_data(self):
        pass