class ContactDAO:
    def __init__(self):

        C1 = [1, 'deigodinero', 'diego', 'amador', 'diego.diner@upr.edu', '7870000000']
        C2 = [2, 'edusanti', 'eduardo', 'santiago', 'edusanti@upr.edu', '7871111111']
        C3 = [3, 'javelez', 'javier', 'velez', 'javier.velez@upr.edu', '7872222222']
        C4 = [4, 'pedro1', 'pedro', 'perez', 'pperez@upr.edu', '7873333333']

        self.data = []
        self.data.append(C1)
        self.data.append(C2)
        self.data.append(C3)
        self.data.append(C4)

    def getAllContacts(self):
        return self.data

    # ByID
    def getContactById(self, id):
        for r in self.data:
            if id == r[0]:
                return r
        return None
