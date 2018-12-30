# this is an official Python runtime, used as the parent image
FROM kennethreitz/pipenv

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
ADD . /app

# unblock port 80 for the Flask app to run on
EXPOSE 80

ENV FLASK_APP=app
ENV FLASK_ENV=prod

# execute the Flask app
CMD python3 app.py