# Python build
FROM python:3.12-alpine

# Set the working directory in the container
RUN adduser -S -s /sbin/nologin -D flask
USER flask
WORKDIR /app

# Install any dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the program over
#COPY static static
COPY templates templates
COPY img img
COPY img_list.txt img_list.txt
COPY main.py .

# Specify the command to run on container start
CMD [ "/home/flask/.local/bin/waitress-serve", "--port", "5000", "main:app" ]