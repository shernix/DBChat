from flask import jsonify, request
from dao.dao import ContactDAO, ChatDAO, MessagesDAO


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

    def getAllContacts(self):
        dao = ContactDAO()
        result = dao.getAllContacts()
        mapped_result = []
        for r in result:
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

    def getAllChats(self):
        dao = ChatDAO()
        result = dao.getAllChats()
        mapped_result = []
        for r in result:
            mapped_result.append(self.mapToChatDict(r))
        return jsonify(Contact=mapped_result)

    def getChatByID(self, id):
        dao = ChatDAO()
        result = dao.getChatByID(id)
        if result == None:
            return jsonify(Error="CHAT NOT FOUND"), 404
        else:
            mapped = self.mapToChatDict(result)
            return jsonify(Chat=mapped)

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
