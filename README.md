gtodo-sprokkel78

A graphical user interface in PyGTK4 for performing TODO list items on MAC, Ubuntu and other Linux distro's. 
It requires Python3.10 or higher, Pip, Venv and the PyGTK apps, it also relies on gnome-terminal for performing portscans.
Developed and tested on Ubuntu 23.10 and MacMini 2020. 

Installation on Ubuntu 23.10

1. $sudo apt install python3 python3-dev python3-pip python3-venv
2. $sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1
3. $sudo apt install gnome-terminal

Added 'install.sh' script for system-wide installation.
- The startup shell script will be /usr/bin/gtodo
- The application is installed in /usr/share/gtodo-sprokkel78
- The .desktop file is placed in /usr/share/applications/com.sprokkel78.gtodo.desktop

Added 'uninstall.sh' script for system-wide uninstallation.
- This will delete /usr/bin/gtodo and /usr/share/gtodo-sprokkel78,
  This will also remove /usr/share/applications/com.sprokkel78.gtodo.desktop
  
Check https://www.github.com/sprokkel78/gtodo for contributing, development features and pre-releases.

Funding: Paypal email: sprokkel78.bart@gmail.com
