## Hospital Appointment System
Stack: Django-Graphene, Postgres, JWT Auth

### Steps

#### To setup the project:

Install virtualenv globally:
pip install virtualenv

Run :

virtualenv env // or python -m virtualenv env

source env/bin/activate

pip install -r requirements.txt

#### To setup postgres db for the app:
docker-compose up

#### To migrate & seed db with json files:

Run:

sh deactivate //deactivate virtualenv shell

make seed

##### NOTE: This project makes use of jwt-auth.

#### To Run dev server:
make runapp

#### To run sample unit test:
make unit-test-cover

#### To login & make graphql calls, use postman for easy workflow [The JWT is stored in the cookies when logged in].

The usernames can be got from the json files.

POST http://localhost:8000/login/ -> Please mind the trailing slash
{
    "username": "<email>",
    "password": "testuser123"
}

#### To end a user session:
POST http://localhost:8000/logout/ -> Please mind the trailing slash
{
    "username": "<email>",
    "password": "testuser123"
}

GraphQL Endpoint: http://localhost:8000/api/graphql 

To access graphiql, visit the same link above in the browser

Note: To login as different users in Postman, ensure that you logout first as session is cookie based

#### To run unit test

Run

python manage.py test api  