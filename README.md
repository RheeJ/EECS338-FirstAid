# EECS338-FirstAid
### Running Application Locally
In order to run the application locally, pull the docker container by running "docker pull treefr0g/eecs338-firstaid" and run by running "docker run -p 8080:8080 treefr0g/eecs338-firstaid" This method will allow you to postman requests locally, but will not be able to talk with the android applcation.
### Running Application in AWS
In order to deploy to an online platform there are a few steps necessary.
##### Clone the Git
##### Set up RDS Database on AWS with MySQL
After setting up a simple MySQL database, configure in settings/settings.py under DATABASES to point to your RDS instance.
##### Dockerize
Docker build any new changes and push to treefr0g/eecs338-firstaid.
##### Upload Dockerrun.aws.json into AWS Elastic Beanstalk to run up an instance with the container.
##### Use the Android App!

# Developing and Improving
### In order to build and test:
You will require a python virtualenv. Configure activate script to run dev_settings.py.
For example: On Windows, add this "set "DJANGO_SETTINGS_MODULE=settings.dev_settings"" to activate.bat.
### The endpoint localhost:8000/manual_app/data_post takes a long time so when posting instruction sets, use Django localhost.
"python manage.py runserver" to run local server. There are three examples in fixtures.json.

# Perhaps New Approach
### Database stores different tools per instruction set.
##### What tools are used in the procedures?
##### What are the warnings?
##### What are the different time parts?
##### What are the different location parts?
##### What are the different temperaturs parts?

### Each of the Database attributes may be linked up with a set.

### Machine Learning amongst different attributes from different sets.
