import django

from djwailer.core.models import LivewhaleCourseCatalog

django.setup()

# delete the current catalog of courses
LivewhaleCourseCatalog.objects.using('livewhale').all().delete()
