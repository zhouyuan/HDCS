#Hyperstash Manager#

**Hyperstash Manager** aims to monitor the hyperstash at this stage.

## Introduction ##

#### 1. Dashboard ####
- **overview**: The overview display of the hyperstash manager(hsm).

#### 2. Server Manage ####
- **Server**: The server which has been installed the hsm related packages(running hsm-agent service) will be list here and admin can activate it as hyperstash instance.

#### 3. Hyperstash Manage ####
- **Hyperstash**: The hyperstash instance is a computing node. From here, you can monitor the performance of it and you can delete it(just from hsm) so you can activate it from Server Manage.
- **RBD**: You can see the performance and cache config of each volume.

#### 4. Global Manage ####
- **User**: User can change the password here.


## Pack ##
1. **Login as Root**
	1. You should login the packing node as root user.
2. **Git**
	1. Install the git.
		1. ubuntu: `apt-get install git -y`
		2. centos: `yum install git -y`
3. **Pack**
	1. `git clone https://github.com/Intel-bigdata/hyperstash.git`
	2. `cp -r hyperstash/hyperstash-manager /opt`
	3. `cd /opt/hyperstash-manager`
	4. `./buildhsm.sh`
	5. You can get the release package in **release** folder.


## Installation ##
> 
> From here, you can learn how to install the Hyperstash Manager(hsm) for your hyperstash on openstack cluster node.
> 
> First of all, you should have a ceph cluster and an openstack cluster which has been installed ceph related packages. And you can fetch information from the openstack node.

1. **Login as Root**
	1. You should login the openstack controller node as root user.
	2. You should make the node to connect all nodes without password.
2. **OpenStack Packages**
	1. You should have installed the openstack repo packages on your nodes.
	2. ubuntu: [http://docs.openstack.org/mitaka/install-guide-ubuntu/environment-packages.html](http://docs.openstack.org/mitaka/install-guide-ubuntu/environment-packages.html "ubuntu")
	3. centos: [http://docs.openstack.org/mitaka/install-guide-rdo/environment-packages.html](http://docs.openstack.org/mitaka/install-guide-rdo/environment-packages.html "centos")
3. **Installrc File**
	- MySQL
		- If you want to use the **existed mysql** for hsm, you should set **MYSQL\_HOST**, **MYSQL\_ROOT\_USER** and **MYSQL\_ROOT\_PASSWORD** in the installrc file.
	- RabbitMQ
		- If you want to use the **existed rabbitmq** for hsm, you should set **RABBITMQ\_HOST**, **RABBITMQ\_USER**, **RABBITMQ\_PASSWORD** and **RABBITMQ\_PORT** in the installrc file.
	- Keystone
		- If you want to use the **existed keystone** for hsm, you should set **MYSQL\_KEYSTONE\_USER**, **MYSQL\_KEYSTONE\_PASSWORD**, **KEYSTONE\_HOST**, **ADMIN\_TOKEN**, **ADMIN\_USER** and **ADMIN\_PASSWORD** in the installrc file.
	1. You should set the **CONTROLLER\_ADDRESS** and **AGENT\_ADDRESS\_LIST** in the installrc file.
	2. At last, you can run the command "**./install.sh**" to finish the installation.


## Upgrade ##
1. After you re-pack the hyperstash-manager from the source code, you will get the hsmrepo under your packing folder.
2. You should upload it to your installation node.
3. In the installation folder where you run "./install.sh" before, you can run command "./upgrade.sh --repo-path <hsmrepo-path>" to upgrade hsm on all nodes.
