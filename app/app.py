
import os
from flask import Flask
from .utils.threads import ThreadPool
from .tasks import Tasks


class ThreadApp(object):
    def __init__(self, app=None, app_host="0.0.0.0", app_port=5000,
                 pool=None, max_threads=5):
        self.version = self.set_version()

        # Flask APP
        self.app_host = app_host
        self.app_port = app_port
        self.app_debug = True
        self.app_folder_templates = 'templates'
        if app:
            self.app = app
        else:
            self.app = Flask(__name__,
                             template_folder=self.app_folder_templates)

        # Thread Pool
        if pool:
            self.pool = pool
        else:
            self.pool = ThreadPool(max_threads)

        # Tasks
        self.tasks = Tasks()


    def get_app(self):
        return self.app

    def get_pool(self):
        return self.pool

    def get_version(self):
        return self.version

    def set_version(self):
        if os.path.isfile('VERSION'):
            with open('VERSION', 'r') as f:
                return f.read().rstrip()
        return 'UNKNOWN'

    def clean(self):
        print("clean()")
        self.pool.clean_all()

    def run(self, daemon=False):
        """
        Run any application or thread you need.
        Check exception and signals to handler
        """
        if daemon:
            print("Running as daemon mode")

        try:
            #Tasks.run_sleep15()
            self.app.run(host=self.app_host, port=self.app_port, debug=self.app_debug)

        except (KeyboardInterrupt, SystemExit):
            #do something else
            self.clean()
            raise

        except:
            self.clean()
            raise
