# UAHExchangeAPI
FastAPI backend to UAH get exchange rate in ukrainian banks,
such as cash or online rate.
<br />
## How to run

The requirements for this project are:

* Python 3.11 or higher
* Redis 

To install using poetry:

```shell
$ poetry install
```

```shell
$ poetry export -f requirements.txt --output requirements.txt 
```

If you want to install with the default Python package manager such as ```pip``` or ```pipx```, use the above command to extract the requirements.txt file.

```shell
$ pip install -r requirements.txt
```

Then you can proceed with the dependency installation with the default ```pip```(Python package manager).

```shell
$ uvicorn app:app --reload --host=0.0.0.0 
```

This project is implemented as an asynchronous function. Therefore, it is recommended to run the server using the ```uvicorn``` command.

<br />