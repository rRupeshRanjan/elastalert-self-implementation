import datetime
import random
import time
import sys
import yaml
from elasticsearch import Elasticsearch
import extractTime
import queryBuilder
import attribute_populator

while True:
    docs = yaml.load_all(open(sys.argv[1], "r"))
    # docs = yaml.load_all(open("elastalert-self-implementation/values.yaml", "r"))
    doc = docs.next()
    docs.close()

    alertName = doc['alertName']
    esHost = doc['esHost']
    indexQueried = doc['index']
    timestamp = doc['timestamp']
    threshold = doc['threshold']
    realert = doc['realert']
    aggregate = bool(doc['aggregate'])
    aggregateAttribute = doc['aggregateAttributes']
    query = doc['query']
    message = doc['message']
    alertAttribute = doc['alertAttributes']

    history = extractTime.getExtractedTime(timestamp, "timestamp")
    intervalTime = extractTime.getExtractedTime(realert, "realert")
    lte = int(round(time.time() * 1000))
    gte = lte-history*1000
    queryJson = queryBuilder.buildQuery(query, gte, lte)
    es = Elasticsearch(hosts=esHost)
    esResponse = es.search(index=indexQueried, body=queryJson)

    hits = len(esResponse['hits']['hits'])
    if hits > 0:
        hits -= 1

    print(str(hits) + " hits found for " + alertName + " between " +
          str(datetime.datetime.fromtimestamp(gte/1000).strftime('%c')) + " and " +
          str(datetime.datetime.fromtimestamp(lte/1000).strftime('%c')))

    if hits > threshold:
        if aggregate:
            alertMessage = attribute_populator.aggregatePopulateAttributes(message, alertAttribute, aggregateAttribute,esResponse, hits)
        else:
            alertMessage = attribute_populator.populateAttributes(message, alertAttribute, esResponse,random.randint(0, hits))

        print("alertMessage: " + alertMessage)

        # data = [('payload', '{"text": "' + alertMessage + '" }')]
        # response = requests.post('slack-hook-url',data=data)
        # print("Trigger sent to Slack at " + str(datetime.datetime.fromtimestamp(time.time()).strftime('%c')))


    time.sleep(intervalTime)