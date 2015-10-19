import os
import subprocess
import sys, pwd, platform

from config import directories
from core.BasicLibs import net, archives, fs, assembly, system
from core.BasicLibs.system import sudo

def build(module_params):
    if assembly.get_dist() == 'centos':

        sudo("yum install -y epel-release")
        assembly.install_distro_dependencies([
          'sudo', 'vim', 'git', 'htop', 'fail2ban'
        ])
        sudo("yum groupinstall 'Development Tools'")







