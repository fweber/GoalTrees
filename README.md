# GoalTrees

This digital companion for hierarchical goal setting in higher education is developed as Ph.D research project in the SIDDATA project (www.siddata.de). at the Insitute of Cognitive Science at Osnabrück University.

# Getting started
To run the project locally, follow this procedure:
- clone the repository
- install the python packages in requirements.txt into a virtual environment
- install posgresql and create an empty database
- copy the file settings_default.py and name it settings.py
- enter the credentials of the empty database into the database settings in settings.py 
- run 'python manage.py migrate' to create database tables
- run 'python manage.py runserver' to start the django application
- now the application should show up in the browser at localhost:8000

# Learning Django
If you are new to django, following a tutorial can be a good starting point:
https://docs.djangoproject.com/en/4.0/intro/tutorial01/


