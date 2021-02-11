## sensor-log-parser

This API is deployed in kubernetes and is accessible via `http://localhost:80/api/sensor-log-parser/`
It will accept a log file through a POST request and it will respond with metrics
derived from those logs. The `src/main.py` file has the api code and the `src/widgettest.py` has the class `WidgetTest` which is the meat of the application. 

The conditions are as follows:
#### thermometer 
	- ultra precise 
		- mean is within 0.5 degrees 
		- standard deviation < 3
	- very precise 
		- mean is within 0.5 degrees
		- standard deviation < 5 
	- precise
		- All else
#### humidity sensor
	- Within 1 humidity percent of the reference value

The format of the logs are as follows:
```
reference <control temp> <control humidity> 
<type of sensor> <sensor name> 
<yyyy-mm-ddThh:mm> <sensor reading> 
thermometer temp-1 
2007-04-05T22:01 69.5 
humidity hum-1 
2007-04-05T22:04 45.2 
humidity hum-2 
2007-04-05T22:04 44.4 
```
How to setup locally with kuberentes:
```
docker build -t sensor-log-parser .
docker tag sensor-log-parser:latest localhost:5000/sensor-log-parser
docker push localhost:5000/sensor-log-parser
kubectl apply -f ./local-dev
```
Testing on local:
How to setup locally with kuberentes:
```
docker build -t sensor-log-parser .
docker run --rm -it -p 127.0.0.1:5000:5000 sensor-log-parser
curl http://localhost:80/api/sensor-log-parser/healthz
```

Postman:
![Alt text](images/postman.png?raw=true "Title")
Kube pod logs showing request:
![Alt text](images/kubelogs.png?raw=true "Title")
Kube service deployment:
![Alt text](images/service.png?raw=true "Title")


#### future improvements:
1. For my own sanity, put the logs in json format
2. Finish step 1 before anything else
3. Clean up regex for log parsing
4. Add api key security through Kong
5. Add monitoring and log aggregation to pods