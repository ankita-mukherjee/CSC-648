# Script to deploy server on stock Ubuntu 20.4 LTS server
# # #
# TODO apt installs

# TODO pip installs

# deploy app
cd ~
git clone -b dev https://github.com/CSC-648-SFSU/csc648-03-fa23-team02.git
sudo systemctl stop apache2
sudo rm -rf /var/www/application
sudo mv csc648-03-fa23-team02/application/ /var/www/
sudo chown -R www-data:www-data /var/www/application
sudo systemctl start apache2