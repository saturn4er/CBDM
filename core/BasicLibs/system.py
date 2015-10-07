import os
import subprocess
import sys
from core.common_defs import is_windows
import getpass

rootPass = ""


def gain_password():
    global rootPass
    user_id = os.getuid()

    if (rootPass == "") and (user_id != 0):
        with open(os.devnull, "w") as devnull:
            while True:
                rootPass = getpass.getpass("Root password: ", sys.stdout)
                proc = sudo(['cat', '/etc/passwd'], stderr=devnull, stdout=devnull, stdlog=False)
                if proc.returncode != 0:
                    print("Bad password! Try again.")
                else:
                    break


def sudo(command, stdout=None, stderr=None, stdlog=True):
    gain_password()
    user_id = os.getuid()
    if stdlog:
        print("Running '{0}' as sudo. ".format(" ".join(command)), end="")
    proc = subprocess.Popen(["sudo", "-S"] + command, stdin=subprocess.PIPE, stderr=stderr, stdout=stdout)
    if user_id != 0:
        proc.stdin.write(bytes(rootPass + "\n", 'UTF-8'))
    proc.communicate()
    if stdlog:
        if proc.returncode == 0:
            print(' [ok]')
        else:
            print(' [code={0}]'.format(proc.returncode))
    return proc


def set_system_variable(var_name, var_value):
    if is_windows():
        shell = True
        with open('setx.log', 'a+') as log_file:
            subprocess.Popen(['setx', var_name, var_value], stdout=log_file, stderr=log_file, shell=shell)
