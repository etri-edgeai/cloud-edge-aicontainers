ansible-playbook autorun.yaml \
-i /home/keti/cloud-edge-aicontainers/v2/bhc/webapp/hosts.ini \
-l rpi6401 \
-t log \
-e "tag=classification ver=v1.0"
