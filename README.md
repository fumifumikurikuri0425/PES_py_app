# # Getting Started PES App

These programs are used on the server side.

This project is based on [FastAPI](https://fastapi.tiangolo.com/)

## About PES App

A potential energy surface (PES) describes the energy of a system, especially a collection of atoms, in terms of certain parameters.

This app can draw beautiful PES and search EQ and TS.

You can draw PES from files or writing function program.

## Installation
Clone and enter the project directory:
```
git clone https://github.com/fumifumikurikuri0425/PES_py_app.git
```
If you haven't cloned JavaScript repository, please clone https://github.com/fumifumikurikuri0425/PES-js-app.git

Prerequisites:
- Python 3.9
- pipenv

Install the project dependencies:
```
pipenv install --dev
```
If you fail to install some dependencies, install them with pip manually.

## Run scripts
In the project directory, Run in development mode:

 ```
pipenv shell
uvicorn app:app --reload
 ```
And open another terminal, enter the JavaScript directory, run JS programs.

## About Files
`function_memo.py` is coded about function for drawing pes. Please customize your favorite function.

`optimize_line.py` and `optimize_from_code.py` is stored the program (New Raphthon method and gradient decent method). Please customize your favorite algorithm.

## License
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
