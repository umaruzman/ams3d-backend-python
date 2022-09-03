from datetime import datetime, timedelta

epoch = datetime(1970, 1, 1)

def getTimeUTC(dateString):
    utc_time = datetime.strptime(dateString[:26], '%Y-%m-%d %H:%M:%S.%f')
    return utc_time

def timestamp_microsecond(utc_time):
    td = utc_time - epoch
    assert td.resolution == timedelta(microseconds=1)
    return (td.days * 86400 + td.seconds) * 10**6 + td.microseconds


def timeStringToMicroSeconds(timestring):
    utc = getTimeUTC(timestring)
    return float(timestamp_microsecond(utc))

def convertMicroSecondsToTime(microseconds):
    s = float(microseconds/10**6)
    return datetime.fromtimestamp(s) - timedelta(days=1)

def futureDateRange(start):
    actualStart = start + timedelta(days=2)
    periods = 30
    daterange = []
    for day in range(periods):
        date = (actualStart + timedelta(days = day)).strftime("%Y-%m-%d %H:%M:%S.%f")
        daterange.append(date)
    print(daterange)
    return daterange