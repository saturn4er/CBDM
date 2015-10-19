import os
import subprocess
import sys, pwd, re

from config import directories
from core.BasicLibs import net, archives, fs, assembly, system
from core.BasicLibs.system import sudo


def download(version):
    archiveLoc = net.download_file("https://nodejs.org/dist/v{0}/node-v{0}.tar.gz".format(version))
    archives.extract_tar(archiveLoc, "temp")


def download_pcre(version):
    pcreLoc = net.download_file(
        "http://sourceforge.net/projects/pcre/files/pcre/{0}/pcre-{0}.tar.gz/download".format(version))
    archives.extract_tar(pcreLoc, "temp")
    fs.rename("temp/pcre-*", "temp/pcre", True)


def download_zlib(version):
    pcreLoc = net.download_file("http://zlib.net/zlib-{0}.tar.gz".format(version))
    archives.extract_tar(pcreLoc, "temp")
    fs.rename("temp/zlib-*", "temp/zlib", True)


def configure():
    configure_params = {
        '--conf-path': '/etc/nginx/nginx.conf',
        '--pid-path': '/var/run/nginx.pid',
        '--error-log-path': '/var/log/nginx/error.log',
        '--http-log-path': '/var/log/nginx/access.log',
        '--user': 'www',
        '--group': 'www',
        '--with-zlib': '../zlib',
        '--with-pcre': '../pcre',

    }
    configure_inline_params = ['--with-http_ssl_module']
    assembly.configure("temp/nginx/", configure_params, configure_inline_params)


def make():
    try:
        assembly.make("temp/nginx/")
        assembly.make_install("temp/nginx/")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error while building nginx: '{0}' in {1}:{2} ".format(e, fname, exc_tb.tb_lineno), file=sys.stderr)
        sys.exit(1)


def build(module_params):
    fs.remove("log")
    fs.remove("temp")
    shasums_url = "https://nodejs.org/dist/latest/SHASUMS256.txt"
    path_to_shasums = net.download_file(shasums_url)
    with open(path_to_shasums) as shasums_file:
        line = shasums_file.readline()
        match = re.search("node-v((\d.?)+?)-", line)
        latest_version = match.group(1)
        node_archive = net.download_file("https://nodejs.org/dist/latest/node-v{0}.tar.gz".format(latest_version))
        archives.extract_tar(node_archive, "temp")
        fs.rename("./temp/node-*", "./temp/node_src", True)
        assembly.configure("temp/node_src/", {}, [])
        try:
            assembly.make("temp/node_src/")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error while building nginx: '{0}' in {1}:{2} ".format(e, fname, exc_tb.tb_lineno), file=sys.stderr)
            print("Make log: ", os.path.abspath('log/make.txt'))
            sys.exit(1)
        try:
            assembly.make_install("temp/node_src/")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error while building nginx: '{0}' in {1}:{2} ".format(e, fname, exc_tb.tb_lineno), file=sys.stderr)
            print("Make log: ", os.path.abspath('log/make_install.txt'))
            sys.exit(1)
    fs.remove("temp")

