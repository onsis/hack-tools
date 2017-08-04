import eventlet

class ThreadTool(object):
    def __init__(self):
        self.job = None
        self.thread_num = 10
        self.queue = eventlet.Queue()
        self.pool = eventlet.GreenPool()


    def set_Thread_num(self):
        pass

    def add_task(self,task):
        self.job = task

    def get_work(self):
        pass

    def push(self,req):
        for urls in req:
            self.queue.put(urls)

        while True:
            while not self.queue.empty():
                url = self.queue.get()
                self.pool.spawn_n(self.do_job,self.job,url)
            self.pool.waitall()
            if self.queue.empty():
                break

    def do_job(self,job,url):
        return job(url)

    def start(self):
        pass