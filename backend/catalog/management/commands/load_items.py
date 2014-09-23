#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from catalog.load_csv import load_csv, attach_images


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        # filename = os.path.join(settings.BASE_DIR, '..', '..', 'vig2.csv')
        # load_csv(filename)

        filename = os.path.join(settings.BASE_DIR, '..', '..', 'test_items.zip')
        attach_images(filename)

