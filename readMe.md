
/*Set up virtual environment*/
1. pip install virtualenv (if you don't have it)
2. virtualenv ve_biogas
3. source [path to ve]/bin/activate
(source /home/scene/Desktop/biogas/ve_biogas/bin/activate)
/*install packages*/
4. cd (go to the saved folder smartbiogas)
5. pip install -r requirements.txt
6. sudo apt-get install binutils libproj-dev gdal-bin
Note: if an error with gdal library run
apt-get -f install
sudo apt-get install binutils libproj-dev gdal-bin

/*install react*/
7. nmp install
8. node_modules/.bin/webpack --config webpack.local.config.js /*creates bunde.js and test the instalation*/




/*Setting up server*/
1. sudo pip install virtualenv
2. sudo pip install virtualenvwrapper
3. pip install -r requirements.txt


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
>>>>>>> 3e0c21213773078ccd48759b79e852696c520c4d
