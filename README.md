#文件分包传输程序
Serial_communicate


## 1. ENV :            系统环境
Ubuntu 16.04
***


## 2. Install dependent packages:  依赖包安装
apt-get install socat
***

## 3. Set virtual serial port      依赖包使用
socat -d -d pty,b115200 pty,b115200
***


## 4. Run                          使用程序
python Client_new.py
python Server_new.py
