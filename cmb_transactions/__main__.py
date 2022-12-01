# -*- coding:utf-8 -*-
import sys
import argparse
import typing as ty
from .models import Request

parser = argparse.ArgumentParser()

"""
Protocol:
 - Input:
     @@ CMB [uid] @@
     [Content]

"""


def stream_stdin(buf: str) -> Request:
    header, content = buf.split('\n', 1)
    header = header.strip('@').strip()
    account, uid = header.split(' ')

    r = Request(uid=int(uid.strip()),
                message=content)

    return r



if __name__ == '__main__':
    current_request: ty.Optional[Request] = None

    while True:
        buf = sys.stdin.readline()
