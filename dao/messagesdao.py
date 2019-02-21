class MessagesDAO:
    def __init__(self):

        C1 = [1, '"This is my first message on kheapp', 'Diego', '01/03/19-13:32:22']
        C2 = [2, '"Wepa!', 'Eduardo', '01/03/19-16:20:45']
        C3 = [2, '"Todo bien?', 'Javier', '01/05/19-18:11:20']
        C4 = [2, '"Saludos Gente', 'Diego', '02/06/19-22:38:01']

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
        if len(result)==0:
            return None
        else: 
            return result
