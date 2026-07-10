from ..template_method_pattern.abstract_class.data_miner import (
    DataMiner,
)

from ..template_method_pattern.concrete_class.csv_data_miner import (
    CSVDataMiner,
)

from ..template_method_pattern.concrete_class.pdf_data_miner import (
    PDFDataMiner,
)


def run_client():
    """
    Modular Mode: Client Entry Point
    UML Role: Client
    Key Logic: Instantiates concrete subsystems and drives the pattern execution flow.
    """print("=" * 50)
    print("CSV DATA MINER")
    print("=" * 50)

    csv = CSVDataMiner()
    csv.mine("data.csv")

    print("\n" + "=" * 50)
    print("PDF DATA MINER")
    print("=" * 50)

    pdf = PDFDataMiner()
    pdf.mine("data.pdf")