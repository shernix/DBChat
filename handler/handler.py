from flask import jsonify, request
from dao.dao import ContactDAO, ChatDAO, MessagesDAO, UserDAO, StatisticsDao


################################################################################################
#                                        CONTACT HANDLER                                       #
################################################################################################

class ContactHandler:

    def mapToContactDict(self, row):
        result = {}
        result['cid'] = row[0]
        result['cusername'] = row[1]
        result['cfirstname'] = row[2]
        result['clastname'] = row[3]
        result['cemail'] = row[4]
        result['cphonenumber'] = row[5]
        return result

    def mapToContactAttributes(self, cid, cusername, cfirstname, clastname, cemail, cphonenumber):
        result = {}
        result['cid'] = cid
        result['cusername'] = cusername
        result['cfirstname'] = cfirstname
        result['clastname'] = clastname
        result['cemail'] = cemail
        result['cphonenumber'] = cphonenumber
        return result

    def getAllContacts(self):
        dao = ContactDAO()
        contact_list = dao.getAllContacts()
        mapped_result = []
        for r in contact_list:
            mapped_result.append(self.mapToContactDict(r))
        return jsonify(Contact=mapped_result)

    def getContactByID(self, id):
        dao = ContactDAO()
        result = dao.getContactByID(id)
        print(id)
        if result == None:
            return jsonify(Error="CONTACT NOT FOUND"), 404
        else:
            mapped = self.mapToContactDict(result)
            return jsonify(Contact=mapped)

    def searchContacts(self, args):
        if len(args) > 1:
            #print(args)
            return jsonify(Error="Malformed search string."), 400
        elif args.get("firstname"):
            keyword = args.get("firstname")
            dictIndex = 2
        elif args.get("lastname"):
            keyword = args.get("lastname")
            dictIndex = 3
        else:
            keyword = args.get("username")
            dictIndex = 1

        print(keyword)
        if keyword:
            dao = ContactDAO()
            contact_list = dao.getContactsByKeyword(keyword, dictIndex)
            result_list = []
            for row in contact_list:
                result = self.mapToContactDict(row)
                result_list.append(result)
            return jsonify(Contacts=result_list)
        else:
            return jsonify(Error="Malformed search string."), 400

    def insertContact(self, form):
        # print("form: ", form)
        if len(form) == 3:
            firstname = form['firstname']
            lastname = form['lastname']
            email = None
            phonenumber = None
            if "email" in form:
                email = form['email']
                if email == '':
                    return jsonify(Error="Malformed post request"), 400
            elif "phonenumber" in form:
                phonenumber = form['phonenumber']
                if phonenumber == '':
                    return jsonify(Error="Malformed post request"), 400
            else:
                return jsonify(Error="Malformed post request"), 400
            if firstname and lastname:
                if email:
                    user = UserDAO().getUserIDOnlyByCredentialsEmail(firstname, lastname, email)
                if phonenumber:
                    user = UserDAO().getUserIDOnlyByCredentialsPhone(firstname, lastname, phonenumber)
                if user == None:
                    return jsonify(Error="User doesn't exist"), 400
                cid = user[0]
                dao =ContactDAO()
                contact = dao.getContactByID(cid)
                if contact == None:
                    cid = dao.insert(cid)
                    return self.getContactByID(cid)
                else:
                    return jsonify(Error="Contact already exists"), 400

        if len(form) == 1:
            cid = form['id']
            user = UserDAO().getUserIDOnly(cid)
            if user == None:
                return jsonify(Error="User doesn't exist"), 400
            dao =ContactDAO()
            contact = dao.getContactByID(cid)
            if contact == None:
                cid = dao.insert(cid)
                return self.getContactByID(cid)
            else:
                return jsonify(Error="Contact already exists"), 400
        else:
            return jsonify(Error="Malformed post request"), 400


    # def updateContact(self, cid, args):
    #     dao = ContactDAO()
    #     if not dao.getContactByID(cid):
    #         return jsonify(Error="Contact not found."), 404
    #     else:
    #         cusername = args.get('cusername')
    #         cfirstname = args.get('cfirstname')
    #         clastname = args.get('clastname')
    #         cemail = args.get('cemail')
    #         cphonenumber = args.get('cphonenumber')
    #         if cemail == None:
    #             cemail = 'empty'
    #         if cphonenumber == None:
    #             cphonenumber = 'empty'
    #         if cusername and cfirstname and clastname and cemail and cphonenumber:
    #             dao.update(cid, cusername, cfirstname, clastname, cemail, cphonenumber)
    #             result = self.mapToContactAttributes(cid, cusername, cfirstname, clastname, cemail, cphonenumber)
    #             return jsonify(Contact=result), 200
    #         else:
    #             return jsonify(Error="Unexpected attributes in update request"), 400

    def deleteContact(self, cid):
        dao = ContactDAO()
        if not dao.getContactByID(cid):
            return jsonify(Error="Contact not found."), 404
        else:
            dao.delete(cid)
            return jsonify(DeleteStatus = "OK"), 200

    def getAllContactsOfUser(self, uid):
        user = UserDAO().getUserByID(uid)
        if user == None:
            return jsonify(Error="USER NOT FOUND"), 400
        dao = ContactDAO()
        contact_list = dao.getAllContactsOfUser(uid)
        mapped_result = []
        for r in contact_list:
            mapped_result.append(self.mapToContactDict(r))
        return jsonify(Contact=mapped_result)


################################################################################################
#                                         CHAT HANDLER                                         #
################################################################################################

class ChatHandler:

    def mapToChatDict(self, row):
        result = {}
        result['chid'] = row[0]
        result['chname'] = row[1]
        result['chadminid'] = row[2]
        result['chadminname'] = row[3]

        return result

    def mapToChatAttributes(self, chid, chname, chadminid, chadminname):
        result = {}
        result['chid'] = chid
        result['chname'] = chname
        result['chadminid'] = chadminid
        result['chadminname'] = chadminname

        return result
    # done
    def getAllChats(self):
        dao = ChatDAO()
        result = dao.getAllChats()
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToChatDict(r))
        return jsonify(Chat=mapped_result)
    # done
    def getChatByID(self, id):
        dao = ChatDAO()
        result = dao.getChatByID(id)
        if result == None:
            return jsonify(Error="CHAT NOT FOUND"), 404
        else:
            mapped = self.mapToChatDict(result)
            return jsonify(Chat=mapped)
    # done
    def getChatMembersByChatID(self, chid):
        dao = ChatDAO()
        result = dao.getChatByID(chid)
        members=[]
        if result == None:
            return jsonify(Error="CHAT NOT FOUND"), 404
        else:
            for x in ChatDAO().getMembers(chid):
                members.append(ContactHandler().mapToContactDict(x))
            return jsonify(members=members)
    # done
    def addChatMember(self, chid, form):
        dao = ChatDAO()
        result = dao.getChatByID(chid)

        if result == None:
            return jsonify(Error="CHAT NOT FOUND"), 404
        else:
            if "cid" in form:
                cid = form['cid']
                if cid == '':
                    return jsonify(Error="Missing contact id ('cid')"), 400
            else:
                return jsonify(Error="Malformed post request (Did not include contact id ('cid'))"), 400
            contact = form['cid']
            if dao.isContactInChat(chid, contact):
                return jsonify(Error="Contact is already in chat"), 400
            else:
                return ContactHandler().getContactByID(dao.insertMember(chid, contact))
    # done
    def deleteChatMember(self, chid, cid):
        print(cid)
        dao = ChatDAO()
        result = dao.getChatByID(chid)

        contact = cid
        print(dao.isContactInChat(chid, contact))
        if result == None:
            return jsonify(Error="CHAT NOT FOUND"), 404
        elif dao.validateAdmin(chid) == None:
            return jsonify(Error="You are not the admin of the chat!"), 400
        else:
            if len(dao.isContactInChat(chid, contact)) < 1:
                return jsonify(Error="Contact is not in chat"), 400
            else:
                return ContactHandler().getContactByID(dao.deleteMember(chid, contact))

    # done
    def searchChats(self, form):
        if len(form) > 1:
            print(form)
            return jsonify(Error="Malformed search string."), 400
        chatname = form["chatname"]
        # print(chatname)
        if chatname:
            dao = ChatDAO()
            chat_list = dao.getChatsByChatName(chatname)
            result_list = []
            for row in chat_list:
                result = self.mapToChatDict(row)
                result_list.append(result)
            return jsonify(Chats=result_list)
        else:
            return jsonify(Error="Malformed search string."), 400
    # done
    def insertChat(self, form):
        print(form)
        if form == None:
            return jsonify(Error="Malformed search string."), 400
        if "chatname" in form:
            chatname = form['chatname']
            if chatname == '':
                return jsonify(Error="Missing chatname"), 400
        else:
            return jsonify(Error="Malformed post request (Did not include chatname)"), 400
        # chname = form['chatname']
        dao = ChatDAO()
        chid = dao.insert(chatname)
        chat = dao.getChatByID(chid)
        result = self.mapToChatAttributes(chat[0], chat[1], chat[2], chat[3])
        return jsonify(Chat=result), 201

    # done
    def updateChat(self, chid, form):
        dao = ChatDAO()
        if not dao.getChatByID(chid):
            return jsonify(Error="Chat not found."), 404

        if form == None:
            return jsonify(Error="Malformed search string."), 400

        if dao.validateAdmin(chid) == None:
            return jsonify(Error="You are not the admin of the chat!"), 400

        chatname = form['chatname']
        chid = dao.update(chid, chatname)
        chat = dao.getChatByID(chid)
        result = self.mapToChatAttributes(chat[0], chat[1], chat[2], chat[3])
        return jsonify(Chat=result), 200

    # done
    def deleteChat(self, chid):
        dao = ChatDAO()
        print(chid)
        if not dao.getChatByID(chid):
            return jsonify(Error="Chat not found."), 404
        if dao.validateAdmin(chid) == None:
            return jsonify(Error="You are not the admin of the chat!"), 400
        else:
            members = dao.getMembers(chid)
            print(members)
            for member in members:
                print(member[0])
                dao.deleteMember(chid, member[0])
            dao.delete(chid)
            return jsonify(DeleteStatus = "OK"), 200

    def getChatGroupSubscribers(self, chid):
        dao = ChatDAO()
        result = dao.getAllChatSubscribers(chid)
        print(result)
        members=[]
        if result == None:
            return jsonify(Error="CHAT NOT FOUND"), 404
        else:
            dao = UserDAO()
            for x in result:
                user = dao.getUserByID(x[0])
                members.append(UserHandler().mapToUserDict(user))
            return jsonify(members=members)

    def getAllChatsDev(self):
        dao = ChatDAO()
        result = dao.getAllChatsDev()
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToChatDict(r))
        return jsonify(Chat=mapped_result)

    def getChatByIDDev(self, id):
        dao = ChatDAO()
        result = dao.getChatByIDDev(id)
        if result == None:
            return jsonify(Error="CHAT DOES NOT EXIST"), 404
        else:
            mapped = self.mapToChatDict(result)
            return jsonify(Chat=mapped)


################################################################################################
#                                       MESSAGES HANDLER                                       #
################################################################################################

class MessagesHandler:

    def mapToMessagesDict(self, row):
        result = {}
        result['chid'] = row[0]
        result['message'] = row[1]
        result['user_id'] = row[2]
        result['time_stamp'] = row[3]
        result['message_id'] = row[4]
        result['likes'] = row[5]
        result['dislikes'] = row[6]
        result['media'] = row[7]
        result['username'] = row[8]
        result['liked']='true'
        result['disliked']='true'
        result['reply'] = row[9]
        return result

    def mapToRepliesDict(self, row):
        result = {}
        result['original'] = row[0]
        result['reply'] = row[1]
        return result

    def mapToMessageAttributes(self, chid, message, user_id, timestamp, message_id, likes, dislikes, media, username, reply):
        result = {}
        result['chid'] = chid
        result['message'] = message
        result['user_id'] = user_id
        result['time_stamp'] = timestamp
        result['message_id'] = message_id
        result['likes'] = likes
        result['dislikes'] = dislikes
        result['media'] = media
        result['username'] = username
        result['reply'] = reply
        return result

    # this is only used for getting the users who liked a message so it includes a time_stamp
    def mapToUserReactWithTimestamp(self, row):
        result = {}
        result['cid'] = row[0]
        result['cusername'] = row[1]
        result['cfirstname'] = row[2]
        result['clastname'] = row[3]
        result['cemail'] = row[4]
        result['cphonenumber'] = row[5]
        result['time_stamp'] = row[6]
        return result
    # done DEV
    def getAllMessages(self):
        dao = MessagesDAO()
        result = dao.getAllMessages()
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToMessagesDict(r))
        return jsonify(Messages=mapped_result)
    # done
    def getMessagesByChatID(self, id):

        chat = ChatDAO().getChatByID(id)
        if chat == None:
            return jsonify(Error="CHAT NOT FOUND"), 403

        dao = MessagesDAO()
        result = dao.getMessagesByChatID(id)
        mapped_result = []
        if result == None:
            return jsonify(Error="MESSAGE NOT FOUND"), 404
        # chat = ChatDAO().getChatByID(id)                      # comment these 3 lines to toggle dev ability
        # if chat == None:
        #     return jsonify(Error="CHAT NOT FOUND"), 404
        else:
            for r in result:
                mapped_result.append(self.mapToMessagesDict(r))
            return jsonify(Messages=mapped_result)
    # done
    def postMessagesByChatID(self, form, chid):
        # cid = json['cid']
        # chid = form['chid']

        if form == None:
            return jsonify(Error="Malformed post request"), 400

        # if password is not in form or is empty
        if "message" in form:
            message = form['message']
            if message == '':
                return jsonify(Error="Missing message"), 400
        else:
            return jsonify(Error="Malformed post request"), 400

        # verify if email is not in form or left blank
        if "media" in form:
            media = form['media']
            if media == '':
                media = ' '
        else:
            media = ' '

        if message == ' ' and media == ' ':
            return jsonify(Error="Missing message or media"), 400
        if (media == ' '):
            dao = MessagesDAO()
            message_id = dao.insertWithoutMedia(chid, message)
            # result = self.getMessageByID(message_id)
            return message_id
        else:
            dao = MessagesDAO()
            media_id = dao.insertMedia(media)
            message_id = dao.insert(chid, message, media_id)
            # result = self.getMessageByID(message_id)
            return message_id
        # return jsonify(Error="Unexpected attributes in post request"), 400
    # done
    def postMessageReply(self, form, chid, original):
        print(form)
        message_id = self.postMessagesByChatID(form, chid)
        print(message_id)
        dao = MessagesDAO()
        result = dao.reply(original, message_id)
        # result = self.getMessageByID(message_id)
        return result

    # def deleteMessagesByChatID(self, cid):
    #     dao = MessagesDAO()
    #     if not dao.getMessagesByChatID(cid):
    #         return jsonify(Error="Messages not found."), 404
    #     else:
    #         dao.delete(cid)
    #         return jsonify(DeleteStatus = "OK"), 200
    #
    # def deleteMessagesByID(self, message_id):
    #     dao = MessagesDAO()
    #     if not dao.getMessagesByChatID(message_id):
    #         return jsonify(Error="Messages not found."), 404
    #     else:
    #         dao.delete(message_id)
    #         return jsonify(DeleteStatus = "OK"), 200
    # done
    def getMessageByID(self, id):
        dao = MessagesDAO()
        result = dao.getMessageByID(id)
        if result == None:
            return jsonify(Error="MESSAGE NOT FOUND"), 404
        else:
            mapped = self.mapToMessagesDict(result)
            return jsonify(Message=mapped)
    # done
    def getMessageLikes(self, message_id):
        dao = MessagesDAO()
        if not dao.getMessageByID(message_id):
            return jsonify(Error="Message not found."), 404
        else:
            likes = dao.getMessageLikes(message_id)
            result = {}
            result['message_id'] = likes[0]
            result['likes'] = likes[1]
            print(result)
            return jsonify(Likes=result)
    # done
    def getMessageDislikes(self, message_id):
        dao = MessagesDAO()
        if not dao.getMessageByID(message_id):
            return jsonify(Error="Message not found."), 404
        else:
            dislikes = dao.getMessageDislikes(message_id)
            result = {}
            result['message_id'] = dislikes[0]
            result['dislikes'] = dislikes[1]
            print(result)
            return jsonify(Disikes=result)
    # done
    def addMessageLike(self, message_id):
        dao = MessagesDAO()
        if not dao.getMessageByID(message_id):
            return jsonify(Error="Message not found."), 404
        # elif dao.validateReaction(message_id) != None:
        #     return jsonify(Error="You already reacted."), 404
        else:
            MessagesHandler().deleteMessageReaction(message_id)
            dao.addLike(message_id)
            return jsonify(Status = "Message Like Added"), 200
    # done
    def addMessageDislike(self, message_id):
        dao = MessagesDAO()
        if not dao.getMessageByID(message_id):
            return jsonify(Error="Message not found."), 404
        # elif dao.validateReaction(message_id) != None:
        #     return jsonify(Error="You already reacted."), 404
        else:
            MessagesHandler().deleteMessageReaction(message_id)
            dao.addDislike(message_id)
            return jsonify(Status = "Message Dislike Added"), 200
    # done
    def deleteMessageReaction(self, message_id):
        dao = MessagesDAO()
        if not dao.getMessageByID(message_id):
            return jsonify(Error="Message not found."), 404
        elif dao.validateReaction(message_id) == None:
            return jsonify(Error="You haven't reacted."), 404
        else:
            dao.deleteReaction(message_id)
            return jsonify(DeleteStatus = "Message Reaction Deleted"), 200


    # def deleteMessageDislike(self, message_id):
    #     dao = MessagesDAO()
    #     if not dao.getMessageByID(message_id):
    #         return jsonify(Error="Message not found."), 404
    #     else:
    #         dao.deleteDislike(message_id)
    #         return jsonify(DeleteStatus = "Message Dislike Deleted"), 200
    # done
    def getAllUsersWhoLiked(self, message_id):
        dao = MessagesDAO()
        if not dao.getMessageByID(message_id):
            return jsonify(Error="Message not found."), 404
        else:
            list = dao.getAllUsersWhoLiked(message_id)
            mapped_result = []
            for r in list:
                mapped_result.append(self.mapToUserReactWithTimestamp(r))
            return jsonify(Likers=mapped_result)
    # done
    def getAllUsersWhoDisliked(self, message_id):
        dao = MessagesDAO()
        if not dao.getMessageByID(message_id):
            return jsonify(Error="Message not found."), 404
        else:
            list = dao.getAllUsersWhoDisliked(message_id)
            mapped_result = []
            for r in list:
                mapped_result.append(self.mapToUserReactWithTimestamp(r))
            return jsonify(Dislikers=mapped_result)

    def postHashtag(self, form):
        if form == None:
            return jsonify(Error="Malformed post request"), 400

        # if hashtag is empty
        if "hashtag" in form:
            hashtag = form['hashtag']
            if hashtag == '':
                return jsonify(Error="Missing hashtag"), 400
        else:
            return jsonify(Error="Malformed post request"), 400

        # if hashtag is empty
        if "id" in form:
            id = form['id']
            if id == '':
                return jsonify(Error="Missing id"), 400
        else:
            return jsonify(Error="Malformed post request"), 400
        dao = MessagesDAO()
        if dao.validateHashtag(hashtag) == None:
            hashtagId = dao.insertHashtag(hashtag)
        else:
            hashtagId = dao.validateHashtag(hashtag)
        dao.addHashtagToMsgId(id, hashtagId)
        return jsonify(Status = "Message Hashtag Added"), 200

    def getAllReplies(self):
        dao = MessagesDAO()
        result = dao.getAllReplies()
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToRepliesDict(r))
        return jsonify(Messages=mapped_result)


################################################################################################
#                                         USER HANDLER                                         #
################################################################################################

class UserHandler:

    def mapToUserDict(self, row):
        result = {}
        result['uid'] = row[0]
        result['username'] = row[1]
        result['firstname'] = row[2]
        result['lastname'] = row[3]
        result['email'] = row[4]
        result['phonenumber'] = row[5]
        result['password'] = row[6]
        return result

    def mapToUserAttributes(self, uid, username, firstname, lastname, email, phonenumber, password):
        result = {}
        result['uid'] = uid
        result['username'] = username
        result['firstname'] = firstname
        result['lastname'] = lastname
        result['email'] = email
        result['phonenumber'] = phonenumber
        result['password'] = password
        return result

    def loginUser(self, form):
        print(form)
        if form == None:
            return jsonify(Error="Malformed post request"), 400

        # if password is not in form or is empty
        if "password" in form:
            password = form['password']
            if password == '':
                return jsonify(Error="Missing password"), 400
        else:
            return jsonify(Error="Malformed post request (Did not include password)"), 400

        # verify if email is not in form or left blank
        if "email" in form:
            email = form['email']
            if email == '':
                email = ' '
        else:
            email = ' '
        if "phonenumber" in form:
            phonenumber = form['phonenumber']
            if phonenumber == '':
                phonenumber = ' '
        else:
            phonenumber = ' '
        if email == ' ' and phonenumber == ' ':
            return jsonify(Error="Missing email or phone"), 400
        dao = UserDAO()
        print(password)

        if dao.loginByEmail(password, email) != None:
            print(dao.loginByEmail(password, email)[0])
            return [dao.loginByEmail(password, email)]
        if dao.loginByPhone(password, phonenumber) != None:
            return [dao.loginByPhone(password, phonenumber)[0]]
        return jsonify(Error="Incorrect Credentials"), 404

    def getAllUsers(self):
        dao = UserDAO()
        user_list = dao.getAllUsers()
        mapped_result = []
        for r in user_list:
            mapped_result.append(self.mapToUserDict(r))
        return jsonify(User=mapped_result)

    def getUserByUserID(self, uid):
        dao = UserDAO()
        user = dao.getUserByID(uid)
        if user == None:
            return jsonify(Error="USER NOT FOUND"), 400
        else:
            mapped = self.mapToUserDict(user)
            return jsonify(User=mapped)

    def getUser(self, form):
        if form == None:
            return jsonify(Error="Malformed post request"), 400
        if "user_id" in form:
            user_id = form['user_id']
            if user_id == '':
                user_id = ' '
        else:
            user_id = ' '
        if "username" in form:
            username = form['username']
            if username == '':
                username = ' '
        else:
            username = ' '
        if user_id == ' ' and username == ' ':
            return jsonify(Error="Missing email or phone"), 400

        if username != ' ':
            dao = UserDAO()
            user_list = dao.getAllUsersByUsername(username)
            mapped_result = []
            print(user_list)
            for r in user_list:
                user = dao.getUserByID(r)
                mapped_result.append(self.mapToUserDict(user))
            return jsonify(User=mapped_result)

        if user_id != ' ':
            return self.getUserByUserID(user_id)
        else:
            return jsonify(Error="Malformed post request"), 400


    def insertUser(self, form):
        print(form)
        print('end json')
        # print("form: ", form)
        if form == None:
            return jsonify(Error="Malformed post request"), 400

        # if password is not in form or is empty
        if "password" in form:
            password = form['password']
            if password == '':
                return jsonify(Error="Missing password"), 400
        else:
            return jsonify(Error="Malformed post request"), 400

        # if username is not in form or is empty
        if "username" in form:
            username = form['username']
            if username == '':
                return jsonify(Error="Missing username"), 400
        else:
            return jsonify(Error="Malformed post request"), 400

        # if firstname is not in form or is empty
        if "firstname" in form:
            firstname = form['firstname']
            if firstname == '':
                return jsonify(Error="Missing firstname"), 400
        else:
            return jsonify(Error="Malformed post request"), 400

        # if lastname is not in form or is empty
        if "lastname" in form:
            lastname = form['lastname']
            if lastname == '':
                return jsonify(Error="Missing lastname"), 400
        else:
            return jsonify(Error="Malformed post request"), 400

        # verify if email is not in form or left blank
        if "email" in form:
            email = form['email']
            if email == '':
                email = ' '
        else:
            email = ' '
        if "phonenumber" in form:
            phonenumber = form['phonenumber']
            if phonenumber == '':
                phonenumber = ' '
        else:
            phonenumber = ' '
        if email == ' ' and phonenumber == ' ':
            return jsonify(Error="Missing email or phone"), 400

        # Validate email or phonenumber entered at registration
        if email != ' ':
            if UserDAO().validateEmail(email) != None:
                return jsonify(Error="email taken"), 403
        if phonenumber != ' ':
            if UserDAO().validatePhone(phonenumber) != None:
                return jsonify(Error="phonenumber taken"), 403
        # OPTIONAL
        # verify username is not taken
        # if UserDAO().validateUsername(username) != None:
        #     return jsonify(Error="Username taken"), 400

        if password and username and firstname and lastname:
            dao = UserDAO()
            uid = dao.insert(username, firstname, lastname, email, phonenumber, password)
            return self.getUserByUserID(uid)


################################################################################################
#                                        DASHBOARD HANDLER                                     #
################################################################################################

class DashboardHandler:

    def mapToTrendingTopicsDict(self, position, row):
        result = {}
        result['hashtag'] = row[0]
        result['position'] = position
        return result

    def mapToMessageRepliesDict(self, row):
        result = {}
        result['media'] = row[0]
        result['replies'] = row[1]
        return result

    def mapToMessageLikesDict(self, row):
        result = {}
        result['media'] = row[0]
        result['likes'] = row[1]
        return result

    def mapToMessageDislikesDict(self, row):
        result = {}
        result['media'] = row[0]
        result['dislikes'] = row[1]
        return result

    def mapToDailyPostsDict(self, row):
        result = {}
        result['day'] = (row[0].strftime("%Y"), row[0].strftime("%m"), row[0].strftime("%d"))
        result['total'] = row[1]
        print(result)
        return result

    def mapToActiveUsersDict(self, row):
        result = {}
        result['day'] = (row[0].strftime("%Y"), row[0].strftime("%m"), row[0].strftime("%d"))
        result['user'] = row[1]
        result['count'] = row[2]
        return result

    def getStatistics(self, stat, form):
        dao = StatisticsDao()
        if stat == 'TrendingTopics':
            result = dao.getTrendingTopics()
            mapped_result = []
            i = 1
            for r in result:
                mapped_result.append(self.mapToTrendingTopicsDict(i, r))
                i = i + 1
            return jsonify(TrendingTopics = mapped_result)
        if stat == 'NumberOfDailyPosts':
            result = dao.getDailyPosts()
            mapped_result = []
            for r in result:
                mapped_result.append(self.mapToDailyPostsDict(r))
            return jsonify(DailyPosts=mapped_result)
        if stat == 'NumberOfDailyReplies':
            result = dao.getDailyReplies()
            mapped_result = []
            for r in result:
                mapped_result.append(self.mapToDailyPostsDict(r))
            return jsonify(DailyReplies=mapped_result)
        if stat == 'NumberOfDailyLikes':
            result = dao.getDailyLikes()
            mapped_result = []
            for r in result:
                mapped_result.append(self.mapToDailyPostsDict(r))
            return jsonify(DailyLikes=mapped_result)
        if stat == 'NumberOfDailyDislikes':
            result = dao.getDailyDislikes()
            mapped_result = []
            for r in result:
                mapped_result.append(self.mapToDailyPostsDict(r))
            return jsonify(DailyDislikes=mapped_result)
        if stat == 'MostActiveUsersPerDay':
            result = dao.getMostActiveUsersPerDay()
            mapped_result = []
            dailybest = result[0]
            reslen = len(result)
            # print(dailybest)
            # print(result[reslen - 1])
            for r in result:
                if dailybest[0] == r[0]:
                    if dailybest[2] < r[2]:
                        dailybest = r
                else:
                    mapped_result.append(self.mapToActiveUsersDict(dailybest))
                    dailybest = r
            if dailybest[0] == result[reslen - 1]:
                if dailybest[2] < result[reslen-1][2]:
                    dailybest = result[reslen-1]
            else:
                mapped_result.append(self.mapToActiveUsersDict(dailybest))
            return jsonify(ActiveUsers=mapped_result)

        # if stat == 'PostsPerDay':
        #     id = form['user_id']
        #     result = dao.getPostsPerDayByUser(id)
        #     mapped_result = []
        #     for r in result:
        #         mapped_result.append(self.mapToActiveUsersDict(r))
        #     return jsonify(TotalPostsPerDayByUser=mapped_result)

        if stat == 'RepliesToAPhoto':
            result = dao.getRepliesToAPhoto()
            mapped_result = []
            for r in result:
                mapped_result.append(self.mapToMessageRepliesDict(r))
            return jsonify(RepliesToAPhoto=mapped_result)
        if stat == 'LikesToAPhoto':
            result = dao.getLikesToAPhoto()
            mapped_result = []
            for r in result:
                mapped_result.append(self.mapToMessageLikesDict(r))
            return jsonify(LikesToAPhoto=mapped_result)
        if stat == 'DislikesToAPhoto':
            result = dao.getDislikesToAPhoto()
            mapped_result = []
            for r in result:
                mapped_result.append(self.mapToMessageDislikesDict(r))
            return jsonify(DislikesToAPhoto=mapped_result)
        if stat == 'LDRToAPhoto':
            result = dao.getLDRToAPhoto()
            mapped_result = []
            for r in result:
                mapped_result.append(self.mapToSpecialStatDict(r))
            return jsonify(SpecialStats=mapped_result)
        else:
            return jsonify(Error="Malformed search string."), 400



    def mapToSpecialStatDict(self, row):
        result = {}
        if row[0] == None:
            result['media'] = 0
        else:
            result['media'] = row[0]

        if row[1] == None:
            result['likes'] = 0
        else:
            result['likes'] = row[1]

        if row[2] == None:
            result['dislikes'] = 0
        else:
            result['dislikes'] = row[2]

        if row[3] == None:
            result['replies'] = 0
        else:
            result['replies'] = row[3]
        return result

    def getSpecialStatistic(self, id):
        dao = StatisticsDao()
        result = dao.getPostsPerDayByUser(id)
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToActiveUsersDict(r))
        return jsonify(TotalPostsPerDayByUser=mapped_result)






