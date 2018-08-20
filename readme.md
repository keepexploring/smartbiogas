To run with development or production settings locally:

python manage.py runserver --settings=django_react.settings.development
python manage.py runserver --settings=django_react.settings.production

To use with lamdba run the environment variables file selecting production or deployment.

Then you can carry out tasks e.g. migrating and managing database or static files or uploading a new version of the app.