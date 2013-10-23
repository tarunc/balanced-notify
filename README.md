balanced-notify
===============

To install:

    python virtualenv.py notify/
    notify/bin/pip install .

(assumes you want the virtualenv in the `notify` subdirectory)

To run production:

    ./runp.py

To run debug:

    ./run.py

To test:

    BALANCED_ENV=test ./tests.py

To run with supervisord:

    notify/bin/pip install supervisor


    notify/bin/supervisord -c supervisor.conf


    notify/bin/supervisorctl -c supervisor.conf

