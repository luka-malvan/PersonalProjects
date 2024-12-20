# LIBRARIES
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

import warnings
warnings.filterwarnings("ignore")

# ----- SOME USEFUL INSTANCE -----
# lists with seasons and models
seasons = [2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002]
models = ['SVM', 'Random Forest']

# path for results file
file_path_metrics = 'C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION/Results/metrics.txt'
file_path_average_metrics = 'C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION/Results/average_metrics.txt'
file_path_parameters = 'C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION/Results/best_parameters.txt'
file_path_results_old_seasons = 'C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION/Results/results_old_seasons.txt'
file_path_results_MVP_2024 = 'C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION/Results/results_MVP_2024.txt'
file_path_results_ROY_2024 = 'C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION/Results/results_ROY_2024.txt'

# ----- FILES' READ -----
# files for old season
totals_2020_2002_df = pd.read_csv("C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION/Data_Used/Player_Totals_2020_2002.csv")
per_game_2020_2002_df = pd.read_csv("C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION/Data_Used/Player_Per_Game_2020_2002.csv")
advanced_2020_2002_df = pd.read_csv("C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION//Data_Used/Advanced_2020_2002.csv")
team_summaries_2020_2002_df = pd.read_csv("C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION//Data_Used/Team_Summaries_2020_2002.csv")
# files for 2024 season
totals_2024_df = pd.read_csv("C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION/Data_Used/Player_Totals_2024.csv")
per_game_2024_df = pd.read_csv("C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION/Data_Used/Player_Per_Game_2024.csv")
advanced_2024_df = pd.read_csv("C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION/Data_Used/Advanced_2024.csv")
team_summaries_2024_df = pd.read_csv("C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION/Data_Used/Team_Summaries_2024.csv")
# MVPs file
awards_2020_2002_df = pd.read_csv("C:/Users/lucam/OneDrive/Desktop/PersonalProjects/NBA_MVP_ROY_PREDICTION/Data_Used/MVPs.csv", sep = ';')

# ----- DATA PROCESSING -----
# creation of some empty datasets
data = pd.DataFrame()
data_2024 = pd.DataFrame()
data_rookie_2024 = pd.DataFrame()

# for old and 2024 seasons merge files with players' stats in one file, so totals, per_game, advanced
# old season
data = totals_2020_2002_df.merge(per_game_2020_2002_df, on=['player', 'season', 'tm'], how='left', validate='m:1').fillna(0)
data = data.merge(advanced_2020_2002_df, on=['player','season', 'tm'], how='left', validate='m:1')
# 2024 season
data_2024 = totals_2024_df.merge(per_game_2024_df, on=['player', 'season', 'tm'], how='left', validate='m:1').fillna(0)
data_2024 = data_2024.merge(advanced_2024_df, on=['player','season', 'tm'], how='left', validate='m:1')

# calculate pct for every team and add it as a statistics for every player
# old season
standings_2020_2002_df = pd.DataFrame()
standings_2020_2002_df = team_summaries_2020_2002_df.copy()
standings_2020_2002_df = standings_2020_2002_df.rename(columns={'abbreviation':'tm'})
standings_2020_2002_df = standings_2020_2002_df[['season', 'tm', 'w','l']]
standings_2020_2002_df['pct'] = round(standings_2020_2002_df['w']/(standings_2020_2002_df['w']+standings_2020_2002_df['l']), 3)
# pct for old seasons calculated
data = data.merge(standings_2020_2002_df, on=['season', 'tm'], how='left', validate='m:1')
# 2024 season
standings_2024_df = pd.DataFrame()
standings_2024_df = team_summaries_2024_df.copy()
standings_2024_df = standings_2024_df.rename(columns={'abbreviation':'tm'})
standings_2024_df = standings_2024_df[['season', 'tm', 'w','l']]
standings_2024_df['pct'] = round(standings_2024_df['w']/(standings_2024_df['w']+standings_2024_df['l']), 3)
# pct for 2024 calculated
data_2024 = data_2024.merge(standings_2024_df, on=['tm'], how='left', validate='m:1')

# substituting eventual * in player's name
data['player'] = data['player'].str.replace('*','')

data_2024['player'] = data_2024['player'].str.replace('*','')

#copy data_2024 in an empty dataset for rookie prediction
data_rookie_2024 = data_2024.copy()

# our datasets are too much so make they smaller
# mantain only these columns for old seasons
data = data[['season', 'player', 'tm', 'g_x', 'fg_percent_x', 'mp_per_game',
             'fga_per_game', 'trb_per_game', 'ast_per_game', 'pts_per_game', 'per', 'pct']]
data = data.rename(columns={'g_x': 'g', 'fg_percent_x': 'fg_percent'})
# mantain only these columns for 2024 season
data_2024 = data_2024[['player', 'tm', 'g_x', 'fg_percent_x', 'mp_per_game',
             'fga_per_game', 'trb_per_game', 'ast_per_game', 'pts_per_game', 'per', 'pct']]
data_2024 = data_2024.rename(columns={'g_x': 'g', 'fg_percent_x': 'fg_percent'})
# mantain these columns for rookie, add the experience, that will be equal to 1
data_rookie_2024 = data_rookie_2024[['player', "experience", 'tm', 'g_x', 'fg_percent_x', 'mp_per_game',
             'fga_per_game', 'trb_per_game', 'ast_per_game', 'pts_per_game', 'per', 'pct']]
data_rookie_2024 = data_rookie_2024.rename(columns={'g_x': 'g', 'fg_percent_x': 'fg_percent'})

# add in old seasons file the mvps file
data = data.merge(awards_2020_2002_df, on=['player','season'], how='left', validate='m:1').fillna(0)

# ----- FILTER DATA -----
# there are many players, so filter they with some historical stats
# removing duplicate lines for traded players because never has an MVP been traded in the middle of the season that he won the award
# Karl Malone was MVP in 98-99 with 49 games
# Giannis Antetokounmpo was MVP in 19-20 with 30.4 min
# Wes Unseld was MVP at 68-69 with 13.8 PPG and with 10.9 FGA
# Steve Nash was MVP at 04-05 with 3.3 REB
# Moses Malone was MVP at 82-83 with 1.3 AST
# Bob Cousy was MVP at 56-57 with 37.8% FG
# Dave Cowens was MVP at 72-73 with a PER of 18.1
# Bob Pettit was MVP at 55-56 with a pct of .458

# create others empty dataframes
dataf = pd.DataFrame()
dataf_2024 = pd.DataFrame()
dataf_rookie_2024 = pd.DataFrame

# old seasons
for season in seasons:
    data_season = data[data['season'] == season]
    data_season = data_season.drop_duplicates(subset=['player'], keep='first')
    dataf = pd.concat([dataf, data_season], ignore_index=True)

dataf = dataf[((dataf['g']>48)
              &(dataf['mp_per_game']>30)
              &(dataf['pts_per_game']>13.5)&(dataf['fga_per_game']>10)
              &(dataf['trb_per_game']>3)
              &(dataf['ast_per_game']>1)
              &(dataf['fg_percent']>0.37)
              &(dataf['per']>18)
              &(dataf['pct']>0.457))
              | (dataf['MVP Votes Share']>0)].reset_index(drop=True)

# 2024 season, so don't count g and votes share
data_2024 = data_2024.drop_duplicates(subset=['player'], keep='first')
dataf_2024 = data_2024.copy()

dataf_2024 = dataf_2024[(
            (dataf_2024['mp_per_game']>30)
           &(dataf_2024['pts_per_game']>13.5)&(dataf_2024['fga_per_game']>10)
           &(dataf_2024['trb_per_game']>3)
           &(dataf_2024['ast_per_game']>1)
           &(dataf_2024['fg_percent']>0.37)
           &(dataf_2024['per']>18)
           &(dataf_2024['pct']>0.457))].reset_index(drop=True)

# rookie 2024, so add experience == 1
data_rookie_2024 = data_rookie_2024.drop_duplicates(subset=['player'], keep='first')
dataf_rookie_2024 = data_rookie_2024.copy()

#here we have different historical statistics
# every rookie must have be only one year of experience
# Malcolm Brogdon won ROY in 16-17 with 26.4 mp
# Malcolm Brogdon won ROY in 16-17 with 10.2 pts per game
# Malcolm Brogdon won ROY in 16-17 with 8.5 fga per game
# Phil Ford won ROY in 78-79 with 2.3 trb per game
# Woody Sauldsberry won ROY in 57-58 with 0.8 ast per game
# Maurice Stokes won ROY in 55-56 with 35.4% fg
# Woody Sauldsberry won ROY in 57-58 with 10.7 per
# Andrew Wiggins won ROY in 14-15 with a pct .152
dataf_rookie_2024 = dataf_rookie_2024[(
                   (dataf_rookie_2024['experience']==1)
                  &(dataf_rookie_2024['mp_per_game']>26.3)
                  &(dataf_rookie_2024['pts_per_game']>10.1)
                  &(dataf_rookie_2024['fga_per_game']>8.4)
                  &(dataf_rookie_2024['trb_per_game']>2.2)
                  &(dataf_rookie_2024['ast_per_game']>0.7)
                  &(dataf_rookie_2024['fg_percent']>0.34)
                  &(dataf_rookie_2024['per']>10)
                  &(dataf_rookie_2024['pct']>0.151))].reset_index(drop=True)

# now our datasets, datafs, are ready to be used

# ----- MODELLING -----
# old seasons
final_results = pd.DataFrame()
metrics = pd.DataFrame()
best_params = []

for season in seasons:
  # use likely a k-fold cross, one season as test set, others as training set
  current_season = season
  data_train = dataf[dataf['season'] != current_season]
  data_test = dataf[dataf['season'] == current_season]

  # remove meaningless columns and predict votes share
  X_train = data_train.drop(['MVP Votes Share', 'MVP Rank', 'player', 'season', 'tm'], axis = 1)
  y_train = data_train['MVP Votes Share']
  X_test = data_test.drop(['MVP Votes Share', 'MVP Rank', 'player', 'season', 'tm'], axis = 1)
  y_test = data_test['MVP Votes Share']

  initial_results = data_test[['player', 'season', 'MVP Votes Share', 'MVP Rank']]
  results = data_test[['player', 'season', 'MVP Votes Share', 'MVP Rank']]

  # data normalization
  scaler = StandardScaler()

  scaled_X_train = scaler.fit_transform(X_train)
  scaled_X_test = scaler.fit_transform(X_test)

  # search best parameters with GridSearch for our models
  # some parameters are already setted to speed up the compiling phase, see report for more details
  for model_name in models:
    if model_name == 'SVM':
      param_grid = {
                    'C' : [0.001,0.01,0.1,0.5,1,2,5,10],
                    'kernel' : ['poly'], # instead ['linear', 'rbf', 'poly']
                    'gamma' : ['scale', 'auto'],
                    'degree' : [2,3,4],
                    'epsilon' : [0.1,0.5,1]
                   }
      svr_model = SVR()
      grid = GridSearchCV(svr_model, param_grid)
      grid.fit(scaled_X_train, y_train)
      model = SVR(**grid.best_params_)
      best_params.append({'race':'MVP','model': 'SVM', 'season': season, 'params': grid.best_params_})

    elif model_name == 'Random Forest':
      param_grid = {
                    'n_estimators' : [1,10,20,30,40,50,100,150,200],
                    'max_features' : [1,2,3,4,5,6,7],
                    'bootstrap' : [True, False],
                    'oob_score' : [True]
                   }
      rfc = RandomForestRegressor()
      grid = GridSearchCV(rfc, param_grid)
      grid.fit(scaled_X_train, y_train)
      model = RandomForestRegressor(**grid.best_params_)
      best_params.append({'race':'MVP','model': 'Random Forest', 'season': season, 'params': grid.best_params_})

    # clean model name
    model_name_clean = model_name.replace(' ', '_').replace('(', '').replace(')', '')

    # fit and predict
    model.fit(scaled_X_train, y_train)
    y_pred = model.predict(scaled_X_test)

    # CALCULATE METRIC
    # define rmse
    rmse = round(np.sqrt(mean_squared_error(y_test, y_pred)),3)

    dict_metrics = {
                    'model' : [model_name_clean],
                    'season' : [season],
                    'RMSE' : [rmse]
                   }

    # put computed metrics in a df
    metric = pd.DataFrame(data = dict_metrics)

    # concatenate all metrics in an other df
    metrics = pd.concat([metrics,metric])

    # RESULT'S CLEANING
    temp1 = initial_results.copy()

    # create a columns with feature and predictions and sort it
    temp1['Predicted MVP Share '+str(model_name_clean)] = pd.Series(y_pred).values
    results_sorted = temp1.sort_values(by='Predicted MVP Share '+str(model_name_clean), ascending = False).reset_index(drop=True)

    # add column rank with the rank in MVP race
    results_sorted['MVP Rank '+str(model_name_clean)] = results_sorted.index + 1

    results = results.merge(results_sorted, on=['player','season','MVP Votes Share','MVP Rank'])

  final_results = pd.concat([final_results,results], ignore_index=True)
  # so in results we calculate the results for one season for each model
  # in final_results we concatenate the results of all seasons

# CLEANING FILE FINAL_RESULTS
results_old_seasons = pd.DataFrame()
n_rank = 3 # we want only top3 for each season

for season in final_results['season'].unique():
  # put in temp2 all season statistics
  temp2 = final_results[final_results['season'] == season]
  seasonal_rank = pd.DataFrame()

  real_rank = temp2.sort_values(by='MVP Votes Share', ascending=False)[:n_rank].reset_index(drop=True)
  seasonal_rank['MVP Rank Real'] = real_rank['player']
  seasonal_rank['MVP Share Real'] = real_rank['MVP Votes Share']

  for model in models:
    try:
      model_name_clean = model.replace(' ', '_').replace('(', '').replace(')', '')
      temp3 = temp2.sort_values(by='Predicted MVP Share '+str(model_name_clean),ascending=False)[:n_rank].reset_index(drop=True)
      seasonal_rank['MVP Rank '+str(model_name_clean)] = temp3['player']
      seasonal_rank['MVP Share '+str(model_name_clean)] = round(temp3['Predicted MVP Share '+str(model_name_clean)], 3)
    except:
      continue

  seasonal_rank['season'] = season
  results_old_seasons = pd.concat([results_old_seasons, seasonal_rank], ignore_index=True)

results_old_seasons.to_csv(file_path_results_old_seasons, index=False, sep='\t')
print('MVPs ranks for old seasons are predicted! Check file results_old_season')



# 2024 season MVP
x_test_2024 = dataf_2024.drop(['player','tm'], axis=1)
initial_results_2024 = dataf_2024[['player']]
results_2024 = dataf_2024[['player']]

# normalization
scaled_X_test_2024 = scaler.transform(x_test_2024)

results_MVP_2024 = pd.DataFrame()

for model_name in models:
  if model_name == 'SVM':
    param_grid = {
                  'C' : [0.001,0.01,0.1,0.5,1,2,5,10],
                  'kernel' : ['poly'], # instead ['linear', 'rbf', 'poly']
                  'gamma' : ['scale', 'auto'],
                  'degree' : [2,3,4],
                  'epsilon' : [0.1,0.5,1]
                  }
    svr_model = SVR()
    grid = GridSearchCV(svr_model, param_grid)
    grid.fit(scaled_X_train, y_train)
    model = SVR(**grid.best_params_)
    best_params.append({'race':'MVP','model': 'SVM', 'season': '2024', 'params': grid.best_params_})

  elif model_name == 'Random Forest':
    param_grid = {
                  'n_estimators' : [1,10,20,30,40,50,100,150,200],
                  'max_features' : [1,2,3,4,5,6,7],
                  'bootstrap' : [True, False],
                  'oob_score' : [True]
                 }
    rfc = RandomForestRegressor()
    grid = GridSearchCV(rfc, param_grid)
    grid.fit(scaled_X_train, y_train)
    model = RandomForestRegressor(**grid.best_params_)
    best_params.append({'race':'MVP','model': 'Random Forest', 'season': '2024', 'params': grid.best_params_})

  # clean model name
  model_name_clean = model_name.replace(' ', '_').replace('(', '').replace(')', '')

  # use the training set used also for 2002 season
  model.fit(scaled_X_train, y_train)
  y_pred_2024 = model.predict(scaled_X_test_2024)

  temp4 = initial_results_2024.copy()

  temp4['Predicted MVP Share '+str(model_name_clean)] = pd.Series(y_pred_2024).values
  results_sorted_2024 = temp4.sort_values(by='Predicted MVP Share '+str(model_name_clean), ascending = False).reset_index(drop=True)
  results_sorted_2024['MVP Rank '+str(model_name_clean)] = results_sorted_2024.index + 1

  results_MVP_2024 = pd.concat([results_MVP_2024, results_sorted_2024], axis=1)

# clean result's file for MVP season 2024
results_MVP_2024 = results_MVP_2024.round(3).head(10)

results_MVP_2024.to_csv(file_path_results_MVP_2024, index=False, sep='\t')
print('MVPs rank for season 2024 is predicted! Check file results_MVP_2024')




# season 2024 rookie
x_test_rookie_2024 = dataf_rookie_2024.drop(['player','experience','tm'], axis=1)
initial_results_rookie_2024 = dataf_rookie_2024[['player']]
results_rookie = dataf_rookie_2024[['player']]

# normalization
scaled_x_test_rookie_2024 = scaler.transform(x_test_rookie_2024)

results_ROY_2024 = pd.DataFrame()

for model_name in models:
  if model_name == 'SVM':
    param_grid = {
                  'C' : [0.001,0.01,0.1,0.5,1,2,5,10],
                  'kernel' : ['poly'], # instead ['linear', 'rbf', 'poly']
                  'gamma' : ['scale', 'auto'],
                  'degree' : [2,3,4],
                  'epsilon' : [0.1,0.5,1]
                  }
    svr_model = SVR()
    grid = GridSearchCV(svr_model, param_grid)
    grid.fit(scaled_X_train, y_train)
    model = SVR(**grid.best_params_)
    best_params.append({'race':'ROY','model': 'SVM', 'season': '2024', 'params': grid.best_params_})

  elif model_name == 'Random Forest':
    param_grid = {
                  'n_estimators' : [1,10,20,30,40,50,100,150,200],
                  'max_features' : [1,2,3,4,5,6,7],
                  'bootstrap' : [True, False],
                  'oob_score' : [True]
                 }
    rfc = RandomForestRegressor()
    grid = GridSearchCV(rfc, param_grid)
    grid.fit(scaled_X_train, y_train)
    model = RandomForestRegressor(**grid.best_params_)
    best_params.append({'race':'ROY','model': 'Random Forest', 'season': '2024', 'params': grid.best_params_})

  # clean model name
  model_name_clean = model_name.replace(' ', '_').replace('(', '').replace(')', '')

  model.fit(scaled_X_train, y_train)
  y_pred_rookie_2024 = model.predict(scaled_x_test_rookie_2024)

  temp5 = initial_results_rookie_2024.copy()

  temp5['Predicted ROY Share '+str(model_name_clean)] = pd.Series(y_pred_rookie_2024).values
  results_sorted_rookie_2024 = temp5.sort_values(by='Predicted ROY Share '+str(model_name_clean),ascending=False).reset_index(drop=True)
  results_sorted_rookie_2024['ROY Rank ' + str(model_name_clean)] = results_sorted_rookie_2024.index + 1

  results_ROY_2024 = pd.concat([results_ROY_2024, results_sorted_rookie_2024], axis=1)

  # clean result's file for ROY season 2024, the votes shares are based for MVPs not for rookies, so delete them, we only want a rank
  results_ROY_2024 = results_ROY_2024.drop('Predicted ROY Share '+str(model_name_clean),axis=1)

results_ROY_2024.to_csv(file_path_results_ROY_2024, index=False, sep='\t')
print('ROYs rank for season 2024 is predicted! Check file results_ROY_2024')

# FINISH WITH METRICS AND LAST FILES
def media_metrics(metrics):
    # now calculate average values for both models
    average_metrics = pd.DataFrame()

    for model in metrics['model'].unique():
        metric = metrics[metrics['model']==model]
        rmse = round(metric['RMSE'].mean(),3)

        dict_met = {'model': [model],
                    'RMSE': [rmse]
                    }

        support2 = pd.DataFrame(data=dict_met)
        average_metrics = pd.concat([average_metrics, support2], ignore_index=True)
    return average_metrics

average_metrics = media_metrics(metrics)
average_metrics.to_csv(file_path_average_metrics, index=False, sep='\t')
metrics.to_csv(file_path_metrics, index=False, sep='\t')
print('Metrics file is created. Check metrics for all metrics in all seasons. Check average_metrics for an average of it')

with open(file_path_parameters, 'w') as file:
    for dict in best_params:
        file.write(str(dict) + '\n')
print('Parameters used are in file parameters')