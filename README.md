# DSP

This is a tiny demand side platform (DSP) application that includes three services: `nginx`, `web` (Django), and `db` (PostgreSQL).

## Prerequisites

* Docker
* Docker Compose

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/Leo-tumo/dsp.git
   ```
2. Navigate to the `dsp` directory:

   ```
   cd dsp
   ```
3. Create a `.env` file with the necessary environment variables:

   ```
   touch .env
   ```

   Here's an example of what the `.env` file might look like:

   ```
   POSTGRES_USER=myuser
   POSTGRES_PASSWORD=mypassword
   POSTGRES_DB=mydb
   ```
4. Run the following command to start the application:

   ```
   make up
   ```

   This command will start the services in detached mode and create a directory called `data` if it doesn't already exist.
5. Navigate to the `printed address` in your web browser to access the Django admin interface.

## Usage

Here are some useful Makefile commands that you can use to manage the DSP application:

* `make build`: Builds the Docker images and starts the services.
* `make up`: Starts the services.
* `make migrate`: Runs the Django database migrations.
* `make stop`: Stops the services.
* `make fclean`: Stops the services and removes all Docker volumes.
* `make re`: Cleans up the Docker environment and restarts the services.
* `make prune`: Removes all unused Docker resources.
* `make bash`: Opens a bash shell in the `web` container.
* `make logs`: It's used to follow the logs of the dsp_web(django) container in real-time.

Note that you can also pass variables to the Makefile commands by using the following syntax:

```
make VARIABLE_NAME=new_value COMMAND_NAME
```

For example, to run the project on `localhost`, you can use the following command:

```
make HOST_IP=127.0.0.1 up
```

## License

This project is licensed under the [MIT Licens](https://chat.openai.com/chat/LICENSE)
