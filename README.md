# IP Address Management API
 - documentations (`docs/`)
 - Requests Example (`docs/request`) 

## Requirements

-	[Python](https://www.python.org/downloads/) >= 3.8.x
-	[Flask] ``` pip install flask ``` >= 1.1.x

## How To Run The App API
there are three methods to run this API
- Local
```
clone repo: git clone git@github.com:mhost39/ip-address-managment.git
cd ip-address-managment
install dependencies: pip install -r requirements.txt
python app.py
```
- build docker image locally
```
docker build -t flask_app:latest .
docker run -p 5000:5000 flask_app
```
- DockerHub
```
docker pull mhost/ip-address-management:latest
```

## Run tests
``` python -m unittest ```

there are github action to run tests nightly and when push


please browse [issues](https://github.com/mhost39/ip-address-managment/issues)