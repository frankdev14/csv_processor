# CSV/API Processor

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Project Overview

Throughout the project, "Simplicity is better" has been taken into account, and
everything has been simplified to allow for more precise development. However, due to my
personality, I wanted to create something that was scalable, just like simple.
That's why the project follows this structure, where the CSV processor is an independent module
or library, which could even be installed as a Python package.

The __CSV processor__ bears similarities with a project I was involved in,
so I have opted to follow the same structure.

On the other hand, __the development of the API__ has been taken into account and
modularized. In production, I would opt for using message queues, but in this case,
since the task requires simplicity and can be executed by anyone outside an environment,
I have chosen to incorporate a database to store records of processed data and maintain
the processing state of each record.

In a production environment, I would opt for a more robust database to store records
of all executions and use RabbitMQ, so that the API can communicate with multiple
processes and avoid leaving tasks hanging.

## Project Structure

The project has been created following a basic webapp structure, where we have the
following folders::

* **app**: The folder contains all the necessary files of the application.
  * **database**: Inside it, we find all the files to create and connect to the database, as well as the
models that have the schemas of the same.
  * **processors**: This folder contains the processors that we will execute in the API.
    * **tmp**: The temporary folder where the CSV files to be executed will be split.
  * **tasks**: On this folder, tasks related to the execution of the processors we add will be
stored.
* **output_data**: Here will be stored the results of the processes carried out by the API.
* **docs**: The documentation on code analysis is located within this folder.


## Requirements for App Execution

First of all, we should have a version of Python 3 available. If we already have it,
we can install the libraries on top of this or, as in your case, create a virtual
environment.

If you have Python installed and do not plan to use a virtual environment, run the
following code:

```sh
pip install -r requirements.txt
```

In the event that you need to create a virtual environment, we will first execute the
following commands:

```sh
python -m venv [env_name]
source env_name/bin/activate
pip install -r requirements.txt
```

Change python for python3 if you are using Unix system.

## Step-by-step execution

### CSV Execution

To run the csv processor I have created a small script to run it, execute the following command: `python run_csvprocessor.py [input_file] [output_file] [chunk_size]`. Note that the `[chunk_size]` argument is optional, and defaults to 1000 if not
provided. The user can modify this value to suit their specific requirements.

**Example:**

```sh
python run_csvprocessor.py --input /home/frank/Development/bmat_task/songs_input.csv --output /home/frank/Development/bmat_task/output.csv --chunk_size 1
```

In this case, I've set the chunk size to 1.

### API Execution

To run the API, I have chosen two variants. The first one is the simple execution in
which I provided two scripts: one for Windows and another for Unix systems. Before
executing either script, please follow the installation steps.

#### First Execution Type
Both scripts have the following configurations:

* **DEBUG_MODE** (True or false) - If the file is very small or the processing is very fast, set to True to simulate a
large file. Otherwise, leave it at False.

* **virtual env** (String) - Depending on the system and whether you're using a virtual environment or not, here
you will uncomment the line and set the path to where the virtual environment's
activator is located. I've left examples in both scripts for your reference.

The rest of the script is best left as it is, as it handles the execution of the API.

For unix execution, I set the permission for execute but if you need it. Use it:

```sh
./start_api_unix.sh

or

exec ./start_api_unix.sh
```

For windows execution, double click on `start_api_windows.ps1` and a terminal will launch.

The execution of the file in Windows has not been tested as I do not have a system to
test it. If this script does not work, please proceed with the next type of execution.

#### Second Execution Type

If you have virtualenv, please activate first:

```sh
source [/your_env_path/activate]

Example:
source /home/frank/Development/bmat_task/bmat_api/bin/activate
```

If not, you can enter into the app folder, and launch the main with uvicorn:

```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The script is simpler and also incorporates the DEBUG environment variable to simulate
heavy file processing. If you choose to use this mode of execution and want to try it in
debug mode, you will need to set the DEBUG environment variable manually.

# API Usage

To call the API, we will need to call the following URLs depending on two endpoints:

#### `API Endpoint for Upload CSV`
Is a POST requests to this url:
```sh
http://127.0.0.1:8000/upload_csv/ [arg]CSVFile

OR

http://0.0.0.0:8000/upload_csv/ [arg]CSVFile
```

___Usage Example with curl:___
```sh
curl -X POST "http://127.0.0.1:8000/upload_csv/" -F "file=@/home/frank/Development/bmat_task/songs_input.csv"
```

Dont remove @ from cUrl request, only change path.
This execution will give you a task ID, which will be stored in the database, along
with whether it has finished processing and the name of the output file.

__Return:__
```sh
{"task_id":1}
```


#### `API Endpoint for Result Download`
Is a GET requests to this url:
```sh
http://127.0.0.1:8000/task_status/{task_id}

OR

http://0.0.0.0:8000/task_status/{task_id}
```

{task_id} is the Task ID obtained when uploading the file

___Usage Example with curl:___
```sh
curl -X GET "http://127.0.0.1:8000/task_status/3"
```

This execution will give you a task ID, which will be stored in the database, along
with whether it has finished processing and the name of the output file.

__Return:__
```sh
{"task_id":3,"is_finished":true,"output_file":"/home/frank/Development/bmat_task/output_data/processed_songs_input.csv"}
```

# API Code review

### [`Read API Code Review`](docs/API.md)

# CSV Processing Code review

### [`Read CSV Processor Code Review`](docs/CSV_PROCESSOR.md)
test
