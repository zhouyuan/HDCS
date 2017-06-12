Python bindings to the Hyperstash Manager API
=============================================

This is a client for the Hyperstash Manager API. There's a Python API (the
``hsmclient`` module), and a command-line script (``hsm``). Each implements
100% of the Hyperstash Manager API.

.. contents:: Contents:
   :local:

Command-line API
----------------

Installing this package gets you a shell command, ``hsm``, that you
can use to interact with any Hyperstash Manager compatible API.

You'll need to provide your Hyperstash Manager username and password. You can
do this with the ``--os-username``, ``--os-password`` and  ``--os-tenant-name``
params, but it's easier to just set them as environment variables::

    export OS_USERNAME=admin
    export OS_PASSWORD=c8c8f9f33beb1e4c9ad5
    export OS_TENANT_NAME=admin

You need to set the OS_AUTH_URL to the keystone endpoint::

    export OS_AUTH_URL=http://example.com:5000/v2.0/

You'll find complete documentation on the shell by running
``hsm help``::

    usage: hsm [--version] [--debug] [--os-username <auth-user-name>]
               [--os-password <auth-password>]
               [--os-tenant-name <auth-tenant-name>] [--os-auth-url <auth-url>]
               [--os-region-name <region-name>]
               <subcommand> ...

    Command-line interface to the Hyperstash Manager API.

    Positional arguments:
      <subcommand>
        hs-instance-list    Lists all hyperstash instances.
        hs-instance-show    Shows details info of a hyperstash instance.
        performance-metric-get-cpu
                            Gets cpu information.
        performance-metric-get-hsm-summary
                            Gets hsm summary.
        performance-metric-get-mem
                            Gets memory information.
        performance-metric-get-os-and-kernel
                            Gets os and kernel information.
        performance-metric-get-value
                            Gets the value of hyperstash performance metric by rbd
                            id and type.
        rbd-cache-config-list
                            Lists all rbd cache configs.
        rbd-cache-config-show
                            Shows details info of a rbd cache config.
        rbd-cache-config-show-by-rbd-id
                            Shows details info of a rbd cache config by rbd id.
        rbd-list            Lists all rbds.
        rbd-refresh         Refresh the rbd info.
        rbd-show            Shows details info of a rbd.
        server-activate     Activates a server as a hyperstash instance.
        server-list         Lists all servers.
        server-show         Shows details info of a server.
        bash-completion     Print arguments for bash_completion.
        help                Display help about this program or one of its
                            subcommands.
        list-extensions     List all the os-api extensions that are available.

    Optional arguments:
      --version             show program's version number and exit.
      --debug               Print debugging output.
      --os-username <auth-user-name>
                            Defaults to env[OS_USERNAME].
      --os-password <auth-password>
                            Defaults to env[OS_PASSWORD].
      --os-tenant-name <auth-tenant-name>
                            Defaults to env[OS_TENANT_NAME].
      --os-auth-url <auth-url>
                            Defaults to env[OS_AUTH_URL].
      --os-region-name <region-name>
                            Defaults to env[OS_REGION_NAME].

    See "hsm help COMMAND" for help on a specific command.

Python API
----------

There's also a complete Python API, but it has not yet been documented.

Quick-start using keystone::

    # use v2.0 auth with http://example.com:5000/v2.0/
    >>> from hsmclient.v1 import client
    >>> nt = client.Client(USER, PASS, TENANT, AUTH_URL, service_type="hsm")
    >>> nt.servers.list()
    [...]

