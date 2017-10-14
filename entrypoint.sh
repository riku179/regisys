#!/bin/sh

wait_db() {
    echo -e "started to wait $DB_HOST..."
#    until curl "$DB_HOST:$DB_PORT" > /dev/null 2>&1; do
    until curl "$DB_HOST:$DB_PORT"; do
        >&2 echo -e "$DB_HOST is unavailable - waiting..."
        sleep 3
    done

    >&2 echo "$DB_HOST is up!"
}

case "$1" in
	shell)
		bash
		;;
    prod)
        wait_db
        echo yes | python manage.py collectstatic
        gunicorn regisys.wsgi --access-logfile - -b 0.0.0.0:8000
        ;;
    *)
        wait_db
        python manage.py $@
        ;;
esac
