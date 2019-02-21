from flask import Flask, request
from handler.handler import ContactHandler, ChatHandler


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
        keyword = request.args['keyword']
        return ContactHandler().searchContacts(keyword)
    else:
        handler = ContactHandler()
        return handler.getAllContacts()


@app.route('/kheApp/contacts/<int:cid>')
def getContactById(cid):
    return ContactHandler().getContactById(cid)


@app.route('/kheApp/messaging')
def messaging():
    return 'messaging'


@app.route('/kheApp/chats')
def chats():
    return ChatHandler().getAllChats()


if __name__ == '__main__':
    app.run(debug=True)


