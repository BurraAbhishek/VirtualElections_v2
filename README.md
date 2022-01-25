# VirtualElections_v2

A forever free, adless and open-source voting platform to conduct elections remotely, written in Django

This is a rewrite of https://github.com/BurraAbhishek/VirtualElections.

This website is written in [Python 3](https://www.python.org/), and relies on the [Django framework](https://www.djangoproject.com/). HTML and [the Django Template Language](https://docs.djangoproject.com/en/4.0/ref/templates/language/) are used for templating, [using CSS for styling](https://github.com/BurraAbhishek/VirtualElections_v2/tree/main/static/css). [MongoDB](https://www.mongodb.com/) is used as the primary backend database, and [redis](https://redis.io/) is used as a cache.

## Setup

### Pre-requisites:

Before beginning, please make sure you have the following tools installed:

### Hardware:

- At least 4 GB of RAM
- A CPU with 64-bit architecture

### Tools:

- `python3`

### Infrastructure

- `mongodb` (>=4.2, [instructions](https://docs.mongodb.com/manual/administration/install-community/), [WSL2](https://stackoverflow.com/questions/62495999/installing-mongodb-in-wsl))
  - For WSL2, you might want to manually create the default `/data/db` directory and give ownership permissions to your user (``sudo chown -R `id -un` /data/db``). If `sudo service mongod start` does not work, you may want to open a terminal and run `mongod` as super-user.
- `redis`

### Python packages

- [django framework](https://www.djangoproject.com/): Install using `pip install django`
- [djongo engine for MongoDB](https://www.mongodb.com/compatibility/mongodb-and-django): Install using `pip install djongo`
- [django-redis](https://github.com/jazzband/django-redis): Install using `pip install django-redis`. Dependencies will also be installed.

## Installation

- Clone (`git clone https://github.com/BurraAbhishek/VirtualElections_v2.git`) or download this repository.
- (Optional, recommended for production) Apply migrations using `python manage.py migrate`. Also check the [official guide](https://docs.djangoproject.com/en/4.0/howto/deployment/). Deploying static files on the same server is not recommended since it may slow down your application.
- Then run `python manage.py runserver` to start the application. 
- If you're running on localhost, you can deploy static files on the same server and can ignore the migrations warning.
- If you're running on localhost (127.0.0.1), then go to `http://localhost:8000/` or `http://127.0.0.1:8000/`. The port number is 8000 by default, and it may be different if you configure a different port number. If your webserver supports TLS, you can use `https` instead of `http`.
- Finally, using your web browser, go to `/modzone/` (in the default localhost configuration, it is `http://localhost:8000/modzone/`) to complete the installation. 

## LICENSE

This repository is [dual-licensed](https://github.com/BurraAbhishek/VirtualElections_v2/blob/main/LICENSE.md) under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt) and the [GNU Affero General Public License 3 or any later version at your choice](https://www.gnu.org/licenses/agpl-3.0.txt).

### External Resources

Files | Author(s) | License
--- | --- | ---
[Font Awesome v4.7 in static:fa](https://github.com/BurraAbhishek/VirtualElections_v2/tree/main/static/fa) | [The Font Awesome Team](https://github.com/FortAwesome/Font-Awesome#team) | [CC-BY 4.0, SIL OFL 1.1, MIT](https://github.com/FortAwesome/Font-Awesome/blob/master/LICENSE.txt)
Noto Sans in static:fonts | [Google](https://fonts.google.com/specimen/Noto+Sans) | [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)
Roboto in static:fonts | [Christian Robertson](https://fonts.google.com/specimen/Roboto) | [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)
