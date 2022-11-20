#!/usr/bin/env bash

DEPLOYMENT_DIR=$(pwd)
BASE_DIR=$(dirname "$0")

print_error_and_exit() {
    local CODE="$1"
    local MESSAGE="$2"
    if [[ -n "$MESSAGE" ]] ; then
        echo "${MESSAGE}; exiting with status ${CODE}"
    fi
    exit "${CODE}"
}

check_sudo_rights() {
    echo "sudo rights are "
    if sudo -n true >/dev/null 2>&1; then
        echo "ok"
        return 0
    else
        echo "failed"
        return -1
    fi    
}

ask_yes_no()
{
    IFS= read -p "$1" -r var

    case $var in
        y | Y | yes | YES | Yes)
            return 0
            ;;
        n | N | no |NO | No)
            return 1
            ;;
        *) #For all other input
            echo "Input yes or no"
            yesNo
            ;;
    esac #ends the case list
}

check_if_package_installed() {
    if [[ $(dpkg-query -W -f='${Status}' ${1} 2>/dev/null | grep -c "ok installed") -eq 0 ]]; then
        echo "Package {1} is installed"
        return 0
    else 
        echo "Package {1} seems to be NOT installed"
        return 1
    fi
}


echo "-------- Starting installation --------"

# check if python3 is installed
if [ "$(command -v python3)" ]; then
    echo "$(python3 -V) found"
else
    print_error_and_exit -1 "python3 not found.\ Aborting installation"
fi

# check if pip3 is installed
if [ "$(command -v pip3)" ]; then
    echo "$(pip3 -V) found"
else
    print_error_and_exit -1 "pip3 not found.\ Aborting installation.\To install pip3 you can use: sudo apt install python3-pip"
fi

# check mongodb-org
check_if_package_installed 'mongodb-org' || echo "Please install MongoDB is required for app to run properly"

# move to basedir
cd ${BASE_DIR}
# create virtual environment
echo "Creating virtual environment"
python3 -m venv .env
# install required packages
echo "Installing python packages"
pip3 install -r "${DEPLOYMENT_DIR}/requirements.txt"
# ask whether to install uWSGI, nginx conf and systemd service
ask_yes_no "Do you want to add configuration to uWSGI and nginx, and create systemd service? Type [y/n]: "
if [[ $? -eq 0 ]]; then
    # check nginx
    check_if_package_installed 'nginx' || print_error_and_exit "Please install nginx first.\ Aborting installation."
    # check for sudo rights
    check_sudo_rights || print_error_and_exit "You must have sudo rights to add systemd files and confgure nignx.\ Aborting installation."
    # configure ini, nginx and systemd files
    echo 'Creating configuration files for uWSGI and nginx'
    cp ${DEPLOYMENT_DIR}/uwsgi.ini ${BASE_DIR}/uwsgi.ini
    sed -i 's~PATH_TO_PROJECT_DIR~${BASE_DIR}~g' ${BASE_DIR}/uwsgi.ini
    sudo cp ${DEPLOYMENT_DIR}/django-sernsors-monitoring.conf /etc/nginx/sites-available/django-sernsors-monitoring
    sed -i 's~PATH_TO_PROJECT_DIR~${BASE_DIR}~g' /etc/nginx/sites-available/django-sernsors-monitoring
    # add nginx conf and enable site
    echo "Adding site to nginx and enabling it"
    sudo ln -s /etc/nginx/sites-available/django-sernsors-monitoring /etc/nginx/sites-enabled/django-sernsors-monitoring
    echo 'Reloading nginx service'
    sudo systemctl reload nginx.service  
    # add systemd service and start it
    echo "Adding django-sernsors-monitoring service to systemd"
    sudo cp ${DEPLOYMENT_DIR}/django-sernsors-monitoring.service /etc/systemd/system/django-sernsors-monitoring.service
    sudo sed -i 's~PATH_TO_PROJECT_DIR~${BASE_DIR}~g' /etc/systemd/system/django-sernsors-monitoring.service
    sudo chmod 664 /etc/systemd/system/django-sernsors-monitoring.service
    sudo systemctl daemon-reload --quiet

    echo "Starting django-sernsors-monitoring service"
    systemctl start django-sernsors-monitoring.service
    sleep 1
    systemctl is-active --quiet django-sernsors-monitoring.service
    if [[ $? -ne 0 ]]; then
        echo "Cannot start django-sernsors-monitoring server"
        systemctl status django-sernsors-monitoring.service
        exit -1
    fi
fi

echo "-------- Installation is finished --------"