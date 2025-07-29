# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from jupyter_core.paths import jupyter_data_dir

c = get_config()
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.notebook_dir = '/home/jovyan/work'
c.NotebookApp.quit_button = False
c.NotebookApp.shutdown_no_activity_timeout = 5*60
c.MappingKernelManager.cull_idle_timeout = 20*60
c.MappingKernelManager.cull_interval = 30
c.MappingKernelManager.cull_connected = True
c.NotebookApp.allow_remote_access = True
c.NotebookApp.allow_password_change = False
c.NotebookApp.allow_origin = '*'
c.NotebookApp.disable_check_xsrf = True
c.FileContentsManager.delete_to_trash = False

c.NotebookApp.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "frame-ancestors https://*.lab-develop.deeplearningai.net https://*.lab.deeplearningai.net https://*.lab.deeplearningai.net https://*.deeplearningai.net https://*.deeplearningai.net:* https://localhost https://localhost:* http://*.lab.deeplearningai.net http://*.lab.deeplearningai.net http://*.deeplearningai.net https://*.deeplearningai.net http://*.deeplearningai.net:* http://localhost http://localhost:* https://*.firebaseapp.com http://*.firebaseapp.com https://*.web.app http://*.web.app http://*.deeplearning.ai https://*.deeplearning.ai http://ac4e-develop.deeplearning.ai http://ac4e-test.deeplearning.ai http://ac4e.deeplearning.ai https://ac4e-develop.deeplearning.ai https://ac4e-test.deeplearning.ai https://ac4e.deeplearning.ai"
    }
}
