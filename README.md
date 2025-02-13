# Python Prometheus Exporter for Bandwidth Metrics

This project provides a **Prometheus exporter** implemented in Python, which scrapes the value by its name that you define in `config.env` from multiple APIs and exposes them as metrics for Prometheus to scrape. The exporter reads API URLs from a `config.env` file (by the format '<name>_API=<API URL>' and fetches the values from these APIs periodically.
It then exposes the metrics on a specified HTTP endpoint, which Prometheus can scrape. (Default port 8000, but can override in config.env with PORT env varaible) 

## Purpose

The purpose of this project is to:
- Collect value by its name that you define in `config.env` from multiple APIs.
- Expose the data in a format that can be scraped by Prometheus.
- Make the collected data available as **Prometheus metrics** for monitoring purposes.

## Features

- **Scrape multiple APIs**: Supports multiple API URLs specified in a [config.env](config.env) file.
- **Expose metrics to Prometheus**: Provides an HTTP endpoint (`/metrics`) that Prometheus can scrape.
- **Customizable Scraping Frequency**: Scrapes API data every 10 seconds by defaults (can override in config.env with TIME_SLEEP env varaible)
- **Dynamic Metric Names**: The metric names are dynamically generated based on the environment variable names.

## Requirements

To run this project, you need:
- Python 3.7+ installed.
- `pip` (Python package installer) to install dependencies.
- Docker (optional, for containerization).

### Dependencies
- `requests`: To make HTTP requests to the API.
- `prometheus_client`: To expose metrics in the Prometheus format.
- `python-dotenv`: To read the environment variables from the `config.env` file.

You can install the dependencies by running:
```bash
pip install -r requirements.txt
```

### How to run

- Create a config.env file with [config.env](config.env) format 
```
docker run -d -p <PORT in config.env | 8000>:<PORT in config.env | 8000> -v $(pwd)/config.env:/app/config.env --name exporter python-prometheus-exporter
```