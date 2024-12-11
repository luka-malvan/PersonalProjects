# NBA MVP and ROY Prediction Project
This project was developed as part of the **Data Science and Artificial Intelligence** course at the university. The objective is to predict the **NBA Most Valuable Player (MVP)** and **Rookie of the Year (ROY)** awards using historical player statistics with two different machine learning models: SVM and Random Forest and compare the results.

## Overview
The project analyzes player data spanning several NBA seasons (2002–2024) and implements predictive models to estimate:
1. The MVP vote share for historical seasons.
2. The MVP and ROY rankings for the 2024 NBA season.
Two machine learning models are used:
- **Support Vector Machines (SVM)**
- **Random Forest Regressor**

## Key Features
- **Historical Analysis:** Using player statistics and team performance from 2002 to 2020, the project predicts MVP vote shares and ranks for each season.
- **2024 Predictions:** Based on the latest player and team statistics, the project predicts the top 10 candidates for the MVP and ROY awards.
- **Model Evaluation:** Root Mean Squared Error (RMSE) is calculated for each model to assess prediction accuracy.
- **Grid Search Optimization:** Parameters for both SVM and Random Forest models are optimized using GridSearchCV.

## Dataset
The project uses datasets derived and slimmed down from the comprehensive **NBA/ABA/BAA Stats** dataset available on Kaggle:  
[Kaggle Dataset Link](https://www.kaggle.com/datasets/sumitrodatta/nba-aba-baa-stats/).
### Data Sources
1. **Player Totals (2002–2020 and 2024):** Player cumulative statistics.
2. **Player Per Game (2002–2020 and 2024):** Player averages per game.
3. **Player Advanced Stats (2002–2020 and 2024):** Advanced metrics like Player Efficiency Rating (PER).
4. **Team Summaries (2002–2020 and 2024):** Team win/loss records.
5. **MVP Awards (2002–2020):** Historical MVP vote shares.

### Data Processing
The datasets were:
- Filtered to include only more relevant statistics.
- Slimmed down to focus on MVP and ROY prediction metrics.
- Preprocessed to merge player stats with team performance and normalize features for machine learning.

## Methodology
1. **Data Preparation:**
   - Merged and cleaned data.
   - Filtered player statistics to remove outliers.
   - Normalized features using StandardScaler.
2. **Modeling:**
   - Used historical seasons as training data and predicted for a single season as a test (leave-one-season-out validation).
   - Optimized hyperparameters using GridSearchCV.
   - Predicted vote shares and ranks using SVM and Random Forest models.
3. **Evaluation:**
   - Computed RMSE for each model.
   - Compared predicted MVP and ROY rankings with real results for past seasons.
4. **2024 Predictions:**
   - Predicted the top 10 candidates for MVP and ROY for the ongoing NBA season.

## File Structure
/Data_Used/ 
  - Player_Totals_2020_2002.csv
  - Player_Per_Game_2020_2002.csv
  - Advanced_2020_2002.csv
  - Team_Summaries_2020_2002.csv
  - MVPs.csv - Player_Totals_2024.csv
  - Player_Per_Game_2024.csv
  - Advanced_2024.csv
  - Team_Summaries_2024.csv

/Results/
  - metrics.txt
  - average_metrics.txt
  - best_parameters.txt
  - results_old_seasons.txt
  - results_MVP_2024.txt
  - results_ROY_2024.txt

Code File:
  - mvp_roy_prediction.py

## How to Run
1. Clone this repository.
2. Ensure the required libraries are installed:
pip install pandas numpy scikit-learn
3. Place all datasets in the `/Data_Used/` folder.
4. Run the `mvp_roy_prediction.py` file to generate predictions and metrics. (it needs some minutes to run)
5. Ensure to modify all path with the correct ones.

## Output
The results include:
- **MVP predictions for historical seasons (2002–2020):** Saved in `results_old_seasons.txt`.
- **2024 MVP predictions:** Saved in `results_MVP_2024.txt`.
- **2024 ROY predictions:** Saved in `results_ROY_2024.txt`.
- **Model evaluation metrics:** RMSE values are stored in `metrics.txt` and `average_metrics.txt`.
- **Best Parameters obtained with the GridSearch:** Saved in `best_parameters.txt`.
