# login.py --------------------------
# Author: Matt Oehler

# libraries
import getpass
import sqlite3

# global
_DATABASE_ = "data/user.db"


class Login():
    def __init__(self, database):
        self.db = database

        return

    def toggle_connection(self):

    def prompt_user_input(self):
        username = input("Username:")
        pwd = input("Password:")
        # pwd = getpass.getpass(prompt='Password: ', stream=None)

        return username, pwd

    def update_db(self):
        pass

    def encrypt(self):
        pass


def main():

    # initialize Login instance
    login = Login(database=_DATABASE_)

    username, pwd = login.prompt_user_input()

    print(f"Username: {username}, Password: {pwd}")

    return


if __name__ == '__main__':
    main()
