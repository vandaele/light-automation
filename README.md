# light-automation
Python module for managing the Lille's FIT IoT-LAB light automation system

# Installation
Do a
```pipenv install``` to install the dependencies in a virtualenv. If you
don't have pipenv, you need to call ```pip install pipenv``` before


# Usage
Specify the correct host and port for the Modbus automaton in config.yml before
starting the scripts. Then start the script you want:

* ```pipenv python all_off.py```
* ```pipenv python all_on.py```
* ```pipenv python loop_write.py```
* ```pipenv python randomize.py```
