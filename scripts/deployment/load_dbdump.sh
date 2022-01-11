#!/bin/bash
#to backup dump + settings:
# sudo -u postgres pg_dump siddata > pinky_dump_$(date +'%Y-%m-%d') && cp /opt/siddata_backend/siddata_backend/siddata_backend/settings.py ./settings.py.save_$(date +'%Y-%m-%d')

has_user=$(sudo -i -u postgres psql -c '\du' | grep "goaltrees")
if [[ "$has_user" == *goaltrees* ]]
then
  echo "Correct user exists already!"
else
  sudo -u postgres psql -U postgres -c "CREATE USER goaltrees WITH PASSWORD 'seertlaog';"
fi
sudo -u postgres psql -U postgres -c "DROP DATABASE goaltrees; "
sudo -u postgres psql -U postgres -c "DROP SCHEMA public CASCADE; "
sudo -u postgres psql -U postgres -c " CREATE SCHEMA public; "
sudo -u postgres psql -U postgres -c " CREATE DATABASE goaltrees; "
sudo -u postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE goaltrees TO goaltrees;"
if [[ "$1" == *.bz2 ]]
then
  bzip2 -d $1
  name=${1:0:-4}
else
  name=$1
fi
echo $name
sudo -u postgres psql goaltrees < $name