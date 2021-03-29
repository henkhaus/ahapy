import os
from ahapy import AhaV1

AHA_KEY = os.environ.get('AHA_API_KEY')
aha = AhaV1('enverus', AHA_KEY)


def test_v1_query():
    data = aha.query('initiatives')
    for i in data:
        print(i['name'])


def test_v1_count():
    count = aha._count('epics')
    print(count)


def test_v1_fields():
    data = aha.query('initiatives', fields='name,id')
    for i in data:
        print(i)


def test_v1_page():
    data = aha.query('initiatives', per_page=200)
    for i in data:
        print(i['name'])


#test_v1_count()
#test_v1_count()

