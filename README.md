# improved-umbrella

Create a .env file in the /app directory

Include the following lines to make this work

TIO_ACCESS_KEY=ACCESS_KEY_GOES_HERE

TIO_SECRET_KEY=SECRET_KEY_GOES_HERE

Build the Docker image

`docker build -f Dockerfile -t <call it whatever you want>:latest .`

Run the docker image

`docker run --name <name for the container in running state> -d -p 8000:8000 <whatever you called the image in the build command>:latest`