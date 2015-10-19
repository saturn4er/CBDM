import os
import platform
from shutil import which
import subprocess
import sys

from core import sys_config
from core.BasicLibs import fs
from core.TemporaryDir import TemporaryDir
from core.tools.vcxproj import Builder
from core.BasicLibs.system import sudo

__author__ = 'saturn4er'


def configure(directory, params, inline_params=[], log_file=False):
    print("Run configure script in " + directory)
    params_str = " ".join(["{0}={1}".format(key, val) for key, val in params.items()])
    params_str += " " + " ".join(inline_params)
    if type(log_file) is not str:
        log_file = "configure.log"
    log_file_name = os.path.join(sys_config.log_folder, log_file)
    with open(log_file_name, 'a+') as log_file:
        TemporaryDir.enter(directory)
        process = subprocess.Popen(['./configure ' + params_str], shell=True, stderr=log_file, stdout=log_file)
        process.communicate()
        TemporaryDir.leave()
        if process.returncode != 0:
            raise Exception("'Configure' finished with status-code " + process.returncode)
            sys.exit(1)


def build_vcxproj(path_to_vcxproj, output_dir=False, configurations=False, architectures=False):
    project = Builder(path_to_vcxproj)
    project.build(configurations, architectures, output_dir)


def make(directory, params=False, dependencies=False):
    print("Building project in " + directory)
    if not bool(params):
        params = {}
    if not bool(dependencies):
        dependencies = {}
    if bool(dependencies):
        install_distro_dependencies(dependencies)
    params_str = " ".join(["{0}={1}".format(key, val) for key, val in params.items()])

    make_loc = which('make')
    if make_loc is None:
        raise Exception("'MAKE' IS NOT INSTALLED ON SYSTEM")
        sys.exit(1)

    login_file_name = os.path.join(sys_config.log_folder, 'make.txt')
    fs.require_full_path(login_file_name)
    with open(login_file_name, 'a+') as log_file:
        TemporaryDir.enter(os.path.abspath(directory))
        process = subprocess.Popen(['make ', params_str], stderr=log_file, stdout=log_file, shell=True)
        process.communicate()
        if process.returncode != 0:
            raise Exception("'MAKE' finished with status-code " + str(process.returncode))
            sys.exit(1)
    TemporaryDir.leave()


def make_install(directory):
    print("Installing project in " + directory)
    log_file = os.path.join(sys_config.log_folder, 'make_install.log')
    with open(log_file, 'a+') as log_file:
        TemporaryDir.enter(directory)
        process = sudo(['make', 'install'], stdout=log_file, stderr=log_file)
        if process.returncode != 0:
            raise Exception("'MAKE INSTALL' finished with status-code " + str(process.returncode))
            sys.exit(1)
        TemporaryDir.leave()


def set_vcxproj_runtime_library(path_to_vcxproj, runtime_library):
    """
    Change runtime library of vcxproj file
    :param path_to_vcxproj: Path to vcxproj
    :param runtime_library: (MT, MD)
    :return:
    """
    if runtime_library not in ('MT', 'MD'):
        raise Exception("Invalid runtime library")
        sys.exit(1)
    project = Builder(path_to_vcxproj)
    debug_conf = project.get_configuration("Debug")
    debug_runtime_library = Builder.runtimeLibraries[runtime_library + "d"]
    debug_conf.set_runtime_library(debug_runtime_library)
    debug_conf.save()

    release_runtime_library = Builder.runtimeLibraries[runtime_library]
    release_conf = project.get_configuration("Release")
    release_conf.set_runtime_library(release_runtime_library)
    release_conf.save()


def set_vcxproj_platform_toolset(path_to_vcxproj, platform_toolset):
    """
    Change platform toolset of vcxproj file
    :param path_to_vcxproj: Path to vcxproj
    :param platform_toolset: Platform toolset
    :return:
    """
    project = Builder(path_to_vcxproj)
    debug_conf = project.get_all_configurations()
    debug_conf.set_platform_toolset(platform_toolset)
    debug_conf.save()


def set_vcxproj_platform_toolset_and_rl(path_to_vcxproj, platform_toolset, runtime_library):
    set_vcxproj_platform_toolset(path_to_vcxproj, platform_toolset)
    set_vcxproj_runtime_library(path_to_vcxproj, runtime_library)

def get_dist():
    distro = platform.dist()
    return distro.split(" ")[0]


def install_distro_dependencies(dependencies):
    distro = get_dist()
    package_manager_install_command = {
        "Ubuntu": ['apt-get', 'install', "-y"],
        "Centos": ["yum", 'install', '-y']
    }
    command = package_manager_install_command[distro] + dependencies
    with open('log/install_deps.log', 'a+') as log:
        dep_process = sudo(command, stderr=log, stdout=log)
        dep_process.communicate()
