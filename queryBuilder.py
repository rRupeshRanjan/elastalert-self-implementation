import json

def buildQuery(query, gte, lte):
    return json.dumps({
      "query": {
        "bool": {
          "must": [
            {
              "query_string": {
                "query": query
              }
            },
            {
              "range": {
                "@timestamp": {
                  "gte": int(gte),
                  "lte": int(lte),
                  "format": "epoch_millis"
                }
              }
            }
          ]
        }
      },
      "size": 9000,
      "from": 1
    })