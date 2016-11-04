pacman -S --noconfirm python-pip mongodb
systemctl start mongodb && systemctl enable mongodb
python3 -m pip install flask flask-WTF flask pymongo flask-socketio flask-login eventlet
