import time as _time

class Cached(object):
    def __init__(self):
        raise NotImplementedError
    def cached(self, key, object, time=3600):
        raise NotImplementedError
        
class MemoryCached(Cached):
    def __init__(self):
        self.cache = {}
    def __call__(self, key, f, time=0):
        if time == 0:
            time = 1000000000
        now = _time.time()
        if key not in self.cache or now > self.cache[key][0]:
            self.cache[key] = (now + time, f())
        return self.cache[key]
    #TODO: jperla: add get/set/etc

        
class MemcachedCached(Cached):
    def __init__(self, locations):
        self.memcache_client = memcache.Client(locations)
    def __call__(self, key, f, time=0):
        cached = self.memcache_client.get(key)
        if not cached:
            cached = f()
            self.memcache_client.set(key, time=time)
        return cached

        
