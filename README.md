Word counter
=====================================

Prerequisites
-------------
- Docker
- docker-compose

Check codestyles
----------------
Run commands from repository root

Check diff on pep8 errors
```python
git diff | pep8 --diff
```

Check diff on flake8 errors
```python
git diff | flake8 --diff
```

Check pylint errors
```python
pylint3 --rcfile=setup.cfg ./*
```

Run tests
---------------------
In web docker container run next command for
Unittests
```python
python -m unittest
```

Run tests with coverage and check report
```python
coverage run -m unittest
coverage report -m
```

Environment variables
---------------------
Please specify and change all environment variables in .env file. Current .env is an example of config suitable for local development.

**WARNING!!!**
Not keep your production settings in repository. You can create .env_prod and specify it on docker run.

Encryption keys
---------------
To safely keep encryption keys, we will specify their names in env config file and add them to .gitignore.
We will generate these files on server if keys where are not generated yet.
