#!/usr/bin/env bash

#-------------------------------------------------------------------------------
#            Usage
#-------------------------------------------------------------------------------

function usage() {
    cat << EOF
Usage: bash upgrade.sh [--repo-path <repo-path>] [--controller <ip>] [--agent <ip,ip>]

Options:
  --help | -h
    Print usage information.
  --repo-path
    The path of new repo.
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
    --repo-path) shift; REPO_PATH=$1 ;;
    --controller) shift; CONTROLLER_ADDRESS=$1 ;;
    --agent) shift; AGENT_ADDRESS_LIST=$1 ;;
    *) shift ;;
  esac
  shift
done

set -o xtrace

TOPDIR=$(cd $(dirname "$0") && pwd)
TEMP=`mktemp`; rm -rfv $TEMP >/dev/null; mkdir -p $TEMP;

apt-get --version >/dev/null 2>&1 && IS_UBUNTU=1

if [[ ! ${CONTROLLER_ADDRESS} ]] && [[ ! ${AGENT_ADDRESS_LIST} ]]; then
    source $TOPDIR/installrc
fi

if [[ ${REPO_PATH} ]]; then
    touch ${REPO_PATH}/test
    if [[ ! -f ${TOPDIR}/hsmrepo/test ]]; then
        rm -rf ${TOPDIR}/hsmrepo
        rm -rf ${REPO_PATH}/test
        cp -rf ${REPO_PATH} ${TOPDIR}
    fi
    rm -rf ${REPO_PATH}/test
fi

if [[ ${CONTROLLER_ADDRESS} ]]; then
    if [[ ${IS_UBUNTU} == 1 ]]; then
        apt-get remove hsm hsm-deploy hsm-dashboard python-hsmclient -y
    else
        service hsm-api stop
        service hsm-conductor stop
        service hsm-scheduler stop
        yum remove hsm hsm-deploy hsm-dashboard python-hsmclient -y
    fi
    CONTROLLER_INSTALL="--controller ${CONTROLLER_ADDRESS}"
fi

if [[ ${AGENT_ADDRESS_LIST} ]]; then
    AGENT_IP_LIST=${AGENT_ADDRESS_LIST//,/ }
    for ip in ${AGENT_IP_LIST}; do
        if [[ ${ip} != ${CONTROLLER_ADDRESS} ]]; then
            if [[ ${IS_UBUNTU} == 1 ]]; then
                apt-get remove hsm hsm-deploy -y
            else
                service hsm-agent stop
                yum remove hsm hsm-deploy -y
            fi
        fi
    done
    AGENT_INSTALL="--agent ${AGENT_ADDRESS_LIST}"
fi

./install.sh ${CONTROLLER_INSTALL} ${AGENT_INSTALL}
