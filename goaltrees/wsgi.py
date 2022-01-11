"""
WSGI config for goaltrees project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

path = "/opt/GoalTrees"
if path not in sys.path:
    sys.path.append(path)

path = "/opt/anaconda3/envs/django_py36/bin"
if path not in sys.path:
    sys.path.append(path)

path = "/opt/anaconda3/envs/django_py36/lib/python3.6/site-packages"
if path not in sys.path:
    sys.path.insert(0, path)



from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goaltrees.settings')

application = get_wsgi_application()
