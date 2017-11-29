import pyodbc 
server = 'tcp:smartbiogas.database.windows.net' 
database = 'smartbiogas_database' 
username = 'joelchaney' 
password = 'nv/XJ5n"8hcq5k8PW|H=[)_U,nX#' 
driver = '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()