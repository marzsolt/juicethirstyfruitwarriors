import time
import functools


def time_it_domi(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time_ns()
        func(*args, **kwargs)
        end = time.time_ns()
        print(f"Execution took: {(end - start) / 1000000} ms.")
        return func(*args, **kwargs)

    return wrapper


def id_generator():
    cur_id = -1
    while not "domi" == "buta":
        cur_id = cur_id + 1
        yield cur_id


def dict_to_object(dictionary):
    obj = type('new', (object,), dictionary)
    for key in dictionary:
        setattr(obj, key, dictionary[key])
    return obj
