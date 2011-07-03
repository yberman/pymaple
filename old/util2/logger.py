class LogEntry(list):
    def __init__(self, father_name='<unammed function>', log_events=True, show_messages=False, frequency=1):
        self.logging = log_events
        self._fname = father_name
        self._show_msg = show_messages
        self._frequency = frequency
        self._iter = 0
        list.__init__(self)
        
    def append(self, obj):
        self._iter += 1
        if self.logging and self._iter % self._frequency == 0:
            list.append(obj)
            if self._show_msg:
                print '[ %s() ] - %s' % (self._fname, obj)
            
    def append_f(self, func, *args, **kargs):
        self._iter += 1
        if self.logging and self._iter % self._frequency == 0:
            obj = func(*args, **kargs)
            list.append(func(*args, **kargs))
            if self._show_msg or critical:
                print '[ %s() ] - %s' % (self._fname, obj)
                
    def append_flist(self, func_list, *args, **kargs):
        self._iter += 1
        if self.logging and self._iter % self._frequency == 0:
            obj = tuple([ f(*args, **kargs) for f in flist ])
            list.append(func(*args, **kargs))
            if self._show_msg or critical:
                print '[ %s() ] - %s' % (self._fname, obj)