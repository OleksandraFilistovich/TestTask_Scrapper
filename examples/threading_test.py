import random
import threading
import time


class Bot:
    def __init__(self):
        self.threads_list: list[threading.Thread] = []
        self.data = {}
        self.max_threads = 3
        self.flags_for_stop = {}

    def foo(self, n):
        if self.flags_for_stop[n] is True:
            return 
        thread = threading.current_thread()
        name = thread.name
        print('Thread name:', name, n)
        time.sleep(random.randint(1, 2))
        self.data[n] = 'sdfdsf'

    def clear_threads(self):
        for thread in self.threads_list[:]:
            if not thread.is_alive():
                self.threads_list.remove(thread)
                
    def run(self):
        while True:
            
            self.clear_threads()

            list_of_data = range(10)
            
            for i in list_of_data:
                
                br = False
                for thread in threading.enumerate():
                    if thread.name == f'New name {i}':
                        br = True
                        break
                        
                if br:
                    continue
                    
                while True:
                    if len(self.threads_list) < self.max_threads:
                        break

                    self.clear_threads()
                        
                    time.sleep(0.1)
                
                x = threading.Thread(target=self.foo, name=f'New name {i}', daemon=True, args=(i,))
                ##
                self.flags_for_stop[i] = False
                x.start()
                self.threads_list.append(x)
    
            for thread in self.threads_list:
                thread.join()


if __name__ == '__main__':
    bot = Bot()
    bot.run()
