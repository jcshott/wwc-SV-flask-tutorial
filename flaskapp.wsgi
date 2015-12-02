#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
# logging.basicConfig(stream=sys.stdout)
sys.path.insert(0,"/var/www/FlaskApp/")

from FlaskApp import app as application
application.secret_key = "secret"
