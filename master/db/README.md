# Usage
Before running the main application `app.py`, you must connect to the database by running
`python db.py`. Our database assumes you have an instance of MySQL server running locally.

# Dependencies
1. MySQL-python
2. mysqlclient
3. passlib
4. wtforms
5. SQLAlchemy (TODO: can this be removed?)

# Installation
1. MySQL Server:  
   - Visit the following link to download and install MySQL Server https://dev.mysql.com/doc/refman/5.7/en/installing.html
2. Python Packages:  
   - `pip install <package-name>`

# Initial Database Setup
1. Open mysql and enter root's password when prompted:  
   - `mysql -u root -p`
2. Grant access to all MySQL databases for user 'dermagram' on localhost with password
also set to 'dermagram':  
   - `GRANT ALL PRIVILEGES TO *.* 'dermagram'@'localhost' IDENTIFIED BY 'dermagram'`
3. Quit out of mysql and create database using 'dbScript.sql':  
   - `mysql -u dermagram -p -h localhost < dbScript.sql`
4. Open connection to the database:  
   - `python db.py`  

# Troubleshooting (by OS)
## Windows 10 64-bit
If you had trouble installing `MySQL Server`, then try the following alternative:  
1. Download the MySQL Installer application to guide you through the setup process:  
   - https://dev.mysql.com/downloads/installer/  
2. Open the Installer application and select to add/install MySQL Server  
3. During the installation, use the default options, but also do the following:  
   - Type and Networking: Enable 'Open Firewall port for network access'  
   - Account and Roles:  Add user 'dermagram' with password 'dermagram'  
   - Plugins & Extensions: Enable 'Open Firewall port for network access'  
4. When you are done, MySQL will be up and running in the background.  
5. If MySQL is not up and running, then return to the Installer application and 
add/download MySQL Workbench. Here you can manually create an instance and start it.


If you had trouble installing `MySQL-python` OR `mysqlclient`, then try the following alternative:  
1. First you must install 'wheel' package to install the forthcoming packages:  
   - `pip install wheel`  
2. Download the 64-bit version of 'MySQL-python' && 'mysqlclient' from the following links:  
http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python  
http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient  
3. Run 
   - `pip install <MySQLPython-filename.whl>`  
   - `pip install <mysqlclient-filename.whl>`  

## Linux

## Mac
