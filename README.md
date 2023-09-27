# whatsapp-group-automation
A flask app containing webhooks from from a php implemented Contact Form.
The code contains a login webhook to accept post request and send an email to you with an whatsapp QR code.
You can scan the QR to login into your account and the driver will store your session.
Everytime the Contact Form is filled, a message will be sent from your whatsapp number to a group containing the Contents of the Form , The data and media file attached.
It will also email you a Response of the Form along with a link to media file.
The project is a part of my freelancing work and hosted on three VPS servers through Apache2.
Make sure to do the required changes to your creds.json file to fill up your credentials.
A complete guide to host the app on VPS is given here

Install :   Ubuntu 22.0.04
            Putty
            WinScp
Open Putty and set :
    Host Name : IP address
Save the session 
Click Open
Login as : username
Password: Password
Run the commands:

sudo apt update
sudo apt install apache2
Enter Y
sudo ufw allow 'Apache'

CHROME AND CHROME DRIVER INSTALLATION
sudo systemctl status apache2
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/117.0.5938.92/linux64/chromedriver-linux64.zip 
unzip chromedriver_linux64.zip
cd chromedriver-linux64
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
chmod 777 /usr/bin/chromedriver

PYTHON INSTALLATION

sudo apt-get install libapache2-mod-wsgi python-dev
Enter Y
cd /var/www/
(This is the directory where your app will be kept)
mkdir appname
cd appname
sudo apt-get install python-pip
pip install flask selenium (inside your appname folder)
sudo nano /etc/apache2/sites-available/appname.conf
(Write this Script there)

    <VirtualHost *:80>
	      ServerName <ip address>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/flaskapp       
        WSGIScriptAlias / /var/www/appname/appname.wsgi

        <Directory /var/www/appname/appname/>
                Order allow,deny
                Allow from all
        </Directory>

	   ErrorLog ${APACHE_LOG_DIR}/error.log
	   LogLevel warn
     CustomLog ${APACHE_LOG_DIR}/access.log combined

    </VirtualHost>

Ctrl+S , Ctrl+X ,Y
sudo a2ensite appname
systemctl reload apache2

(Create the wsgi file)
On directory /var/www/appname :
sudo nano appname.wsgi

      #!/user/bin/python
      activate_this = '/var/www/appname/appname/venv/bin/activate_this.py'
      exec(open(activate_this).read(),dict(__file__=activate_this))
      import sys
      import logging
      logging.basicConfig(stream=sys.stderr)
      sys.path.insert(0,"/var/www/appname/appname")
      from main import app as application



Now open Winscp
Login using Host Name (ip address), username: root and password:password (Save your login)
Go to root directory --> var --> www --> appname
Create a new folder here with name (appname)
Go to var/www/appname/appname and Drag and Drop your Flask files from Local system (make sure your python file is main.py and flask app name is app (Same as wsgi file))

Now make your main.py file ready to run
Restart apache server using:

sudo service apache2 restart (Everytime you make changes on the server)

You can view your error file from:

/var/log/apache2/error.log

