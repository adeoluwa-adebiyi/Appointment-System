seed:
	# rm db.sqlite3
	env/bin/python manage.py migrate
	env/bin/python manage.py seed_db

runapp:
	env/bin/python manage.py runserver

unit-test-cover:
	env/bin/python manage.py test api
