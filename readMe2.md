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
