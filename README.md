# Beer
List of beer hub around given address. Data from Google Map API

# How to run script?
You can run this script by following steps:
## Step 1: Create API_key.txt file
1. Create a Google Map API key, [Google Docs](https://developers.google.com/places/web-service/get-api-key)
2. Create API_key.txt file, and copy your API key to this file and save
## Step 2: Run script  
Open terminal and run following commands
1. Clone this repo  
```git clone https://github.com/vuonglv1612/Beer.git```
2. Create a virtual environment.  
```cd Beer```  
```virtualenv -p python3 venv```
3. Activate this venv and install requirement packages.  
```source venv/bin/activate```  
```pip install -r requirements.txt```
4. Run script
```python3 beer.py 'xxx, yyy' 'path/to/your/result/geojson/file'```  
Example  
```python3 beer.py '21.013111,105.799972' 'beer_hub_nearby_me.geojson'```