import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from catalog.load_csv import load_csv, attach_images

class Command(BaseCommand):
    def add_arguments(self, parser):

        parser.add_argument('--load-csv',
                            dest='csv_file',
                            help='Load items from CSV file')
        parser.add_argument('--attach-images',
                            dest="images_archive",
                            help="Update images from archive")


    def handle(self, *args, **options):
        handled = False
        images_archive = options.get("images_archive")
        if images_archive and os.path.exists(images_archive):
            attach_images(images_archive)
            self.stderr.write("Loaded images from %s" % images_archive)
            handled = True

        csv_file = options.get("csv_file")
        if csv_file and os.path.exists(csv_file):
            load_csv(csv_file)
            self.stderr.write("Imported csv file %s" % csv_file)
            handled = True

        if not handled:
            raise CommandError("No valid import files specified!")
