# MileFriend Maintenance Backend Project

This repository includes a boilerplate project for React Native applications used for Seedstars Labs.

## Readme Notes

* Command line starts with $, the command should run with user privileges
* Command line starts with #, the command should run with root privileges


## Retrieve code

* `$ git clone https://github.com/Seedstars/milefriend-maintenance-backend.git`
* `$ cd milefriend-maintenance-backend`

## Installation

### Main Project

* `$ virtualenv -p /usr/bin/python3 virtualenv`
* `$ source virtualenv/bin/activate`
* `$ pip install -r py-requirements/dev.txt`

* `$ cd src`
* `$ python manage.py migrate`
* `$ python manage.py runserver`

## Running

Run Django development http server

* `$ cd src`
* `$ python manage.py runserver`

## Testing

Backend (django/python tests)

* `$ ./scripts/test_local_backend.sh`


### Static analysis

To make sure the code respects all coding guidelines you should run the statics analysis script before pushing any code.

Backend (django/python static analysis)

* `$ ./scripts/static_validate_backend.sh`