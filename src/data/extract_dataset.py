import logging 
from zipfile import ZipFile
from pathlib import Path
from src.logger import create_log_path , CustomLogger


log_file_path = create_log_path(module_name= "extract_dataset")

custom_logger = CustomLogger(logger_name= "extract_dataset", log_filename= log_file_path)

custom_logger.set_log_level(level = logging.INFO)


def extract_zipfile(input_path:Path , output_path: Path):
    
    with ZipFile(file = input_path) as f:
        f.extractall(path = output_path)
        input_file_name = input_path.stem + input_path.suffix
        custom_logger.save_logs(msg = f"{input_file_name} extracted succesfully at the target path")


def main():

    current_path = Path(__file__)
    root_path = current_path.parent.parent.parent
    input_path = root_path/"data"/"raw"/"zipped"
    output_path = root_path/"data"/"raw"/"extracted"
    output_path.mkdir(parents=True, exist_ok=True)
    
    extract_zipfile(input_path = input_path/"train.zip" , output_path= output_path)
    extract_zipfile(input_path = input_path/"test.zip" , output_path= output_path)


if __name__ == "__main__":
    # call the main function
    main()