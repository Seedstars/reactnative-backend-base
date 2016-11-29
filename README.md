# Mobile App Base Project (Backend)

This repository includes a boilerplate project for backend to be used by React Native applications built in Seedstars Labs.

Download the React Native app here: https://github.com/seedstars/reactnative-mobile-app-base

## Readme Notes

* Command line starts with $, the command should run with user privileges
* Command line starts with #, the command should run with root privileges


## Retrieve code

* `$ git clone https://github.com/Seedstars/reactnative-backend-base.git`
* `$ cd reactnative-backend-base`
* `$ git submodule init`
* `$ git submodule update`
* `$ ./scripts/get_static_validation.sh`

Remember that when you copy this repository for a new project you need to add the scripts external module using:

* `$ git submodule add https://github.com/Seedstars/culture-scripts scripts`

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
