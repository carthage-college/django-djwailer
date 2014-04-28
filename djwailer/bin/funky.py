# -*- coding: utf-8 -*-
#!/usr/bin/python

from djwailer.core.models import LivewhaleNews

funky = LivewhaleNews.objects.using('livewhale').get(pk=286)
print funky.headline
#funky.headline = funky.headline.replace( "’", "'" ).replace( "“", '"' ).replace( "”", '"' )
#funkey.save()
