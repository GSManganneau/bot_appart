import hashlib


def h11(w):
    return hashlib.md5(w.encode('utf-8')).hexdigest()[:9]

