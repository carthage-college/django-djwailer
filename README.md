django-djwailer
===============

Django applications that interact with LiveWhale data.

# MySQL setup

GRANT ALL PRIVILEGES ON livewhale_www.* TO 'livewhale'@'x.x.x.x' IDENTIFIED BY 'xxx' WITH GRANT OPTION;
flush PRIVILEGES;

# UFW

sudo ufw allow from x.x.x.x to any port 3306
