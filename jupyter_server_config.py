# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from jupyter_core.paths import jupyter_data_dir
import subprocess
import os
import errno
import stat

c = get_config()
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.port = 8888
c.NotebookApp.open_browser = False
c.ServerApp.notebook_dir = '/home/jovyan/work'
c.ServerApp.quit_button = False
c.ServerApp.shutdown_no_activity_timeout = 5*60
c.MappingKernelManager.cull_idle_timeout = 20*60
c.MappingKernelManager.cull_interval = 30
c.MappingKernelManager.cull_connected = True
c.ServerApp.allow_remote_access = True
c.PasswordIdentityProvider.allow_password_change = False
c.ServerApp.allow_origin = '*'
c.ServerApp.disable_check_xsrf = True


c.ServerApp.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "frame-ancestors https://*.lab-develop.deeplearningai.net https://*.lab.deeplearningai.net https://*.lab.deeplearningai.net https://*.deeplearningai.net https://*.deeplearningai.net:* https://localhost https://localhost:* http://*.lab.deeplearningai.net http://*.lab.deeplearningai.net http://*.deeplearningai.net https://*.deeplearningai.net http://*.deeplearningai.net:* http://localhost http://localhost:* https://*.firebaseapp.com http://*.firebaseapp.com https://*.web.app http://*.web.app http://*.deeplearning.ai https://*.deeplearning.ai http://ac4e-develop.deeplearning.ai http://ac4e-test.deeplearning.ai http://ac4e.deeplearning.ai https://ac4e-develop.deeplearning.ai https://ac4e-test.deeplearning.ai https://ac4e.deeplearning.ai 'self' "
    }
}
c.ServerApp.terminals_enabled=True

c.ServerApp.terminado_settings = { "shell_command": "/bin/bash /start_terminal.sh" }


# https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash = False

# Generate a self-signed certificate
if 'GEN_CERT' in os.environ:
    dir_name = jupyter_data_dir()
    pem_file = os.path.join(dir_name, 'notebook.pem')
    try:
        os.makedirs(dir_name)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(dir_name):
            pass
        else:
            raise
    # Generate a certificate if one doesn't exist on disk
    subprocess.check_call(['openssl', 'req', '-new',
                           '-newkey', 'rsa:2048',
                           '-days', '365',
                           '-nodes', '-x509',
                           '-subj', '/C=XX/ST=XX/L=XX/O=generated/CN=generated',
                           '-keyout', pem_file,
                           '-out', pem_file])
    # Restrict access to the file
    os.chmod(pem_file, stat.S_IRUSR | stat.S_IWUSR)
    c.NotebookApp.certfile = pem_file

# Change default umask for all subprocesses of the notebook server if set in
# the environment
if 'NB_UMASK' in os.environ:
    os.umask(int(os.environ['NB_UMASK'], 8))
