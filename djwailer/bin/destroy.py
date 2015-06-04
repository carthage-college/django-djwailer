from djwailer.core.models import LivewhaleCourseCatalog

# delete the current catalog of courses

LivewhaleCourseCatalog.objects.using('livewhale').all().delete()
