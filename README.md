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

### Database commands

 - Initialize the database
 `docker-compose exec website wayblazer db init`
 
 - Seed the database with one user
 `docker-compose exec website wayblazer db seed`
 _user: roryshively1@gmail.com_
 _password: asdfasdf_
 
 - Reset the database
 `docker-compose exec website wayblazer db reset`
 _clears the database, runs init, then runs seed_

 - Access the database in the terminal
 `docker-compose exec postgres psql -U wayblazer`
 
### Testing commands

 - Run test suite
 `docker-compose exec website wayblazer test`
 
 - Run test coverage
 `docker-compose exec website wayblazer cov`
 
 - Run flake8
 `docker-compose exec website wayblazer flake8`
 
## REST docs and Interview questions

View REST API docs and interview questions in the browser
at `localhost:8000/rest-docs` and `localhost:8000/questions`
respectively



 
Who works for Rapid Trading Intl?
  localhost:8000/api/employee?company=Rapid%20Trading%20Intl

Do any employees have the same personal phone number? 504-845-1427
  localhost:8000/api/employee?duplicate_number=true

Bonus: Find all employees with a personal Gmail email address but exclude
 anyone from CA.
  localhost:8000/api/employee?email_provider=gmail&exclude_state=CA


