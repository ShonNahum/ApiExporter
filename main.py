import os
import requests
import time
import threading
from dotenv import load_dotenv
from prometheus_client import start_http_server, Gauge

load_dotenv("config.env")

def extract_bandwidth_from_api(api_url):
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and data:
            bandwidth_value = data[0].get(os.getenv('BUZZ_WORD'))
            return float(bandwidth_value) if bandwidth_value is not None else None
        print(f"Invalid API response from {api_url}.")
        return None
    except requests.RequestException as e:
        print(f"API request error: {e}")
        return None

def update_metrics():
    while True:
        for metric_name, gauge in metrics.items():
            api_url = api_urls.get(metric_name)
            if api_url:
                bandwidth_value = extract_bandwidth_from_api(api_url)
                if bandwidth_value is not None:
                    gauge.set(bandwidth_value)
                    print(f"Updated value of{metric_name} to {bandwidth_value}")
                else:
                    print(f"Skipping update for {metric_name}")

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
