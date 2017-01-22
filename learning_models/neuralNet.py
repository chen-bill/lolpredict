from keras.models import Sequential
from keras.layers import Dense
import dataRepository
import numpy
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

df = dataRepository.getTrainingDataframe()
X = df.drop(['bWin'], 1).as_matrix()
y = df['bWin'].as_matrix()
FEATURE_SIZE = X.shape[1]

#define model
model = Sequential()
model.add(Dense(400, input_dim=FEATURE_SIZE, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))

#logloss with gradient descent
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#model fit
model.fit(X, y, nb_epoch=150, batch_size=100)

# evaluate the model
df = dataRepository.getTrainingDataframe()
testX = df.drop(['bWin'], 1).as_matrix()
testy = df['bWin'].as_matrix()

scores = model.evaluate(testX, testy)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
