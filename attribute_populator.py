import re

# for taking attributes in messages
def populateAttributes(message, alertAttribute, esResponse, alertIndex):
    try:
        for index in (re.findall('{[0-9]*}', message)):
            alertAttributeIndex = alertAttribute[(int)(index.lstrip('{').rstrip('}'))]
            alertAttributeValue = (str) (esResponse['hits']['hits'][alertIndex]['_source'][alertAttributeIndex])
            message = message.replace(index, alertAttributeValue)
        return message
    except:
        raise Exception( alertAttributeIndex + " not present in log" )

def aggregatePopulateAttributes(message, alertAttribute, aggregateAttribute, esResponse, hits):
    indexList = list()
    attributeSet = set()
    alertMessage = ""
    try:
        for i in range(0, hits):
            if esResponse['hits']['hits'][i]['_source'][aggregateAttribute] not in attributeSet:
                attributeSet.add(esResponse['hits']['hits'][i]['_source'][aggregateAttribute])
                indexList.append(i)
    except:
       raise Exception(aggregateAttribute + " attribute not in ES log entry.")

    for index in indexList:
        alertMessage +=populateAttributes(message, alertAttribute, esResponse, index) +"\n"

    return alertMessage