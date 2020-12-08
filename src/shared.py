from threading import Event
import crypt
from sys import stderr
from psutil import process_iter
from flask_login import UserMixin

shutdown_event = Event()

Actions = {
    "Poweroff": "poweroff",
    "Reboot": "reboot",
    "Hibernate": "",  # TBA
    "Suspend": "",   # TBA
    "Script": None
}

Monitor = {
    'Network': 'net',
    'CPU': 'cpu',
    'RAM': 'ram',
    'Sound': 'audio',
    'Process': 'proc',
    'Display': 'disp'
}

# https://stackoverflow.com/questions/28195805/running-notify-send-as-root


def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


def list_processes() -> list:
    processes = list()
    for proc in process_iter():
        processes.append({'name': proc.name(), 'pid': proc.pid})
    return processes


def list_users() -> list:
    lines = list()
    users = list()
    with open('/etc/shadow', 'rt') as f:
        lines = f.readlines()
    for line in lines:
        username = line.split(':')[0]
        users.append(User(username))
    return users


def check_password(user, password):
    lines = list()
    with open('/etc/shadow', 'rt') as f:
        lines = f.readlines()
    user_p_line = [x for x in lines if x[:len(user)] == user]   # Get line from user
    if user_p_line:  # user found
        pass_part = user_p_line[0].split(':')[1]
        pass_part = [x for x in pass_part.split('$') if x != '']
        p_hash = pass_part[2]
        salt = pass_part[1]
        alg_id = pass_part[0]
        print(alg_id, salt, p_hash, sep=' ')
        print(crypt.crypt(password, f'${alg_id}${salt}'))
        return crypt.crypt(password, f'${alg_id}${salt}') == user_p_line[0].split(':')[1]
    else:   # user not found
        return False


# User for login
class User(UserMixin):

    def __init__(self, username: str):
        self.name = username

    @property
    def id(self):
        return self.name