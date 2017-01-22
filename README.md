# Lolpredict
* Skip to bottom to see the interesting stuff

## Intro
The goal of this project is to determine the winner of a League of Legends
ranked solo queue 5x5 match based on various game and player statistics. Using these
statistics, we want to determine solo queue strategies/meta which would yeild to higher 
win rates.

## Data
The 'data_collection_scripts/' folder contains multiple scripts to query the Riot
Games API for the game/summoner data that we need, and save it into a local
sql database for querying when we build our model. It also contains a web scraper script
to op.gg which pulls precalculated champion statistics (saves us lots of time). 
Running '/data_collection_scripts/main.py' will keep making requests until
terminated by the user. I did this for ~10 hours/day for a week and was able to
get ~35,000 full samples of data.


## Model
Within 'learningModels/' contains three models:
* Linear SVM classifier (scikit)
* Logistic Regression (tensorflow)
* Artificial Neural Net (keras - tensorflow)

The performance of these models will be discussed further in the documentation.

## Dataframes
We only want to look at Ranked 5v5 games which are plat or above since many matches
below this yeilds data with results that are not based on champion picks (elo
boosting, smurfing, players not understanding matchups). To determine if a specific
match is plat or above, we can count the number of players with 'highestAchievedSeasonTier'
of plat or higher. If this number is >= to 5, it is considered a valid game.

The output for these models is very straightforward: either the blue team wins,
or the blue team loses (eg purple team wins).

The feature vector includes various personal champion statistics as well as
statistics for the champion in the specific server (in my case NA). Some examples
include:
* Win rate on champion
* Average KDA
* Average physical/magic damange dealt
* Number of games on champion

It also considers combined team statistics. For example:
* Total physical/magic damange dealth on team
* Total kills/deaths
* Total average tower kills/game
* Total games played

These features are repeated for every single champion and summoner for their
respective positions. There are a total of 391 parameters to consider.

## Machine learning
Why each model was selected
* SVM - scikit provides a good SVM trainer which make it easy to train a simple
model and be able to switch kernals easily. It is also better for high 
dimensional spaces.
* Logistic Regression - Easy to do especially with yes/no inputs. Sigmoidal function
yields a result with a probability, which is what I want. We could also analyze what
weightings the model puts on certain features, which might be interesting. Why 
tensorflow? because I want to try out tensorflow.
* ANN - Gotta make use of the buzzwords/memes. No hidden layer based off of 
the assumption that the problem is linearly separable

## Iteration 1 Results
For iteration 1, I focused on games with complete data. Many (around 20%) of the games
has incomplete data - for example when a summoner plays a champion for the first time
in the current ranked season or when summoners swap roles in champion select. I 
decided to ignore this for now, and deal with missing data in the next iteration.
This dataframe was created using an extensive sql query.

The data was split into 3 sets - Training (60%), Test (20%), and Validation (20%)
Surprisingly enough, for games that have complete data, all three of the models
predicted the outcome of the match with above 80% accuracy on the test set! The
best performing model (highest accuracy based on validation set) was the Logistic
Regression model. Neat.

Looking at the feature weightings for our Logistic regression model after analyzing
~20,000 games (refer to /notes/logisticRegressionModel.csv), we can conclude that:
* High Importance/High feature weighting:
  * Team Tower kills are **extremely** important -> Focus on tower objectives
  * Number of deaths in midlane are detrimental to winning, much than other lanes -> Camp Mid
  * The more damage the support takes, the more likely the team will win -> Tanky supports
* Low Importance
  * Support average gold earned -> Don't take cs as support...please
  * Jungler Kills -> Give kills to laners
  * Top Damage dealt to champions -> Top laners should cc and focus on building resistance as
    opposed to damage

**My all time favourite statistic:**
The absolute most important stat for the late 2016/ early 2017 season is the summoner's win 
rate on a champion (as expected) in the following order:
1. Mid
2. Top
3. Jungle
4. Support
5. ADC

Final comments: "adc in 2017, feels adc man"

