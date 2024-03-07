from configparser import ConfigParser

config = ConfigParser()
config.read("config/config.ini", encoding="utf-8")

from_user = config['fromUser']
from_email = from_user['emailNumber']
from_pwd = from_user['emailPwd']
port = from_user['port']
server_address = from_user['serverAddress']
to_email = config['toUser']['emailNumber']

print("from_email:", from_email)
print("from_password:", from_pwd)
print("port:", port)
print("email_server:", server_address)
print("to_email:", to_email)