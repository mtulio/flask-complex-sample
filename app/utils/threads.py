from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import time


class ThreadPool(object):
    """
    Keep all threads and multiplex it between running list and history.
    """

    def __init__(self, workers_max, queue_max=100):
        self.q_running_max = workers_max
        self.q_waiting_max = queue_max
        self.q_waiting_cur = 0
        self.q_history_max = 100

        self.runner = ThreadPoolExecutor(self.q_running_max)

        # Queues / Lists
        self.q_running = []
        self.q_waiting = Queue()
        self.q_history = []

        # Start thread manager
        self.manager_enabled = True
        self.manager_job = self.runner.submit(self.manager)

        # Metrics
        self.metrics = {
            'manager': str(self.manager_job),
            '_waiting': {},
            '_running': {},
            '_finished': {}
        }

    def remove(self, thread):
        """Remove job from the pool."""
        pos = 0
        pos_found = -1
        for w in self.q_running:
            if w['job'] == thread['job']:
                pos_found = pos
            pos += 1

        if pos_found >= 0:
            w = self.q_running.pop(pos_found)
            w['_time'] = time.time()
            w['_result'] = str(w['job'].result(timeout=1))
            self.q_history.append(w)


    def manager(self, **kwargs):
        """
        Control the thread pool:
        - remove finished threads from workers;
        - add threads from queue to workers;
        - ensure that the number of threads does not exced the max workers;
        - ensure that the queue is not max than the defined (auto)
        """
        try:
            while self.manager_enabled:
                wait_now = False

                for w in self.q_running:
                    if w['job'].done():
                        self.remove(w)

                if len(self.q_running) >= self.q_running_max:
                    wait_now = True

                if (not self.q_waiting.empty()) and (not wait_now):
                    w = self.q_waiting.get_nowait()
                    f = w['_func']
                    a = w['_args']
                    w['job'] = self.runner.submit(f, a)
                    self.q_running.append(w)

                time.sleep(1)
        except Exception as e:
            print(e)
            raise

    def clean_all(self):
        """Remove all threads when an exception was raised."""
        print("clean_all()")
        self.manager_enabled = False
        self.runner.shutdown()

    def run(self, **kwargs):
        """Run an thread and append it to the thread pool."""
        alias = 'default-name'
        func = None
        force = False
        for k in kwargs:
            if 'alias' == k:
                alias = kwargs[k]
            if 'func' == k:
                func = kwargs[k]

        worker = {
            'name': alias,
            '_func': func,
            '_args': kwargs
        }
        self.queue_put(worker)

    def queue_put(self, worker):

        print("#> queue_put() {}".format(self.q_waiting.qsize()))
        if self.q_waiting.full():
            print("#> queue_full()")
            return  False

        return self.q_waiting.put_nowait(worker)

    def queue_pop(self):
        """FIFO"""
        return self.q_waiting.get_nowait()

    def format_list(self, list_name, detailed=False):
        r = []
        for l in list_name:
            d = {}
            for k in l.keys():
                if (type(l[k]) == int) or \
                    (type(l[k]) == bool) or \
                    (type(l[k]) == str):
                    d[k] = l[k]
                else:
                    d[k] = str(l[k])

            r.append(d)

        t_list = {}
        if detailed:
            t_list['list'] = r
        t_list['_count'] = len(r)
        return t_list

    def list_running(self, detailed=False):
        """Return a list with running thread."""
        t_list = self.format_list(self.q_running, detailed=detailed)
        t_list['_max'] = self.q_running_max
        return t_list

    def list_queue(self, detailed=False):
        """Return a list with running thread."""
        #t_list = self.format_list(self.queue, detailed=detailed)
        t_list = {}
        t_list['_count'] = self.q_waiting.qsize()
        t_list['_max'] = self.q_waiting_max
        return t_list

    def list_history(self, detailed=False):
        """Return a list with running thread."""
        t_list = self.format_list(self.q_history, detailed=detailed)
        t_list['_max'] = self.q_history_max
        return t_list

    def metrics_list(self):
        """ Update statc metrics"""
        self.metrics.update({'_waiting': self.list_queue()})
        self.metrics.update({'_running': self.list_running()})
        self.metrics.update({'_finished': self.list_history()})
        return self.metrics

    def metrics_list_detailed(self):
        """ Update statc metrics"""
        self.metrics.update({'_waiting': self.list_queue(detailed=True)})
        self.metrics.update({'_running': self.list_running(detailed=True)})
        self.metrics.update({'_finished': self.list_history(detailed=True)})
        return self.metrics
