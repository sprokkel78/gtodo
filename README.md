gtodo-sprokkel78

A graphical user interface in PyGTK4 for performing TODO list items on Ubuntu and other Linux distro's. 
It requires Python3.10 and the PyGTK apps. Developed on Fedora 40 and tested on Ubuntu 24.04.

![Screenshot](https://github.com/sprokkel78/gtodo/blob/develop/screenshots/gTodo-2.png)

Installation on Fedora 40 & Ubuntu 24.04

1. $git clone https://github.com/sprokkel78/gtodo.git
2. $cd gtodo
3. $python3 ./gtodo.py 

For System-Wide Installation, run:
- $sudo ./install.sh

Then start with:
- $gtodo
- or by clicking the application icon.

Added 'install.sh' script for system-wide installation.
- The startup shell script will be /usr/bin/gtodo
- The application is installed in /usr/share/gtodo-sprokkel78
- The .desktop file is placed in /usr/share/applications/com.sprokkel78.gtodo.desktop

Added 'uninstall.sh' script for system-wide uninstallation.
- This will delete /usr/bin/gtodo and /usr/share/gtodo-sprokkel78,
  This will also remove /usr/share/applications/com.sprokkel78.gtodo.desktop
- After uninstall it is optional to remove the .gtodo directory in your home-directory.

Check https://www.github.com/sprokkel78/gtodo for contributing, development features and pre-releases.

Check https://pypi.org/project/gtodo-sprokkel78/ for the full python package.

Funding: Paypal email: sprokkel78.bart@gmail.com

