from config.dbconfig import pg_config
import psycopg2

tokenId = 1;

class ContactDAO:
    def __init__(self):

        # C1 = [1, 'deigodinero', 'diego', 'amador', 'diego.diner@upr.edu', '7870000000']
        # C2 = [2, 'edusanti', 'eduardo', 'santiago', 'edusanti@upr.edu', '7871111111']
        # C3 = [3, 'javelez', 'javier', 'velez', 'javier.velez@upr.edu', '7872222222']
        # C4 = [4, 'pedro1', 'pedro', 'perez', 'pperez@upr.edu', '7873333333']
        # C5 = [5, 'moosclus', 'diego', 'perez', 'dieguito@yahoo.com', '7874444444']
        # C6 = [6, 'wop', 'panky', 'arroyo', '', '']
        #
        # self.data = []
        # self.data.append(C1)
        # self.data.append(C2)
        # self.data.append(C3)
        # self.data.append(C4)
        # self.data.append(C5)
        # self.data.append(C6)

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)


    # http://127.0.0.1:5000/kheApp/contacts
    def getAllContacts(self):
        cursor = self.conn.cursor()
        query = "select user_id, user_name, first_name, last_name, email, phone_number " \
                    "from contact, usr " \
                    "where contact.contacted = usr.user_id "\
                    "and contact.contacts = %s;"
        cursor.execute(query, (tokenId,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # http://127.0.0.1:5000/kheApp/contacts/2
    def getContactByID(self, id):
        cursor = self.conn.cursor()
        query = "select user_id, user_name, first_name, last_name, email, phone_number " \
                    "from contact, usr " \
                    "where contact.contacted = usr.user_id "\
                    "and contact.contacted = %s "\
                    "and contact.contacts = %s;"
        cursor.execute(query, (id, tokenId,))
        result = cursor.fetchone()
        return result

    # http://127.0.0.1:5000/kheApp/contacts?username=edusanti
    # http://127.0.0.1:5000/kheApp/contacts?lastname=edusanti
    # http://127.0.0.1:5000/kheApp/contacts?firstname=edusanti
    def getContactsByKeyword(self, keyword, dictIndex):             # has to be reworked
        contact_list = self.getAllContacts()
        print(contact_list)
        result = []
        for r in contact_list:
            if keyword.lower() == r[dictIndex].lower():
                result.append(r)
        return result

    # http://127.0.0.1:5000/kheApp/contacts
    # key: id   value: 2
    # key: id   value: 5
    def insert(self, id):
        cursor = self.conn.cursor()
        query = "insert into contact(contacts, contacted) values (%s, %s) returning contacted;"
        cursor.execute(query, (tokenId, id,))
        cid = cursor.fetchone()[0]
        self.conn.commit()
        return cid

    # def update(self, cid, cusername, cfirstname, clastname, cemail, cphonenumber):
    #     # cursor = self.conn.cursor()
    #     # query = "update contacts set cusername = %s, cfirstname = %s, clastname = %s, cemail = %s, cphonenumber = %s where cid = %s;"
    #     # cursor.execute(query, (cusername, cfirstname, clastname, cemail, cphonenumber, cid,))
    #     # self.conn.commit()
    #     # return cid
    #     return cid

    # http://127.0.0.1:5000/kheApp/contacts/2
    def delete(self, cid):
        cursor = self.conn.cursor()
        query = "delete from contact where contacts = %s and contacted = %s;"
        cursor.execute(query, (tokenId, cid,))
        self.conn.commit()
        return cid


class ChatDAO:
    def __init__(self):
        # CH = [chatid, chatname, chatadminid
        CH1 = [1, 'PLBois', 3]
        CH2 = [2, 'Los traperos full', 1]
        CH3 = [3, 'TestChat', 1]

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

    def insert(self, chname, chadminid):
        # cursor = self.conn.cursor()
        # query = "insert into chats(chnamem chadminid) values (%s, %s) returning chid;"
        # cursor.execute(query, (chname, chadminid))
        # cid = cursor.fetchone()[0]
        # self.conn.commit()
        # return chid
        return 3

    def update(self, chid, chname, chadminid):
        # cursor = self.conn.cursor()
        # query = "update chats set chname = %s, cadminid = %s where chid = %s;"
        # cursor.execute(query, (chname, chadminid, chid,))
        # self.conn.commit()
        # return cid
        return chid

    def delete(self, chid):
        # cursor = self.conn.cursor()
        # query = "delete from chats where chid = %s;"
        # cursor.execute(query, (cid,))
        # self.conn.commit()
        # return cid
        return chid

    def getMembers(self, chid):
        # self.getChatByID(chid)
        if chid == 1:
            members = ['1', '2', '3']
        elif chid == 2:
            members = ['1', '2']
        elif chid == 3:
            members = ['1', '2', '3', '4', '5', '6']
        return members


class MessagesDAO:
    def __init__(self):
        #    ChatID,    Message,   userID,   Timestamp,    messageID,     Likes,     Dislikes     Image
        C1 = [1, 'This is my first message on kheapp', 1, '01/03/19-13:32:22', 1, 0, 3, 'http://www.google.com/cat.png']
        C2 = [1, 'Wepa!', 2, '01/03/19-16:20:45', 2, 1, 3, ' ']
        C3 = [2, 'Todo bien?', 3, '01/05/19-18:11:20', 3, 3, 0, ' ']
        C4 = [1, 'Saludos Gente', 1, '02/06/19-22:38:01', 4, 3, 0, 'http://www.google.com/greetings.png']

        self.data = []
        self.data.append(C1)
        self.data.append(C2)
        self.data.append(C3)
        self.data.append(C4)

    def getAllMessages(self):
        return self.data

    # ByChatID
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

    # ByID
    def getMessageByID(self, id):
        for r in self.data:
            if id == r[4]:
                return r
        return None

    def getMessageLikes(self, id):
        for r in self.data:
            if id == r[4]:
                return r[5]
        return None

    def insert(slef, chid, message, user_id, timestamp, likes, dislikes, image):
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

    def addLike(self, message_id):
        return message_id

    def deleteLike(self, message_id):
        return message_id

    def addDislike(self, message_id):
        return message_id

    def deleteDislike(self, message_id):
        return message_id


class UserDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllUserID(self):
        cursor = self.conn.cursor()
        query = "select user_id " \
                    "from usr " \
                    "where usr.user_id <> %s;"
        cursor.execute(query, (tokenId,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # http://127.0.0.1:5000/kheApp/contacts?id=2
    # http://127.0.0.1:5000/kheApp/contacts?id=14
    def getUserByUserID(self, id):
        cursor = self.conn.cursor()
        query = "select user_id " \
                    "from usr " \
                    "where usr.user_id = %s " \
                    "and usr.user_id <> %s;"
        cursor.execute(query, (id, tokenId,))
        result = cursor.fetchone()
        return result

