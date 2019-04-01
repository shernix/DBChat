from flask import jsonify, request
from dao.dao import ContactDAO, ChatDAO, MessagesDAO, UserDAO


################################################################################################
#                                         CONTACT HANDLER                                      #
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


################################################################################################
#                                         CHAT HANDLER                                         #
################################################################################################

class ChatHandler:

    def mapToChatDict(self, row):
        result = {}
        result['chid'] = row[0]
        result['chname'] = row[1]
        result['chadminid'] = row[2]

        return result

    def mapToChatAttributes(self, chid, chname, chadminid):
        result = {}
        result['chid'] = chid
        result['chname'] = chname
        result['chadminid'] = chadminid

        return result

    def getAllChats(self):
        dao = ChatDAO()
        result = dao.getAllChats()
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToChatDict(r))
        return jsonify(Chat=mapped_result)

    def getChatByID(self, id):
        dao = ChatDAO()
        result = dao.getChatByID(id)
        if result == None:
            return jsonify(Error="CHAT NOT FOUND"), 404
        else:
            mapped = self.mapToChatDict(result)
            return jsonify(Chat=mapped)

    def getChatMembersByChatID(self, chid):
        dao = ChatDAO()
        result = dao.getChatByID(chid)
        if result == None:
            return jsonify(Error="CHAT NOT FOUND"), 404
        else:
            members = ChatDAO().getMembers(chid)
            return jsonify(members=members)

    def addChatMember(self, chid, args):
        dao = ChatDAO()
        result = dao.getChatByID(chid)
        if result == None:
            return jsonify(Error="CHAT NOT FOUND"), 404
        else:
            members = self.getChatMembersByChatID(chid)
            mapped = []
            for r in members.json['members']:
                mapped.append(r)
            if not mapped.__contains__(args.get('members')):
                mapped.append(args.get('members'))
            print(mapped)
            return jsonify(members=mapped)

    def deleteChatMember(self, chid, args):
        dao = ChatDAO()
        result = dao.getChatByID(chid)
        if result == None:
            return jsonify(Error="CHAT NOT FOUND"), 404
        else:
            members = self.getChatMembersByChatID(chid)
            mapped = []
            for r in members.json['members']:
                mapped.append(r)
            if mapped.__contains__(args.get('members')):
                mapped.remove(args.get('members'))
            print(mapped)
            return jsonify(members=mapped)


    def searchChats(self, args):
        if len(args) > 1:
            #print(args)
            return jsonify(Error="Malformed search string."), 400
        chatname = args.get("chatname")
        print(chatname)
        if chatname:
            dao = ChatDAO()
            chat_list = dao.getChatsByChatName(chatname)
            result_list = []
            for row in chat_list:
                result = self.mapToChatDict(row)
                result_list.append(result)
            return jsonify(Chas=result_list)
        else:
            return jsonify(Error="Malformed search string."), 400

    def insertChat(self, args):
        chname = args.get('chname')
        chadminid = 1  # args.get('chadminid')
        if chname and chadminid:
            dao = ChatDAO()
            chid = dao.insert(chname, chadminid)
            result = self.mapToChatAttributes(chid, chname, chadminid)
            return jsonify(Chat=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def updateChat(self, chid, args):
        dao = ChatDAO()
        if not dao.getChatByID(chid):
            return jsonify(Error="Chat not found."), 404
        else:
            chname = args.get('chname')
            chadminid = 1  # placeholder
            if chname and chadminid:
                dao.update(chid, chname, chadminid)
                result = self.mapToChatAttributes(chid, chname, chadminid)
                return jsonify(Chat=result), 200
            else:
                return jsonify(Error="Unexpected attributes in update request"), 400

    def deleteChat(self, chid):
        dao = ChatDAO()
        if not dao.getChatByID(chid):
            return jsonify(Error="Chat not found."), 404
        else:
            dao.delete(chid)
            return jsonify(DeleteStatus = "OK"), 200


################################################################################################
#                                        MESSAGES HANDLER                                      #
################################################################################################

class MessagesHandler:

    def mapToMessagesDict(self, row):
        result = {}
        result['chid'] = row[0]
        result['message'] = row[1]
        result['user_id'] = row[2]
        result['timestamp'] = row[3]
        result['message_id'] = row[4]
        result['likes'] = row[5]
        result['dislikes'] = row[6]
        result['image'] = row[7]
        return result

    def mapToMessageAttributes(self, chid, message, user_id, timestamp, message_id, likes, dislikes, image):
        result = {}
        result['chid'] = chid
        result['message'] = message
        result['user_id'] = user_id
        result['timestamp'] = timestamp
        result['message_id'] = message_id
        result['likes'] = likes
        result['dislikes'] = dislikes
        result['image'] = image
        return result

    def getAllMessages(self):
        dao = MessagesDAO()
        result = dao.getAllMessages()
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToMessagesDict(r))
        return jsonify(Messages=mapped_result)

    def getMessagesByChatID(self, id):
        dao = MessagesDAO()
        result = dao.getMessagesByChatID(id)
        mapped_result = []
        if result == None:
            return jsonify(Error="MESSAGE NOT FOUND"), 404
        else:
            for r in result:
                mapped_result.append(self.mapToMessagesDict(r))
            return jsonify(Messages=mapped_result)

    def postMessagesByChatID(self, args):
        # cid = json['cid']
        chid = args.get('chid')
        message = args.get('message')
        user_id = args.get('user_id')
        timestamp = args.get('timestamp')
        likes = args.get('likes')
        dislikes = args.get('dislikes')
        image = args.get('image')
        
        if message == None:
                message = ' '
        if image == None:
                image = ' '

        if chid and message and user_id and timestamp and likes and dislikes and image:
            dao = MessagesDAO()
            message_id = dao.insert(chid, message, user_id, timestamp, likes, dislikes, image)
            result = self.mapToMessageAttributes(chid, message, user_id, timestamp, message_id, likes, dislikes, image)
            return jsonify(Contact=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def deleteMessagesByChatID(self, cid):
        dao = MessagesDAO()
        if not dao.getMessagesByChatID(cid):
            return jsonify(Error="Messages not found."), 404
        else:
            dao.delete(cid)
            return jsonify(DeleteStatus = "OK"), 200
    
    def deleteMessagesByID(self, cid):
        dao = MessagesDAO()
        if not dao.getMessagesByChatID(cid):
            return jsonify(Error="Messages not found."), 404
        else:
            dao.delete(cid)
            return jsonify(DeleteStatus = "OK"), 200

    def getMessageByID(self, id):
        dao = MessagesDAO()
        result = dao.getMessageByID(id)
        if result == None:
            return jsonify(Error="MESSAGE NOT FOUND"), 404
        else:
            mapped = self.mapToMessagesDict(result)
            return jsonify(Message=mapped)

    def getMessageLikes(self, message_id):
        return jsonify(Likes=MessagesHandler().getMessageByID(message_id).json['Message']['likes'])

    def getMessageDislikes(self, message_id):
        return jsonify(Dislikes=MessagesHandler().getMessageByID(message_id).json['Message']['dislikes'])


    def addMessageLike(self, message_id):
        dao = MessagesDAO()
        if not dao.getMessageByID(message_id):
            return jsonify(Error="Message not found."), 404
        else:
            dao.addLike(message_id)
            return jsonify(Status = "Message Like Added"), 200

    def deleteMessageLike(self, message_id):
        dao = MessagesDAO()
        if not dao.getMessageByID(message_id):
            return jsonify(Error="Message not found."), 404
        else:
            dao.deleteLike(message_id)
            return jsonify(DeleteStatus = "Message Like Deleted"), 200

    def addMessageDislike(self, message_id):
        dao = MessagesDAO()
        if not dao.getMessageByID(message_id):
            return jsonify(Error="Message not found."), 404
        else:
            dao.addDislike(message_id)
            return jsonify(Status = "Message Dislike Added"), 200

    def deleteMessageDislike(self, message_id):
        dao = MessagesDAO()
        if not dao.getMessageByID(message_id):
            return jsonify(Error="Message not found."), 404
        else:
            dao.deleteDislike(message_id)
            return jsonify(DeleteStatus = "Message Dislike Deleted"), 200


################################################################################################
#                                           USER HANDLER                                       #
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
        if dao.loginByEmail(password, email) != None:
            return 1
        if dao.loginByPhone(password, phonenumber) != None:
            return 1
        return 0

    def getAllUsers(self):
        dao = UserDAO()
        user_list = dao.getAllUsers()
        mapped_result = []
        for r in user_list:
            mapped_result.append(self.mapToUserDict(r))
        return jsonify(Contact=mapped_result)

    def getUserByUserID(self, uid):
        dao = UserDAO()
        user = dao.getUserByID(uid)
        if user == None:
            return jsonify(Error="USER NOT FOUND"), 400
        else:
            mapped = self.mapToUserDict(user)
            return jsonify(User=mapped)

    def insertUser(self, form):
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
                return jsonify(Error="email taken"), 400
        if phonenumber != ' ':
            if UserDAO().validatePhone(phonenumber) != None:
                return jsonify(Error="phonenumber taken"), 400
        # OPTIONAL
        # verify username is not taken
        # if UserDAO().validateUsername(username) != None:
        #     return jsonify(Error="Username taken"), 400

        if password and username and firstname and lastname:
            dao = UserDAO()
            uid = dao.insert(username, firstname, lastname, email, phonenumber, password)
            return self.getUserByUserID(uid)

