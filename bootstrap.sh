#!/usr/bin/env bash

echo "This DOES NOT WORK AND NEEDS TO BE REIMPLEMENTED"

exit 1
# install base packages
yum install -y epel-release git gzip tar
yum install -y wget bzip2 bzip2-utils bzip2-devel gcc gcc-c++
yum install -y httpd httpd-devel 
yum install -y lzo lzo-devel cmake screen
yum install -y policycoreutils-python setroubleshoot

# open port 5000 for http
firewall-cmd --permanent --add-port=5000/tcp

# open port 80 for http
firewall-cmd --permanent --add-port=80/tcp

# open port 8000 for http
firewall-cmd --permanent --add-port=8000/tcp

# restart firewalld
service firewalld restart

# install miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod a+x Miniconda3-latest-Linux-x86_64.sh

# install miniconda
./Miniconda3-latest-Linux-x86_64.sh -p /opt/miniconda3 -b
rm ./Miniconda3-latest-Linux-x86_64.sh

# set path to miniconda -- should really add to /etc/profile.d so everyone gets it
export PATH=/opt/miniconda3/bin:$PATH
echo "export PATH=/opt/miniconda3/bin:$PATH" >> /root/.bash_profile
echo "export PATH=/opt/miniconda3/bin:$PATH" >> /root/.bashrc
sudo -u vagrant echo "export PATH=/opt/miniconda3/bin:$PATH" >> /home/vagrant/.bash_profile

conda install -y scipy
conda install -y numpy
conda install -y -c anaconda flask
conda install -y -c conda-forge flask-restplus 

# install mod_wsgi for apache
pip install mod_wsgi

# install w2v_tissues
# TODO this should install the version in /vagrant
git clone --single-branch --depth 1 https://github.com/shfong/w2v_tissues.git
pushd w2v_tissues
make dist
pip install dist/w2v_tissues*whl
# copy the http configuration file
cp wordtovectortissues.httpconf /etc/httpd/conf.d/wordtovectortissues_rest.conf
popd

mkdir /var/www/wordtovectortissues_rest

# write the WSGI file
cat <<EOF > /var/www/ddot_rest/w2v_tissues.wsgi
#!/usr/bin/env python

import os
os.environ['WORDTOVECTORTISSUES_REST_SETTINGS']="/var/www/w2v_tissues/wordtovectortissues_rest.cfg"

from w2v_tissues import app as application
EOF

# write the configuration file
cat <<EOF > /var/www/w2v_tissues/wordtovectortissues_rest.cfg
WAIT_COUNT=600
SLEEP_TIME=1
EOF

mod_wsgi-express module-config > /etc/httpd/conf.modules.d/02-wsgi.conf

# https://www.serverlab.ca/tutorials/linux/web-servers-linux/configuring-selinux-policies-for-apache-web-servers/
# and tell SElinux its okay if apache writes to the directory
semanage fcontext -a -t httpd_sys_rw_content_t "/var/www/wordtovectortissues_rest/tasks(/.*)?"
restorecon -Rv /var/www/wordtovectortissues_rest/tasks

service httpd start

echo "Visit http://localhost:8081/wordtovectortissues/rest/v1 in your browser"

