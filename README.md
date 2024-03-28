# Shanghai Second-hand House Price Prediction

## Overview
This project involves scraping second-hand housing data from the Lianjia website for the city of Shanghai and predicting housing prices using machine learning models. It integrates web scraping, data processing, feature engineering, and predictive modeling techniques to provide insights into the real estate market trends in Shanghai.

## Implementation

### Crawler
- **File**: `crawler/crawler.py`
- **Description**: This script serves the purpose of scraping second-hand housing data from the Lianjia website. It extracts essential information such as house title, price, type, floor, area, structure, orientation, building type, renovation condition, and geographical coordinates. Additionally, it utilizes the Baidu Map API to fetch nearby amenities' data, including public transportation stations, medical facilities, entertainment venues, educational institutions, and lifestyle establishments. The collected data is then stored in a CSV file for further analysis and machine learning model training.

### Data Processing and Feature Engineering
- **File**: `processor/add_macro_variables.py`
- **Description**: This script integrates macroeconomic data with transactional information. It reads monthly average house prices, consumer price index, and other macro indicators from an Excel file. Then, it imports transactional data from the previously crawled CSV file. Subsequently, it matches the transactional data with corresponding macroeconomic indicators based on time and region. Finally, the script combines the matched data into a DataFrame and exports the result to a new CSV file.

- **File**: `processor/data_processing.py`
- **Description**: This script initially loads the raw data and then parses housing information. Subsequently, it integrates various amenities information such as transportation facilities, education, dining, medical services, fitness, shopping, finance, and entertainment. Following this, the script creates new columns to represent the integrated information of these amenities and selects a set of key columns including region, price, square footage, interior structure, building type, and more. Afterwards, it excludes specific values from the data, such as "N/A" or "Not applicable", and performs value replacements for encoding purposes on certain columns. Lastly, the script handles exceptional values, normalizes selected columns, and ultimately saves the processed data into a new CSV file.

### Evaluation
- **File**: `evaluation/evaluation.py`
- **Description**: This script contains portions of code for data visualization, machine learning model training, prediction, and evaluation. It serves the purpose of assessing the performance of different models and visualizing important trends and relationships in the data.

## Results

### Correlation Heatmap
The correlation heatmap shows the relationship between features. While some connections exist, overall correlation is weak. ![Correlation Heatmap](plots/correlation_heatmap.png)

### Price Heatmap based on Longitude and Latitude
House prices tend to rise closer to the city center. ![Price Heatmap](plots/price_heatmap.png)

### Model Performance
| Model Name        | Linear Regression | Stacking  | Random Forest | XGBoost | SVR    |
|-------------------|-------------------|-----------|---------------|---------|--------|
| MAE               | 0.4998            | 0.3244    | 0.1981        | 0.1989  | 0.1052 |
| MSE               | 0.4535            | 0.1981    | 0.1095        | 0.1147  | 0.06734|
| RMSE              | 0.6734            | 0.3309    | 0.3169        | 0.3387  | 0.1971 |
| R-squared         | 0.5340            | 0.8874    | 0.8821        | 0.7494  | 0.8918 |

### Scatter Plots
 ![Scatter Plots](plots/scatter_plots.png)
