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


@app.route('/kheApp/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        return 'contact added!'
    else:
        if not request.args:
            return ContactHandler().getAllContacts()
        else:
            return ContactHandler().searchContacts(request.args)


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


