# Set base image
FROM python:3.8

# Set working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip3 install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# command to run on the container start
CMD [ "python", "-u", "./twitterBot.py" ]
