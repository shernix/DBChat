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
        if not request.json:
            # print('wop')
            return jsonify(Error="Missing form"), 405
        result = UserHandler().loginUser(request.json)
        if len(result) > 1:
            return jsonify(Error="Incorrect credentials"), 404
        cred = result[0]
        # print(result)
        # if len(id) > 1:
        #     return id
        if len(cred) > 0:
            session['logged_in'] = True
            id = cred[0]
            print(id)
            globallyChangeTokenId(id)
            return jsonify(id=id, user_name = cred[1])
        else:
            return jsonify(Error="Method not allowed."), 404
    return jsonify(Error="Method not allowed."), 404


@app.route("/kheApp/logout", methods=['POST'])
def logout():
    if request.method == 'POST':
        session['logged_in'] = False
        globallyChangeTokenId(-1)
        return jsonify(Success="Logout successful."), 200

    return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/register', methods=['POST'])
def register():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="Missing form"), 405
        result = UserHandler().insertUser(request.json)
        print(result)
        # print(result[0])
        # print(result[1])

        return result
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        if not request.json:
            return jsonify(Error="Missing form"), 405
        else:
            return ContactHandler().insertContact(request.json)  # 'Contact added!'
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
        if not request.json:
            return jsonify(Error="Missing form"), 405
        else:
            return jsonify(id=MessagesHandler().postMessagesByChatID(request.json, chid)), 200  # maybe eliminate the getMessageByIdpart and leave just the ID
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
        if not request.json:
            return jsonify(Error="Missing form"), 405
        else:
            return jsonify(id=MessagesHandler().postMessageReply(request.json, chid, message_id)), 200
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/kheApp/messages/replies', methods=['GET'])
def getReply():
    if request.method == 'GET':
        return MessagesHandler().getAllReplies()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/chats', methods=['GET', 'POST'])
def getChats():
    if request.method == 'POST':
        print("REQUEST: ", request.method)
        if not request.json:
            return jsonify(Error="Malformed post request (Did not include chatname)"), 400
        else:
            return ChatHandler().insertChat(request.json)  # 'Chat created!'
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
        print(request.json)

        if not request.json:
            return jsonify(Error="Malformed post request (Did not include form)"), 400
        else:
            return ChatHandler().addChatMember(chid, request.json)
    # elif request.method == 'DELETE':
    #     if not request.form:
    #         print(request.form)
    #         return jsonify(Error="Malformed post request (Did not include form)"), 400
    #     else:
    #         print('hello')
    #         return ChatHandler().deleteChatMember(chid, request.form)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/chats/<int:chid>/members/<int:cid>', methods=['DELETE'])
def deleteMemebersByChatID(chid, cid):
    if request.method == 'DELETE':
        if not cid:
            print(cid)
            return jsonify(Error="Malformed post request (Did not include form)"), 400
        else:
            print(cid)
            return ChatHandler().deleteChatMember(chid, cid)
    else:
        return jsonify(Error="Method not allowed."), 405



@app.route('/kheApp/dashboard/<stat>', methods=['GET'])
def dashboard(stat):
    if request.method == 'GET':
        return DashboardHandler().getStatistics(stat, request.form)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/dashboard/PostsPerDayByUsers/<int:id>', methods=['GET'])
def specialDashboard(id):
    if request.method == 'GET':
        return DashboardHandler().getSpecialStatistic(id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/hashtag', methods=['POST'])
def hashtag():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="Missing form"), 405
        else:
            MessagesHandler().postHashtag(request.json)
            return jsonify(Success="Hashtag updated")


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


