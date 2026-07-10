from abc import ABC, abstractmethod


class DataMiner(ABC):
    """
    Role: DataMiner
    Description: Core participant in the Data Miner.Py structure.
    """

    def mine(self, file_path: str):

        self.open_file(file_path)

        self.extract_data()

        self.parse_data()

        self.analyze_data()

        self.export_report()

        self.close_file()

    # =====================================================
    # Steps (abstract)
    # =====================================================

    @abstractmethod
    def open_file(self, file_path: str):
        pass

    @abstractmethod
    def extract_data(self):
        pass

    @abstractmethod
    def parse_data(self):
        pass

    @abstractmethod
    def close_file(self):
        pass

    # =====================================================
    # Steps (concrete shared)
    # =====================================================

    def analyze_data(self):

        print("Analyzing data using shared logic...")

    def export_report(self):

        print("Exporting report (common implementation)...")