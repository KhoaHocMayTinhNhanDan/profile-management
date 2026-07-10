from ..abstract_class.data_miner import DataMiner


class CSVDataMiner(DataMiner):

    def open_file(self, file_path: str):
        print(f"Opening CSV file: {file_path}")

    def extract_data(self):
        print("Extracting CSV rows...")

    def parse_data(self):
        print("Parsing CSV format...")

    def close_file(self):
        print("Closing CSV file...")