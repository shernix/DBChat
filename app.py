from flask import Flask, request, jsonify, session
from handler.handler import ContactHandler, MessagesHandler, ChatHandler, UserHandler, DashboardHandler
from flask_cors import CORS, cross_origin
import os
from dao.dao import globallyChangeTokenId

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'This is the home of the messaging app'


@app.route('/kheApp/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if not request.form:
            return jsonify(Error="Missing form"), 405
        id = UserHandler().loginUser(request.form)
        if len(id) > 1:
            return jsonify(Error="Missing form"), 405
        if id[0] > 0:
            session['logged_in'] = True
            globallyChangeTokenId(id[0])
            return 'Login successful'
        else:
            return 'Login unsuccessful'
    return jsonify(Error="Method not allowed."), 405


@app.route("/kheApp/logout", methods=['POST'])
def logout():
    if request.method == 'POST':
        session['logged_in'] = False
        globallyChangeTokenId(-1)
        return 'Logout successful'
    return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # print("REQUEST: ", request.form)
        return UserHandler().insertUser(request.form)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/dashboard/<stat>', methods=['GET'])
def dashboard(stat):
    if request.method == 'GET':
        return DashboardHandler().getStatistics(stat)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        print("REQUEST: ", request.form)
        if not request.form:
            return jsonify(Error="Missing form"), 405
        else:
            return ContactHandler().insertContact(request.form)  # 'Contact added!'
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
        if not request.form:
            return jsonify(Error="Missing form"), 405
        else:
            return MessagesHandler().getMessageByID(MessagesHandler().postMessagesByChatID(request.form, chid))
    # elif request.method == 'DELETE':
    #     return MessagesHandler().deleteMessagesByID(chid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/messages/like/<int:message_id>', methods=['GET', 'POST', 'DELETE'])
def messageLikes(message_id):
    if request.method == 'GET':
        return MessagesHandler().getMessageLikes(message_id)
    elif request.method == 'POST':
        return MessagesHandler().addMessageLike(message_id)  # hacer un post, no put
    elif request.method == 'DELETE':
        return MessagesHandler().deleteMessageReaction(message_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/messages/dislike/<int:message_id>', methods=['GET', 'POST', 'DELETE'])
def messageDislikes(message_id):
    if request.method == 'GET':
        return MessagesHandler().getMessageDislikes(message_id)
    elif request.method == 'POST':
        return MessagesHandler().addMessageDislike(message_id)  # hacer un post, no put
    elif request.method == 'DELETE':
        return MessagesHandler().deleteMessageReaction(message_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/messages/<int:chid>/reply/<int:message_id>', methods=['POST'])
def reply(message_id, chid):
    if request.method == 'POST':
        if not request.form:
            return jsonify(Error="Missing form"), 405
        else:
            return MessagesHandler().postMessageReply(request.form, chid, message_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/chats', methods=['GET', 'POST'])
def getChats():
    if request.method == 'POST':
        print("REQUEST: ", request.method)
        if not request.form:
            return jsonify(Error="Malformed post request (Did not include chatname)"), 400
        else:
            return ChatHandler().insertChat(request.form)  # 'Chat created!'
    else:
        if not request.form:
            return ChatHandler().getAllChats()
        else:
            return ChatHandler().searchChats(request.form)


@app.route('/kheApp/chats/<int:chid>', methods=['GET', 'PUT', 'DELETE'])
def getChatsByID(chid):
    if request.method == 'GET':
        return ChatHandler().getChatByID(chid)
    elif request.method == 'PUT':
        if not request.form:
            return jsonify(Error="Malformed post request (Did not include chatname)"), 400
        else:
            return ChatHandler().updateChat(chid, request.form)  # 'Updated Chat!'
    elif request.method == 'DELETE':
        return ChatHandler().deleteChat(chid)  # 'Deleted Chat!'
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/chats/<int:chid>/members', methods=['GET', 'POST', 'DELETE'])
def getChatMemebersByChatID(chid):
    if request.method == 'GET':
        return ChatHandler().getChatMembersByChatID(chid)
    elif request.method == 'POST':
        if not request.form:
            return jsonify(Error="Malformed post request (Did not include form)"), 400
        else:
            return ChatHandler().addChatMember(chid, request.form)
    elif request.method == 'DELETE':
        if not request.form:
            return jsonify(Error="Malformed post request (Did not include form)"), 400
        else:
            return ChatHandler().deleteChatMember(chid, request.form)
    else:
        return jsonify(Error="Method not allowed."), 405


################################################################################################
#                                         Dev Routes                                           #
################################################################################################

# @app.route('/kheApp/dev/messages/<int:chid>', methods=['GET', 'POST', 'DELETE'])

@app.route('/kheApp/dev/messages', methods=['GET'])
def getAllMessagesInSystem():
    if request.method == 'GET':
        return MessagesHandler().getAllMessages()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/dev/messages/likers/<int:message_id>', methods=['GET'])
def getAllUsersWhoLiked(message_id):
    if request.method == 'GET':
        return MessagesHandler().getAllUsersWhoLiked(message_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/dev/messages/dislikers/<int:message_id>', methods=['GET'])
def getAllUsersWhoDisliked(message_id):
    if request.method == 'GET':
        return MessagesHandler().getAllUsersWhoDisliked(message_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/dev/contacts/<int:user_id>', methods=['GET'])
def contactsOfUser(user_id):
    if request.method == 'GET':
        return ContactHandler().getAllContactsOfUser(user_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/dev/chats/<int:chid>/members', methods=['GET'])
def getChatGroupSubscribers(chid):
    if request.method == 'GET':
        return ChatHandler().getChatGroupSubscribers(chid)


@app.route('/kheApp/dev/users', methods=['GET'])
def getAllUsersInSystem():
    if request.method == 'GET':
        return UserHandler().getAllUsers()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/dev/chats', methods=['GET'])
def getChatsDev():
    if request.method == 'GET':
        return ChatHandler().getAllChatsDev()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/dev/chats/<int:chid>', methods=['GET'])
def getChatOwnerByIDDev(chid):
    if request.method == 'GET':
        return ChatHandler().getChatByIDDev(chid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/dev/user', methods=['GET'])
def getAllUsersInSystemByCredential():
    if request.method == 'GET':
        return UserHandler().getUser(request.form)
    else:
        return jsonify(Error="Method not allowed."), 405


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)


