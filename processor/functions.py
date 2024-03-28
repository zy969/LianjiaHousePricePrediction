import pandas as pd
import numpy as np
import re
from typing import Tuple

def exclude(df, drop_grid) -> Tuple[pd.DataFrame]:
    """Remove specified values."""
    for col_name in list(drop_grid.keys()):
        print("**********\n","For feature:",col_name,":")
        for value in drop_grid[col_name]:
            before = df.shape[0]
            df = df[df[col_name].str.contains(value)==False]
            after = df.shape[0]
            no_dropped = before - after 
            print("  string:",value,",",no_dropped,"values are dropped")
        print("")
    return df

def subset_by_iqr(df, col_list, whisker_width=1.5) -> pd.DataFrame:
    """Remove outliers using IQR."""
    for column in col_list:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        up = q3 + whisker_width * iqr
        df.loc[df[column] >= up, column] = up
    return df

def normal(m) -> np.ndarray:
    """Normalize data."""
    return (m - np.min(m)) / (np.max(m) - np.min(m))

def replace_values(df, column_name, replacements) -> pd.DataFrame:
    """Replace column values."""
    for old_value, new_value in replacements.items():
        df.loc[df[column_name] == old_value, column_name] = new_value
    return df

def parse_housing_data(df) -> pd.DataFrame:
    """Parse housing data."""
    rooms, halls, kitchens, toilets, current_floors, total_floors, areas = [], [], [], [], [], [], []
    errors = []
    for n in range(len(df)):
        try:
            housing_type = df['房屋户型'][n]
            room_info = re.findall(r'(.)室(.)厅(.)厨(.)卫', housing_type, re.S)[0]
            rooms.append(int(room_info[0]))
            halls.append(int(room_info[1]))
            kitchens.append(int(room_info[2]))
            toilets.append(int(room_info[3]))

            floor_info = df['所在楼层'][n]
            current_floors.append(re.findall(r'(.)楼层', floor_info, re.S)[0])
            total_floors.append(int(re.findall('共(.*?)层', floor_info)[0]))

            area_info = df['建筑面积'][n]
            areas.append(float(re.findall(r'(.*?)㎡.*', area_info, re.S)[0]))
        except:
            errors.append(n)

    df = df.drop(errors)
    df.index = range(len(df))
    df['卧室'] = rooms
    df['客厅'] = halls
    df['厨房'] = kitchens
    df['卫生间'] = toilets
    df['当前楼层'] = current_floors
    df['总楼层数'] = total_floors
    df['建筑面积'] = areas
    return df


