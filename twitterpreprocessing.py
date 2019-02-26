from flask import Flask
from redis import Redis, RedisError
import os
import socket
import urllib.request
import json

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    data = {
        "Inputs": {
                "input1":
                [
                    {
                            'created_at': "Mon Aug 28 15:29:16 +0000 2017",   
                            'text': "In Texas Flooding, FEMA Asks ‘All Citizens to Get Involved’ to Help Calling Hurricane Harvey a “landmark event for… https://t.co/swhIa5Sqjl",   
                            'geo_enabled': "",   
                            'coordinates': "",   
                            'place': "",   
                    }
                ],
            },
       "GlobalParameters":  {
       }
    }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/5f68284cfa39454db82e7f1a47c1c0f2/services/fe9d26d494f947809c396689770fdbb8/execute?api-version=2.0&format=swagger'
    api_key = 'COiP3ngTOAgeVYZtiJqS5LTfzEVd8pZPkIlYE3D+7rVZG451qZc4ivu4GYNyq1Idsjro2cQUBe6jYvtVEAN5UA==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))

    html = "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Results:</b> {result}"
    return html.format(hostname=socket.gethostname(), result=result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

