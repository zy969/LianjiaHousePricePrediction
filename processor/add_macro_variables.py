import pandas as pd
import numpy as np
import os

if __name__ == '__main__':
    # Read macro data from Excel
    df1 = pd.read_excel(os.path.join(os.path.dirname(__file__), 'macro.xlsx'))
    
    # Read transaction data from CSV
    df2 = pd.read_csv(r'data.csv', encoding='gbk', sep=",", header=0,on_bad_lines='skip')
    
    # Extract data from df1 for matching
    Month = np.array(df1.iloc[18:, 0])
    Monthly_average = np.array(df1.iloc[18:, 1])
    Consumer_index_price = np.array(df1.iloc[:17, 1])

    m = []
    for i in Month:
        arr = i.split('.')
        if(len(arr[1]) == 1):
            arr[1] = '0' + arr[1]
        m.append(arr[0] + '.' + arr[1])

    # Store average house prices as a dictionary {date: price}
    map1 = {}
    for key, value in zip(m, Monthly_average):
        map1[key] = value

    # Format regions uniformly
    rent_table = np.array(df1.iloc[18:, 3:])
    map2 = {}
    for row in rent_table:
        if(row[0] == '浦东新区'):
            row[0] = '浦东'
        map2[row[0]] = row[1:]

    # Store price consumer index data as a dictionary
    map3 = {}
    for key, value in zip(m[:Consumer_index_price.shape[0]], Consumer_index_price):
        map3[key] = value

    # Extract monthly house prices
    key_df2 = df2['成交时间'].tolist()
    key2_df2 = df2['区域'].tolist()
    key3_df2 = df2['房屋朝向'].tolist()

    monthly_house_price = []
    monthly_area_rent = []
    south = []
    north = []
    east = []
    west = []
    consumer_index = []
    GRP = []
    PCDI = []
    PCE = []

    for x, y, z in zip(key_df2, key2_df2, key3_df2):
        monthly_house_price.append(map1[x[:7]])
        consumer_index.append(map3[x[:7]])
        year, month, _ = x.split('.')
        index = int(year) % 2021*4 + int((int(month) - 1)/3)

        if(index >= map2[y].size):
            index = map2[y].size-1

        monthly_area_rent.append(map2[y][index])

        GRP.append(df1[df1.columns[-3]][index])
        PCDI.append(df1[df1.columns[-2]][index])
        PCE.append(df1[df1.columns[-1]][index])

        north.append(0)
        south.append(0)
        west.append(0)
        east.append(0)

        if('南' in z):
            south[-1] = 1
        if('北' in z):
            north[-1] = 1
        if('西' in z):
            west[-1] = 1
        if('东' in z):
            east[-1] = 1

    # Import data into DataFrame
    df2['Monthly_average_house_price'] = monthly_house_price
    df2['Monthly_average_rent'] = monthly_area_rent
    df2['South'] = south
    df2['North'] = north
    df2['West'] = west
    df2['East'] = east
    df2['Consumer_price_index'] = consumer_index
    df2['Gross_regional_product'] = GRP
    df2['Per_capita_disposable_income'] = PCDI
    df2['Per_capita_consumption_expenditure'] = PCE
    df2.to_csv(os.path.join(os.path.dirname(__file__), 'combined.csv'))
