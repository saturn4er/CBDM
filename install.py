from core.BasicLibs.system import gain_sudo_password
from core.Dependencies.dependencies import Dependencies

gain_sudo_password()
dependencies = Dependencies()
dependencies.run_tasks()
