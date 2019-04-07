from config.dbconfig import pg_config
import psycopg2

tokenId = -1

def globallyChangeTokenId(id):

    global tokenId
    tokenId = id
    print(tokenId)


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

    def getAllContactsOfUser(self,uid):
        cursor = self.conn.cursor()
        query = "select user_id, user_name, first_name, last_name, email, phone_number " \
                    "from contact, usr " \
                    "where contact.contacted = usr.user_id "\
                    "and contact.contacts = %s;"
        cursor.execute(query, (uid,))
        result = []
        for row in cursor:
            result.append(row)
        return result


class ChatDAO:
    def __init__(self):
        # # CH = [chatid, chatname, chatadminid
        # CH1 = [1, 'PLBois', 3]
        # CH2 = [2, 'Los traperos full', 1]
        # CH3 = [3, 'TestChat', 1]
        #
        # self.data = []
        # self.data.append(CH1)
        # self.data.append(CH2)
        # self.data.append(CH3)
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllChats(self):
        cursor = self.conn.cursor()
        query = "select distinct chat.chid, chat.chat_name, chat.user_id, usr.user_id "\
                "from (chat full outer join member on chat.chid = member.chid), usr "\
                "where usr.user_id = chat.user_id "\
                "and (chat.user_id = %s "\
                "or member.user_id = %s)"
        cursor.execute(query, (tokenId, tokenId,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getChatByID(self, id):
        cursor = self.conn.cursor()
        query = "select distinct chat.chid, chat.chat_name, chat.user_id, usr.user_id "\
                "from (chat full outer join member on chat.chid = member.chid), usr "\
                "where usr.user_id = chat.user_id "\
                "and (chat.user_id = %s "\
                "or member.user_id = %s) " \
                "and chat.chid = %s"
        cursor.execute(query, (tokenId, tokenId, id,))
        result = cursor.fetchone()
        return result

    def getChatsByChatName(self, chatname):
        chat_list = self.getAllChats()
        #print(chat_list)
        result = []
        for r in chat_list:
            if chatname.lower() == r[1].lower():
                result.append(r)
        return result


    def insert(self, chname):
        cursor = self.conn.cursor()
        query = "insert into chat(chat_name, user_id) values (%s, %s) returning chid;"
        cursor.execute(query, (chname, tokenId))
        chid = cursor.fetchone()[0]
        self.conn.commit()
        return chid

    def update(self, chid, chname):
        cursor = self.conn.cursor()
        query = "update chat set chat_name = %s where chid = %s;"
        cursor.execute(query, (chname, chid,))
        self.conn.commit()
        return chid

    def delete(self, chid):
        cursor = self.conn.cursor()
        query = "delete from chat where chid = %s and user_id = %s;"
        cursor.execute(query, (chid, tokenId,))
        self.conn.commit()
        return chid


    def getMembers(self, chid):
        cursor = self.conn.cursor()
        query = "select usr.user_id, usr.user_name, usr.first_name, usr.last_name, usr.email, usr.phone_number "\
                "from chat,usr "\
                "where chat.user_id = usr.user_id "\
                "and chid =%s "\
                "UNION " \
                "select usr.user_id, usr.user_name, usr.first_name, usr.last_name, usr.email, usr.phone_number "\
                "from member,usr "\
                "where member.user_id = usr.user_id "\
                "and chid = %s;"
        cursor.execute(query, (chid, chid, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insertMember(self, chid, contactID):
        cursor = self.conn.cursor()
        query = "insert into member(chid, user_id) values (%s, %s) returning user_id;"
        cursor.execute(query, (chid, contactID,))
        cid = cursor.fetchone()[0]
        self.conn.commit()
        return cid

    def deleteMember(self, chid, contactID):
        cursor = self.conn.cursor()
        query = "delete from member where chid = %s and user_id = %s;"
        cursor.execute(query, (chid, contactID,))
        # cid = cursor.fetchone()[0]
        self.conn.commit()
        return contactID

    def validateAdmin(self, chid):
        cursor = self.conn.cursor()
        query = "select user_id from chat where chid = %sand user_id = %s;"
        cursor.execute(query, (chid, tokenId,))
        result = cursor.fetchone()
        return result

    def isContactInChat(self, chid, contact):
        cursor = self.conn.cursor()
        query = "select usr.user_id, usr.user_name, usr.first_name, usr.last_name, usr.email, usr.phone_number "\
                    "from member,usr "\
                    "where member.user_id = usr.user_id "\
                    "and chid = %s and member.user_id = %s;"
        cursor.execute(query, (chid, contact, ))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllChatSubscribers(self, id):
        cursor = self.conn.cursor()
        query = "select member.user_id " \
                "from member left join chat on chat.chid = member.chid "\
                "where chat.chid = member.chid and chat.chid = %s "\
                "UNION "\
                "select chat.user_id "\
                "from chat "\
                "where chid = %s;"
        cursor.execute(query, (id, id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllChatsDev(self):
        cursor = self.conn.cursor()
        query = "select chat.chid, chat.chat_name, chat.user_id, usr.user_name from chat, usr " \
                "where usr.user_id = chat.user_id;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getChatByIDDev(self, id):
        cursor = self.conn.cursor()
        query = "select chat.chid, chat.chat_name, chat.user_id, usr.user_name from chat, member, usr "\
                    "where chat.chid = member.chid and chat.chid = %s and usr.user_id = chat.user_id "\
                    "UNION "\
                    "select chat.chid, chat.chat_name, chat.user_id, usr.user_name "\
                    "from chat, usr "\
                    "where chid = %s "\
                    "and usr.user_id = chat.user_id;"
        cursor.execute(query, (id, id,))
        result = cursor.fetchone()
        return result


class MessagesDAO:
    def __init__(self):
        # #    ChatID,    Message,   userID,   Timestamp,    messageID,     Likes,     Dislikes     Image
        # C1 = [1, 'This is my first message on kheapp', 1, '01/03/19-13:32:22', 1, 0, 3, 'http://www.google.com/cat.png']
        # C2 = [1, 'Wepa!', 2, '01/03/19-16:20:45', 2, 1, 3, ' ']
        # C3 = [2, 'To bien?', 3, '01/05/19-18:11:20', 3, 3, 0, ' ']
        # C4 = [1, 'Saludos Gente', 1, '02/06/19-22:38:01', 4, 3, 0, 'http://www.google.com/greetings.png']
        #
        # self.data = []
        # self.data.append(C1)
        # self.data.append(C2)
        # self.data.append(C3)
        # self.data.append(C4)
        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)


    def getAllMessages(self):
        cursor = self.conn.cursor()
        query = "with message_likes as ( " \
                "select message.message_id as mid, count(reaction) as likes " \
                "from message left join react on message.message_id = react.message_id " \
                "where reaction = 'like' " \
                "group by message.message_id), " \
                "message_dislikes as ( " \
                "select message.message_id as mid, count(reaction) as dislikes " \
                "from message left join react on message.message_id = react.message_id " \
                "where reaction = 'dislike' " \
                "group by message.message_id) " \
                "select message.chid, message.message, message.user_id, message.time_stamp, message.message_id, " \
                "message_likes.likes, message_dislikes.dislikes, media.file, usr.user_name " \
                "from (((message left join message_likes on message_likes.mid = message.message_id) " \
                "left join message_dislikes on message_dislikes.mid = message.message_id) " \
                "left join media on message.media_id = media.media_id), usr " \
                "where usr.user_id = message.user_id " \
                "order by message.chid, message.time_stamp desc; "
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    # ByChatID
    def getMessagesByChatID(self, id):
        cursor = self.conn.cursor()
        query = "with message_likes as ( " \
                "select message.message_id as mid, count(reaction) as likes " \
                "from message left join react on message.message_id = react.message_id " \
                "where reaction = 'like' " \
                "group by message.message_id), " \
                "message_dislikes as ( " \
                "select message.message_id as mid, count(reaction) as dislikes " \
                "from message left join react on message.message_id = react.message_id " \
                "where reaction = 'dislike' " \
                "group by message.message_id) " \
                "select message.chid, message.message, message.user_id, message.time_stamp, message.message_id, " \
                "message_likes.likes, message_dislikes.dislikes, media.file, usr.user_name " \
                "from (((message left join message_likes on message_likes.mid = message.message_id) " \
                "left join message_dislikes on message_dislikes.mid = message.message_id) " \
                "left join media on message.media_id = media.media_id), usr " \
                "where usr.user_id = message.user_id " \
                "and message.chid = %s" \
                "order by message.chid, message.time_stamp desc; "
        cursor.execute(query, (id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # ByID
    def getMessageByID(self, id):
        cursor = self.conn.cursor()
        query = "with message_likes as ( " \
                "select message.message_id as mid, count(reaction) as likes " \
                "from message left join react on message.message_id = react.message_id " \
                "where reaction = 'like' " \
                "group by message.message_id), " \
                "message_dislikes as ( " \
                "select message.message_id as mid, count(reaction) as dislikes " \
                "from message left join react on message.message_id = react.message_id " \
                "where reaction = 'dislike' " \
                "group by message.message_id) " \
                "select message.chid, message.message, message.user_id, message.time_stamp, message.message_id, " \
                "message_likes.likes, message_dislikes.dislikes, media.file, usr.user_name " \
                "from (((message left join message_likes on message_likes.mid = message.message_id) " \
                "left join message_dislikes on message_dislikes.mid = message.message_id) " \
                "left join media on message.media_id = media.media_id), usr " \
                "where usr.user_id = message.user_id " \
                "and message.message_id = %s;"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return result

    def getMessageLikes(self, id):
        cursor = self.conn.cursor()
        query = "select message_id, count(reaction) as likes "\
                "from react "\
                "where reaction = 'like' "\
                "and message_id = %s " \
                "group by message_id;"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return result

    def getMessageDislikes(self, id):
        cursor = self.conn.cursor()
        query = "select count(reaction) as likes "\
                "from react "\
                "where reaction = 'dislike' "\
                "and message_id = %s;"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return result


    def insertWithoutMedia(self, chid, message):
        cursor = self.conn.cursor()
        query = "insert into message(message, user_id, chid, time_stamp) values (%s, %s, %s, now()) returning message_id;"
        cursor.execute(query, (message, tokenId, chid, ))
        message_id = cursor.fetchone()[0]
        self.conn.commit()
        return message_id

    def insert(self, chid, message, media_id):
        cursor = self.conn.cursor()
        query = "insert into message(message, user_id, chid, media_id, time_stamp) values (%s, %s, %s, %s, now()) returning message_id;"
        cursor.execute(query, (message, tokenId, chid, media_id, ))
        message_id = cursor.fetchone()[0]
        self.conn.commit()
        return message_id

    def insertMedia(self, media):
        cursor = self.conn.cursor()
        query = "insert into media(file) values (%s) returning media_id;"
        cursor.execute(query, (media,))
        media_id = cursor.fetchone()[0]
        self.conn.commit()
        return media_id

    def reply(self, original, message_id):
        cursor = self.conn.cursor()
        query = "insert into isreply(original, reply) values (%s, %s) returning reply;"
        cursor.execute(query, (original, message_id,))
        message_id = cursor.fetchone()[0]
        self.conn.commit()
        return message_id

    # def delete(self, message_id):
    #     cursor = self.conn.cursor()
    #     query = "delete from message where message_id = %s;"
    #     cursor.execute(query, (message_id,))
    #     self.conn.commit()
    #     return message_id

    def addLike(self, message_id):
        cursor = self.conn.cursor()
        query = "insert into react(user_id, message_id, reaction, time_stamp) values (%s, %s, 'like', now()) returning message_id;"
        cursor.execute(query, (tokenId, message_id,))
        message_id = cursor.fetchone()[0]
        self.conn.commit()
        return message_id

    def deleteReaction(self, message_id):
        cursor = self.conn.cursor()
        query = "delete from react where message_id = %s and user_id = %s;"
        cursor.execute(query, (message_id, tokenId,))
        self.conn.commit()
        return message_id

    def addDislike(self, message_id):
        cursor = self.conn.cursor()
        query = "insert into react(user_id, message_id, reaction, time_stamp) values (%s, %s, 'dislike', now()) returning message_id;"
        cursor.execute(query, (tokenId, message_id,))
        message_id = cursor.fetchone()[0]
        self.conn.commit()
        return message_id


    def validateReaction(self, message_id):
        cursor = self.conn.cursor()
        query = "select react.user_id "\
                "from (message left join react on message.message_id = react.message_id) "\
                "where message.message_id = %s" \
                "and react.user_id = %s"
        cursor.execute(query, (message_id, tokenId,))
        result = cursor.fetchone()
        return result


    def getAllUsersWhoLiked(self, message_id):
        cursor = self.conn.cursor()
        query = "select usr.user_id, usr.user_name, usr.first_name, usr.last_name, usr.email, usr.phone_number, react.time_stamp "\
                "from (message left join react on message.message_id = react.message_id), usr "\
                "where usr.user_id = react.user_id "\
                "and reaction = 'like' "\
                "and message.message_id = %s;"
        cursor.execute(query, (message_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUsersWhoDisliked(self, message_id):
        cursor = self.conn.cursor()
        query = "select usr.user_id, usr.user_name, usr.first_name, usr.last_name, usr.email, usr.phone_number, react.time_stamp "\
                "from (message left join react on message.message_id = react.message_id), usr "\
                "where usr.user_id = react.user_id "\
                "and reaction = 'dislike' "\
                "and message.message_id = %s;"
        cursor.execute(query, (message_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result


class UserDAO:
    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = "select * from usr;"
        cursor.execute(query, (tokenId,))
        result = []
        for row in cursor:
            result.append(row)
        return result

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

    def getUserByID(self,id):
        cursor = self.conn.cursor()
        query = "select user_id, user_name, first_name, last_name, email, phone_number, password " \
                    "from usr " \
                    "where user_id = %s;"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return result

    # http://127.0.0.1:5000/kheApp/contacts?id=2
    # http://127.0.0.1:5000/kheApp/contacts?id=14
    def getUserIDOnly(self, id):
        cursor = self.conn.cursor()
        query = "select user_id " \
                    "from usr " \
                    "where usr.user_id = %s " \
                    "and usr.user_id <> %s;"
        cursor.execute(query, (id, tokenId,))
        result = cursor.fetchone()
        return result

    # http://127.0.0.1:5000/kheApp/contacts
    # firstname ::  testy
    # lastname ::   tested
    # email ::      test@gmail.com
    def getUserIDOnlyByCredentialsEmail(self, firstname, lastname, email):
        cursor = self.conn.cursor()
        query = "select user_id from usr where first_name = %s and last_name = %s and email = %s;"
        cursor.execute(query, (firstname, lastname, email,))
        result = cursor.fetchone()
        return result

    # http://127.0.0.1:5000/kheApp/contacts
    # firstname ::  testy
    # lastname ::   tested
    # phonenumber:: 7876666666
    def getUserIDOnlyByCredentialsPhone(self, firstname, lastname, phonenumber):
        cursor = self.conn.cursor()
        query = "select user_id from usr where first_name = %s and last_name = %s and phone_number = %s;"
        cursor.execute(query, (firstname, lastname, phonenumber,))
        result = cursor.fetchone()
        return result

    def insert(self, username, firstname, lastname, email, phonenumber, password):
        cursor = self.conn.cursor()
        query = "insert into usr(user_name, first_name, last_name, email, phone_number, password) "\
                "values (%s, %s, %s, %s, %s, %s) returning user_id;"
        cursor.execute(query, (username, firstname, lastname, email, phonenumber, password,))
        cid = cursor.fetchone()[0]
        self.conn.commit()
        return cid

    def validateUsername(self, username):
        cursor = self.conn.cursor()
        query = "select user_id from usr where user_name = %s;"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result

    def validateEmail(self, email):
        cursor = self.conn.cursor()
        query = "select user_id from usr where email = %s;"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result

    def validatePhone(self, phonenumber):
        cursor = self.conn.cursor()
        query = "select user_id from usr where phone_number = %s;"
        cursor.execute(query, (phonenumber,))
        result = cursor.fetchone()
        return result

    def loginByEmail(self, password, email):
        cursor = self.conn.cursor()
        query = "select user_id from usr where password = %s and email = %s;"
        cursor.execute(query, (password, email,))
        result = cursor.fetchone()
        return result

    def loginByPhone(self, password, phonenumber):
        cursor = self.conn.cursor()
        query = "select user_id from usr where password = %s and phone_number = %s;"
        cursor.execute(query, (password, phonenumber,))
        result = cursor.fetchone()
        return result

    def getAllUsersByUsername(self, username):
        cursor = self.conn.cursor()
        query = "select user_id from usr where user_name = %s;"
        cursor.execute(query, (username,))
        result = []
        for row in cursor:
            result.append(row)
        return result


class StatisticsDao:

    def __init__(self):

        connection_url = "dbname=%s user=%s password=%s" % (pg_config['dbname'],
                                                            pg_config['user'],
                                                            pg_config['passwd'])
        self.conn = psycopg2._connect(connection_url)

    def getTrendingTopics(self):
        cursor = self.conn.cursor()
        query = "select hashtag.hashtag, count(hashtag.tag_id) as position "\
                "from hasHash, hashtag "\
                "where hasHash.tag_id = hashtag.tag_id "\
                "group by hashtag.tag_id "\
                "order by count(hashtag.tag_id) desc;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getDailyPosts(self):
        cursor = self.conn.cursor()
        query = "select time_stamp::timestamp::date, count(time_stamp) as total "\
                "from message "\
                "group by time_stamp::timestamp::date;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

