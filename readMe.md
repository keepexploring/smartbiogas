Setting up server
sudo pip install virtualenv
sudo pip install virtualenvwrapper
pip install -r requirements.txt


Install pip
sudo apt-get install python-setuptools python-dev build-essential
sudo easy_install pip

Install services for deployment:
sudo apt-get update
sudo apt-get install ufw
sudo apt-get install nginx
sudo apt-get install python-dev libpq-dev
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install git
sudo pip install virtualenv
sudo apt-get install binutils libproj-dev gdal-bin

Managing the Nginx Process
Now that you have your web server up and running, we can go over some basic management commands.

To stop your web server, you can type:

sudo systemctl stop nginx
To start the web server when it is stopped, type:

sudo systemctl start nginx
To stop and then start the service again, type:

sudo systemctl restart nginx
If you are simply making configuration changes, Nginx can often reload without dropping connections. To do this, this command can be used:

sudo systemctl reload nginx
