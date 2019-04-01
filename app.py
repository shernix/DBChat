from flask import Flask, request, jsonify
from handler.handler import ContactHandler, MessagesHandler, ChatHandler, UserHandler
#  from flask_cors import CORS, cross_origin

app = Flask(__name__)


@app.route('/')
def index():
    return 'This is the home of the messaging app'


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        return 'Login successful'
    return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # print("REQUEST: ", request.form)
        return UserHandler().insertUser(request.form)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/dashboard', methods=['GET'])
def dashboard():
    if request.method == 'GET':
        return 'statistics'
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        print("REQUEST: ", request.form)
        return ContactHandler().insertContactJson(request.form)  # 'Contact added!'
    else:
        if not request.args:
            return ContactHandler().getAllContacts()
        else:
            return ContactHandler().searchContacts(request.args)


@app.route('/kheApp/contacts/<int:cid>', methods=['GET', 'DELETE'])
def getContactByID(cid):
    if request.method == 'GET':
        return ContactHandler().getContactByID(cid)
    # elif request.method == 'PUT':
    #     return ContactHandler().updateContact(cid, request.args)  # 'Updated contact!'
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
    elif request.method == 'POST':
        return MessagesHandler().postMessagesByChatID(request.args)
    elif request.method == 'DELETE':
        return MessagesHandler().deleteMessagesByChatID(chid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/messages/like/<int:message_id>', methods=['GET', 'POST', 'DELETE'])
def messageLikes(message_id):
    if request.method == 'GET':
        return MessagesHandler().getMessageLikes(message_id)
    elif request.method == 'POST':
        return MessagesHandler().addMessageLike(message_id)  # hacer un post, no put
    elif request.method == 'DELETE':
        return MessagesHandler().deleteMessageLike(message_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/messages/dislike/<int:message_id>', methods=['GET', 'POST', 'DELETE'])
def messageDislikes(message_id):
    if request.method == 'GET':
        return MessagesHandler().getMessageDislikes(message_id)
    elif request.method == 'POST':
        return MessagesHandler().addMessageDislike(message_id)  # hacer un post, no put
    elif request.method == 'DELETE':
        return MessagesHandler().deleteMessageDislike(message_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/chats', methods=['GET', 'POST'])
def getChats():
    if request.method == 'POST':
        print("REQUEST: ", request.method)
        return ChatHandler().insertChat(request.args)  # 'Chat created!'
    else:
        if not request.args:
            return ChatHandler().getAllChats()
        else:
            return ChatHandler().searchChats(request.args)


@app.route('/kheApp/messages/reply/<int:message_id>', methods=['POST'])  # this should have a delete reply option imo
def reply(message_id):
    if request.method == 'POST':
        return 'Reply to message posted'
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/chats/<int:chid>', methods=['GET', 'PUT', 'DELETE'])
def getChatsByID(chid):
    if request.method == 'GET':
        return ChatHandler().getChatByID(chid)
    elif request.method == 'PUT':
        return ChatHandler().updateChat(chid, request.args)  # 'Updated Chat!'
    elif request.method == 'DELETE':
        return ChatHandler().deleteChat(chid)  # 'Deleted Chat!'
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/chats/<int:chid>/members', methods=['GET', 'POST', 'DELETE'])
def getChatMemebersByChatID(chid):
    if request.method == 'GET':
        return ChatHandler().getChatMembersByChatID(chid)
    elif request.method == 'POST':                                                   # CHANGED to be a post
        return ChatHandler().addChatMember(chid, request.args)
    elif request.method == 'DELETE':
        return ChatHandler().deleteChatMember(chid, request.args)
    else:
        return jsonify(Error="Method not allowed."), 405


if __name__ == '__main__':
    app.run(debug=True)


