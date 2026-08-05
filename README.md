# Emotion Detection Web Application

This repository contains the final project for the IBM Python and Flask course.
The application sends English text to the IBM Skills Network emotion service and
displays scores for anger, disgust, fear, joy, and sadness.

## Project structure

```text
EmotionDetection/       Python package and service client
static/                  Browser JavaScript
templates/               Flask HTML template
tests/                   Automated tests with mocked API calls
docs/course-progress/    Archived course exercises and terminal output
server.py                Flask application entry point
requirements.txt         Runtime dependencies
```

Only `EmotionDetection/emotion_detection.py` and `server.py` are used by the
running application. Earlier course steps are kept under `docs/course-progress`
for reference.

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run the application

```bash
python server.py
```

Open `http://127.0.0.1:5000` in a browser.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The test suite mocks the external emotion service, so tests do not require
network access and return deterministic results.
