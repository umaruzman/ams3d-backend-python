import sys
import psycopg2

def getMetrics(assetId = 0, metricType = 0):
    conn = psycopg2.connect(
        host="localhost",
        database="armsnewbackend",
        user="postgres",
        password="root")

    cur = conn.cursor()
    q = 'SELECT * FROM "Metrics"'

    if(assetId or metricType):
        q += ' WHERE '

    if(assetId):
        q+= '"AssetId"=' + str(assetId)

    if(assetId and metricType):
        q+= ' AND '

    if(metricType):
        q+= '"MetricTypeId"=' + str(metricType)

    q+= 'ORDER BY "DateTime" ASC'

    cur.execute(q)
    metrics = cur.fetchall()
    cur.close()
    conn.close()
    return metrics