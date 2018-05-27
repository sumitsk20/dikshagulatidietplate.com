#!/home1/sumitsk20/public_html/dikshagulatidietplate.com/bin/python

import os,sys
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

load_dotenv(find_dotenv())

try:
    from flup.server.fcgi import WSGIServer
    from django.core.wsgi import get_wsgi_application
    sys.path.insert(0, "/home1/sumitsk20/public_html/dikshagulatidietplate.com/src/")
    os.environ['DJANGO_SETTINGS_MODULE'] = "dietplate.settings"
    import traceback
    WSGIServer(get_wsgi_application()).run()
except Exception as e:
    with open('/home1/sumitsk20/public_html/dikshagulatidietplate.com/logs/fcgi.log', 'a+') as f:
        f.write("\n\n")
        f.write(str(e))
        f.write(traceback.format_exc())





