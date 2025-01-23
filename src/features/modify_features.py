import sys
import logging
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
from pathlib import Path
from src.logger import CustomLogger , create_log_path


TARGET_COLUMN = "trip_duration"
PLOT_PATH = Path("reports/figures/target_distribution.png")



log_file_path = create_log_path('modify_features')
my_logger = CustomLogger(logger_name= "modify_features",log_filename=log_file_path)
my_logger.set_log_level(level = logging.INFO)


def convert_target_to_minutes(df:pd.DataFrame , target_column:str)->pd.DataFrame:
    df.loc[: , target_column] =  df[target_column]/60
    my_logger.save_logs(msg = "Target column converted from seconds to minutes")
    return df 


def drop_above_two_hundred_minutes(df: pd.DataFrame , target_column:str)->pd.DataFrame:
    filter_series = df[target_column]<=200
    new_df = df.loc[filter_series , :].copy()

    max_value = new_df[target_column].max()
    my_logger.save_logs(msg = f"The max value in the target column after transformation is {max_value} ")

    if max_value<=200:
        return new_df
    else:
        raise ValueError("Outlier target values not removed from data")

def plot_target(df:pd.DataFrame , target_column: str , save_path:Path):
    root_path_copy = root_path
    my_logger.save_logs(f'Plot path: {PLOT_PATH}')
    my_logger.save_logs(f"TOTAL - {root_path_copy / PLOT_PATH} ")

    sns.kdeplot(data = df , x = target_column)
    plt.title(f"Distribution of {target_column}")
    plt.savefig(save_path)
    my_logger.save_logs(msg = "Distribution plot saved at destination")


def drop_columns(df: pd.DataFrame )->pd.DataFrame:
    my_logger.save_logs(f"Columns in data before removal are {list(df.columns)}")

    if 'dropoff_datetime' in df.columns:
        columns_to_drop = ['id' ,'dropoff_datetime','store_and_fwd_flag']

        df_after_removal = df.drop(columns= columns_to_drop)
        
    else:
        columns_to_drop = ['id' ,'store_and_fwd_flag']
        df_after_removal = df.drop(columns= columns_to_drop)
    my_logger.save_logs(msg = f'Columns in data after removal are {list(df_after_removal.columns)}')

    return df_after_removal

def make_datetime_features(df:pd.DataFrame)->pd.DataFrame:
    new_df = df.copy()
    o_rows , o_cols = new_df.shape
    new_df['pickup_datetime'] = pd.to_datetime(new_df['pickup_datetime'])
    my_logger.save_logs(f'pickup_datetime converted to datetime {new_df['pickup_datetime'].dtype}')

    new_df.loc[: , 'pickup_hour'] = new_df['pickup_datetime'].dt.hour
    new_df.loc[: , 'pickup_date'] = new_df['pickup_datetime'].dt.day
    new_df.loc[: , 'pickup_month'] = new_df['pickup_datetime'].dt.month
    new_df.loc[: , 'pickup_day'] = new_df['pickup_datetime'].dt.weekday
    new_df.loc[: , 'is_weekend'] = new_df.apply(lambda row : row['pickup_day']>=5 , axis = 1).astype('int')

    # drop off reduntant datetime 
    new_df.drop(columns= ['pickup_datetime'],inplace= True)

    n_rows , n_cols = new_df.shape
    my_logger.save_logs(msg = f"The number of columns increased by 4 verify = {n_cols == (o_cols + 5 - 1)}")
    my_logger.save_logs(msg = f'The number of rows remaind the same  verify = {o_rows ==n_rows}')
    return new_df 

def remove_passengers(df: pd.DataFrame )->pd.DataFrame:
    # list of pas.. to keep 
    passengers_to_include = list(range(1 , 7))
    # filter out rows which matches the passenger
    new_df_filter = df['passenger_count'].isin(passengers_to_include)
    new_df = df.loc[new_df_filter,:]
    unique_passenger = list(np.sort(new_df['passenger_count'].unique()))
    my_logger.save_logs(msg = f"The unique passenger list is {unique_passenger} verify = {unique_passenger == passengers_to_include}")
    return new_df

def input_modifications(df:pd.DataFrame)->pd.DataFrame:
    # drop the columns
    new_df = drop_columns(df)
    # remove excluded passengers 
    df_passengers_modification = remove_passengers(new_df)
    # add datetime features
    df_with_datetime_features = make_datetime_features(df_passengers_modification)
    my_logger.save_logs('Modifications with the input feature are complete')
    return df_with_datetime_features

def target_modifications(df: pd.DataFrame , target_column:str = TARGET_COLUMN)->pd.DataFrame:

    # convert to minutes
    minutes_df = convert_target_to_minutes(df,target_column)
    # remove values greater than 200
    target_outlier_removal_df = drop_above_two_hundred_minutes(minutes_df,target_column)
    #plot the target
    plot_target(df = target_outlier_removal_df,target_column=target_column,save_path=root_path / PLOT_PATH )
    my_logger.save_logs("Modifications with the target column are complete")
    return target_outlier_removal_df

# read the df from location 
def read_data(data_path):
    df = pd.read_csv(data_path)
    return df

# save the dataframe to location 
def save_data(df: pd.DataFrame , save_path: Path):
    df.to_csv(save_path , index = False)


def main(data_path , filename):
    df = read_data(data_path)

    df_input_modifications = input_modifications(df)

    if filename == 'train.csv' or filename == 'val.csv':
        df_final = target_modifications(df_input_modifications , TARGET_COLUMN)
    else:
        df_final = df_input_modifications

    return df_final 

if __name__ == "__main__":
    for i in range(1 , 4):
        input_file_path = sys.argv[i]

        current_path = Path(__file__)

        root_path = current_path.parent.parent.parent
        # input data path 
        data_path = root_path/input_file_path

        filename = data_path.parts[-1]

        df_final = main(data_path=input_file_path , filename=filename)

        output_path = root_path/ "data/processed/transformations"
        output_path.mkdir(parents=True , exist_ok= True)
        save_data(df_final , output_path/filename)
        my_logger.save_logs(msg=f'{filename} saved at the destination folder')
        
