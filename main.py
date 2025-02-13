import os
import requests
import time
from dotenv import load_dotenv
from prometheus_client import start_http_server, Gauge

# Load the .env file
load_dotenv()

# Function to extract bandwidth from the API response (JSON)
def extract_bandwidth_from_api(api_url):
    try:
        # Make an API request to the provided URL
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Check if the response is a list
        if isinstance(data, list):
            # Assuming the first element in the list contains the 'bandwidth' field
            if len(data) > 0:
                bandwidth_value = data[0].get(os.getenv('BUZZ_WORD'))
                if bandwidth_value is not None:
                    return float(bandwidth_value)  # Return as a float for Prometheus compatibility
            else:
                print(f"The response list from {api_url} is empty.")
                return None
        else:
            print(f"API response from {api_url} is not a list.")
            return None
    except requests.RequestException as e:
        print(f"Error making API request to {api_url}: {e}")
        return None

# Initialize a dictionary to store Prometheus Gauge metrics for each API
metrics = {}

# Load all API URLs and their names from the .env file
api_keys = [key for key in os.environ.keys() if key.endswith("_API")]

# Create a Gauge for each API using the name specified in the .env file
for api_key in api_keys:
    api_url = os.getenv(api_key)
    metric_name = api_key.replace("_API", "")  # Remove '_API' to use the base name as the metric name
    
    if api_url and metric_name:
        metrics[metric_name] = Gauge(metric_name, f"Current {os.getenv('BUZZ_WORD')} usage for {metric_name}")
        print(f"Configured metric for {metric_name} with URL: {api_url}")
    else:
        print(f"Skipping invalid configuration for {api_key}: Missing API URL or Metric Name")

# Start the Prometheus metrics server on port 8000
start_http_server(8000)

if __name__ == "__main__":
    while True:
        for api_key in api_keys:
            api_url = os.getenv(api_key)
            metric_name = api_key.replace("_API", "")  # Get the metric name by removing '_API'
            
            if api_url and metric_name and metric_name in metrics:
                # Fetch bandwidth value for the current API
                bandwidth_value = extract_bandwidth_from_api(api_url)
                
                if bandwidth_value is not None:
                    # Update the corresponding Prometheus metric
                    metrics[metric_name].set(bandwidth_value)
                    print(f"Updated {metric_name} {os.getenv('BUZZ_WORD')} to {bandwidth_value}.")
                else:
                    print(f"Skipping metric update for {metric_name} due to invalid bandwidth data.")
            else:
                print(f"Skipping {metric_name}: No valid API URL or metric name found.")
                
        # Sleep for 10 seconds before making the next request
        time.sleep(10)  # Fetch data from all APIs every 10 seconds
