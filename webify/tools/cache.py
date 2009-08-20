import time as _time

class Cache(object):
    def __init__(self):
        raise NotImplementedError
    def set(self, key, value, time=0):
        raise NotImplementedError
    def get(self, key):
        raise NotImplementedError
    #TODO: jperla: implement these
    def delete(self, key):
        raise NotImplementedError
    def set_multi(self, key):
        raise NotImplementedError
    def get_multi(self, key):
        raise NotImplementedError
    def cached(self, key, f, time=0):
        found = self.get(key)
        if not found:
            cached = f()
            self.set(key, cached)
            return cached
        else:
            return found

class MemoryCache(Cache):
    def __init__(self):
        self.cache = {}
    def set(self, key, value, time=0):
        if time == 0:
            time = 1000000000
        now = _time.time()
        self.cache[key] = (now + time, value)
    def get(self, key):
        now = _time.time()
        if key in self.cache:
            expires, value = self.cache[key]
            if now > expires:
                return value
            else:
                return None
        else:
            return None

class MemcachedCache(Cache):
    def __init__(self, locations):
        self.memcache_client = memcache.Client(locations)
    def set(self, key, value, time=0):
        self.memcache_client.set(key, time=time)
    def get(self, key):
        return self.memcache_client.get(key)

        
