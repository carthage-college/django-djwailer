# -*- coding: utf-8 -*-
from djtools.templatetags.text_mungers import convert_smart_quotes
from djwailer.core.models import LivewhaleEvents, LivewhaleNews

import re

body = """
Last month in your Student Government:
Elections were held for the positions of Secretary, Parliamentarian, two Academic Senators, Organization Liaison, and Multicultural liaison.
Organization budgets were approved for Pals and Partners and the National Association for Music Educators.
Budgetary Special Allocations were granted for The Current and Multicultural Affairs.
Organization 30 day trials were granted for Chess Club and the National Dance Education Organization
Full recognition was granted for Tea Club.
The Student Government President is conducting regular talks with President Woodward, relaying the voice of the student body while the College focuses its future direction. The first topic of conversation revolved around student opinion on the state of the Carthage College curriculum.
An Amendment to the Constitution of the Student Government (Article VII section D) was passed by the student body which now states:
“The order of business and meeting structure will be defined by the executive board with discretion.”
This allows reasonable flexibility in the schedule of SG meetings. For example, the last SG meeting of every month is designed to allow more discussion by representatives in order to make the student body voice heard.
Chairs have been elected for SG committees:
Programming committee
Student Life Enhancement committee
Public Relations committee
Forum committee
Budget and Finance committee
Student Life Enhancement committee will soon be tabling in the Cafeteria for feedback from the student body.
A Student Government Facebook page is in development.
Additional Discussion in Student Government:
Carthage College has a new Nurse and Sexual Assault Counselor.
The upcoming 1st year Reading Experience is in development.
The “Bridge” system is the new method of intra-campus communication. The Student Government Organization Liaison ran an Org 101 on Tuesday 10/1 to educate about the new system.
President Woodward’s State of the College Address is planned for Nov. 14th.
Student Government task forces are in effect with representatives planning proposals to President Woodward to address Campus Busing improvements as well as College concerns.
This year’s Student Government goals include funding large-scale projects that would improve quality of student life.
An updated Student Government website is in development.
Tabling space may soon be available in the Student Union to make up for limited space in the remodeled TWC.
Applications for the Educational Programming Fund for Student Organizations are in the Office of Student Life and are due 10/7.
Discussion by the Executive Board of Student Government:
Eboard is looking to define the central mission of the Student Government. Developing this identity will be a process undertaken by all SG representatives of the student body.
"""
#newbod = convert_smart_quotes(body)
#print newbod

#news = LivewhaleNews.objects.using('livewhale').get(pk=911)
news = LivewhaleNews.objects.using('livewhale').get(pk=853)
#body = convert_smart_quotes(news.body.encode('utf-8'))
body = convert_smart_quotes(news.body.encode('latin1'))
#bod = news.body.encode('latin1').replace('“','"').replace('”','"')
#bod = news.body.encode('utf-8')
bod = news.body
#body = convert_smart_quotes(bod)
#body = bod.replace(u"\u201c", "\"").replace(u"\u201d", "\"")
#body = bod.replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u02BC", "'")
#body = re.sub(u'[\u00ab\u00bb\u201c\u201d\u201e\u201f\u300e\u300f]','"', news.body.encode('latin1'))
#print news.body
print body
