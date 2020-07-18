from functools import wraps
from flask import request, abort
import os


def split_args(args: str) -> list:
    if "," in args:
        return args.split(",")
    return [args]


def split_dict_args(dict_args: dict, args: list = []) -> dict:
    return {
        key: (split_args(value) if key in args or not args else value)
        for key, value in dict_args.items()
    }

