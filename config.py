import os

directories = {
    'downloadDir': 'Download',
    'libFolder': 'Lib',
    'buildDir': os.path.abspath('Build'),
    'tools_path': os.path.abspath('Tools'),
    'project_dir': os.getcwd()
}

projectName = 'FrozenEngine'
cmakeVersion = '3.2.2'
cmakeGenerator = 'Visual Studio 12'
buildArchitecture = 'x64'  # x86 | x32
visual_studio_toolset = 'v120'
visual_studio_runtime_library = 'MD'

dependencies = {
    'nginx': {
        'version': '1.5.4',
        'zlib_version': '1.2.8',
        'pcre_version': '8.37',
        'rebuild': True
    }
}
