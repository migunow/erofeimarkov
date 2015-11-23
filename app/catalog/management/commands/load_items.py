#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division


import django

# Implementation differs (Django uses argparse since 1.8)
if django.VERSION[:2] < (1,8):
    from ._pre18 import Command
else:
    from ._post18 import Command
