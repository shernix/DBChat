from flask import jsonify, request
from dao.messagesdao import MessagesDAO

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
            if result == None:
                return jsonify(Error="NOT FOUND"), 404
            else:
                mapped = self.mapToMessagesDict(result)
                return jsonify(Part=mapped)