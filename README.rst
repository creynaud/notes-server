Notes server
============

Installation
------------

Requirements:

* Python 2.7.4 + dev (ubuntu package: python-dev)
* PostgreSQL (ubuntu packages: postgresql postgresql-server-dev-?.?, mac os: http://postgresapp.com/)
* ubuntu package: daemontools (for "envdir")
* ubuntu package: pyflakes (for "flake8")
* ubuntu package: virtualenvwrapper (for "mkvirtualenv") (reopen a new shell after install)

Getting the code::

    git clone https://github.com/creynaud/notes-server
    cd notes-server
    mkvirtualenv -p python2.7 notes-server
    add2virtualenv .
    pip install -r requirements-dev.txt

Configuration
-------------

The notes server relies on environment variables for its configuration. The required environment variables are:

* ``DJANGO_SETTINGS_MODULE``: set it to ``notes.settings``.
* ``SECRET_KEY``: set to a long random string.
* ``ALLOWED_HOSTS``: space-separated list of hosts which serve the web app.
  E.g. ``www.awesomenotes.net awesomenotes.net``.
* ``FROM_EMAIL``: the email address that sends automated emails (password
  lost, etc.). E.g. ``Notes <info@awesomenotes.net>``.
* ``DATABASE_URL``: a heroku-like database URL. E.g.
  ``postgres://user:password@host:port/database``.
* ``AWS_ACCESS_KEY_ID``: your amazon S3 key id
* ``AWS_SECRET_ACCESS_KEY``: your amazon S3 secret access key
* ``S3_BUCKET_NAME``: your amazon S3 bucket name
* ``SENTRY_DSN``: your sentry URL
* ``SMTP_URL``: your smtp URL, e.g. //username:password@host:port?sender=info@awesomenotes.net

Optionally you can customize:

* ``DEBUG``: set it to a non-empty value to enable the Django debug mode.

Here is a bash command to show the current values::

    (cd envdir/ && for i in *; do echo $i = $(cat $i) ; done)

Create a super user in postgres::

    # inspired by http://obroll.com/how-to-reset-postgres-password-in-postgresql-ubuntu-11-10-oneiric/
    sudo su postgres
       psql
          ALTER USER postgres WITH PASSWORD '123';

Create the notes database::

    createdb -U postgres notes

"Sync" the db (django)::

    make syncdb
    make user
       # enter a mail for your *admin* user and a password

Then you can run and create stuff manually to see the thing::

    make run
    http://127.0.0.1:8000/admin
    http://127.0.0.1:8000

Development
-----------

Listing available commands::

    make <tab>

Before commiting anything, make sure to:

Run the tests::

    make test

Run the source code checker::

    flake8

The Django debug toolbar is enabled when the ``DEBUG`` environment variable is
true and the ``django-debug-toolbar`` package is installed.

Environment variables for development are set in the ``envdir`` directory. For
tests, they are located in the ``tests/envdir`` directory.
