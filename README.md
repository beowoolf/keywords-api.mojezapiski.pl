# Keywords-API

[![Python](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/)
[![spaCy](https://img.shields.io/badge/spaCy-3.5.0-09a3d5.svg)](https://spacy.io/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)](https://www.docker.com/)

A small HTTP Web API that extracts the most frequent keywords from a piece of Polish text. It uses [spaCy](https://spacy.io/) with the `pl_core_news_lg` language model to lemmatize words and keep only meaningful parts of speech.

## Table of contents

- [Project description](#project-description)
- [Tech stack](#tech-stack)
- [Getting started locally](#getting-started-locally)
- [Available scripts](#available-scripts)
- [API usage](#api-usage)
- [Project scope](#project-scope)
- [Project status](#project-status)
- [License](#license)

## Project description

Keywords-API accepts Polish text and returns the lemmatized words that occur most often in it. Only the following word classes are considered:

- common nouns (`NOUN`)
- proper nouns (`PROPN`)
- adjectives (`ADJ`)

Stop words and punctuation are ignored, and the text is lowercased before analysis. The result contains the top 10 keywords ordered by frequency. Keywords that share the same count as the 10th entry are included as well, so the list can be longer than 10 in case of ties.

## Tech stack

| Area               | Technology                                              |
| ------------------ | ------------------------------------------------------- |
| Language           | Python 3.8                                              |
| NLP                | spaCy 3.5.0, `pl_core_news_lg` 3.5.0 model              |
| HTTP server        | Python standard library (`http.server`)                 |
| Containerization   | Docker (`python:3.8-slim-buster`), Docker Compose 3.1   |

The project has no third-party web framework. The server is built on `BaseHTTPRequestHandler` and `HTTPServer`.

## Getting started locally

### Prerequisites

- Python 3.8 (the version the project is built and pinned for)
- `pip`
- Or, alternatively: [Docker](https://www.docker.com/) and optionally Docker Compose

### Option 1: Run with Docker Compose (recommended)

```bash
docker-compose up -d
```

The API is then available at `http://localhost:20334`.

### Option 2: Build and run the Docker image manually

```bash
# build the image
docker build -f Dockerfile -t keywords-api .

# run the container
docker run -d -p 20334:20334 keywords-api
```

### Option 3: Run directly with Python

```bash
# clone the repository
git clone <repository-url>
cd keywords-api.mojezapiski.pl

# create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# install dependencies (this also downloads the pl_core_news_lg model from GitHub)
pip install -r requirements.txt

# start the server
python server.py
```

The server listens on port **20334** on all interfaces.

## Available scripts

This project does not use a build tool or task runner. The commands below are the ones you will need:

| Command                                                   | Description                                                  |
| --------------------------------------------------------- | ------------------------------------------------------------ |
| `pip install -r requirements.txt`                         | Install Python dependencies and the Polish spaCy model       |
| `python server.py`                                        | Start the API server on port `20334`                         |
| `docker build -f Dockerfile -t keywords-api .`            | Build the Docker image                                       |
| `docker run -d -p 20334:20334 keywords-api`               | Run the Docker image in the background                       |
| `docker-compose up -d`                                    | Build and start the service with Docker Compose              |
| `docker-compose down`                                     | Stop and remove the Compose service                          |

## API usage

### `GET /`

Health-check style endpoint. Returns a plain text response:

```
Keywords-API
```

### `POST /`

Extracts keywords from the submitted text.

**Request**

- Header: `Content-Type: application/json`
- Body:

  ```json
  {
    "text": "Your Polish text goes here."
  }
  ```

**Example**

```bash
curl -X POST http://localhost:20334/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Kot siedzi na macie. Mały kot lubi spać na słońcu."}'
```

**Response** (`200 OK`, `application/json`)

Each entry contains the rank (`index`), the lemmatized keyword (`word`), and the number of occurrences (`count`). The array is sorted by `count` in descending order:

```json
[
  { "index": 1, "word": "kot", "count": 2 },
  { "index": 2, "word": "mały", "count": 1 },
  { "index": 3, "word": "słońce", "count": 1 }
]
```

> The values above illustrate the response format; the actual keywords depend on the spaCy model's analysis of the input.

If the request body is not valid JSON, has no `text` field, or is missing the `Content-Length` header, the server currently fails to answer correctly (see [Project status](#project-status)).

## Project scope

**In scope**

- Extracting lemmatized keywords (nouns, proper nouns, adjectives) from Polish text
- A single HTTP endpoint for keyword extraction and a simple health-check response
- Containerized deployment with Docker and Docker Compose

**Out of scope (currently)**

- Languages other than Polish
- Authentication, rate limiting, or any form of access control
- HTTPS / TLS termination (expected to be handled by a reverse proxy if needed)
- Persistent storage of requests or results
- Configurable keyword count, part-of-speech selection, or scoring methods

## Project status

The project is an early-stage, experimental service. It works for its core use case, but it is not production-hardened.

Known limitations and open items:

- **Startup side effect:** `server.py` calls `run()` at module level, so importing the module (for example from `passenger_wsgi.py`) starts the server immediately.
- **Model loading per request:** `pl_core_news_lg` is loaded inside `get_keywords()` on every request, which is slow. Loading it once at startup would be a significant improvement.
- **Limited error handling:** malformed JSON, a missing `text` field, or a missing `Content-Length` header causes an unhandled exception instead of a proper `4xx` response.
- **Single-threaded HTTP server:** `HTTPServer` processes one request at a time.
- **Outdated base image:** `python:3.8-slim-buster` is an end-of-life Python version and Debian release.
- **No automated tests** and no CI pipeline.
- **No versioned releases** or changelog yet.

## License

No license has been specified for this project yet. Until a `LICENSE` file is added, all rights are reserved by the author and the code may not be reused, modified, or distributed without permission.
