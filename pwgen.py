#!/usr/bin/env python

def generate_password(length):
    if not isinstance(length, int) or length < 8:
        raise ValueError("temp password must have positive length")

    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefjklmnpqrstuvwxyzg#@$%^*_-"
    from os import urandom
    return "".join([chars[ord(c) % len(chars)] for c in urandom(length)])

howmany = 1
length = 12
for i in range(howmany):
    print str(generate_password(length)).strip()

