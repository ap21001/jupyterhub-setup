adduser -q --gecos '""' --disabled-password $1
mkdir -p -m 777 /home/$1/notebook
chown $1: /home/$1/
cp /srv/jupyterhub/bootstrap-script/nbgrader_config.py /home/$1/
