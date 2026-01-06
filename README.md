# What is this?

* That's the third version of my Task manager. here is the [first version](https://github.com/abdulrahman-wael/task_manager), [second version](https://github.com/abdulrahman-wael/task_manager_2)
* I'm trying here to be as independent as possible which creating this. The target was to not use even google search while coding this all (and most of the code is written in this way), but the docker part needed help by some google searches and AI prompts (also looking at previous versions of this Task manager :).
* Tech stack: as the previous versions: I'm using these libraries/programs and concepts: fastapi, streamlit, docker, docker-compose, pytest, pyproject.toml and behind the scenes: ruff, mypy, black + .env (environment variables), .venv (virtual environment)
* In the previous version I've documented the API file .. now I'll try document the APP (streamlit) file.

# To be improved

1. api: more comprehensive endpoints for the different needs of the app are wanted.
2. streamlit app:
3. testing: streamlit, journies, integrated tests, using fragmented unittests (not composite)
4. linting and formatting: pyproject.toml needs improvement.
5. docker: using another USER
6. deployment: Make the setup suitable for deployment in a popular cloud provider
7. documentation: applying best practices and making a comprehensive documentation.
8. database: using Postgres instead of SQLite (needed in production)

## Related questions

1. Must I change the host of streamlit to match that of fastapi in order for it to work?
2. How to make the docker ecosystem more suitable for trial and error (continous testing and improvement)?
3. What libraries are inside python:3.11-slim and what aren't?
4. How to be better in the linux commands I need (docker, fastapi, streamlit, curl, ....)?
5. How to document streamlit code?
6. How using postgres will change the code of docker-compose.yml, .env, api.py files?
7. What to do first: documentation or preparing docker? testing or documentation? ruff-related or pytest-related tasks?
