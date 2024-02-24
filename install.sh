#!/bin/sh
#
# THIS SCRIPT WILL INSTALL THE GTODO APP SYSTEM WIDE
# THE SCRIPT MUST BE RUN WITH SUDO
#
# It will create a startup shell script named gtodo in /usr/bin,
# the app will be placed in /usr/share/gtodo-sprokkel78
# The .desktop file will be placed in /usr/share/applications/ as com.sprokkel78.gtodo.desktop

mkdir -p /usr/share/gtodo-sprokkel78
cp -r ./* /usr/share/gtodo-sprokkel78/
echo "#!/bin/sh" > /usr/bin/gtodo
echo "cd /usr/share/gtodo-sprokkel78" >> /usr/bin/gtodo
echo "python3 ./gtodo.py" >> /usr/bin/gtodo
cp ./gtodo.desktop /usr/share/applications/com.sprokkel78.gtodo.desktop
chmod 755 /usr/bin/gtodo
chmod 644 /usr/share/gtodo-sprokkel78/*
