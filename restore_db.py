import os, django, pickle

print('Deleting database')
os.system('rm db.sqlite3')

print('Running migrations')
os.system('python3 manage.py migrate')

dumpfile = 'db_dump.p'

print('Loading objects from', dumpfile)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

objects = pickle.load( open( dumpfile, "rb" ) )
num_objects = len(objects)
while objects:
    _object = objects.pop(0)
    try:
        _object.save()
    except django.db.utils.IntegrityError:
        # A key this object depends on has not been loaded yet.
        # Load it at the end instead.
        objects.append(_object)

print ('Saved', num_objects, 'objects')
