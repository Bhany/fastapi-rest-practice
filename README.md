# fastapi-rest-practice

Practice challenge to get rest service up and running with FastAPI


### Setup

To get it up and running, you must have Python 3.8+

0. Clone this repo to your local machine
> git clone https://www.github.com/bhany/fast-api-practice
> cd fast-api-practice
1. Optional, but recommended(steps 1-3): install virtual environment
> pip install --user virtualenv
2. Create virtual environment:
> virtualenv $name_of_your_env
3. Activate virtual environment:
> source ./$path_to_your_activate/bin/activate
4. Pip install requirements.txt
> pip install -r requirements.txt
5. Run uvicorn to load the main app; add python3 -m if needed
> python3 -m uvicorn main:app --reload
6. Now that the server is up you can check it out on your browser at
> localhost:8000

The pages empty since I haven't developed the app's frontend yet, but you can checkout all the api at:
> localhost:8000/docs

Sample data are located in /test/ you can send listed data within the script to the servers by running:
> python /test/send_messages.py

### TODOs
1. Generalize CRUD to inherit from base class
2. Add more unit tests
3. Integrate Alembic for database migrations
4. Add User/Auth system
5. Implement Frontend
6. Migrate to Postgres