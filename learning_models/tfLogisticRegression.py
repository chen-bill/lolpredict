import pandas as pd
import tensorflow as tf
import numpy as np
import dataRepository
import pdb
import pprint
pp = pprint.PrettyPrinter(indent=2)

df = dataRepository.getTrainingDataframe()

#metrics for csv parsing
dfMean = df.mean(axis=0)
dfStd = df.std(axis=0)
dfMin = df.min(axis=0)
dfMax = df.max(axis=0)

print dfMin
print dfMax

# parameters
learningRate = 0.01
trainingEpochs = 100
batchSize = 100
displayStep = 1

#minus one because y is included in the dataframe
numFeatures = df.shape[1]-1
numExamples = df.shape[0]

# tf graph input
x = tf.placeholder(tf.float32, [None, numFeatures])
y = tf.placeholder(tf.float32, [None, 1]) #either 1 for bWin or 0 for pWin

# set model weights
W = tf.Variable(tf.zeros([numFeatures,1]))
b = tf.Variable(tf.zeros([1]))

#construct model
# hypothesis = tf.nn.softmax(tf.matmul(x, W) + b) # Softmax
hypothesis = tf.sigmoid(tf.matmul(x, W) + b) # Sigmoid hypothesis because we want probability

# Minimize error using cross entropy
# cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(hypothesis), reduction_indices=1)) #cross entropy
# cost = tf.reduce_mean(tf.square(tf.sub(hypothesis, y))) #least squares
#logloss seems to yield the best results
cost = -tf.reduce_mean(y*tf.log(hypothesis) + (1-y)*tf.log(1-hypothesis))

# gradient descent
optimizer = tf.train.GradientDescentOptimizer(learningRate).minimize(cost)

#initialize variables
init = tf.initialize_all_variables()

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

#run graph session
with tf.Session() as sess:
    sess.run(init)

    #training
    for epoch in range(trainingEpochs):
        averageCost = 0.
        totalBatch = int(numExamples/batchSize)

        #split data in chunks
        for i in chunker(df, batchSize):
            batchXs, batchYs = i.drop(['bWin'], 1), i[['bWin']]

            #run backprop optimization using defined cost function
            _, c = sess.run([optimizer, cost], feed_dict={x: batchXs,
                                                          y: batchYs})
            #calculating average cost
            averageCost += c / totalBatch
            # pdb.set_trace()
        # Display logs per epoch step
        if (epoch+1) % displayStep == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(averageCost))

    print("Optimization Finished!")

    #calculates accuracy
    testDataframe = dataRepository.getTestDataframe()

    #get test set
    testX = testDataframe.drop(['bWin'],1)
    testY = testDataframe['bWin']
    testY = testY.as_matrix().flatten()

    predict = tf.to_int32(tf.round(hypothesis))
    teY = sess.run(predict, {x: testX}).flatten()

    #create bool vector for accuracy calculation
    correct_predictions = tf.equal(testY, teY)

    # TODO: figure out why this doesn't work
    # accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    # print ('Accuracy:', accuracy.eval())

    #workaround to get accuracy
    def getAccuracy(booleanArray):
        correctValues = 0
        totalValues = 0;
        for value in booleanArray:
            if value:
                correctValues+=1
            totalValues+=1
        return float(correctValues)/float(totalValues)

    wValues = list(W.eval().flatten())
    headerValues = list(testX.columns.values)

    with open('../notes/tfLogisticRegressionResults.csv', 'w') as file_:
        #write header
        file_.write('Parameter, W Value, Scaled Min, Scaled Max, Std, Mean \n')
        wDict = {}
        for i in range(len(headerValues)):
            csvRow = headerValues[i] + ',' + str(wValues[i]) + ',' + \
                str(dfMin[headerValues[i]]) + ',' + str(dfMax[headerValues[i]]) + ',' + \
                str(dfStd[headerValues[i]]) + ',' + str(dfMean[headerValues[i]]) + '\n'
            file_.write(csvRow)
            wDict[headerValues[i]] = wValues[i]
        # pp.pprint(wDict)

    print ('--------------------------------')
    print ('Training Size: ' + str(numExamples))
    print ('Test Size: ' + str(testY.shape[0]))
    print ('Accuracy:', "%.4f" % getAccuracy(correct_predictions.eval()))
