# Simple React Structure on Django

### USAGE
> Follow next article or Download this repository

#### Follow this article.
* https://medium.com/@urangurang/react-on-django-boilerplate-3c3735df41f2#.4dslhg6us

- - -
#====================Local Installation=======================================
#### Git Clone


#Set up virtual environment
* pip install virtualenv (if you don't have it)
* virtualenv ve_biogas
* source [path to ve]/bin/activate
(source /home/scene/Desktop/biogas/ve_biogas/bin/activate)

#install libs
* cd (go to the saved folder smartbiogas)
* pip install -r requirements.txt
* sudo apt-get install binutils libproj-dev gdal-bin
Note: if an error with gdal library run
apt-get -f install
sudo apt-get install binutils libproj-dev gdal-bin

* python manage.py migrate

#install react packages
* npm install
* webpack --config webpack.config.js
* python manage.py migrate

python manage.py collectstatic

#run the App
* python manage.py runserver


#====================Deployment=======================================
#Setting up server
* sudo pip install virtualenv
* sudo pip install virtualenvwrapper
* pip install -r requirements.txt


#Install pip
sudo apt-get install python-setuptools python-dev build-essential
sudo easy_install pip

##Install services for deployment:
sudo apt-get update
sudo apt-get install ufw
sudo apt-get install nginx
sudo apt-get install python-dev libpq-dev
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install git
sudo pip install virtualenv
sudo apt-get install binutils libproj-dev gdal-bin

###Managing the Nginx Process
Now that you have your web server up and running, we can go over some basic management commands.

To stop your web server, you can type:

sudo systemctl stop nginx
To start the web server when it is stopped, type:

sudo systemctl start nginx
To stop and then start the service again, type:

sudo systemctl restart nginx
If you are simply making configuration changes, Nginx can often reload without dropping connections. To do this, this command can be used:

sudo systemctl reload nginx
