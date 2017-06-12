#!/usr/bin/env bash

#-------------------------------------------------------------------------------
#            Usage
#-------------------------------------------------------------------------------

function usage() {
    cat << EOF
Usage: bash install.sh [--controller <ip>] [--agent <ip,ip>]

Options:
  --help | -h
    Print usage information.
  --controller [ip or hostname]
    Installing the controller node only.
  --agent [ip,ip or hostname]
    Install the agent node(s), like: --agent ip,ip or hostname with no blank.
EOF
    exit 0
}

while [ $# -gt 0 ]; do
  case "$1" in
    -h| --help) usage ;;
    --controller) shift; CONTROLLER_ADDRESS=$1 ;;
    --agent) shift; AGENT_ADDRESS_LIST=$1 ;;
    *) shift ;;
  esac
  shift
done

set -o xtrace

TOPDIR=$(cd $(dirname "$0") && pwd)
TEMP=`mktemp`; rm -rfv ${TEMP} >/dev/null; mkdir -p ${TEMP};

apt-get --version >/dev/null 2>&1 && IS_UBUNTU=1

if [[ ${CONTROLLER_ADDRESS} ]]; then
    old_str_controller_address=`cat installrc |grep CONTROLLER_ADDRESS=|awk -F "=" '{print $2}'`
    sed -i "s,^CONTROLLER_ADDRESS=*.*,#CONTROLLER_ADDRESS=${old_str_controller_address},g" ${TOPDIR}/installrc
fi
if [[ ${AGENT_ADDRESS_LIST} ]]; then
    old_str_agent_address_list=`cat installrc |grep AGENT_ADDRESS_LIST=|awk -F "=" '{print $2}'`
    sed -i "s,^AGENT_ADDRESS_LIST=*.*,#AGENT_ADDRESS_LIST=${old_str_agent_address_list},g" ${TOPDIR}/installrc
fi

source ${TOPDIR}/installrc

if [[ ${MYSQL_HOST} || ${MYSQL_ROOT_USER} || ${MYSQL_ROOT_PASSWORD} ]] && \
[[ ! ${MYSQL_HOST} && ${MYSQL_ROOT_USER} && ${MYSQL_ROOT_PASSWORD} ]]; then
    echo "Please supply all these parameters: MYSQL_HOST, MYSQL_ROOT_USER and MYSQL_ROOT_PASSWORD"
    exit 1
fi
if [[ ${MYSQL_HOST} ]]; then
    MYSQL_PARAMS="--mysql-host ${MYSQL_HOST} --mysql-root-user ${MYSQL_ROOT_USER} --mysql-root-password ${MYSQL_ROOT_PASSWORD}"
fi

if [[ ${RABBITMQ_HOST} || ${RABBITMQ_USER} || ${RABBITMQ_PASSWORD} || ${RABBITMQ_PORT} ]] && \
[[ ! ${RABBITMQ_HOST} && ${RABBITMQ_USER} && ${RABBITMQ_PASSWORD} && ${RABBITMQ_PORT} ]]; then
    echo "Please supply all these parameters: RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD and RABBITMQ_PORT"
    exit 1
fi
if [[ ${RABBITMQ_HOST} ]]; then
    RABBITMQ_PARAMS="--rabbitmq-host ${RABBITMQ_HOST} --rabbitmq-user ${RABBITMQ_USER} --rabbitmq-password ${RABBITMQ_PASSWORD} --rabbitmq-port ${RABBITMQ_PORT}"
fi

if [[ ${MYSQL_KEYSTONE_USER} || ${MYSQL_KEYSTONE_PASSWORD} || ${KEYSTONE_HOST} || ${ADMIN_TOKEN} || ${ADMIN_USER} || ${ADMIN_PASSWORD} ]] && \
[[ ! ${MYSQL_KEYSTONE_USER} && ${MYSQL_KEYSTONE_PASSWORD} && ${KEYSTONE_HOST} && ${ADMIN_TOKEN} && ${ADMIN_USER} && ${ADMIN_PASSWORD} ]]; then
    echo "Please supply all these parameters: MYSQL_KEYSTONE_USER, MYSQL_KEYSTONE_PASSWORD, KEYSTONE_HOST, ADMIN_TOKEN, ADMIN_USER and ADMIN_PASSWORD"
    exit 1
fi
if [[ ${KEYSTONE_HOST} ]]; then
    KEYSTONE_PARAMS="--mysql-keystone-user ${MYSQL_KEYSTONE_USER} --mysql-keystone-password ${MYSQL_KEYSTONE_PASSWORD} --keystone-host ${KEYSTONE_HOST} --admin-token ${ADMIN_TOKEN} --admin-user ${ADMIN_USER} --admin-password ${ADMIN_PASSWORD}"
fi

SSH='ssh -t'
SCP='scp'

if [[ ${CONTROLLER_ADDRESS} ]]; then
    if [[ ${IS_UBUNTU} == 1 ]]; then
        cat <<"EOF" >hsm.list
deb file:///opt hsmrepo/
EOF
        rm -rf /etc/apt/sources.list.d/hsm.list
        cp hsm.list /etc/apt/sources.list.d
        rm -rf /opt/hsmrepo
        cp -r hsmrepo /opt
        apt-get update
        apt-get install hsm hsm-deploy hsm-dashboard python-hsmclient -y --force-yes
    else
        cat <<"EOF" >hsm.repo
[hsmrepo]
name=hsmrepo
baseurl=file:///opt/hsmrepo
gpgcheck=0
enabled=1
proxy=_none_
EOF
        rm -rf /etc/yum.repos.d/hsm.repo
        cp hsm.repo /etc/yum.repos.d
        rm -rf /opt/hsmrepo
        cp -r hsmrepo /opt
        yum makecache
        yum install hsm hsm-deploy hsm-dashboard python-hsmclient -y
    fi
    hsm-preinstall
    hsm-generate-deployrc --controller ${CONTROLLER_ADDRESS} ${MYSQL_PARAMS} ${RABBITMQ_PARAMS} ${KEYSTONE_PARAMS}
    hsm-deploy c-deploy
fi

function setup_diamond_centos() {
    ${SCP} ${TOPDIR}/diamond-4-0.noarch.rpm $1:/tmp
    source /etc/hsmdeploy/deployrc
    SITE_PACKAGES="/usr/lib/python2.7/site-packages"
    HSM_PATH="${SITE_PACKAGES}/hsm"
    HSMMYSQL_FILE_PATH="${HSM_PATH}/diamond/handlers/hsmmysql.py"
    HANDLER_PATH="${SITE_PACKAGES}/diamond/handler"
    DIAMOND_CONFIG_PATH="/etc/diamond"
    DIAMOND_DB_HOST=${MYSQL_HOST}
    ${SSH} $1 "bash -x -s" <<EOF
yum install python-redis -y
rpm -ivh /tmp/diamond-4-0.noarch.rpm
chmod 755 /etc/init.d/diamond
rm -rf ${DIAMOND_CONFIG_PATH}/diamond.conf
cp ${HSM_PATH}/diamond/diamond.conf ${DIAMOND_CONFIG_PATH}/diamond.conf
sed -i "s,%MYSQL_DB_HOSTNAME%,${DIAMOND_DB_HOST},g" ${DIAMOND_CONFIG_PATH}/diamond.conf
sed -i "s,%HSM_DB_PASSWORD%,${MYSQL_HSM_PASSWORD},g" ${DIAMOND_CONFIG_PATH}/diamond.conf
cp ${HSMMYSQL_FILE_PATH} ${HANDLER_PATH}
cp -rf ${HSM_PATH}/diamond/collectors/hyperstash /usr/share/diamond/collectors
service diamond restart
EOF
}

function setup_diamond_ubuntu() {
    ${SCP} ${TOPDIR}/diamond_4.0_all.deb $1:/tmp
    source /etc/hsmdeploy/deployrc
    SITE_PACKAGES="/usr/local/lib/python2.7/dist-packages"
    HSM_PATH="${SITE_PACKAGES}/hsm"
    HSMMYSQL_FILE_PATH="${HSM_PATH}/diamond/handlers/hsmmysql.py"
    HANDLER_PATH="/usr/lib/pymodules/python2.7/diamond/handler"
    DIAMOND_CONFIG_PATH="/etc/diamond"
    DIAMOND_DB_HOST=${MYSQL_HOST}
    ${SSH} $1 "bash -x -s" <<EOF
apt-get install python-redis -y
dpkg -i /tmp/diamond_4.0_all.deb
rm -rf ${DIAMOND_CONFIG_PATH}/diamond.conf
cp ${HSM_PATH}/diamond/diamond.conf ${DIAMOND_CONFIG_PATH}/diamond.conf
sed -i "s,%MYSQL_DB_HOSTNAME%,${DIAMOND_DB_HOST},g" ${DIAMOND_CONFIG_PATH}/diamond.conf
sed -i "s,%HSM_DB_PASSWORD%,${MYSQL_HSM_PASSWORD},g" ${DIAMOND_CONFIG_PATH}/diamond.conf
cp ${HSMMYSQL_FILE_PATH} ${HANDLER_PATH}
cp -rf ${HSM_PATH}/diamond/collectors/hyperstash /usr/share/diamond/collectors
service diamond restart
EOF
}

if [[ ${AGENT_ADDRESS_LIST} ]]; then
    AGENT_IP_LIST=${AGENT_ADDRESS_LIST//,/ }
    for ip in ${AGENT_IP_LIST}; do
        if [[ ${IS_UBUNTU} == 1 ]]; then
            ${SSH} ${ip} rm -rf /etc/apt/sources.list.d/hsm.list
            ${SCP} hsm.list ${ip}:/etc/apt/sources.list.d
        else
            ${SSH} ${ip} rm -rf /etc/yum.repos.d/hsm.repo
            ${SCP} hsm.repo ${ip}:/etc/yum.repos.d
        fi
        ${SSH} ${ip} rm -rf /opt/hsmrepo
        ${SCP} -r hsmrepo ${ip}:/opt
        ${SSH} ${ip} mkdir -p /etc/hsmdeploy
        ${SCP} /etc/hsmdeploy/deployrc ${ip}:/etc/hsmdeploy
        if [[ ${IS_UBUNTU} == 1 ]]; then
            ${SSH} ${ip} "bash -x -s" <<EOF
apt-get update
apt-get install hsm hsm-deploy -y --force-yes
hsm-preinstall agent
hsm-deploy a-deploy
EOF
            setup_diamond_ubuntu ${ip}
        else
            ${SSH} ${ip} "bash -x -s" <<EOF
yum makecache
yum install hsm hsm-deploy -y
hsm-preinstall agent
hsm-deploy a-deploy
EOF
            setup_diamond_centos ${ip}
        fi
    done
fi

echo "Finished."

set +o xtrace
