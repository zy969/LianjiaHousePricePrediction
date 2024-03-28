import pandas as pd
from processor.functions import exclude, subset_by_iqr, normal, replace_values, parse_housing_data


# Load data
df = pd.read_csv('rawdata.csv')
df = parse_housing_data(df)


# Integrate amenities
交通设施 = df["交通_公交站"] + df["交通_地铁站"]
教育 = df["教育_小学"] + df["教育_中学"] + df["教育_幼儿园"] + df["教育_大学"]
美食 = df["生活_咖啡馆"] + df["生活_餐厅"] 
医疗 = df["医疗_医院"] + df["医疗_药店"] 
运动健身 = df["娱乐_健身房"] + df["娱乐_体育馆"]
购物 = df["购物_商场"] + df["购物_市场"] + df["购物_超市"] 
金融 = df["生活_ATM"] + df["生活_银行"]
娱乐 = df["娱乐_公园"] + df["娱乐_电影院"]

df["Transportation_Facilities"] = 交通设施
df["Educational_Institutions"] = 教育 
df["Restaurants"] = 美食
df["Medical_Facilities"] = 医疗
df["Fitness_Facilities"] = 运动健身
df["Shopping_Places"] = 购物
df["Financial_Institutions"] = 金融
df["Entertainment_Facilities"] = 娱乐
df["Price"]= df["价格"]
df["Square_Footage"]= df["建筑面积"]  
df["Building_Type"]= df["建筑类型"]  
df["Building_Structure"]= df["建筑结构"] 
df["Interior_Finishes"]= df["装修情况"] 
df["Interior_Structure"]= df["户型结构"] 
df["Bedrooms"]= df["卧室"] 
df["Living_Rooms"]= df["客厅"] 
df["Kitchens"]= df["厨房"] 
df["Bathrooms"]= df["卫生间"] 
df["Total_Height"]= df["楼层数"] 
df["Height"]= df["楼层高度"] 
df["Longitude"]= df["经度"] 
df["Latitude"]= df["纬度"] 
df["Parks"]= df["娱乐_公园"]
df["Cinemas"]= df["娱乐_电影院"]
df['Region']=df['区域']
df['Price'] = df['价格']
df['Elevator'] = df['电梯']
df['Year_Built'] = df['建成年代']
df["East"]=df["东"]
df["South"]=df["南"]
df["West"]=df["西"]
df["North"]=df["北"]
df["CPI"] =df["居民消费价格指数"]
df["PCDI"] =df["居民人均可支配收入"]
df["PCE"] =df["居民人均消费支出"]
df["GRP"] =df["地区生产总值"]
df["Average_Price"] =df["月平均房价"]
df["Average_Rent"] =df["月平均租金"]

selected = ['Region','Price', 'Square_Footage', 'Interior_Structure', 'Building_Type', 'Building_Structure', 'Interior_Finishes',
           'Latitude', 'Longitude',  'Bedrooms', 'Living_Rooms', 'Kitchens', 'Bathrooms', 'Elevator','Year_Built',
           'Height','Total_Height', 'Parks','Cinemas','Entertainment_Facilities','Transportation_Facilities', 'Educational_Institutions', 'Restaurants', 'Medical_Facilities', 'Fitness_Facilities', 'Shopping_Places', 'Financial_Institutions',
           'East','South','West','North','CPI','PCDI','PCE','GRP','Average_Price','Average_Rent']
df = df[selected]


# Exclude specified values from DataFrame
drop_grid = {"Building_Type":["暂无数据","平房","框架结构","混合结构","钢结构","砖混结构","平房","别墅"],#剔除异常值
             "Building_Structure":["钢结构","未知","暂无数据","未知结构"], 
             "Region":["nan"],
             "Elevator":["暂无数据"],
             }
df = exclude(df,drop_grid)



# Replace values for encoding
replacements_interior_finishes = {
    '精装     ': 1,
    '简装     ': 2,
    '其他     ': 3,
    '毛坯     ': 4
}
df = replace_values(df, 'Interior_Finishes', replacements_interior_finishes)

replacements_height = {
    '低': 1,
    '中': 2,
    '高': 3
}
df = replace_values(df, 'Height', replacements_height)

replacements_interior_structure = {
    '暂无数据              ': 1,
    '平层              ': 1,
    '复式              ': 2,
    '错层              ': 3,
    '跃层              ': 4
}
df = replace_values(df, 'Interior_Structure', replacements_interior_structure)

replacements_building_type = {
    '塔楼       ': 2,
    '板塔结合       ': 3,
    '板楼       ': 1
}
df = replace_values(df, 'Building_Type', replacements_building_type)

replacements_building_structure = {
    '混合结构  ': 5,
    '框架结构  ': 4,
    '砖木结构  ': 3,
    '砖混结构  ': 2,
    '钢混结构  ': 1
}
df = replace_values(df, 'Building_Structure', replacements_building_structure)

replacements_total_height = {
    '低': 1,
    '中': 2,
    '高': 3
}
df.loc[df['Total_Height'] < 8, 'Total_Height'] = 1
df.loc[(df['Total_Height'] >= 8) & (df['Total_Height'] < 20), 'Total_Height'] = 2
df.loc[df['Total_Height'] >= 20, 'Total_Height'] = 3

replacements_elevator = {
    '无           ': 0,
    '有           ': 1
}
df = replace_values(df, 'Elevator', replacements_elevator)

replacements_region = {
    '嘉定': 3,
    '闵行': 2,
    '浦东': 1,
    '宝山': 4,
    '松江': 5,
    '普陀': 6,
    '杨浦': 7,
    '长宁': 8,
    '徐汇': 9,
    '奉贤': 10,
    '青浦': 11,
    '虹口': 12,
    '静安': 13,
    '金山': 14
}
df = replace_values(df, 'Region', replacements_region)




# Exceptional value removal and normalization
col_list = ["Price","Square_Footage",
"Bedrooms","Living_Rooms","Kitchens","Bathrooms","Parks","Cinemas","Entertainment_Facilities",
"Height","Total_Height","Transportation_Facilities","Educational_Institutions"	,
"Restaurants","Medical_Facilities","Fitness_Facilities","Shopping_Places","Financial_Institutions"]

df = subset_by_iqr(df,col_list,whisker_width=3)

columns_to_normalize = [
    "Bedrooms", "Living_Rooms", "Kitchens", "Bathrooms", "Transportation_Facilities", 
    "Parks", "Entertainment_Facilities", "Educational_Institutions", "Restaurants", 
    "Medical_Facilities", "Fitness_Facilities", "Shopping_Places", "Financial_Institutions",
    "Square_Footage", "Year_Built", "CPI", "PCDI", "PCE", "GRP", "Cinemas", 
    "Average_Price", "Average_Rent", "Latitude", "Longitude"
]

for column in columns_to_normalize:
    df[column] = normal(df[column].astype('float'))


df.to_csv('data.csv')
print(df.isnull().sum())
