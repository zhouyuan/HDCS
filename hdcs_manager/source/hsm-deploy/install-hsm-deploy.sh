#!/usr/bin/env bash
#
# Small script to install hsm-deploy to local filesystem

export HSM_DEPLOY_ROOT_PATH=debian/hsm-deploy

#---------------------------
# usr/local/bin/
#---------------------------
install -g root -o root -d -m 755 $HSM_DEPLOY_ROOT_PATH/usr/local/bin/
install -g root -o hsm -v -m 755 -t $HSM_DEPLOY_ROOT_PATH/usr/local/bin/ hsm-deploy
install -g root -o hsm -v -m 755 -t $HSM_DEPLOY_ROOT_PATH/usr/local/bin/ hsm-generate-deployrc
install -g root -o hsm -v -m 755 -t $HSM_DEPLOY_ROOT_PATH/usr/local/bin/ hsm-preinstall
cp -rf hsm-lib $HSM_DEPLOY_ROOT_PATH/usr/local/bin/
