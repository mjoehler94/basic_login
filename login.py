# login.py --------------------------
# Author: Matt Oehler

# libraries
import getpass
import sqlite3

# global
_DATABASE_ = "data/user.db"
_LOGIN_OPTION_ = 1
_REGISTER_OPTION_ = 2
_QUIT_OPTION_ = 3


class Login():
    def __init__(self, database):
        self.db = database
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.is_open_connection = True

        # create tables if they don't already exist
        self.cursor.execute('''CREATE TABLE  IF NOT EXISTS USER (
                    "UserId"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    "DateJoined"	TEXT NOT NULL,
                    "UserName"	TEXT NOT NULL UNIQUE,
                    "Password_Raw"	TEXT NOT NULL,
                    "Password_Encrypted"	TEXT);
                    ''')

        self.cursor.execute('''CREATE TABLE  IF NOT EXISTS LoginHistory (
                            "UserHistoryId"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                            "UserId"	INTEGER NOT NULL,
                            "LoginTime"	TEXT NOT NULL
                            ,FOREIGN KEY (UserId) REFERENCES USER(UserId)
                            );
                            ''')

        # Save (commit) the changes and close connection
        self.conn.commit()
        self.conn.close()
        self.is_open_connection = False
        return

    def open_connection(self, verbose=False):
        if self.is_open_connection:
            if verbose:
                print("The database is already open")
        else:
            self.conn = sqlite3.connect(self.db)
            self.cursor = self.conn.cursor()
            self.is_open_connection = True
            if verbose:
                print("The database has been opened")
        return

    def close_connection(self, verbose=False):
        if self.is_open_connection:
            self.conn.close()
            self.is_open_connection = False

            if verbose:
                print("The database has been closed")
        else:
            if verbose:
                print("The database is already closed")
        return

    def login(self):
        # get username
        username = input("Username:")

        # check username
        self.open_connection()
        check_username = self.cursor.execute(f"SELECT UserName, UserId FROM USER WHERE UserName = '{username}'").fetchone()
        if check_username is None:
            print(f'Username {username} does  not exist')
            self.close_connection()
            return None, None
        # get password
        # pwd = input("Password:")
        pwd = getpass.getpass()
        # check password:
        check_password = self.cursor.execute(f"""SELECT Password_Raw 
                                                 FROM USER WHERE UserName = '{username}'""").fetchone()[0]
        if check_password == pwd:
            self.cursor.execute(f"""INSERT INTO LoginHistory (UserId, LoginTime)
                               VALUES ('{check_username[1]}',DATETIME('now'))""")
            self.conn.commit()
            print("Login was successful!\n")
        else:
            print("Incorrect Password\n")
            username = None

        self.close_connection()
        return username, pwd

    def register(self, verbose=False):
        # get and check username
        print("Enter a Username (must be at least 5 characters).")
        username = input("Username:")
        if len(username) < 5:
            print("Invalid Username")
            return None, None
        elif len(username) >= 5:
            self.open_connection()
            check_username = self.cursor.execute(f"SELECT Username FROM USER WHERE Username = '{username}'").fetchone()
            self.close_connection()
            if check_username is not None:
                print(f"Sorry. The Username '{username}' is already taken.")
                return None, None
            else:
                # get and check password
                print('Create your password. (Passwords must be at least 7 characters)')
                pwd = input("Password:")
                if len(pwd) < 7:
                    print("Invalid Password")
                    return None, None
                elif len(pwd) >= 7:
                    print("Confirm your password")
                    pwd2 = input("Password:")
                    if pwd != pwd2:
                        print("Passwords don't match")
                        return None, None
                    else:
                        self.add_user(username=username, password=pwd)
                        print("Regristration was successful!")
                        return username, pwd

    def add_user(self, username, password):
        encrypted_pwd = self.encrypt(password)
        self.open_connection()
        self.cursor.execute(f"""INSERT INTO USER (DateJoined, UserName, Password_Raw, Password_Encrypted)
                               VALUES (DATETIME('now'), '{username}', '{password}','{encrypted_pwd}')""")
        self.conn.commit()
        self.close_connection()
        return

    def fill_db(self, user_data=None):
        # fake user data
        if not user_data:
            user_data = [
                ('KBryant_24', 'MVP_2008'),  # R.I.P Kobe
                ('john_smith', 'hi-im-johnny'),
                ('robert_johnson', 'VERY SECURE PASSWORD'),
                ('t_jefferds', 'yogurt'),
                ('captain_holt', 'i<3kevin')

            ]

        for username, pwd in user_data:
            self.open_connection()
            check_username = self.cursor.execute(f"SELECT Username FROM USER WHERE Username = '{username}'").fetchone()
            self.close_connection()
            if check_username is not None:
                continue
            else:
                self.add_user(username=username, password=pwd)
        return

    @staticmethod
    def encrypt(text):
        # TODO: run an encryption algorithm on the password to store in the database
        return 'encrypted_password'
    @staticmethod
    def decrypt(text):
        # TODO: decrypt the password to ensure credentials are valid
        return 'decrypted_password'


def main():

    # initialize Login instance ---------------
    login = Login(database=_DATABASE_)
    login.fill_db()

    # Main Menu ------------------
    while True:
        print("\nMain Menu -------------------------------")
        option = input("""Please enter:
         '1' to Login
         '2' to Register
         '3' to Quit\n-->""")
        try:
            option = int(option)
        except:
            option = -1  # invalid input
        if option == _QUIT_OPTION_:
            print("Quitting the program.")
            return
        elif option not in [1, 2]:
            print("Invalid Selection. Please try again.")
            continue
        elif option == _LOGIN_OPTION_:
            print("Enter your Username and Password to login.")
            username, pwd = login.login()
            if username is None:
                continue
        elif option == _REGISTER_OPTION_:
            print("To Register, enter in your desired Username then password.")
            username, pwd = login.register(True)
            if username is None:
                continue

        break

    # login or register ----------------------------
    # username, pwd = login.prompt_user_input()
    #
    print(f"Username: {username}, Password: {pwd}")
    login.conn.close()
    return


if __name__ == '__main__':
    main()
