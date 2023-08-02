# add edge device
echo 'install openssh-server'
apt update
apt upgrade
apt install openssh-server
echo "IPQoS cs0 cs0" >> /etc/ssh/sshd_config
cat /etc/ssh/sshd_config

