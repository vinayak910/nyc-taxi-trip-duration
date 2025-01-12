import sys
import logging
import pandas as pd
from yaml import safe_load
from pathlib import Path
from src.logger import create_log_path , CustomLogger
from sklearn.model_selection import train_test_split


log_file_path = create_log_path(module_name= "make_dataset")
my_logger = CustomLogger(logger_name= "make_dataset",log_filename= log_file_path)
my_logger.set_log_level(level=logging.INFO)


def load_raw_data(input_path: Path)->pd.DataFrame:
    raw_data = pd.read_csv(input_path)
    rows , columns = raw_data.shape
    my_logger.save_logs(msg = f"Read {input_path.stem} data having {rows} rows and {columns} columns.",
                        log_level= 'info')
    return raw_data


def train_val_split(data:pd.DataFrame , test_size:float , 
                     random_state:int)->tuple[pd.DataFrame , pd.DataFrame]:
    
    train_data , val_data = train_test_split(data , test_size= test_size ,
                                             random_state=random_state)

    my_logger.save_logs(msg=f'Data is split into train split with shape {train_data.shape} and val split with shape {val_data.shape}',
                             log_level='info')
    my_logger.save_logs(msg=f'The parameter values are {test_size} for test_size and {random_state} for random_state',
                             log_level='info')
    
    return train_data , val_data


def save_data(data: pd.DataFrame , output_path:Path):
    data.to_csv(output_path, index = False)
    my_logger.save_logs(msg=f'{output_path.stem + output_path.suffix} data saved successfully to the output folder',
                            log_level='info')

def read_params(input_file):

    try:
        with open(input_file) as f:
            params_file = safe_load(f)
        
    except FileNotFoundError as e:
        my_logger.save_logs(msg = "Parameters file not found , Switching to dfault values for train test split",log_level= 'error')

        default_dict = {'test_size':0.25,
                        'random_state':None}
        test_size = default_dict["test_size"]
        random_state = default_dict["random_state"]
        return test_size , random_state
    
    else:
        my_logger.save_logs(msg= "Parameters file read successfully",log_level= 'info')
        test_size = params_file['make_dataset']['test_size']
        random_state = params_file['make_dataset']['random_state']
        return test_size , random_state

def main():

    input_file_name = sys.argv[1]
    current_path = Path(__file__)
    root_path = current_path.parent.parent.parent
    interim_data_path = root_path/"data"/"interim"
    interim_data_path.mkdir(exist_ok= True)
    raw_data_path = root_path/"data"/"raw"/"extracted"/input_file_name
    
    # func -> to convert data to df 
    raw_df = load_raw_data(input_path= raw_data_path)
    # func to read params file 
    test_size , random_state = read_params("params.yaml")

    train_df , val_df = train_val_split(data = raw_df, test_size= test_size , random_state= random_state)

    save_data(data = train_df , output_path= interim_data_path/"train.csv")
    save_data(data = val_df , output_path= interim_data_path/"val.csv")

if __name__ == '__main__':
    main()
    