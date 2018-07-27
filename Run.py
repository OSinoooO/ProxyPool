# -*- coding:utf-8 -*-
from multiprocessing import Process
from proxyAPI_module import app
from Getter_module import Getter
from Tester_module import Tester
import time

TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GERTER_ENABLED = True
API_ENABLED = True

class Scheduler(object):
    def scheduler_getter(self, cycle=GETTER_CYCLE):
        """
        定是获取代理
        :param cycle: 间隔时间
        """
        getter = Getter()
        while True:
            getter.run()
            time.sleep(cycle)

    def scheduler_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        :param cycle: 间隔时间
        """
        tester = Tester()
        while True:
            tester.run()
            time.sleep(cycle)

    def scheduler_api(self):
        """
        开启API
        """
        app.run()
        print('API接口已开启...')

    def run(self):
        if TESTER_ENABLED:
            tester_process = Process(target=self.scheduler_tester)
            tester_process.start()

        if GERTER_ENABLED:
            getter_process = Process(target=self.scheduler_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.scheduler_api)
            api_process.start()

if __name__ == '__main__':
    #代理池API接口:  http://localhost:5000/random
    scheduler = Scheduler()
    scheduler.run()