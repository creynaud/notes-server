django = envdir envdir python manage.py
testdjango = envdir tests/envdir python manage.py

run:
	$(django) runserver

test:
	$(testdjango) test --traceback --failfast --noinput ${TEST}
	rm -rf notes/test_media

syncdb:
	$(django) syncdb --noinput

freshdb:
	$(django) reset_db --router=default --noinput && $(django) syncdb --noinput

user:
	$(django) createsuperuser

shell:
	envdir envdir python

devshell:
	envdir tests/envdir python

coverage:
	envdir tests/envdir coverage run --source=notes manage.py test --noinput
	coverage html

gunicorn:
	envdir envdir gunicorn notes.wsgi

compass:
	envdir envdir compass watch --force --no-line-comments --output-style compressed --require less --sass-dir scss --css-dir notes/core/static/core/css scss/screen.scss
