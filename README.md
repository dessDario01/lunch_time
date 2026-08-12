# Coffee Hunter

A simple Flask + SQLite coffee collection app.

## Features

- Search sample coffees by name, origin, roast, or flavor.
- Save coffees with a 1–5 star rating and tasting notes.
- View all saved coffees in **My Collection**.
- Delete saved coffees.
- Responsive, warm coffee-themed UI.
- SQLite database is created automatically on first run.

## Requirements

- Python 3.9+
- pip

## Installation

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open:

http://127.0.0.1:5000

The SQLite database `coffee_hunter.db` will be generated automatically.

## Project structure

```text
coffee_hunter/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   └── collection.html
└── static/
    └── style.css
```

## Notes

The coffee catalog is sample data stored directly in `app.py`. The saved collection is persisted in SQLite.
