class UsersDAO:
    def __init__(self):
        # U = [id, 'first name', 'last name', 'email', 'phone number', 'password', 'username']

        U1 = [1, 'diego', 'amador', 'diego.diner@upr.edu', '7870000000', 'abcd0001', 'deigodinero']
        U2 = [2, 'eduardo', 'santiago', 'edusanti@upr.edu', '7871111111', 'abcd0002', 'edusanti']
        U3 = [3, 'javier', 'velez', 'javier.velez@upr.edu', '7872222222', 'abcd0003', 'javelez']
        U4 = [4, 'pedro', 'perez', 'pperez@upr.edu', '7873333333', 'abcd0004', 'pedro1']

        self.data = []
        self.data.append(U1)
        self.data.append(U2)
        self.data.append(U3)
        self.data.append(U4)

    # def getChatsByUserId(self, id):
    #     if id == 1 or id == 2:
    #         T = []
    #         T.append(['1', 'PLBois'])
    #         T.append(['2', 'traperos'])
    #         return T
    #
    #     elif id == 3:
    #         return [['1', 'PLBois']]
    #     else:
    #         return []
    #
    # def getContactsByUserId(self, id):
    #     if id == 1:
    #         T = []
    #         T.append(['2', 'edusanti'])
    #         T.append(['3', 'javelez'])
    #         return T
    #     elif id == 2:
    #         T = []
    #         T.append(['1', 'diegodinero'])
    #         T.append(['3', 'javelez'])
    #         return T
    #     elif id == 3:
    #         T = []
    #         T.append(['1', 'diegodinero'])
    #         T.append(['2', 'edusanti'])
    #         T.append(['4', 'pedro1'])
    #         return T
    #     elif id == 4:
    #         T = []
    #         T.append(['3', 'javelez'])




