# Arborator-Flask
This a flask port of the [arborator-server](https://github.com/Arborator/arborator-server) as commisioned by [Kim Gerdes](https://github.com/kimgerdes)

# Development
## On Windows
To create database
* `flask db init`
* `flask db migrate`
* `flask db upgrade`

Then run

* `set FLASK_CONFIG = development`
* `set FLASK_APP = run.py`
* `flask run`

## On Linux
* `export FLASK_CONFIG = development`
* `export FLASK_APP = run.py`
* `flask run`


## TODO
* Complete project functions conversions (25/5/18)
* Set redirect urls for oauth providers
* in-app edit of project config(ini) files or find alternative
* correct dead links on project page
* css corrections/additions/subtractions 


Check out the guide on the [Wiki page](https://github.com/Arborator/arborator-server/wiki).
