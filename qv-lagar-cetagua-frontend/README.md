# Qv-Lagar-Cetagua-Frontend

Version
Angular 16.1.0

## Project description

Web application for monitoring various parameters in water distribution networks,from anomaly detection, network status operations, historical performance data, the upload and download files associated with network status and automatic corrections of assignments clients to sectors, all within three main modules: Leaks search module, the hydraulic performance calculation module and user's assignment for hydraulic sectors module


## Environment Configuration

### Configuring `environments.ts`

The `environments.ts` file is located in the `src/environments` folder and contains configuration for the environment and some constants uses on the project. This is where the domains of the backends and frontend are registered. To configure the domains, follow these steps:

1. Open the `environments.ts` file in your code editor.

2. In the section corresponding to the development environment (`environment.ts`), set the domains of the backends and frontend as follows:

export const domainSettings = {
  domainApiAuth: 'http://backend1-domain.com/',
  domainBackend: 'http://backend2-domain.com/',
  domainFrontend: 'http://frontend-domain.com/'
};


## Run the ptoject

### 🐳 Using Docker
Build the docker image fro the Dockerfile located in the project root and then, run a container for the project

1. In console, on the project path, build the docker image with your own preferences 

    docker build -t <nombre_imagen> ./

2. In console, on the project path, run the container with your own preferences 

    docker run --name <nombre_contenedor> -p <puerto_host>:<puerto_contenedor> -d <nombre_imagen>


More information for Unix environment: 
- `make up`: Launch the project.
- `make ps`: Execute the `ps` command.
- `make stop`: Halt the Docker containers without removing them.
- `make rebuild`: Reconstruct the base Docker images.
- `make reset`: Update the Docker images and reset the local databases.
- `make pull`: Update the Docker images without losing the local databases.
- `make bash`: Open a shell in the project directory.
- `make log`: Retrieve only the Django project log.
- `make logs`: Fetch logs from the entire project.

### Prefer local environment 
With Node.js and Angular CLI installed, runs the follow commands:

1. npm install
2. ng serve -o


