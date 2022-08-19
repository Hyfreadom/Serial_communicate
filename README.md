# Serial_communicate
env: Ubuntu 16.04

apt-get install socat
socat -d -d pty,b115200 pty,b115200

