import numpy as np
import pandas as pd
from sklearn import linear_model
from functions import *
from databasecon import *

from flask import Flask
from flask import request
app = Flask(__name__)

@app.get('/predict-metrics')
def predict_metrics():
    assetId = request.args.get('assetId', default = 0, type = int)
    metricType = request.args.get('metricType', default = 0, type = int)
    
    df = pd.DataFrame(getMetrics(assetId, metricType))
    df = df.drop([0, 3, 4], axis="columns")
    
    df[2] = df[2].apply(str)
    df[2].apply(type)
    
    initDatesString = list(df[2])

    df[2] = df[2].apply(timeStringToMicroSeconds)
    df[1] = df[1].apply(float)
    
    values = df[1]
    dates = df.drop(1, axis="columns")

    print('Dates ', dates)
    print('String Time', convertMicroSecondsToTime(dates[2].values[0]))
    
    lr = linear_model.LinearRegression()
    lr.fit(dates, values)
    
    date = "2022-08-28 18:46:47.857"
    date2 = "2022-09-30 18:46:47.857"
    dateMS = timeStringToMicroSeconds(date)
    dateMS2 = timeStringToMicroSeconds(date2)
    futureDates = futureDateRange(convertMicroSecondsToTime(list(dates[2])[-1]))
    fdMicroSecondsArray = np.array(list(map(timeStringToMicroSeconds, futureDates)));
    reshapedFDArray = fdMicroSecondsArray.reshape(fdMicroSecondsArray.size, 1)

    result = lr.predict(reshapedFDArray)
    
    print('Results', result)
    
    newDatesArray = initDatesString
    newValuesArray = list(values)

    for date in futureDates:
        newDatesArray.append(date)

    for val in result:
        newValuesArray.append(val)

    return {"dates":newDatesArray, "data":newValuesArray}

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 9000, app)