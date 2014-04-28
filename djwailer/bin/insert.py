# -*- coding: utf-8 -*-
from djtools.utils.database import mysql_db

import datetime
import MySQLdb

headline="Los periódicos se convierten en juguetes de multimillonarios"
summary="""
Pocas personas saben hoy que cuando se crearon las primeras agencias de noticias en el siglo XIX, la Havas francesa y la británica Reuter dividieron el mundo entre ellas. La división siguió las fronteras de los dos imperios coloniales.
"""
body="""
América Latina fue a parar a manos de Havas, mientras Reuter se quedó con Estados Unidos.
La primera agencia estadounidense que rompió el monopolio fue la United Press International (UPI), alegando que Estados Unidos no podía ser visto a través de los ojos británicos, un argumento muy parecido a la queja del Tercer Mundo contra el monopolio de información del Norte.

En el mundo de los medios, esta agencia era considerada un gigante, por lo que fue una sorpresa cuando en 1985 un millonario mexicano, Mario Vázquez Raña, compró la UPI por 41 millones de dólares y pronunció la célebre frase: “Yo tenía dos jets Falcon. Vendí uno y compré la UPI”.

Desde entonces, la concentración de medios en manos de multimillonarios ha proliferado. Los casos de Rupert Murdoch y Silvio Berlusconi son los más famosos. Algunos observadores ven en esto un giro a la derecha, impulsado por los que tienen dinero. No se trata de una teoría conspirativa. Simplemente 100 poseedores de un Ferrari tienden a tener una visión más coincidente sobre las cosas que, por ejemplo, los dueños de 100 Volkswagen.
"""
date_dt = datetime.datetime.combine(datetime.date.today(),datetime.time())
date    = date_dt.strftime("%m/%d/%Y")
status  = 1
contact_info = "Larry"
sql = "INSERT INTO livewhale_news (gid,suggested,rank,last_user,created_by,date_created,last_modified,headline,summary,body,status,date,date_dt,contact_info) VALUES ('94','','0','7','7','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (date_dt,date_dt,headline,summary,body,status,date,date_dt,contact_info)
print sql
hs = "localhost"
us = ""
ps = ""
db = "livewhale_www"
conn  = MySQLdb.connect(host=hs,user=us,passwd=ps,db=db)
curr = conn.cursor()
curr.execute(sql)
conn.commit()
curr.close ()
conn.close ()

