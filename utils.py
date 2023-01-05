def checkUserLogged(username, users):
        for user in users:
            if username in user and user.split(";")[4] == "True":
                return True
            else:
                return False
