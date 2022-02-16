#!/bin/bash

username="sync"
job="* */12 * * * /home/$username/sync.sh"

if id -u "$username" > /dev/null 2>&1; then goto main; else goto create_user; fi
:create_user
useradd "$username" -m -s /usr/sbin/nologin || exit

su -s /bin/bash "$username" <<EOF
declare -A detect_list
detect_list["global:docker"]=$(docker -v > /dev/null 2>&1; echo "$?")
detect_list["global:python3.9"]=$(python3.9 -V > /dev/null 2>&1; echo "$?")
detect_list["global:pip3"]=$(pip3 -V > /dev/null 2>&1; echo "$?")
detect_list["pip3:requests"]=$([ ! $(($(pip3 list | grep -c requests))) -eq 0 ]; echo "$?")
detect_list["pip3:pytz"]=$([ ! $(($(pip3 list | grep -c pytz))) -eq 0 ]; echo "$?")
detect_list["env:SUBMIT_URL"]=$([ ! "url:$SUBMIT_URL" == "url:" ]; echo "$?")

for name in ${!detect_list[*]}; do
  if [ "${detect_list[$name]}" == "0" ]; then echo "[√]$name"; else echo "[x]$name"; detect=127; fi
done
if [ ${detect=0} -ne 0 ]; then echo "environment detection failed." exit $detect; fi
EOF

cp client/* /home/sync
cp -r lib /home/sync
cp -r docker /home/sync
cp script/sync.sh /home/sync
echo "export SUBMIT_URL=$SUBMIT_URL" >> /home/sync/.profile
chown -R "$username":"$username" /home/sync
su - -s /bin/bash "$username" <<EOF
. ~/.profile
cd docker || exit
./build.sh 8
./build.sh 16
./build.sh 17
cd .. && chmod +x ./sync.sh
echo "$job" | crontab -
EOF
