# Login System
___

**Description**

A simple system that allows users to login using a username and password.
If the user doesn't already have an account they will have the option to create a new account.
The information will be in stored in an sqlite database. 

**Resources**

I used this [database browser](https://sqlitebrowser.org/) to verify that my program was working properly.

**To Do:**

- use encryption to store the passwords in the database 
- create a frontend or gui to use instead of just command-line interface
- use `getpass` module to keep passwords secure when being input by the user
- demonstrate how to properly collect user input to avoid injection attacks
- use a log module to keep track of db operations without printing to stdout (since that is the user interface)
