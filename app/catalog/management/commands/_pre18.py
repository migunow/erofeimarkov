import os
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from catalog.load_csv import load_csv, attach_images
from notifications.notifier import send_notification


class Command(BaseCommand):
    args = ''
    help = ''

    option_list = BaseCommand.option_list + (
        make_option('--load-csv',
                    dest='csv_file',
                    help='CSV file to import'),
        make_option('--attach-images',
                    dest="images_archive",
                    help="Updated images archive")
        )

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
        else:
            params = {
                "images_archive": images_archive,
                "csv_file": csv_file,
            }
            send_notification("load_items", params)
