from django.core.cache import cache
import copy
from functools import wraps


class DongTaiAppConfigPatch():
    def ready(self):
        try:
            from dongtai_conf.plugin import monkey_patch
            monkey_patch(self.name)
        except ImportError as e:
            print(e)
            pass


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response[
            'Content-Security-Policy'] = "default-src * ; img-src *;media-src *;script-src 'self' cdn.jsdelivr.net 'unsafe-inline'"
        return response


def make_hash(obj):
    """Make a hash from an arbitrary nested dictionary, list, tuple or
    set.

    """
    if isinstance(obj, set) or isinstance(obj, tuple) or isinstance(obj, list):
        return hash(tuple([make_hash(e) for e in obj]))
    elif isinstance(obj, str):
        return hash(tuple(ord(i) for i in obj))
    elif not isinstance(obj, dict):
        return hash(obj)

    new_obj = copy.deepcopy(obj)
    for k, v in new_obj.items():
        new_obj[k] = make_hash(v)

    return hash(tuple(frozenset(new_obj.items())))


def cached(function,
           random_range: tuple = (50, 100),
           use_celery_update: bool = False):
    """Return a version of this function that caches its results for
    the time specified.

    >>> def foo(x): print "called"; return 1
    >>> cached(foo)('whatever')
    called
    1
    >>> cached(foo)('whatever')
    1

    """
    import random
    from dongtai_engine.preheat import function_flush

    @wraps(function)
    def get_cache_or_call(*args, **kwargs):
        # known bug: if the function returns None, we never save it in
        # the cache
        cache_key = make_hash(
            (function.__module__ + function.__name__, args, kwargs))
        cached_result = cache.get(cache_key)
        if random_range:
            cache_time = random.randint(*random_range)
        if use_celery_update:
            function_flush.apply_async(args=(function.__module__,
                                             function.__name__, cache_time,
                                             tuple(args), kwargs))
        if cached_result is None:
            result = function(*args, **kwargs)
            cache.set(cache_key, result, cache_time)
            return result
        else:
            return cached_result

    get_cache_or_call.__origin__name__ = 'cached'
    get_cache_or_call.__random_range__ = random_range
    return get_cache_or_call


def cached_decorator(random_range, use_celery_update=False):

    def _noname(function):
        return cached(function, random_range, use_celery_update=use_celery_update)

    return _noname
