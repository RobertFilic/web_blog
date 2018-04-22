__author__ = 'robee'

from flask import Flask

# initiate the app
app = Flask(__name__)  # '__name__' containes '__main__'


# define an endpoint
@app.route('/')  # endpoint is www.mywebsite.com/api/
def hello_method():
    return "Hello, world!"


# Requirement to run the app:
if __name__ == '__main__':
    app.run() # we can change the port by entering exmp: port=4995
