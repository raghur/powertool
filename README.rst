=========
powertool
=========


.. image:: https://img.shields.io/pypi/v/powertool.svg
        :target: https://pypi.python.org/pypi/powertool

.. image:: https://img.shields.io/travis/raghur/powertool.svg
        :target: https://travis-ci.org/raghur/powertool

.. image:: https://readthedocs.org/projects/powertool/badge/?version=latest
        :target: https://powertool.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/raghur/powertool/shield.svg
     :target: https://pyup.io/repos/github/raghur/powertool/
     :alt: Updates


Python utility to wake up(wol) and suspend Linux machines remotely


* Free software: MIT license


Features
--------

* Wake up remote machines using hostname/ip.
* Suspend remote machines using hostname

Wake on lan (WOL) 
-----------------

wake up feature uses WOL magic packet. Since mac addresses are hard to remember/use, this tool lets you wake up or suspend machines
by their name or IP.

1. First register your machines ::

        powertool register -b 192.168.1.255 aa:bb:cc:dd:ee:ff you@host
   
   - `-b Broadcast_IP` - this is the subnet on which your machine's ip is. If your machine's ip is 192.168.1.xxx, then this is 192.168.1.255(default)
   - aa:bb:cc:dd:ee:ff - your machines' mac address. You can find this on your machine or on the router's device list.
   - you\@host - your username on the remote host - this is used by the sleep function to do a passwordless ssh and run pm-suspend.

2. `register` saves machine details so that you can later do this::

        powertool wol host
        powertool sleep host
3. `register` just saves machine details to a `~/.powertool` as a json file.

Sleep/suspend
---------------

Sleep/suspend feature has quite a few dependencies

- you should have passwordless ssh to the remote host. There are a lot of guides on the internet on how to set this up - 
  like this one http://www.linuxproblem.org/art_9.html. Verify that it works by running `ssh user@host` - you 
  should not be prompted for a password.
- You should have `pm-utils` package on your remote machine http://manpages.ubuntu.com/manpages/precise/man8/pm-action.8.html
- Your user should be able to run `sudo pm-suspend` without being prompted for password. To set this up, login to the 
  remote machine and do the following::

        sudo visudo
        # add the following - where user is your username on the remote machine
        user ALL=(ALL) NOPASSWD: /usr/sbin/pm-suspend

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

