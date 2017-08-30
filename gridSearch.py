'''
Code inspired from: https://machinelearningmastery.com/grid-search-hyperparameters-deep-learning-models-python-keras/
'''
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import sys
import numpy
from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasClassifier
import time
from keras.wrappers.scikit_learn import KerasClassifier
from keras.constraints import maxnorm
from sklearn.metrics import make_scorer, accuracy_score, roc_auc_score
from prepareDATA import *
import localConfig as cfg
import datetime 

from commonFunctions import gridClassifier, myClassifier

os.chdir(cfg.lgbk+"Searches")

compileArgs = {'loss': 'binary_crossentropy', 'optimizer': 'adam', 'metrics': ["accuracy"]}

l=len(XDev)

# Fix seed for reproducibility
seed = 42
numpy.random.seed(seed)

# Tune the Number of Neurons in the Hidden Layer 

model = KerasClassifier(build_fn=myClassifier,nIn=len(trainFeatures),nOut=1, compileArgs=compileArgs,batch_size=20, verbose = 1)

#Hyperparameters
neurons = [14,20]
layers = [3]
epochs = [15]
batch_size = [l/100, l/10000]
learn_rate = [0.001]
dropout_rate = [0.1, 0.5]

begin = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")

#param_grid = dict(neurons=neurons, layers=layers, epochs=epochs, batch_size=batch_size, learn_rate=learn_rate, dropout_rate=dropout_rate)
param_grid = dict(epochs=epochs,batch_size=batch_size,dropout_rate=dropout_rate)
scoring = 'accuracy'
#scoring = 'roc_auc'
#scoring = scoring = {'AUC': 'roc_auc', 'Accuracy': make_scorer(accuracy_score)}
grid = GridSearchCV(estimator = model, param_grid = param_grid, scoring=scoring, n_jobs=-1) #n_jobs = -1 -> Total number of CPU/GPU cores
print("Starting the training")
start = time.time()

#dataVal["NN"] = valPredict
grid_result = grid.fit(XDev,YDev)
#grid_result = grid.fit(dataVal.category,dataVal.NN)

end = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
filename="gS:"+end+".txt"
sys.stdout=open(filename,"w")

print("Begin: "+begin)
print("End: "+end+"\n")

print("Training took ", time.time()-start, " seconds")

print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
        print("%f +/-%f with: %r" % (mean, stdev, param))
sys.stdout.close()