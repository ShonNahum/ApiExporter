# Python Prometheus Exporter for Bandwidth Metrics

This project provides a **Prometheus exporter** implemented in Python, which scrapes bandwidth usage metrics from multiple APIs and exposes them as metrics for Prometheus to scrape. The exporter reads API URLs from a `.env` file and fetches bandwidth values from these APIs periodically (every 10 seconds). It then exposes the metrics on a specified HTTP endpoint, which Prometheus can scrape.

## Purpose

The purpose of this project is to:
- Collect bandwidth usage data from multiple APIs.
- Expose the data in a format that can be scraped by Prometheus.
- Make the collected data available as **Prometheus metrics** for monitoring purposes.

## Features

- **Scrape multiple APIs**: Supports multiple API URLs specified in a `.env` file.
- **Expose metrics to Prometheus**: Provides an HTTP endpoint (`/metrics`) that Prometheus can scrape.
- **Customizable Scraping Frequency**: Scrapes API data every 10 seconds by default.
- **Dynamic Metric Names**: The metric names are dynamically generated based on the environment variable names (e.g., `Base509_API` → `Base509`).

## Requirements

To run this project, you need:
- Python 3.7+ installed.
- `pip` (Python package installer) to install dependencies.
- Docker (optional, for containerization).

### Dependencies
- `requests`: To make HTTP requests to the API.
- `prometheus_client`: To expose metrics in the Prometheus format.
- `python-dotenv`: To read the environment variables from the `.env` file.

You can install the dependencies by running:

```bash
pip install -r requirements.txt


### How to run
1. Create a .env file With the example .env in project

2. docker run -d -p 8000:8000 -v $(pwd)/.env:/app/.env --name exporter python-prometheus-exporter
