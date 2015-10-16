import requests

def get_nr(nr):
    r=requests.get('http://46.101.159.170/A60EHNNQ/esrever/{}'.format(nr))
    print r.text
    return r.json()['number']



nr='321'
while True:
    x=get_nr(nr)
    print x
    nr=str(x)[::-1]
