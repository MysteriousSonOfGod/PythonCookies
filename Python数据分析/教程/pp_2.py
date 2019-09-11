import pandas as pd

countries = pd.read_csv('lahman-csv/countries.csv')
income = pd.read_excel('lahman-csv/income.xlsx', sheetname='Data')
# print(countries.head())
# print(income.head())
income.index = income[income.columns[0]]  # Make the countries as the index
income = income.drop(income.columns[0], axis=1)
income.columns = map(lambda x: int(x), income.columns)  # Convert years from floats to ints
income = income.transpose()
income.head()
