import os
import platform
from core.BasicLibs import net, archives, fs, assembly, system


def build(module_params):
    distro = platform.linux_distribution()
    deps = {
        "Ubuntu": ['bind9'],
        "Centos": ['bind', 'bind-utils']
    }
    assembly.install_distro_dependencies(deps[distro[0]])



