pip install uwsgi


$ cat wsgi.py
from main import app
if __name__ == "__main__":
    app.run()


uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app


$ cat script.sh
#!/bin/bash
uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app