# Homes& Real Estate Chatbot

## Overview

The Homes& Real Estate Chatbot is an intelligent assistant designed to help users find their dream homes or investment properties. Built with Flask and integrated with OpenAI's language models, the chatbot engages users in a conversational flow to gather preferences and provide personalized property recommendations.

## Getting Started

To run the chatbot project locally, follow the steps below:

## Prerequisites

- Python 3.10 or higher
- Flask
- MySQL

## Installation

1. Clone the repository

```bash
git clone <repository_url>
```

2. Install the dependencies

```bash
pip install -r requirements.txt
```

3. Run the migrations

```bash
Flask db init
Flask db migrate
Flask db upgrade
```

4. Create an `.env` put in it the env variables

```bash
touch .env
```

5. Run the server

```bash
Flask run
```

## Project Structure

- api_client
  - used to call the API endpoint
- app
  - the Flask application
  - used to run the application
- data
  - used to store the data
- localization
  - used to store the responses messages in different languages
- migrations
  - used to manage the database migrations
- routes
  - used to define the routes
- services
  - used to define the services
- utilities
  - used to define the utilities

## Environment Variables

| Variable           | Description                              | Example                           |
| ------------------ | ---------------------------------------- | --------------------------------- |
| OPENAI_API_KEY     | The OpenAI API key                       | YOUR_OPENAI_API_KEY               |
| FLASK_ENV          | The environment of the Flask application | development                       |
| DB_DIALECT         | The database dialect                     | mysql                             |
| DB_USERNAME        | The database username                    | beltone                           |
| DB_PASSWORD        | The database password                    | beltone                           |
| DB_HOST            | The database host                        | localhost                         |
| DB_NAME            | The database name                        | beltone_db                        |
| HOMES_API_BASE_URL | The base URL of the homes API            | https://homes-api.dev.beltone.ai/ |
