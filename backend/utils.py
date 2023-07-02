from itertools import islice


def chunks(iterable, size=10):
    iterator = iter(iterable)
    chunk = list(islice(iterator, size))
    while chunk:
        yield chunk
        chunk = list(islice(iterator, size))
