
class User:

    def __init__(self, filename):
        self._userlogin = False
        self.filename = filename
        self._username = ''
        self.file = None
        #self.load()

    def auth(self, name, pw):
        if pw == 'root':
            self._username = name
            self._userlogin = True
            return True
        else:
            self._userlogin = False
            return False
