from flask import Flask, request, jsonify, session
from handler.handler import ContactHandler, MessagesHandler, ChatHandler, UserHandler, DashboardHandler
from flask_cors import CORS, cross_origin
import os
from dao.dao import globallyChangeTokenId


loggedInTokens = []


def saveTken(dict):
    loggedInTokens.append(dict)
    # print(loggedInTokens)


def getId(rngToken):
    for t in loggedInTokens:
        if t['rngToken'] == rngToken:
            print(t['id'])
            return t['id']
    return -1

def removeId(rngToken):
    for t in loggedInTokens:
        if t['rngToken'] == rngToken:
            # print(t['id'])
            loggedInTokens.remove(t)
            print(loggedInTokens)
            return -1
    return -1


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
            # print(id)
            # globallyChangeTokenId(id)
            dict = UserHandler().generateToken(id)
            saveTken(dict)
            # print(dict['rngToken'])
            return jsonify(id=id, user_name=cred[1], rngToken=dict['rngToken'])
        else:
            return jsonify(Error="Method not allowed."), 404
    return jsonify(Error="Method not allowed."), 404


@app.route("/kheApp/logout/<int:rngToken>", methods=['POST'])
def logout(rngToken):
    if request.method == 'POST':
        session['logged_in'] = False
        # globallyChangeTokenId(-1)
        removeId(rngToken)
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


@app.route('/kheApp/<int:rngToken>/contacts', methods=['GET', 'POST'])
def contacts(rngToken):
    id = getId(rngToken)
    if request.method == 'POST':
        print("REQUEST: ", request.json)
        if not request.json:
            return jsonify(Error="Missing form"), 405
        else:
            return ContactHandler().insertContact(id, request.json)  # 'Contact added!'
    else:
        if not request.args:
            return ContactHandler().getAllContacts(id)
        else:
            return ContactHandler().searchContacts(request.args)


@app.route('/kheApp/<int:rngToken>/contacts/<int:cid>', methods=['GET', 'DELETE'])
def getContactByID(rngToken, cid):
    id = getId(rngToken)
    if request.method == 'GET':
        return ContactHandler().getContactByID(cid)
    # elif request.method == 'PUT':
    #     return ContactHandler().updateContact(cid, request.args)  # 'Updated contact!'
    elif request.method == 'DELETE':
        return ContactHandler().deleteContact(id, cid)  # 'Deleted contact!'
    else:
        return jsonify(Error="Method not allowed."), 405


# #this is a route that isn't supposed to exist
# @app.route('/kheApp/messages')
# def getMessage():
#     handler = MessagesHandler()
#     return handler.getAllMessages()


@app.route('/kheApp/<int:rngToken>/messages/<int:chid>', methods=['GET', 'POST', 'DELETE'])
def getMessageByChatID(rngToken, chid):
    id = getId(rngToken)
    if request.method == 'GET':
        return MessagesHandler().getMessagesByChatID(id, chid)
    elif request.method == 'POST':
        if not request.json:
            return jsonify(Error="Missing form"), 405
        else:
            return jsonify(id=MessagesHandler().postMessagesByChatID(id, request.json, chid)), 200  # maybe eliminate the getMessageByIdpart and leave just the ID
    # elif request.method == 'DELETE':
    #     return MessagesHandler().deleteMessagesByID(chid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/<int:rngToken>/messages/like/<int:message_id>', methods=['GET', 'POST', 'DELETE'])
def messageLikes(rngToken, message_id):
    id = getId(rngToken)
    if request.method == 'GET':
        return MessagesHandler().getMessageLikes(message_id)
    elif request.method == 'POST':
        return MessagesHandler().addMessageLike(id, message_id)  # hacer un post, no put
    elif request.method == 'DELETE':
        return MessagesHandler().deleteMessageReaction(message_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/<int:rngToken>/messages/dislike/<int:message_id>', methods=['GET', 'POST', 'DELETE'])
def messageDislikes(rngToken, message_id):
    id = getId(rngToken)
    if request.method == 'GET':
        return MessagesHandler().getMessageDislikes(message_id)
    elif request.method == 'POST':
        return MessagesHandler().addMessageDislike(id, message_id)  # hacer un post, no put
    elif request.method == 'DELETE':
        return MessagesHandler().deleteMessageReaction(message_id)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/<int:rngToken>/messages/<int:chid>/reply/<int:message_id>', methods=['POST'])
def reply(rngToken, message_id, chid):
    id = getId(rngToken)
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="Missing form"), 405
        else:
            return jsonify(id=MessagesHandler().postMessageReply(id, request.json, chid, message_id)), 200
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route('/kheApp/messages/replies', methods=['GET'])
def getReply():
    if request.method == 'GET':
        return MessagesHandler().getAllReplies()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/<int:rngToken>/chats', methods=['GET', 'POST'])
def getChats(rngToken):
    id = getId(rngToken)
    if request.method == 'POST':
        print("REQUEST: ", request.method)
        # print(request.json)
        if not request.json:
            return jsonify(Error="Malformed post request (Did not include chatname)"), 400
        else:
            return ChatHandler().insertChat(id, request.json)  # 'Chat created!'
    elif request.method == 'GET':
        # if not request.form:
            # print("id: ")
            # print(id)
            return ChatHandler().getAllChats(id)
        # else:
        #     return ChatHandler().searchChats(request.form)
    else:
        return jsonify(Error="Method not allowed."), 405



@app.route('/kheApp/<int:rngToken>/chats/<int:chid>', methods=['GET', 'PUT', 'DELETE'])
def getChatsByID(rngToken, chid):
    id = getId(rngToken)
    if request.method == 'GET':
        return ChatHandler().getChatByID(chid)
    elif request.method == 'PUT':
        if not request.form:
            return jsonify(Error="Malformed post request (Did not include chatname)"), 400
        else:
            return ChatHandler().updateChat(chid, request.form)  # 'Updated Chat!'
    elif request.method == 'DELETE':
        return ChatHandler().deleteChat(id, chid)  # 'Deleted Chat!'
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/<int:rngToken>/chats/<int:chid>/members', methods=['GET', 'POST', 'DELETE'])
def getChatMemebersByChatID(chid, rngToken):
    id = getId(rngToken)
    if request.method == 'GET':
        return ChatHandler().getChatMembersByChatID(id, chid)
    elif request.method == 'POST':
        print(request.json)

        if not request.json:
            return jsonify(Error="Malformed post request (Did not include form)"), 400
        else:
            return ChatHandler().addChatMember(id, chid, request.json)
    # elif request.method == 'DELETE':
    #     if not request.form:
    #         print(request.form)
    #         return jsonify(Error="Malformed post request (Did not include form)"), 400
    #     else:
    #         print('hello')
    #         return ChatHandler().deleteChatMember(chid, request.form)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route('/kheApp/<int:rngToken>/chats/<int:chid>/members/<int:cid>', methods=['DELETE'])
def deleteMemebersByChatID(rngToken, chid, cid):
    id = getId(rngToken)
    if request.method == 'DELETE':
        if not cid:
            print(cid)
            return jsonify(Error="Malformed post request (Did not include form)"), 400
        else:
            print(cid)
            return ChatHandler().deleteChatMember(id, chid, cid)
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





