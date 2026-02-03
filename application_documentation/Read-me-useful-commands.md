## This document will help you to introduce useful commands to run project

### Working with `uv`

<div id="badges">
  <a href="https://docs.astral.sh/uv/">
    <img src="https://docs.astral.sh/uv/assets/logo-letter.svg" alt="uv Badge"/>
  </a>

An extremely fast Python package and project manager

</div>

### To install uv or check version

`pip install uv`

- then lets check whether its installed properly by printing its version

`uv --version`

- if you want to add new dependancy library into project, eg. pandas

`uv add pandas`

### Running project

after installing `uv` we will spin our project directory to run as local server,
here we will bind our `main.py` which is kept inside of `app` folder to `:app`, with port of `8000` and we will reload server if any changes happen to file with flag `--reload`

`uv run uvicorn app.main:app --port 8000 --reload`

this will run our project with `http://localhost:8000`

### Working with Environment varibale `.env`

We can set the secrete of our project required variable values,
like Database, Server crediantials
in our project if we have `.env` file, then we can set all values to systems enviorenment by running
`set -o allexport; source /home/your-env-file-location/.env; set +o allexport`

then we can check whether our values are set to `env` or not by running
`printenv`

`note:` if we reboot our machine then all values set by above command will be flushed, to overcome this we can set our `.env` file values on start-up

change your `cwd` on your home directory by running `cd ~`

run `ls -la` to check file with name `.procfile`

open this `.procfile` in your favioute editor, eg `vi .procfile`, and then at bottom of the file paste the command
`set -o allexport; source /home/your-env-file-location/.env; set +o allexport`

then reconnect with your system by `exit` or `reboot` and you can check your variables in environment by running `printenv`, this will keep your `.env` files values into your system whenever you reboot or exit, hence no flush or values.

### Working with `almebic`

Alembic provides for the creation, management, and invocation of change management scripts for a relational database, using SQLAlchemy as the underlying engine
https://alembic.sqlalchemy.org/en/latest/index.html

you can find docs of almebic by running
`uv run alembic --help`

- this command will create new .py file in name of version_number and comment of it which we will use to change db

`uv run alembic revision -m "add user table"`

- to check your current version number
  `uv run alembic current`

- to check history of your versions
  `uv run alembic history`

- to check your current head
  `uv run alembic heads`

- to run the latest revesion
  `uv run alembic upgrade head`

- to run previous version, can simply run commands using numrical value, like `+1, +2 or -1, -2`, where each number represents steps from current version
  `uv run alembic upgrade +1`

- almebic is intelegent enough to detect your models defination and your current tabel structure in db
  `uv run alembic revision --autogenerate -m "auto-vote"`

### Working with Docker

`docker ps`

`docker images`

`docker system prune -f`

`docker rmi $(docker images -aq)`

`docker build -t backend:backend .`

`docker run -d --env-file ./.env -p 9000:9000 --rm backend:backend`

When to Use
Use `--rm` for:

Local development

- Testing images
- One-off scripts
- Temporary jobs
- CI pipelines

Avoid `--rm` for:

- Production servers
- Containers with volumes/data
- Long-running services
- Debugging crash loops

Best Practice Pattern
Dev
`docker run --rm -it backend:backend`

Production
`docker run -d --restart unless-stopped backend:backend`

Using `docker-compose`
if you want to up your Dockerfile
`docker-compose up -d`

if any changes happen to code of file and you want to rebuild the image
`docker-compose up -d --build`

Running custom docker compose file
`docker-compose -f docker-compose-prod.yml up -d --remove-orphans`

To shutdown and terminate the Docker
`docker-compose down`

### Working with Service file to host application

`sudo systemctl daemon-reload`

`sudo systemctl restart fastapi-updated-backend.service`

`sudo systemctl status fastapi-updated-backend.service`

`journalctl -xeu fastapi-updated-backend.service`

Enable service so it can up on system reboot
`sudo systemctl enable fastapi-updated-backend.service`
this will create the symlink and you will see output like

`Created symlink /etc/systemd/system/multi-user.target.wants/fastapi-updated-backend.service → /etc/systemd/system/fastapi-updated-backend.service.`

If we want to print the `.env` variables loaded on service running
`cat /run/gunicorn/workers.env`

### Working with webserver

**NGINX**

- High performance webserver that can act as a proxy
- Can handle SSL termination

![Nginx Server](/application_documentation/image.png)

install nginx into system
`sudo apt install nginx -y`

Since nginx is inactive, you must start it first:
`sudo systemctl start nginx`

Optional but recommended: enable on boot
`sudo systemctl enable nginx`

Now check status:
`sudo systemctl status nginx`

You should see:
Active: active (running)

hide Server header (advanced)
`sudo apt install nginx-extras`

from project foler in name of `application_documentation` copy the sample `nginx_fastapi_gunicorn_service.conf` file to the location
`/etc/nginx/sites-available` by running

`sudo cp /your-project-file-path/hosting/nginx_fastapi_gunicorn_service.conf .`
you can make necessary changes as required, but thi file will work

we will create the symlink file to load our conf file into the folder `/etc/nginx/sites-enabled`, lets run the below command

Disable the default site
`sudo unlink /etc/nginx/sites-enabled/default`
(or, equivalently)
`sudo rm /etc/nginx/sites-enabled/default`
This only removes the symlink, not the actual file in sites-available.

Enable your new FastAPI config
Create a symlink from sites-available → sites-enabled:
`sudo ln -s /etc/nginx/sites-available/nginx_fastapi_gunicorn_service.conf /etc/nginx/sites-enabled/nginx_fastapi_gunicorn_service.conf`

Lets check whether is there any syntax error is there in file
`sudo nginx -t`
if above command returns

```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

then it means we are good to go

now lets reload nginx to take effect of our newly created service
`sudo systemctl reload nginx`

your service will be available with proxy name as `http;//your-ip-address/webservice`

#### What to restart when code/config changes

You changed FastAPI application code (.py files)

- Restart Gunicorn service, NOT nginx.

`sudo systemctl restart fastapi.service`

Why?

- Gunicorn loads your Python code into memory
- Code changes are NOT picked up automatically in production
- Nginx just forwards requests — it doesn’t care about Python code

What NOT to restart
| Change | Don’t restart |
|---|---|
|FastAPI code |nginx
|Nginx config |gunicorn
|.env values |nginx

**Mental model (easy to remember)**

- Nginx → traffic cop
- Gunicorn → app engine
- FastAPI → engine internals

Change engine internals? → restart engine
Change traffic rules? → reload traffic cop

- if required
  Log rotation (IMPORTANT)

Create `/etc/logrotate.d/nginx-fastapi`

```
/var/log/nginx/fastapi_*.log {
  daily
  rotate 14
  compress
  missingok
  notifempty
  sharedscripts
  postrotate
      systemctl reload nginx > /dev/null 2>&1 || true
  endscript
}
```
