from flask import Flask, request, jsonify
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
        print("REQUEST: ", request.method)
        return ContactHandler().insertContactJson(request.args)  # 'Contact added!'
    else:
        if not request.args:
            return ContactHandler().getAllContacts()
        else:
            return ContactHandler().searchContacts(request.args)


@app.route('/kheApp/contacts/<int:cid>', methods=['GET', 'PUT', 'DELETE'])
def getContactByID(cid):
    if request.method == 'GET':
        return ContactHandler().getContactByID(cid)
    elif request.method == 'PUT':
        return ContactHandler().updateContact(cid, request.args)  # 'Updated contact!'
    elif request.method == 'DELETE':
        return ContactHandler().deleteContact(cid)  # 'Deleted contact!'
    else:
        return jsonify(Error="Method not allowed."), 405


# #this is a route that isn't supposed to exist
# @app.route('/kheApp/messages')
# def getMessage():
#     handler = MessagesHandler()
#     return handler.getAllMessages()


@app.route('/kheApp/messages/<int:chid>', methods=['GET', 'POST', 'DELETE'])
def getMessageByChatID(chid):
    if request.method == 'GET':
        return MessagesHandler().getMessagesByChatID(chid)
    #elif request.method == 'POST':
    #    return MessagesHandler().updateMessagesByChatID(chid, request.args)  
    elif request.method == 'DELETE':
        return MessagesHandler().deleteMessagesByChatID(chid) 
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/kheApp/messages/like/<int:message_id>', methods=['GET', 'POST', 'DELETE'])
def messageLikes(message_id):
    if request.method == 'GET':
        return MessagesHandler().getMessageLikes(message_id)
    elif request.method == 'POST':
        return MessagesHandler().likeMessage(message_id)
    elif request.method == 'DELETE':
        return MessagesHandler().dislikeMessage(message_id)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/kheApp/chats', methods=['GET', 'POST'])
def getChats():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        return 'Chat created!'
    
    else:
        if not request.args:
            return ChatHandler().getAllChats()
        else:
            return ChatHandler().searchChats(request.args)


@app.route('/kheApp/chats/<int:chid>', methods=['GET', 'PUT', 'DELETE'])
def getChatsByID(chid):
    if request.method == 'GET':
        return ChatHandler().getChatByID(chid)
    elif request.method == 'PUT':
        return 'Updated Chat!'  # ChatHandler().updateChat(chid, request.form)
    elif request.method == 'DELETE':
        return 'Deleted Chat!'  # ChatHandler().deleteChat(chid)
    else:
        return jsonify(Error="Method not allowed."), 405


if __name__ == '__main__':
    app.run(debug=True)


