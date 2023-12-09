#!/bin/bash

declare -a INSTANCE_IPS=(
    "ec2-18-223-99-117.us-east-2.compute.amazonaws.com"
)

KEY_PATH="/Users/conny/.ssh/id_rsa"

setup_instance() {
    INSTANCE_IP=$1
    ssh -i $KEY_PATH -o StrictHostKeyChecking=no ubuntu@$INSTANCE_IP <<EOF
        sudo apt-get update
        sudo apt-get install -y python3-pip
        sudo apt-get install -y python3-venv
        python3 -m venv pyenv
        source pyenv/bin/activate
        pip3 install numpy
        pip3 install pandas
        pip3 install jupyterlab
        if [ ! -f ~/.jupyter/jupyter_lab_config.py ]; then
            jupyter lab --generate-config
        fi
        nohup jupyter lab --ip 0.0.0.0 --no-browser --NotebookApp.token='' &
EOF
}

for ip in "${INSTANCE_IPS[@]}"
do
   setup_instance $ip
done
