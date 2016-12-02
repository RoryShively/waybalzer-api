# Project

Description of the project goes here

## Requirements

This project has been tested using:
 - Docker version `v 1.12.3`
 - Docker-compose `v 1.8.1`

## Installation

Open up your terminal under the directory you want to put this project in and clone this repo

`git clone https://github.com/RoryShively/wb.git`

cd into the project

`cd wb`

Build the containers with docker-compose and run them

`docker-compose up --build`'

In another terminal window and cd into the project directory

`cd /path/to/directory/`

Initiaize the database to create tables

`docker-compose exec website wayblazer db init`

Open up your browser and go to `localhost:8000`

From here you should:
 - Click Sign Up in the top right corner to create an account
 - Once logged in, click CSV Upload in the top right corner
 - Upload `us-500.csv`

## Command line Tools
