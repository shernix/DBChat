from flask import jsonify, request
from dao.dao import ContactDAO, ChatDAO


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

    def getContactById(self, id):
        dao = ContactDAO()
        result = dao.getContactById(id)
        if result == None:
            return jsonify(Error="NOT FOUND"), 404
        else:
            mapped = self.mapToContactDict(result)
            return jsonify(Part=mapped)

    def searchContacts(self, keyword):
        print(keyword)
        dao = ContactDAO()
        result = dao.getAllContacts()
        mapped_result = []
        for r in result:
            if keyword == r[1] or keyword == r[2] or keyword == r[3]:
                mapped_result.append(self.mapToContactDict(r))
        return jsonify(Contact=mapped_result)


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
