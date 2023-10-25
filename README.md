# opencv openapi

[![python version](https://img.shields.io/badge/Python-3.7-success.svg?style=flat)]()
[![build status](https://img.shields.io/badge/build-pass-success.svg?style=flat)]()

## Technology stack

- [py3utils](https://github.com/reggiepy/py3utils.git)
- *template generate
  by* [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D)
- fastapi==0.98.0
- sqladmin==0.15.2

## Installation

```bash
pip install -r requirements.txt
git clone https://github.com/reggiepy/py3utils.git
```

## Init Databases

* first init alembic

```console
alembic init alembic  
```

* If you created a new model in `./backend/app/app/models/`, make sure to import it in `./backend/app/app/db/base.py`,
  that Python module (`base.py`) that imports all the models will be used by Alembic.

* After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```console
$ alembic upgrade head
```

If you don't want to use migrations at all, uncomment the line in the file at `./backend/app/app/db/init_db.py` with:

```python
Base.metadata.create_all(bind=engine)
```

and comment the line in the file `prestart.sh` that contains:

```console
$ alembic upgrade head
```

If you don't want to start with the default models and want to remove them / modify them, from the beginning, without
having any previous revision, you can remove the revision files (`.py` Python files)
under `./backend/app/alembic/versions/`. And then create a first migration as described above.

## Build

```bash
# 打包
Pyinstaller --noconfirm -i favicon.ico yf_agent.py --uac-admin -p ./ --add-binary VERSION;. --add-binary database_empty.db;. --add-data static;static --add-data data;data --hidden-import aiosqlite --hidden-import yf_agent --distpath "C:\dist\app" --workpath "C:\dist\build"

# 打包cli
Pyinstaller --noconfirm -i favicon.ico cli.py -n yf_cli -p ./ --add-binary VERSION;. --add-data static;static  --distpath "C:\dist\app" --workpath "C:\dist\build"

python cli.py license generate_file -fn license_a64210ce.key -exp "2023-12-31 00:00:00"
```