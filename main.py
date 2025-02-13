import os
import requests
import time
from dotenv import load_dotenv
from prometheus_client import start_http_server, Gauge

load_dotenv("config.env")

def extract_bandwidth_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  

        data = response.json()

        if isinstance(data, list):
            if len(data) > 0:
                bandwidth_value = data[0].get(os.getenv('BUZZ_WORD'))
                if bandwidth_value is not None:
                    return float(bandwidth_value)
            else:
                print(f"The response list from {api_url} is empty.")
                return None
        else:
            print(f"API response from {api_url} is not a list.")
            return None
    except requests.RequestException as e:
        print(f"Error making API request to {api_url}: {e}")
        return None

metrics = {}

api_keys = [key for key in os.environ.keys() if key.endswith("_API")]

for api_key in api_keys:
    api_url = os.getenv(api_key)
    metric_name = api_key.replace("_API", "") 
    
    if api_url and metric_name:
        metrics[metric_name] = Gauge(metric_name, f"Current {os.getenv('BUZZ_WORD')} usage for {metric_name}")
        print(f"Configured metric for {metric_name} with URL: {api_url}")
    else:
        print(f"Skipping invalid configuration for {api_key}: Missing API URL or Metric Name")

start_http_server(int(os.getenv("PORT", 8000)))

if __name__ == "__main__":
    while True:
        for api_key in api_keys:
            api_url = os.getenv(api_key)
            metric_name = api_key.replace("_API", "") 
            
            if api_url and metric_name and metric_name in metrics:
                bandwidth_value = extract_bandwidth_from_api(api_url)
                
                if bandwidth_value is not None:
                    metrics[metric_name].set(bandwidth_value)
                    print(f"Updated {metric_name} {os.getenv('BUZZ_WORD')} to {bandwidth_value}.")
                else:
                    print(f"Skipping metric update for {metric_name} due to invalid bandwidth data.")
            else:
                print(f"Skipping {metric_name}: No valid API URL or metric name found.")
                
        time.sleep(int(os.getenv('TIME_SLEEP', 10))) 

