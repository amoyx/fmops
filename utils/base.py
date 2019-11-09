#!/usr/bin/python
# -*- coding=utf-8 -*-


def is_empty(x):
    return True if x else False


def is_exist(args):
    return list(map(is_empty, args)) if isinstance(args, list) else [False]
