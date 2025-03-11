
# scapi

Dead simple, **S**elf-**C**ontained, single-file **API** load testing tool built
on FastAPI.

---
**Source Code**: <a href="https://github.com/enodllew/scapi.git"
target="_blank">https://github.com/enodllew/scapi.git</a>

Sometimes, I need a simple tool to make a few requests to external APIs, create
a bit of load, experiment with headers, check the average response time, and so
on. I want to be able to launch this tool from any environment with one click
without having to figure anything out.

The existing tools seemed inconvenient to me, so I created a tiny tool that
generates load and can be launched with just one command. Thanks to the inline
metadata format and the [uv](https://github.com/astral-sh/uv) package and
project manager, there's no need to manually set up environments.

You just need Python installed on the target machine, and that's it. No more
worrying about virtual environments. **One file**, **one command**, and you get
your beautiful FastAPI Swagger UI ready to work.

## Installation

### Live demo

[![asciicast](https://asciinema.org/a/686996.svg)](https://asciinema.org/a/686996)


```shell
curl -LOs https://github.com/enodllew/scapi/releases/latest/download/scapi.py
```
or
```shell
wget https://github.com/enodllew/scapi/releases/latest/download/scapi.py
```

Install the [uv](https://docs.astral.sh/uv/getting-started/installation/) using
the official script or via pip install, and then simply run:

```shell
uv run scapi.py
```

Done!

If you want to run `scapi.py` in a container, just run:

```
docker run -ti --rm -p "8000:8000" python:3.12-slim-bookworm bash
```

And repeat the same steps, but this time in a container.

## Requirements
+ `wget` or `curl`;
+ Python version 3.12* or higher;
+ Install the [uv](https://docs.astral.sh/uv/getting-started/installation/);

\* It may work on other versions, but I haven't tested them as I don't see much
point in doing so.

## How to use it

When the application starts, you will see two endpoints: `/load` and `/results`.

It's incredibly simple to use — you just specify the domain, request method,
delay between requests, number of attempts, headers and body (if needed), and
whether you want to see the response body and response headers (see the
screenshots below).

You can also click "Execute" multiple times to generate more tasks for event
loop.

![load](images/load.png)

At the end of or during the execution, you can also execute the
`/results` endpoint to see the total number of requests sent, broken down by
status, along with the average response time for requests to the specified URL.

![load](images/results.png)

## You should know

It is important to understand this is a very simple, single-threaded
application. Its purpose is to conduct small, quick tests by generating a
relatively small number of requests, with the ability to run in almost any
environment where Python is available and the `uv` binary can be copied.

If you need to perform serious load testing, this application will not be
suitable, and you should consider more robust tools such as Locust, Apache
JMeter, and others.

## License

This repository is licensed under the [MIT
License](https://github.com/enodllew/scapi/blob/0.2.4/LICENSE)
