import os
import subprocess
import sys, pwd, grp

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
    download(module_params['version'])
    # download_pcre(module_params['pcre_version'])
    # download_zlib(module_params['zlib_version'])
    # configure()
    # make()
    # TODO: download init.d script
    # fs.remove("temp")
    # fs.copy("nginx_default.sh", "/etc/init.d/nginx", True, True)
    # system.chmod("/etc/init.d/nginx", "a+x", True)
    # fs.copy("nginx.conf", "/etc/nginx/nginx.conf", True, True)

