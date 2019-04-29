import os, django
import pickle
import django.apps

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

django.apps.apps.get_models()

all_objects = []
models = django.apps.apps.get_models()
for model in models:
    objects = model.objects.all()
    all_objects.extend(objects)

print ('all_objects:', all_objects)
pickle.dump(all_objects, open( "db_dump.p", "wb" ) )

# Uploaded this file from Heroku with
# curl --upload-file db_dump.p \
    # https://transfer.sh/fivefishyfishermen_dbdump.p
#
# Downloaded on client with
# curl https://transfer.sh/gaZU9/fivefishyfishermen_dbdump.p \
    # -o db_dump.p
