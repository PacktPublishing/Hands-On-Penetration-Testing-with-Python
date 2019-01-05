>>> import multiprocessing
>>> def process_me(id):
...     print("Process " +str(id))
... 
>>> for i in range(5):
...     p=multiprocessing.Process(target=process_me,args=(i,))
...     p.start()
>>> Process  0
>>> Process  1
>>> Process  2
>>> Process  3
>>> Process  4
import multiprocessing as mp
>>> class a(mp.Process):
...     def __init__(self):
...             threading.Thread.__init__(self)
...     def run(self):
...             print("Process started")
... 
>>> obj=a()
>>> obj.start()
