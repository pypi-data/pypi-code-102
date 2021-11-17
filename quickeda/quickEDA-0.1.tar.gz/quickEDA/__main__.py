import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from quickEDA import dataframe
from scipy import stats

def main():
    def desc_fn(df):
        print('\n')
        print(f'Statistical information of dataset')
        return df.describe()


    def info_fn(df):
        print('\n')
        print(f'Overview of dataset')
        return df.info()


    def dtype_fn(df):
        print('\n')
        print('Data types')
        return df.dtypes


    def head_fn(df):
        print('\n')
        print('Sample - First 5 rows')
        return df.head()


    def tail_fn(df):
        print('\n')
        print('Sample - Last 5 rows')
        return df.tail()


    def corr_fn(df):
        print('\n')
        print('Correlation')
        return df.corr()


    def shape_fn(df):
        print('\n')
        print("Shape of data")
        global cols
        cols = df.shape[1]
        print(f'Number of columns: {df.shape[1]}')
        print(f'Number of Rows: {df.shape[0]}')
        return df.shape


    def missing_fn(df):
        print('\n')
        print('Overall missing values')
        return df.isna().sum()


    def missing_cell_fn(df):
        print('\n')
        missing_cell = df.isna().sum()
        cmiss = 0
        tot_missing = 0
        for x in range(cols):

            tot_missing = tot_missing + missing_cell[x]
            if missing_cell[x] > 0:
                cmiss = cmiss + 1
        tot_percent = (tot_missing / (df.shape[0] * df.shape[1])) * 100
        print(f'Missing cells: {cmiss}')
        print(f'Missing Percentage: {tot_percent}')


    def dup_fn(df):
        print('\n')
        print(f'Duplicate Rows: {df.duplicated().sum()}')
        print(f'Duplicate %: {(df.duplicated().sum() / (df.shape[0] * df.shape[1])) * 100}')
        return df[df.duplicated()]


    def plot_fn(df):
        print('\n')
        print('Scatter matrix')
        sns.pairplot(df)
        plt.show()

        print('\n')
        print('Box Plot')
        plt.figure(figsize=(15, 7))
        sns.boxplot(data=data)
        plt.show()


    def col_fn(df):
        plotnumber = 1
        plotnumber1 = 1
        fig = plt.figure()
        for x in df.columns:
            print('\n')
            print(f'Feature    : {x}')
            print(f'Distinct   : {len(data[x].unique())}')
            print(f'Distinct % : {(len(data[x].unique()) / len(data[x])) * 100}')
            if len(data[x].unique()) <= 20:
                print(f'Unique values are {data[x].unique()}')
            print(f'Missing    : {df[x].isna().sum()}')
            print(f'Missing %  : {(df[x].isna().sum() / len(data[x])) * 100}')
            print(f'Zeroes     : {(df[x] == 0).sum()}')
            print(f'Zeroes %   : {((df[x] == 0).sum() / len(data[x])) * 100}')
            print(df[x].describe())
            if df[x].dtype == 'int64' or df[x].dtype == 'float64':
                IQR = stats.iqr(df[x], interpolation='midpoint')
                print(f'IQR        : {IQR}')
                Q1 = np.percentile(df[x], 25, interpolation='midpoint')
                Q3 = np.percentile(df[x], 75, interpolation='midpoint')
                upper = (Q3 + 1.5 * IQR)
                lower = (Q1 - 1.5 * IQR)
                print(f'Upper_limit : {upper}  Lower_limit : {lower}')
                lower_outliers = list(data[x].iloc[np.where((data[x] < lower))])
                upper_outliers = list(data[x].iloc[np.where((data[x] > upper))])
                print(f'Total Lower Outliers : {len(lower_outliers)}')
                print(f'Total Upper Outliers : {len(upper_outliers)}')
                print(f'Lower Outliers % : {(len(lower_outliers) / len(df[x])) * 100}')
                print(f'Upper Outliers % : {(len(upper_outliers + lower_outliers) / len(df[x])) * 100}')
                print(f'Outliers % : {(len(upper_outliers) / len(df[x])) * 100}')
                print(f'Lower Outliers are {lower_outliers}')
                print(f'Upper Outliers are {upper_outliers}')

                print('Spread')
                if plotnumber <= len(df.columns):
                    plt.figure(figsize=(15, 15), facecolor='white')
                    ax = plt.subplot(4, 4, plotnumber)
                    sns.distplot(df[x])
                    plt.xlabel(x, fontsize=10)
                    plt.show()
                plotnumber += 1

                print(f'Correlation between {x} and Target ')
                if plotnumber1 <= len(df.columns):
                    plt.figure(figsize=(15, 15), facecolor='white')
                    ax = plt.subplot(4, 4, plotnumber1)
                    plt.scatter(df[x], df.iloc[:, -1])
                    plt.xlabel(x, fontsize=10)
                    plt.ylabel('Target', fontsize=10)
                    plt.show()
                plotnumber1 += 1
            print('\n')

    def eda(dataset):
        data = DataFrame(dataset).readcsv()
        print(f'Start time : {datetime.datetime.now()}')
        fn_list = [desc_fn, info_fn, dtype_fn, head_fn, tail_fn, corr_fn, shape_fn, missing_fn, missing_cell_fn, dup_fn,
               plot_fn, col_fn]
        for i in fn_list:
            j = i(data)

        print(f'End time : {datetime.datetime.now()}')

if __name__ == "__main__":
    main()