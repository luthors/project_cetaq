# Qv-Lagar-Cetagua-Backend

Version:
Python 3.10.12
Django 4.2.7

### Initialization

If you want to initialize this project, please follow the steps below :

1. Create an .env file inside the envs folder.
2. In the .env create the following variables, with the value of your choice. :

   ##### - `POSTGRES_PASSWORD`=pasword_example

   ##### - `POSTGRES_USER`=user_example

   ##### - `POSTGRES_DB`=cetaqua_DB `DON'T MODIFY THIS VALUE`

   ##### - `POSTGRES_HOST`=cetagua_db `DON'T MODIFY THIS VALUE`

After that, you can start Docker

### 🐳 Using Docker

Prefer Docker? We've got you covered:
- `make up`: Launch the project.
- `make ps`: Execute the `ps` command.
- `make stop`: Halt the Docker containers without removing them.
- `make rebuild`: Reconstruct the base Docker images.
- `make reset`: Update the Docker images and reset the local databases.
- `make pull`: Update the Docker images without losing the local databases.
- `make bash`: Open a shell in the project directory.
- `make log`: Retrieve only the Django project log.
- `make logs`: Fetch logs from the entire project.
