Clone the repository.
Navigate to the project directory.
Running the Application

To start the application, run the following command:
docker-compose up --build

If you don't have docker compose installed, you can install it by running:
sudo apt install docker-compose

To run tests, follow these steps:

Access the container's shell using:
docker exec -it <container_name> bash

Once inside the container, execute the test suite using pytest:
pytest
