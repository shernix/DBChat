class ContactDAO:
    def __init__(self):

        C1 = [1, 'deigodinero', 'diego', 'amador', 'diego.diner@upr.edu', '7870000000']
        C2 = [2, 'edusanti', 'eduardo', 'santiago', 'edusanti@upr.edu', '7871111111']
        C3 = [3, 'javelez', 'javier', 'velez', 'javier.velez@upr.edu', '7872222222']
        C4 = [4, 'pedro1', 'pedro', 'perez', 'pperez@upr.edu', '7873333333']
        C5 = [5, 'moosclus', 'diego', 'perez', 'dieguito@yahoo.com', '7874444444']
        C6 = [6, 'wop', 'panky', 'arroyo', '', '']

        self.data = []
        self.data.append(C1)
        self.data.append(C2)
        self.data.append(C3)
        self.data.append(C4)
        self.data.append(C5)
        self.data.append(C6)

    def getAllContacts(self):
        return self.data

    # ByID
    def getContactByID(self, id):
        for r in self.data:
            if id == r[0]:
                return r
        return None

    def getContactsByKeyword(self, keyword, dictIndex):
        mapped_result = []
        for r in self.data:
            if keyword.lower() == r[dictIndex].lower():
                mapped_result.append(r)
        return mapped_result

    def insert(self, cusername, cfirstname, clastname, cemail, cphonenumber):
        # cursor = self.conn.cursor()
        # query = "insert into contacts(cusername, cfirstname, clastname, cemail, cphonenumber) values (%s, %s, %s, %s) returning cid;"
        # cursor.execute(query, (cusername, cfirstname, clastname, cemail, cphonenumber))
        # cid = cursor.fetchone()[0]
        # self.conn.commit()
        # return cid
        return 7

    def update(self, cid, cusername, cfirstname, clastname, cemail, cphonenumber):
        # cursor = self.conn.cursor()
        # query = "update contacts set cusername = %s, cfirstname = %s, clastname = %s, cemail = %s, cphonenumber = %s where cid = %s;"
        # cursor.execute(query, (cusername, cfirstname, clastname, cemail, cphonenumber, cid,))
        # self.conn.commit()
        # return cid
        return cid

    def delete(self, cid):
        # cursor = self.conn.cursor()
        # query = "delete from contacts where cid = %s;"
        # cursor.execute(query, (cid,))
        # self.conn.commit()
        # return cid
        return cid



class ChatDAO:
    def __init__(self):

        # CH = [chatid, ownerid, chatname]
        CH1 = [1, 3, 'PLBois']
        CH2 = [2, 1, 'Los traperos full']
        CH3 = [3, 1, 'TestChat']

        self.data = []
        self.data.append(CH1)
        self.data.append(CH2)
        self.data.append(CH3)

    def getAllChats(self):
        return self.data

    def getChatByID(self, id):
        for r in self.data:
            if id == r[0]:
                return r
        return None

    def getChatsByChatName(self, chatname):
        mapped_result = []
        for r in self.data:
            if chatname.lower() == r[2].lower():
                mapped_result.append(r)
        return mapped_result


class MessagesDAO:
    def __init__(self):

        C1 = [1, '"This is my first message on kheapp', '1', '01/03/19-13:32:22']
        C2 = [1, '"Wepa!', '2', '01/03/19-16:20:45']
        C3 = [2, '"Todo bien?', '3', '01/05/19-18:11:20']
        C4 = [1, '"Saludos Gente', '1', '02/06/19-22:38:01']

        self.data = []
        self.data.append(C1)
        self.data.append(C2)
        self.data.append(C3)
        self.data.append(C4)

    def getAllMessages(self):
        return self.data

    # ByID
    def getMessagesByChatID(self, id):
        result = []
        for r in self.data:
            if id == r[0]:
                result.append(r)
                print(result)
        if len(result) == 0:
            return None
        else:
            return result
    
    def insert(self, cusername, cfirstname, clastname, cemail, cphonenumber):
        # cursor = self.conn.cursor()
        # query = "insert into contacts(cusername, cfirstname, clastname, cemail, cphonenumber) values (%s, %s, %s, %s) returning cid;"
        # cursor.execute(query, (cusername, cfirstname, clastname, cemail, cphonenumber))
        # cid = cursor.fetchone()[0]
        # self.conn.commit()
        # return cid
        return 7

    def delete(self, cid):
        # cursor = self.conn.cursor()
        # query = "delete from contacts where cid = %s;"
        # cursor.execute(query, (cid,))
        # self.conn.commit()
        # return cid
        return cid

