web: gunicorn sifibr_collections.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate && python manage.py create_test_data 