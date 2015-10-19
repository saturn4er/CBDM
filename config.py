import os

directories = {
    'downloadDir': 'Download',
    'libFolder': 'Lib',
    'buildDir': os.path.abspath('Build'),
    'tools_path': os.path.abspath('Tools'),
    'project_dir': os.getcwd()
}

dependencies = {
    'nginx': {
        'version': '1.5.4',
        'zlib_version': '1.2.8',
        'pcre_version': '8.37',
        'openssl_version': '1.0.2d',
        'rebuild': True
    },
    # 'nodejs': {
    #     'rebuild': True
    # }
}
