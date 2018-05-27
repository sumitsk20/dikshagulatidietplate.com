#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

load_dotenv(find_dotenv())

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

try:
    if __name__ == "__main__":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dietplate.settings")
        try:
            from django.core.management import execute_from_command_line
        except ImportError:
            # The above import may fail for some other reason. Ensure that the
            # issue is really that Django is missing to avoid masking other
            # exceptions on Python 2.
            try:
                import django
            except ImportError:
                raise ImportError(
                    "Couldn't import Django. Are you sure it's installed and "
                    "available on your PYTHONPATH environment variable? Did you "
                    "forget to activate a virtual environment?"
                )
            raise
        execute_from_command_line(sys.argv)
except Exception as e:
    import traceback
    with open('../logs/debug-manage-py.log', 'a+') as f:
        f.write("\n\n++++++++ [" + str(datetime.now()) + "] ++++++++++\n\n")
        f.write(str(e))
        f.write(traceback.format_exc())

