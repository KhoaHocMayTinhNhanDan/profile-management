from ..abstract_class.data_miner import DataMiner


class PDFDataMiner(DataMiner):

    def open_file(self, file_path: str):
        print(f"Opening PDF file: {file_path}")

    def extract_data(self):
        print("Extracting text from PDF...")

    def parse_data(self):
        print("Parsing PDF structure...")

    def close_file(self):
        print("Closing PDF file...")