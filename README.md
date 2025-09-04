# SCAPI

![Total](https://img.shields.io/github/downloads/sesav/scapi-py/total)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
[![codecov](https://codecov.io/github/sesav/scapi/graph/badge.svg?token=GSHBWZGXAH)](https://codecov.io/github/sesav/scapi)
![License](https://img.shields.io/github/license/sesav/scapi-py)

> Dead simple, **S**elf-**C**ontained, single-file **API** load testing tool built on FastAPI.

A lightweight tool for ad-hoc API testing. It generates controlled request loads, customizes headers and payloads, collects latency metrics, and runs anywhere with minimal setup — just launch and start testing.

## Features

- **Zero Configuration** - One file, one command
- **Self-Contained** - Uses uv's inline metadata format
- **FastAPI Swagger UI** - Beautiful Swagger UI interface;
- **Async Load Testing** - Built on httpx (encode) and asyncio
- **Real-time Results** - View metrics in stdout during execution
- **Container Ready** - Works in any environment (uv handles it)

## Quick Start

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) with the official script or via pip if Python is available on your laptop or server.

### Option 1: Run Directly (No Installation)

```bash
# Download and run the tool directly
curl -LOs https://github.com/sesav/scapi-py/releases/latest/download/scapi.py
uv run scapi.py

# Or with wget
wget https://github.com/sesav/scapi-py/releases/latest/download/scapi.py
uv run scapi.py
```

### Option 2: Install as Package

```bash
# Install from PyPI
pip install scapi-py

# Run the tool
scapi
```

### Option 3: Install with uv

```bash
# Install with uv
uv add scapi-py

# Run the tool
scapi
```

### Usage

1. Open http://localhost:8000 in your browser
2. Use the `/load` endpoint to send requests
3. Check `/results` for metrics and response times

## API Reference

### POST /load
Send load test requests to a target URL.

**Parameters:**
* `url` (string, required) - Target URL to test
* `method` (string, required) - HTTP method (GET, POST, PUT, etc.)
* `attempts` (int, default: 10) - Number of requests to send
* `delay` (float, default: 0.1) - Delay between requests in seconds
* `headers` (dict, optional) - Custom HTTP headers
* `body` (dict, optional) - Request body for POST/PUT requests
* `response_header` (bool, default: false) - Include response headers in stdout
* `response_body` (bool, default: false) - Include response body in stdout

### GET /results
Get aggregated test results and metrics.

**Response:**
```json
{
  "results": {
    "200": 10,
    "404": 2
  },
  "average_request_time": 0.25
}
```

## Docker Usage

```bash
docker run -ti --rm -p "8000:8000" python:3.12-slim-bookworm bash
```
Then follow the installation steps inside the container.

## Screenshots

![Load Testing Interface](https://github.com/sesav/scapi-py/blob/main/images/load.png)
*Configure your load test parameters*

![Results Dashboard](https://github.com/sesav/scapi-py/blob/main/images/results.png)
*View real-time results and metrics*

## Limitations

It's important to understand that this is a very simple, single-threaded application. Its purpose
is to perform small, quick tests by generating a limited number of requests, and it can run in
almost any environment where the uv binary is available. If you need serious load testing at scale,
consider more robust solutions such as Locust, Apache JMeter, or similar tools.

## Development

```bash
# Clone the repository
git clone https://github.com/sesav/scapi-py.git
cd scapi-py

# Install development dependencies
make install

# Run tests
make test

# Run
make run
```

## Requirements

- Python 3.10+
- uv package manager
- wget or curl (for installation)

## License

This project is licensed under the [MIT License](LICENSE).
