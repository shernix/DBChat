from flask import Flask, request
from handler.handler import ContactHandler, MessagesHandler, ChatHandler


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


@app.route('/kheApp/contacts')
def contacts():
    if request.args:
        keyword = request.args['keyword']
        return ContactHandler().searchContacts(keyword)
    else:
        handler = ContactHandler()
        return handler.getAllContacts()


@app.route('/kheApp/contacts/<int:cid>')
def getContactByID(cid):
    return ContactHandler().getContactByID(cid)


# #this is a route that isn't supposed to exist
# @app.route('/kheApp/messages')
# def getMessage():
#     handler = MessagesHandler()
#     return handler.getAllMessages()


@app.route('/kheApp/messages/<int:chid>')
def getMessageByChatID(chid):
    handler = MessagesHandler()
    return handler.getMessagesByChatID(chid)


@app.route('/kheApp/chats')
def getChats():
    return ChatHandler().getAllChats()


if __name__ == '__main__':
    app.run(debug=True)


