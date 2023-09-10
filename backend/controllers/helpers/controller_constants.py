from enum import Enum, unique

@unique
class FileNames(Enum):
    report: str = "report.json"
    experiment: str = "experiment.json"
    report_data: str = "data.json"
    base_data_csv: str = "base_data.csv"
    carriage_data_csv: str = "carriage_data.csv"

@unique
class ModuleConstant(Enum):
    config: str = "config.json"
    module: str = "module.py"