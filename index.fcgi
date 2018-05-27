#!/home1/sumitsk20/public_html/dikshagulatidietplate.com/bin/python

import os,sys
try:
    from flup.server.fcgi import WSGIServer
    from django.core.wsgi import get_wsgi_application
    sys.path.insert(0, "/home1/sumitsk20/public_html/dikshagulatidietplate.com/src/")
    sys.path.insert(0, "/home1/sumitsk20/public_html/dikshagulatidietplate.com/static/")
    sys.path.insert(0, "/home1/sumitsk20/public_html/dikshagulatidietplate.com/media/")
    os.environ['DJANGO_SETTINGS_MODULE'] = "dietplate.settings"
    import traceback
    WSGIServer(get_wsgi_application()).run()
except Exception as e:
    with open('../fcgi-log.log, 'a+') as f:
        f.write("\n\n")
        f.write(str(e))
        f.write(traceback.format_exc())

