# Linux_server_configuration

### The IP address and SSH port
      IP address: 52.10.172.52
      SSH port: 2200
   
### The complete URL to the hosted web application
      URL: http://52.10.172.52/

### Configuration Steps

      # create catalog user
      'sudo usermod -a -G sudo <username>'
   
      # update and upgrade the installed packages
      'sudo apt-get update'
      'sudo apt-get upgrade'
  
      # update sshd_config
      portNumber="Port 2200"
      'sudo vi /etc/ssh/sshd_config'
      Then change port number from 22 to 2200

      # update ufw policy
      # https://help.ubuntu.com/community/UFW
      'ufw enable'
      'ufw allow ntp'
      'ufw allow http'
      'ufw allow 2200'
  
      # configure to UTC time
      'timedatectl set-timezone Europe/London'

       # Setup database and migration
      # install git
      'apt-get install git'
      #  install apache2, mod_wsgi and PostgreSQL and dependencies
      'apt-get install -y libapache2-mod-wsgi apache2 postgresql'
      'apt-get -qqy install postgresql python-psycopg2'
      'apt-get -qqy install python-flask python-sqlalchemy'
      'apt-get -qqy install python-pip'
      'pip install bleach'
      'pip install oauth2client'
      'pip install requests'
      'pip install httplib2'
   
      # Setting up a virtual environment
      'sudo pip install virtualenv'
      'sudo virtualenv venv'
      'source venv/bin/activate'
   
      # configure database 
      #create database catalogmenu
      'su postgres -c 'createdb catalogmenu''
      'su postgres'
      psql <<EOF
      # connect to database catalogmenu
      \c catalogmenu
      # create user catalog with password
      create user catalog PASSWORD 'catalog';
      # grant catalog all privileges to the databse catalogmenu
      GRANT ALL PRIVILEGES ON DATABASE catalogmenu TO catalog;
      EOF

      # back to root account
      'exit'
   
      # setup database
      'su catalog'
      'cd ~'
      'git clone https://github.com/YH-Zhou/Item-Catalog.git'
      path='/home/Item-Catalog'
      
      # alter application.py to item_catalog.py
      'mv $path"application.py" $path"item_catalog.py"'
      
      # initialize database
      'python $path"database_setup.py"' 
      'python $path"fill_database.py"'

      # Setup web application
      # copy source files to /var/www
      'sudo mkdir -p /var/www/catalog'
      'sudo cp -R $path /var/www/catalog'
      
      # create wsgi file
      'sudo vim /var/www/catalog/item_catalog.wsgi'


      # Configure the virtual host
      'sudo vim /etc/apache2/sites-available/item_catalog.conf'

      # Configure item_catalog.wsgi as follows:
            #!/usr/bin/python
            import sys
            import logging
            logging.basicConfig(stream=sys.stderr)
            sys.path.insert(0, '/var/www/catalog/catalog/')
            from item_catalog import app as application

      # Configure the virtual host
      'sudo vim /etc/apache2/sites-available/item_catalog.conf'
      # Configure item_catalog.conf as follows:
            <VirtualHost *:80>
                ServerName 52.10.172.52
                ServerAdmin http://ec2-52-10-172-52.us-west-2.compute.amazonaws.com
                WSGIDaemonProcess item_catalog user=catalog group=admin threads=5
                WSGIScriptAlias / /var/www/catalog/item_catalog.wsgi
                <Directory /var/www/catalog/catalog/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/catalog/catalog/static
                <Directory /var/www/catalog/catalog/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
            </VirtualHost>


      # enable item_catalog application
      'a2ensite item_catalog.conf'
  
      # reload server to apply the change
      'service apache2 reload'
   
   
### Resources used for the linux server configuration
      https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps
      https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
      https://www.digitalocean.com/community/tutorials/how-to-set-up-apache-virtual-hosts-on-ubuntu-14-04-lts
      http://askubuntu.com/questions/7477/how-can-i-add-a-new-user-as-sudoer-using-the-command-line
      https://help.ubuntu.com/community/AptGet/Howto#Maintenance_commands
      https://help.ubuntu.com/community/UbuntuTime#Using_the_Command_Line_.28terminal.29
      https://help.ubuntu.com/community/UFW
      http://www.postgresql.org/docs/9.1/static/app-createuser.html
      http://killtheyak.com/use-postgresql-with-django-flask/
      http://killtheyak.com/use-postgresql-with-django-flask/
  

### Contents in ~/.ssh/udacity_key.rsa file

      -----BEGIN RSA PRIVATE KEY-----
      MIIEpQIBAAKCAQEA0Ap3bmb/geXMEKKwu6Ja+kTOHriDrYs/MkwhWQEBAyu/78cY
      4ELas6CpSuz3m2zxfYThj4QwEwIl18CcObzfeqq0XC+udlzhWIQDUjrYLEFHBWpZ
      UrMldNMjNF9dBaei6b+Oy9hK6ibCWz7hg7HTVQZcXJ4HktID775Qj0ty5tNTbVME
      E6r1wyyQGLetLJouX20UMSuYMltkcoLg5sQ+cKlBrnwZCyTOYG5WcjTNxdu9wsF8
      zvAhbjBy/EYc7DplNlRLGouFMnuJMyKxBciXiNkj1dv6IHZxypxXTiV5lX63DTy0
      lKZj2q33ZGlV2lhTmtlCx6K7N83q7v8Qsm8lkwIDAQABAoIBAQDOm/ZsgIH0QYHe
      a5RVZDIyJq8Ft32elpHWo+Digaq9uW9O9E3yOrL0ffRjYt+tTg6u948DduY/mnx2
      vuToOnk/W9TvULNU/X0W6VRbD/GsUc/0wt+e0Ce81As8chDyEsAqoIFyVIZh8MhI
      0jQpFCurXzvPB2rCFyytpjZfeTDNpvnRzojhF8J4nb6lZ2g0qSvbvpNu2zXfTzy2
      ZEFyTarUrDzJ6JZ4bcyMt8v09Wy3P917dkSxfxLoKmLwt4fDjmDXyfTLRSc3XX/p
      aVn7VfBmETKZC7FubMCgmtczRsnHylhTZsKX4lyGGAmxS9pKQQnArn0hiQQb4MZS
      UrA7O3QxAoGBAP3vaUx9Z2/e16/Yb4XRfMxD3YGV84qCrK/ZsYaj438Y2EqcEtQG
      9m8cB6GvsCCFXz9d9GPkdyEZeI4cfHhzzqGfn7Q41ZLPSkAcQJu/ihcM8Q1uLe6H
      r45CvuP8s7bn11GxBvZSB69l16B8YjFV+lUlpFlxn6GLC/wNSoh9TbLfAoGBANG7
      hakFB5b5/LoJ9p5sWEskRnTnk6HvwjrlQsHEQxEJE3yK4ahBnBUjlKrgY83LA2rV
      FrowMcrBTXiyh53t1gP1sMGPgX+1FobGZ1oknXeubUvldtwdMXfTLl/C80tRQtyF
      7f4kRGVNPi2mK9VtPACzbgv02CaId0FprosgVzfNAoGBAOXSsqiJrv4u32LFLloc
      uSheG7HWty6bChO1oNhMp+812zvbeabwDkWNRtLtISitzQCa1j86XR9V4CguW/Dg
      Txk0UORZs+JFPdw8NbVAa4hlLB2NpICHyTml6wKIiVZ3CgdjgvuYTmBOehNDv9ML
      D5/Ui6RwE5uvLs+Wb+iMD7BdAoGBAJqPkGPL4hkAJ6BOgWGkxLizhfzXQHQhhcjz
      dWvon+gpASRSERR3LXhinUgET2i0iNMtMC+MHtWl+NrO7qSTRpnqcRVkFXIw2OX/
      xuCmhSlS8RbyhtKV7QO6LL3DpJpHy3dKd+ZHgeQJtZ3cjQcfFg4KLTpAeR6EiSY6
      pLfA4KWtAoGAb8wsXfjV3yewepEolmEARrh9fXCFWAcmHIVLhplsLZY2LyWg3iSW
      32Aw9XUIwUGLFPxgM6RY+yY0ZRdejiFD8nRZGr+hwGWAfpC3ijuq3c78FNgAU2UO
      IGe3JyNbkc7dwIIEZXOQOFgBIshlntrXt46HU2T1bcqQDVgnsLjh8X4=
      -----END RSA PRIVATE KEY-----
