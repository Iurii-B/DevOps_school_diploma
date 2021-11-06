pip install uwsgi

uwsgi --socket 0.0.0.0:5000 --protocol=http -w main:app

Config file uwsgi.ini:
[uwsgi]
module = main:app
protocol = http
socket = 0.0.0.0:5000
env = DB_ADMIN_USERNAME=$(DB_ADMIN_USERNAME)
env = DB_ADMIN_PASSWORD=$(DB_ADMIN_PASSWORD)
env = DB_URL=$(DB_URL)

uwsgi --ini uwsgi.ini