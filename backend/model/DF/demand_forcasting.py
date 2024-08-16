import numpy as np
import pandas as pd
import lightgbm as lgb
import warnings
import os
import matplotlib.pyplot as plt
import plotly.express as px

warnings.filterwarnings('ignore')

def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Nunique #####################")
    print(dataframe.nunique())
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

def create_date_features(df):
    df['month'] = df.date.dt.month
    df['day_of_month'] = df.date.dt.day
    df['day_of_year'] = df.date.dt.dayofyear
    df['day_of_week'] = df.date.dt.dayofweek
    df['year'] = df.date.dt.year
    df["is_wknd"] = df.date.dt.weekday // 4
    df['is_month_start'] = df.date.dt.is_month_start.astype(int)
    df['is_month_end'] = df.date.dt.is_month_end.astype(int)
    return df

def random_noise(dataframe):
    return np.random.normal(scale=1.6, size=(len(dataframe),))

def lag_features(dataframe, lags):
    for lag in lags:
        dataframe['sales_lag_' + str(lag)] = dataframe.groupby(["store", "item"])['sales'].transform(
            lambda x: x.shift(lag)) + random_noise(dataframe)
    return dataframe

def roll_mean_features(dataframe, windows):
    for window in windows:
        dataframe['sales_roll_mean_' + str(window)] = dataframe.groupby(["store", "item"])['sales']. \
                                                          transform(
            lambda x: x.shift(1).rolling(window=window, min_periods=10, win_type="triang").mean()) + random_noise(
            dataframe)
    return dataframe

def ewm_features(dataframe, alphas, lags):
    for alpha in alphas:
        for lag in lags:
            dataframe['sales_ewm_alpha_' + str(alpha).replace(".", "") + "_lag_" + str(lag)] = \
                dataframe.groupby(["store", "item"])['sales'].transform(lambda x: x.shift(lag).ewm(alpha=alpha).mean())
    return dataframe

def smape(preds, target):
    n = len(preds)
    masked_arr = ~((preds == 0) & (target == 0))
    preds, target = preds[masked_arr], target[masked_arr]
    num = np.abs(preds - target)
    denom = np.abs(preds) + np.abs(target)
    smape_val = (200 * np.sum(num / denom)) / n
    return smape_val

def lgbm_smape(preds, train_data):
    labels = train_data.get_label()
    smape_val = smape(np.expm1(preds), np.expm1(labels))
    return 'SMAPE', smape_val, False

def train_model(train_df, val_df):
    cols = [col for col in train_df.columns if col not in ['date', 'id', 'sales', 'year']]

    Y_train = train_df['sales']
    X_train = train_df[cols]

    Y_val = val_df['sales']
    X_val = val_df[cols]

    lgb_params = {'num_leaves': 10,
                  'learning_rate': 0.02,
                  'feature_fraction': 0.8,
                  'max_depth': 5,
                  'verbose': 0,
                  'num_boost_round': 1000,
                  'early_stopping_rounds': 200,
                  'nthread': -1}

    lgbtrain = lgb.Dataset(data=X_train, label=Y_train, feature_name=cols)
    lgbval = lgb.Dataset(data=X_val, label=Y_val, reference=lgbtrain, feature_name=cols)

    model = lgb.train(
        lgb_params,
        lgbtrain,
        valid_sets=[lgbtrain, lgbval],
        callbacks=[lgb.early_stopping(lgb_params['early_stopping_rounds'])]
    )

    return model, cols

def predict_sales(model, test_df, cols):
    X_test = test_df[cols]
    test_preds = model.predict(X_test, num_iteration=model.best_iteration)
    return np.expm1(test_preds)

def save_predictions(preds, test_df, output_path):
    output_df = test_df[['id']].copy()
    output_df['sales'] = preds
    output_df.to_csv(output_path, index=False)

def plot_sales_trend(df, output_path):
    fig = px.line(df, x='date', y='sales', title='Sales Trend Over Time')
    fig.write_html(output_path)

def plot_store_sales(df, output_path):
    if 'store' not in df.columns:
        print(f"'store' column not found in DataFrame. Skipping plot_store_sales.")
        return
    
    fig = px.bar(df.groupby('store').agg({'sales': 'sum'}).reset_index(),
                 x='store', y='sales', title='Total Sales per Store')
    fig.write_html(output_path)

def process_data(train_file, test_file, output_file, plot_folder):
    train = pd.read_csv(train_file, parse_dates=['date'])
    test = pd.read_csv(test_file, parse_dates=['date'])

    df = pd.concat([train, test], sort=False)
    df = create_date_features(df)

    df = lag_features(df, [91, 98, 105, 112, 119, 126, 182, 364, 546, 728])
    df = roll_mean_features(df, [365, 546])
    df = ewm_features(df, [0.95, 0.9, 0.8, 0.7, 0.5], [91, 98, 105, 112, 180, 270, 365, 546, 728])
    df = pd.get_dummies(df, columns=['store', 'item', 'day_of_week', 'month'])
    df['sales'] = np.log1p(df["sales"].values)

    train_df = df.loc[(df["date"] < "2017-01-01"), :]
    val_df = df.loc[(df["date"] >= "2017-01-01") & (df["date"] < "2017-04-01"), :]

    model, cols = train_model(train_df, val_df)

    test_df = df.loc[df.sales.isna()]
    test_preds = predict_sales(model, test_df, cols)

    save_predictions(test_preds, test_df, output_file)

    # Plot graphs and save them as HTML
    plot_sales_trend(df.loc[~df.sales.isna()], os.path.join(plot_folder, 'sales_trend.html'))
    plot_store_sales(df.loc[~df.sales.isna()], os.path.join(plot_folder, 'store_sales.html'))

if __name__ == "__main__":
    process_data('train.csv', 'test.csv', 'forecast_results.csv', 'plots')