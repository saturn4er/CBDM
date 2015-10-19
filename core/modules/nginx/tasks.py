import os
import subprocess
import sys, pwd, platform

from config import directories
from core.BasicLibs import net, archives, fs, assembly, system
from core.BasicLibs.system import sudo


def download_nginx(version):
    archiveLoc = net.download_file("http://nginx.org/download/nginx-{0}.tar.gz".format(version))
    archives.extract_tar(archiveLoc, "temp")
    fs.rename("temp/nginx-*", "temp/nginx", True)


def download_pcre(version):
    pcreLoc = net.download_file(
        "http://sourceforge.net/projects/pcre/files/pcre/{0}/pcre-{0}.tar.gz/download".format(version))
    archives.extract_tar(pcreLoc, "temp")
    fs.rename("temp/pcre-*", "temp/pcre", True)


def download_zlib(version):
    pcreLoc = net.download_file("http://zlib.net/zlib-{0}.tar.gz".format(version))
    archives.extract_tar(pcreLoc, "temp")
    fs.rename("temp/zlib-*", "temp/zlib", True)

def download_openssl(version):
    opensslUrl = "ftp://ftp.openssl.org/source/openssl-{0}.tar.gz".format(version)
    opensslPath= net.download_file(opensslUrl)
    archives.extract_tar(opensslPath, "temp")
    fs.rename("temp/openssl-*", "temp/openssl", True)

# --with-http_ssl_module --conf-path=/etc/nginx/nginx.conf --pid-path=/var/run/nginx.pid --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --user=www --group=www --with-zlib=../zlib --with-pcre=../pcre

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
        '--with-openssl': '../openssl'

    }
    assembly.configure("temp/nginx/", configure_params, [])


def make():
    try:
        assembly.make("temp/nginx/")
        assembly.make_install("temp/nginx/")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error while building nginx: '{0}' in {1}:{2} ".format(e, fname, exc_tb.tb_lineno), file=sys.stderr)
        sys.exit(1)


def copy_init_d_script():
    if(assembly.get_dist() == 'centos'):
        init_script = "nginx_default_centos.sh"
    else:
        init_script = "nginx_default.sh"
    fs.copy("configs/"+init_script, "/etc/init.d/nginx", True, True)
    system.chmod("/etc/init.d/nginx", "a+x", True)


def change_configs():
    fs.copy("nginx.conf", "/etc/nginx/nginx.conf", True, True)
    if os.path.exists("/etc/nginx/configs"):
        system.sudo(["rm", "-rf", "/etc/nginx/configs"])
    system.sudo(["mkdir", "/etc/nginx/configs"])


def create_www_user():
    try:
        pwd.getpwnam('www')
    except KeyError:
        system.sudo(["useradd", "-M", "www"])


def build(module_params):
    fs.remove("log")
    fs.remove("temp")
    download_openssl(module_params['openssl_version'])
    download_nginx(module_params['version'])
    download_pcre(module_params['pcre_version'])
    download_zlib(module_params['zlib_version'])
    configure()
    make()
    copy_init_d_script()
    change_configs()
    create_www_user()
    fs.remove("temp")







