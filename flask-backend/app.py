from flask import Flask, request
from handler.contacts import ContactHandler


app = Flask(__name__)


@app.route('/')
def index():
    return 'This is the home of the messaging app'


@app.route('/login')
def login():
    return 'You cannot log in at the moment lol'


@app.route('/kheApp/dashboard')
def dashboard():
    return 'statistics'


#working on this rn
@app.route('/kheApp/contacts')
def contacts():
    if request.args:
        return ContactHandler().searchContacts(request.args)
    else:
        handler = ContactHandler()
        return handler.getAllContacts()


@app.route('/kheApp/contacts/<int:cid>')
def getContactById(cid):
    return ContactHandler().getContactById(cid)

# #search by first name
# @app.route('/kheApp/contacts/<cfirstname>')
# def getContactByFirstName(cfirstname):
#     return ContactHandler().getContactByFirstName(cfirstname)


@app.route('/kheApp/messaging')
def messaging():
    return 'messaging'


if __name__ == '__main__':
    app.run(debug=True)


