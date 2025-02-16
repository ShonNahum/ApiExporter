import os
import requests
import time
import threading
from dotenv import load_dotenv
from prometheus_client import start_http_server, Gauge
import logging

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  
    ]
)

logger = logging.getLogger(__name__)
load_dotenv("config.env")

def find_bandwidth_in_json(data, keyword):
    """Recursively search for the keyword in any part of the JSON response."""
    if isinstance(data, dict):  
        for key, value in data.items():
            if keyword.lower() in key.lower():
                try:
                    return float(value)  
                except ValueError:
                    pass  
            result = find_bandwidth_in_json(value, keyword)  
            if result is not None:
                return result
    elif isinstance(data, list):  
        for item in data:
            result = find_bandwidth_in_json(item, keyword)
            if result is not None:
                return result
    return None  

def extract_bandwidth_from_api(api_url):
    api_token = os.getenv("API_TOKEN")  
    keyword = os.getenv('BUZZ_WORD', 'bandwidth')  

    headers = {
        "Authorization": f"Bearer {api_token}",  
        "Accept": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=5) 
        response.raise_for_status()
        data = response.json()

        bandwidth_value = find_bandwidth_in_json(data, keyword)  
        if bandwidth_value is not None:
            return bandwidth_value  

        logger.error(f"Bandwidth value not found in API response from {api_url}.")
        return None
    except requests.RequestException as e:
        logger.error(f"API request error: {e}")
        return None



def update_metrics():
    while True:
        for metric_name, gauge in metrics.items():
            api_url = api_urls.get(metric_name)
            if api_url:
                bandwidth_value = extract_bandwidth_from_api(api_url)
                if bandwidth_value is not None:
                    gauge.set(bandwidth_value)
                    logger.info(f"Updated value of {metric_name} to {bandwidth_value}")
                else:
                    logger.info(f"Skipping update for {metric_name}")

        time.sleep(TIME_SLEEP)


metrics = {}
api_urls = {}
api_keys = [key for key in os.environ.keys() if key.endswith("_API")]
TIME_SLEEP = int(os.getenv('TIME_SLEEP', 60))
PORT = int(os.getenv("PORT", 8000))

for api_key in api_keys:
    api_url = os.getenv(api_key)
    metric_name = api_key.replace("_API", "")
    if api_url and metric_name:
        metrics[metric_name] = Gauge(metric_name, f"Current {os.getenv('BUZZ_WORD')} usage for {metric_name}")
        api_urls[metric_name] = api_url

start_http_server(PORT)

# Run metric update loop in a background thread
threading.Thread(target=update_metrics, daemon=True).start()

# Keeping the main thread alive
while True:
    time.sleep(3600)
