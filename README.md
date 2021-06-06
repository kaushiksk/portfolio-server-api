# portfolio-server-api
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub](https://img.shields.io/github/license/kaushiksk/pyportfolio)](https://github.com/kaushiksk/portfolio-server-api//blob/main/LICENSE)
[![codecov](https://codecov.io/gh/kaushiksk/portfolio-server-api/branch/main/graph/badge.svg?token=NYYT6B3KYV)](https://codecov.io/gh/kaushiksk/portfolio-server-api)

Self hosted Web API to query your portfolio data

## Pre-requisites
 - Local installation of mongodb. Run `docker-compose up -d` to create one using hte docker config provided.
 - Preferably a virtual environment (conda/venv)
 - A CAS pdf file from [CAMS](https://new.camsonline.com/Investors/Statements/Consolidated-Account-Statement)/[KARVY]((https://mfs.kfintech.com/investor/General/ConsolidatedAccountStatement)

## Installation
 - Clone and install requirements
 ```bash
 $ git clone --recurse-submodules https://github.com/kaushiksk/portfolio-server-api/ && cd portfolio-server-api
 $ pip install -r requirements.txt # Preferably inside your venv
 ```
 - Copy and paste your CAS file as `cas-portfolio.pdf` under `portfolio-server-api/`
 - Initialize the db with your data
 ```bash
 $ python manage.py init-db # You will be prompted for the pdf password
 ```
 - Run the server
 ```bash
 $ python manage.py run 
 $ # or
 $ uvicorn portfolioserver:create_app
 ```

## API Docs
Visit `localhost:8000/docs` to view the Swagger UI docs.

## Development
Run the following additional commands during development.
```bash
$ pip install -r requirements-dev.txt
$ pre-commit install
```

## Testing
```bash
$ pytest -v
```
