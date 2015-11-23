# -*- coding: utf-8 -*-
import os, sys
import pyinotify
import logging

# setting up django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "erofeimarkov.settings")
sys.path.append("../app")
from django.core.management import call_command

logger = logging.getLogger("inotify")

class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        path = event.pathname
        if path.endswith(".csv"):
            params = {"csv_file": path}
        elif path.endswith("zip"):
            params = {"images_archive": path}
        else:
            logger.error("Unexpected file in inotify directory: {0}".format(path))
            return
        call_command("load_items", **params)

    #def process_IN_MOVED_TO(self, event):
    #    print "IN_MOVED_TO: ", getattr(event, "src_pathname", None), "->", event.pathname

    #def process_IN_MOVED_FROM(self, event):
    #    print "IN_MOVED_FROM: ", event.pathname


def main():
    args = sys.argv[1:]
    if len (args) > 0:
        watch_dir = args[0]
    else:
        print ("Usage: {0} directory_to_watch".format(sys.argv[0]))
        exit(1)
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch(watch_dir, pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO | pyinotify.IN_MOVED_FROM, rec=True)

    # event handler
    eh = MyEventHandler()

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

if __name__ == '__main__':
    main()
