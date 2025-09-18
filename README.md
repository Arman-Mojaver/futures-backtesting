## Introduction

This project provides an end-to-end, reproducible pipeline for collecting market data from **Databento**, storing it in the compact **`.dbn`** format, and running backtests in **Nautilus Trader**. It is designed for quant developers, researchers, and traders who need reliable historical market data ingestion, deterministic backtesting, and automated result reporting.

At its core the project automates three primary responsibilities:

1. **Data acquisition**: request and retrieve tick and bar-level market data from Databento.
2. **Data storage**: persist the raw market data to disk in the `.dbn` format so that datasets are compact, versionable, and easily distributed across environments.
3. **Backtesting and reporting**: run strategy backtests in Nautilus Trader using a CLI-driven workflow, capture performance metrics, and export a detailed PDF report summarizing results.

## Dependencies
In order to run the CLI the following dependencies are required:
- Docker
- docker-compose (optional)

## How to get started
In order to get started the following lines of code clone the repository and set up the project in one go (docker-compose required).
```
git clone https://github.com/Arman-Mojaver/futures-backtesting.git
cd futures-backtesting
make setup
```
The setup will prompt for the `DATABENTO_API_KEY`. If the `DATABENTO_API_KEY` is not introduced, the `save` command will not work (an API key is required to access Databento API). If left blank the setup will continue, and the other commands will work fine (there is example data in the repository).

Each step of the setup can also be done manually as follows (the following steps are not necessary if `make setup` is run):

1. Clone the repository:
```
git clone https://github.com/Arman-Mojaver/futures-backtesting.git
```
2. Create an `.env` file:

Make a copy of `.env.example` and name it `.env`, or run:
```
make env-file
```

3. Optionally add your Databento API key in `.env`, by setting the environment variable `DATABENTO_API_KEY`.

4. Start the container using docker compose:
```
docker compose -f docker-compose.yaml up -d
```
or
```
make up
```
5. Open a bash shell in the container:
```
docker compose -f docker-compose.yaml exec -it cli bash
```
or
```
make in
```
6. Execute the CLI:
```
bt
```

## Setup without docker-compose
The following command allows you to execute the CLI by using only Docker, in case docker-compose is not installed on the machine. The `DATABENTO_API_KEY`environment variable has to be set below for the `save` command to work:
```
git clone https://github.com/Arman-Mojaver/futures-backtesting.git
cd futures-backtesting
docker build -t futures-backtesting .
docker run -it --name futures-backtesting \
  -v "$(pwd):/code" \
  -e ENVIRONMENT="development" \
  -e DATABENTO_API_KEY="db-..." \
  futures-backtesting bash
```
Once the image has been built and the container started, execute the CLI:
```
bt
```

## CLI
The CLI is accessed by opening up a bash shell inside the container, and typing `bt`.
1. Open a bash shell inside the container:
```
docker compose -f docker-compose.yaml exec -it cli bash
```
or
```
make in
```
2. Execute the CLI:
```
bt
```

Example commands:
```
bt save --limit 1000 --start_date 2024-01-10 --end_date 2024-01-11
```
```
bt stats
```
```
bt indicator ma_cross --fast_period 20 --slow_period 50
```

## How to backtest strategies
The CLI supports two functionalities:
* Retrieve data from Databento and store it in a local file
* Use the retrieved data to run backtesting strategies.

In order to retrieve data from Databento, you have to introduce your Databento API Key in the environment variable named `DATABENTO_AKI_KEY`, and start/restart the containers.

Once the environment variable has been filled, you can access the CLI and run the save command:
```
make down && make up && make in
```
```
bt save
```
The command is specified so that by default it is safe, and does not retrieve a large amount of data by accident. It just retrieves one data bar by default (defined by the `--limit` parameter). If larger amounts of data needs to be retrieved, all parameters need to be specified:
```
bt save --limit 400000 --start_date 2024-01-01 --end_date 2025-01-01
```

Every time the `bt save` is run, a new file is generates in the folder `price_data`.
When files are parsed from the `price_data` folder, all the files are sorted alphabetically, and since the file names start with the timestamp from when they were created, the latest file will be always parsed.

In order to inspect the metadata of the current file in `price_data`, run the following command:
```
bt stats
```

If no Databento is available to you, you can still use the default data that exists in the repository.
In order to see the available strategies, run the following command:
```
bt indicator --help
```
It will display a list of available commands, one per indicator.
The following command is an example of running an ema_cross indicator:
```
bt indicator ema_cross --fast_period 20 --slow_period 50
```

Once the strategy has finished running, check the results in the `results` folder.


## Key components

* **Databento client layer**: Responsible for constructing data requests, handling authentication, and saving returned data as `.dbn` files.

* **Storage layer (.dbn)**: The project standardizes on `.dbn` files as the canonical on-disk format.

* **Backtesting engine (Nautilus Trader)**: Nautilus consumes `.dbn` datasets and executes strategy logic.

* **CLI (Click)**: All main interactions are exposed through a CLI, including commands to request data, list and inspect `.dbn` files, run backtests, and generate PDF reports.

## Outputs

The repository organizes produced artifacts into two main folders for clarity and reproducibility:

* price_data/: the storage location for all `.dbn` dataset files.

* results/: stores backtest outputs (PDF and `.json`)


## Environments

This project supports three runtime environments: `production`, `development` and `testing`. The active environment is selected by setting the `ENVIRONMENT` variable inside a `.env` file at the repository root. Docker Compose reads that `.env` file automatically and the variable is passed into containers so application code and entrypoints can branch behavior accordingly. The default environment is `development`.


## Tests
In order to run the tests, run the following command:
```
make pytest
```
