# jm8wx 4/14/19
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.contrib.auth.models import User
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("user")
args = parser.parse_args()
if not args.user:
    print ("Please provide a user argument to make a superuser.")

print ("Making", args.user, "a superuser")
user = User.objects.get(username=args.user)
if user.is_superuser:
	print (args.user, "already a superuser")
	quit()
user.is_staff = True
user.is_admin = True
user.is_superuser = True
user.save()
print ("Saved", args.user + ".")
