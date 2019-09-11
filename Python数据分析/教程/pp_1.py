import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# salaries.ix[salaries.teamID == 'BAL']
# teams = salaries.teamID.unique()
# years = salaries.yearID.unique()
# df = salaries.loc[(salaries['yearID']==2012) & (salaries['teamID']=='BAL')].salary.sum()


a

salaries = pd.read_csv('lahman-csv/Salaries.csv')
teams = pd.read_csv('lahman-csv/Teams.csv')
teams = teams[['yearID', 'teamID', 'W']]  # We only need them
totSalaries = salaries.groupby(['yearID', 'teamID'], as_index=False).sum()
# print(totSalaries.head())
joined = pd.merge(totSalaries, teams, how="inner", on=['yearID', 'teamID'])

teamName = 'OAK'
years = np.arange(2000, 2004)

for yr in years:
    df = joined[joined['yearID'] == yr]
    plt.scatter(df['salary'] / 1e6, df['W'])
    plt.title('Wins versus Salaries in year ' + str(yr))
    plt.xlabel('Total Salary (in millions)')
    plt.ylabel('Wins')
    plt.xlim(0, 180)
    plt.ylim(0, 130)
    plt.grid()
    plt.annotate(teamName,
                 xy=(df['salary'][df['teamID'] == teamName] / 1e6, df['W'][df['teamID'] == teamName]),
                 xytext=(-20, 20), textcoords='offset points', ha='right', va='bottom',
                 bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                 arrowprops=dict(arrowstyle='->', facecolor='black', connectionstyle='arc3,rad=0'))
    plt.show()

teamName = 'OAK'
years = np.arange(1999, 2005)
residData = pd.DataFrame()

for yr in years:
    df = joined[joined['yearID'] == yr]
    x_list = df['salary'].values / 1e6
    y_list = df['W'].values

    # least squares estimates
    A = np.array([x_list, np.ones(len(x_list))])
    y = y_list
    w = np.linalg.lstsq(A.T, y)[0]  # coefficients
    yhat = (w[0] * x_list + w[1])  # regression line
    residData[yr] = y - yhat

residData.index = df['teamID']
residData = residData.T
residData.index = residData.index.format()

residData.plot(title='Residuals from least squares estimates across years', figsize=(15, 8),
               color=map(lambda x: 'blue' if x == 'OAK' else 'gray', df.teamID))
plt.xlabel('Year')
plt.ylabel('Residuals')
plt.show()
