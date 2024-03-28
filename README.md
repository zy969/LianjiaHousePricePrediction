# Shanghai Second-hand House Price Prediction

## Overview
This project involves scraping second-hand housing data from the [Lianjia website](https://sh.lianjia.com/) for the city of Shanghai and predicting housing prices using machine learning models. It integrates web scraping, data processing, feature engineering, and predictive modeling techniques to provide insights into the real estate market trends in Shanghai.

### Key Methods

- **Web Scraping**: 
  - Scraped housing data from the [Lianjia website](https://sh.lianjia.com/) using `requests`, `lxml`, and `re`, and stored it in CSV format.
  
- **Data Processing**: 
  - Processed the scraped data and integrated macroeconomic data using `pandas` for feature engineering.
  
- **Machine Learning Modeling**: 
  - Implemented machine learning models including Linear Regression, Stacking, Random Forest, XGBoost, and SVR using `scikit-learn`.
  
- **Evaluation**: 
  - Evaluated model performance using metrics such as Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and R-squared. 
  - Visualization using `matplotlib`.

## Implementation

### Crawler
- **File**: [`crawler.py`](https://github.com/zy969/LianjiaHousePricePrediction/blob/main/crawler/crawler.py)
- **Description**: This script serves the purpose of scraping second-hand housing data from the Lianjia website. It extracts essential information such as house title, price, type, floor, area, structure, orientation, building type, renovation condition, and geographical coordinates. Additionally, it utilizes the [Baidu Map API](https://lbsyun.baidu.com/) to fetch nearby amenities' data, including public transportation stations, medical facilities, entertainment venues, educational institutions, and lifestyle establishments. The collected data is then stored in a CSV file for further analysis and machine learning model training.

### Data Processing and Feature Engineering
- **File**: [`add_macro_variables.py`](https://github.com/zy969/LianjiaHousePricePrediction/blob/main/processor/add_macro_variables.py)
- **Description**: This script integrates macroeconomic data with transactional information. It reads monthly average house prices, consumer price index, and other macro indicators from an Excel file. Then, it imports transactional data from the previously crawled CSV file. Subsequently, it matches the transactional data with corresponding macroeconomic indicators based on time and region. Finally, the script combines the matched data into a DataFrame and exports the result to a new CSV file.

- **File**: [`data_processing.py`](https://github.com/zy969/LianjiaHousePricePrediction/blob/main/processor/data_processing.py)
- **Description**: This script initially loads the raw data and then parses housing information. Subsequently, it integrates various amenities information such as transportation facilities, education, dining, medical services, fitness, shopping, finance, and entertainment. Following this, the script creates new columns to represent the integrated information of these amenities and selects a set of key columns including region, price, square footage, interior structure, building type, and more. Afterwards, it excludes specific values from the data, such as "N/A" or "Not applicable", and performs value replacements for encoding purposes on certain columns. Lastly, the script handles exceptional values, normalizes selected columns, and ultimately saves the processed data into a new CSV file.

### Evaluation
- **File**: [`evaluation.py`](https://github.com/zy969/LianjiaHousePricePrediction/blob/main/evaluation/evaluation.py)
- **Description**: This script contains portions of code for data visualization, machine learning model training, prediction, and evaluation. It serves the purpose of assessing the performance of different models and visualizing important trends and relationships in the data.


## Results

### Model Performance
In terms of model performance, the Stacking model outperformed others.
| Model Name        | Linear Regression | Stacking  | Random Forest | XGBoost | SVR    |
|-------------------|-------------------|-----------|---------------|---------|--------|
| MAE               | 0.4998            | 0.3244    | 0.1981        | 0.1989  | 0.1052 |
| MSE               | 0.4535            | 0.1981    | 0.1095        | 0.1147  | 0.06734|
| RMSE              | 0.6734            | 0.3309    | 0.3169        | 0.3387  | 0.1971 |
| R-squared         | 0.5340            | 0.8874    | 0.8821        | 0.7494  | 0.8918 |

### Scatter Plots
 ![Scatter Plots](plots/scatter_plots.png)
### Correlation Heatmap
The correlation heatmap shows the relationship between features. <img src="plots/correlation_heatmap.png" alt="Correlation Heatmap" width="400">

### Price Heatmap based on Longitude and Latitude
 <img src="plots/price_heatmap.png" alt="Price Heatmap" width="400">
