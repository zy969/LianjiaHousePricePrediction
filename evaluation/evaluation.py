import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import warnings
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import scale
from sklearn.model_selection import KFold, cross_val_score
from sklearn.inspection import plot_partial_dependence
from sklearn.metrics import r2_score

warnings.filterwarnings("ignore")

# Load dataset
data = pd.read_csv('data.csv')
Y = data.loc[:, "Price"].values 
X=data.loc[:, [ 'Square_Footage', 'Interior_Finishes',
           'Latitude', 'Longitude',  'Bedrooms', 'Living_Rooms', 'Kitchens', 'Bathrooms','Year_Built',
           'Height','Total_Height', 'Parks','Cinemas','Transportation_Facilities', 'Educational_Institutions',
            'Restaurants', 'Medical_Facilities', 'Fitness_Facilities', 'Shopping_Places', 'Financial_Institutions',
           'East','South','West','North','CPI','PCDI','PCE','GRP','Average_Price','Average_Rent']].values

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42, shuffle = True)


# Correlation analysis
fig, axes = plt.subplots(1, 10, figsize=(16, 1))
arr_x = np.array(X)
arr_y = np.array(Y)
for i, ax in enumerate(axes.ravel()):
    ax.plot(arr_x[::10, i], arr_y[::10], '.', alpha=.5)
    ax.set_xlabel("feature {}".format(i))
    ax.set_ylabel("target y")

# Label distribution
plt.hist(arr_y, bins='auto')
plt.show()

# Scale and covariance
df_scaled = scale(X)
cov = np.cov(df_scaled, rowvar=False)
plt.figure(figsize=(8, 8), dpi=100)
plt.imshow(cov)

plt.xticks(range(35), ['Price','Square_Footage', 'Interior_Structure', 'Building_Type', 'Building_Structure', 'Interior_Finishes',
           'Latitude', 'Longitude',  'Bedrooms', 'Living_Rooms', 'Kitchens', 'Bathrooms', 'Elevator','Year_Built',
           'Height','Total_Height', 'Parks','Cinemas','Transportation_Facilities', 'Educational_Institutions',
            'Restaurants', 'Medical_Facilities', 'Fitness_Facilities', 'Shopping_Places', 'Financial_Institutions',
           'East','South','West','North','CPI','PCDI','PCE','GRP','Average_Price','Average_Rent'],rotation=90)
plt.yticks(range(35), ['Price','Square_Footage', 'Interior_Structure', 'Building_Type', 'Building_Structure', 'Interior_Finishes',
           'Latitude', 'Longitude',  'Bedrooms', 'Living_Rooms', 'Kitchens', 'Bathrooms', 'Elevator','Year_Built',
           'Height','Total_Height', 'Parks','Cinemas','Transportation_Facilities', 'Educational_Institutions',
            'Restaurants', 'Medical_Facilities', 'Fitness_Facilities', 'Shopping_Places', 'Financial_Institutions',
           'East','South','West','North','CPI','PCDI','PCE','GRP','Average_Price','Average_Rent']);
plt.savefig('./a.jpg',bbox_inches='tight')

# Evaluation setup
col = ['MAE', 'MSE', 'RMSE','R2']
idx = ['Random Forest', 'XGBoost', 'Ridge', 'Lasso', 'OLS']
result = pd.DataFrame(index = idx, columns = col)

# Evaluation and visualization function
def evaluate_visualize(pred, name, true=y_test):
    """
    Plots predictions vs true values.
    Calculates and prints metrics: MAE, MSE, RMSE, R2.
    Updates result DataFrame.
    """
    x = range(pred.shape[0])
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(x, true, 'o', label='ground truth', alpha=0.5)
    ax.plot(x, pred, 'o', label=name, alpha=0.5)
    ax.legend(loc='best')
    
    mae = metrics.mean_absolute_error(true, pred)
    mse = metrics.mean_squared_error(true, pred)
    rmse = np.sqrt(metrics.mean_squared_error(true, pred))
    R2 = r2_score(true, pred)
    result.loc[name, :] = [mae, mse, rmse, R2]
    print('Metrics:', mae, mse, rmse, R2)

def plot_importance(some_dict):
    """
    Plots feature importance.
    """
    plt.figure(figsize=(10, 4))
    df = pd.DataFrame(some_dict)
    ax = plt.gca()
    df.plot.bar(ax=ax, width=.9)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlim(-.5, len(df) - .5)
    ax.set_xlabel("feature index")
    ax.set_ylabel("importance value")
    plt.vlines(np.arange(.5, len(df) -1), -1.5, 1.5, linewidth=.5)


# Grid search for best parameters
rf = RandomForestRegressor(random_state=0)
estimator_range = [500, 600, 700, 800]
depth_range = [5, 10, 15, None]

param_grid=[{'n_estimators':estimator_range,'max_depth':depth_range}]
clf_gs = GridSearchCV(estimator=rf,param_grid=param_grid,scoring='neg_mean_absolute_error',cv=10,n_jobs=-1)
gs = clf_gs.fit(X_train,y_train)

# Display best parameters
best_params = gs.best_params_
print("Best parameters:", best_params)

# Train model with best parameters
rf_best = RandomForestRegressor(n_estimators=best_params['n_estimators'], max_depth=best_params['max_depth'], random_state=0)

# K-Fold cross-validation
kfold = KFold(n_splits=5)
cv_scores = cross_val_score(rf_best, X_train, y_train, cv=kfold)
print(f'K-Fold CV average score: {cv_scores.mean():.4f}')

rf_best.fit(X_train, y_train)

# Predict and evaluate
y_pred_rf_best = rf_best.predict(X_test)
evaluate_visualize(y_pred_rf_best, 'Random Forest')

# Partial dependence plot
fig = plot_partial_dependence(rf, X_train, range(34), n_cols=10,
                                       feature_names=['Square_Footage', 'Interior_Structure', 'Building_Type', 'Building_Structure', 'Interior_Finishes',
           'Latitude', 'Longitude',  'Bedrooms', 'Living_Rooms', 'Kitchens', 'Bathrooms', 'Elevator','Year_Built',
           'Height','Total_Height', 'Parks','Cinemas','Transportation_Facilities', 'Educational_Institutions',
            'Restaurants', 'Medical_Facilities', 'Fitness_Facilities', 'Shopping_Places', 'Financial_Institutions',
           'East','South','West','North','CPI','PCDI','PCE','GRP','Average_Price','Average_Rent'], grid_resolution=50)

