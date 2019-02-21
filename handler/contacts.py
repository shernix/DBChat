from flask import jsonify, request
from dao.contactdao import ContactDAO


class ContactHandler:
    # def getAllContacts(self):
    #     C1 = {}
    #     C1['username'] = DiegoXDinero
    #     C1['first_name'] = Diego
    #     C1['last_name'] = Amador
    #
    #     C2 = {}
    #     C2['username'] = Geeklusion
    #     C2['first_name'] = Eduardo
    #     C2['last_name'] = Santiago
    #
    #     C3 = {}
    #     C3['username'] = coochielover
    #     C3['first_name'] = JeanPaul
    #     C3['last_name'] = Vicente
    #
    #     contacts = []
    #     contacts.append(C1)
    #     contacts.append(C2)
    #     return jsonify(Contacts=contacts)

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
        result = dao.getContactById(id)
        if result == None:
            return jsonify(Error="NOT FOUND"), 404
        else:
            mapped = self.mapToContactDict(result)
            return jsonify(Part=mapped)
