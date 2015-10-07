#!/usr/bin/env bash
yum update

Ubuntu:
	sudo apt-get install libxml2-dev libcurl4-openssl-dev pkg-config libjpeg-dev libpng-dev libfreetype6-dev libmcrypt-dev
Centos 6 rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm

yum install gcc gcc-c++
yum install mc fail2ban libxml2 libxml2-devel openssl openssl-devel bzip2 bzip2-devel curl curl-devel libjpeg libjpeg-devel libpng-devel freetype-devel gmp-devel mysql-devel ncurses ncurses-devel unixODBC-devel pspell-devel libmcrypt libmcrypt-devel libc-client-devel mysql-server mysql php-mysql php-pecl-memcache
mkdir sources && cd sources
wget http://nginx.org/download/nginx-1.5.4.tar.gz
wget http://sourceforge.net/projects/pcre/files/latest/download?source=files
wget zlib http://zlib.net/zlib-1.2.8.tar.gz
wget http://ua1.php.net/get/php-5.4.19.tar.gz/from/this/mirror
wget http://acelnmp.googlecode.com/files/eaccelerator-0.9.6.1.tar.bz2
tar xvjf eaccelerator-0.9.6.1.tar.bz2wget http://nginx.org/download/nginx-1.5.4.tar.gz
tar -zxf php
tar -zxf zlib-1.2.8.tar.gz
tar -zxf nginx-1.5.4.tar.gz
tar -xvjf pcre
cd nginx-1.5.4
./configure --conf-path=/etc/nginx/nginx.conf --pid-path=/var/run/nginx.pid --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --user=www --group=www --with-zlib=../zlib-1.2.8 --with-pcre=../pcre-8.33 --with-http_ssl_module
cd ../

#php
cd php

#UBUNTU
sudo apt-get install libxml2-dev libssl-dev libcurl4-openssl-dev pkg-config.

./configure --with-gd --with-pear --with-curl --with-mcrypt --with-config-file-path=/etc --with-jpeg-dir --with-png-dir --with-zlib --with-xmlrpc --with-gettext --with-openssl --with-fpm-user=www --with-fpm-group=www --disable-debug --enable-fpm --enable-exif --enable-zip --enable-sockets --enable-mbstring --enable-ftp --with-mysql=mysqlnd --with-mysqli=mysqlnd --with-iconv --enable-mbstring --with-freetype-dir --disable-fileinfo --with-pdo-mysql
make
make install
cp sapi/fpm/init.d.php-fpm /etc/init.d/php-fpm
chmod 0755 /etc/init.d/php-fpm
mv /usr/local/etc/php-fpm.conf.default /usr/local/etc/php-fpm.conf

#eaccelerator
cd ~
cd eaccelerator-0.9.6.1
./phpize
./configure --enable-eaccelerator=shared --with-php-config=/usr/bin/php-config --with-eaccelerator-shared-memory
make
make install
mkdir -p /etc/
d/eaccelerator.ini
==========================
extension="eaccelerator.so"
eaccelerator.shm_size="16"
eaccelerator.cache_dir = "/var/cache/php-eaccelerator"
eaccelerator.enable="1"
eaccelerator.optimizer="1"
eaccelerator.check_mtime="1"
eaccelerator.debug="0"
eaccelerator.filter=""
eaccelerator.shm_max="0"
eaccelerator.shm_ttl="0"
eaccelerator.shm_prune_period="0"
eaccelerator.shm_only="0"
eaccelerator.compress="1"
eaccelerator.compress_level="9"
Если используется Zend Optimizer:
zend_extension="/usr/lib/php/modules/eaccelerator.so"
eaccelerator.shm_size="16"
eaccelerator.cache_dir = "/var/cache/php-eaccelerator"
eaccelerator.enable="1"
eaccelerator.optimizer="1"
eaccelerator.check_mtime="1"
eaccelerator.debug="0"
eaccelerator.filter=""
eaccelerator.shm_max="0"
eaccelerator.shm_ttl="0"
eaccelerator.shm_prune_period="0"
eaccelerator.shm_only="0"
eaccelerator.compress="1"
eaccelerator.compress_level="9"
#mysql
chkconfig --levels 235 mysqld on
service mysqld start
mysql -u root

/usr/local/etc/php-fpm.conf ->
	pm.max_children = ceil(mem/32)
	pm.min_spare_server = floor(ceil(mem/32)/2)
	pm.start_server (3/4)*ceil(mem/32);
	pm.process_idle_timeout = 5s;



