import mysql.connector
import db_config as cfg

class UserDAO:
    """A data object class to interact with the users table in the MySQL database, sewing_patterns."""
    host =""
    user = ""
    password =""
    database =""
    connection = ""
    cursor =""


    def __init__(self):
        """Initializes the database credentials from config file. """
        self.host= cfg.mysql['host']
        self.user= cfg.mysql['user']
        self.password= cfg.mysql['password']
        self.database= cfg.mysql['database']

    def getCursor(self):
        """Sets up connection to the database and returns a cursor."""
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        """Close the database connection and cursor."""
        self.connection.close()
        self.cursor.close()

    def convertToDictionaryUsers(self, resultLine):
        """Converts the result from a query to the users table into a dictionary."""
        attkeys=['userID', 'first_name','last_name', 'email', 'password']
        user = {}
        currentkey = 0
        for attrib in resultLine:
            user[attkeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return user
    
    def get_all_users(self):
        """Get all the details from the users table. 
        For security, does not return the password_hash. """
        try:
            cursor = self.getCursor()
            sql = "SELECT userID, first_name, last_name, email FROM users"
            cursor.execute(sql)
            results = cursor.fetchall()
            if not results:
                return None

            users = []
            for row in results:
                users.append(self.convertToDictionaryUsers(row))
            self.closeAll()
            return users
        except Exception as e:
            print(f"Database error in get_all_users: {e}")
            raise
        finally:
            self.closeAll()
    
    def create_user(self, user):
        """Create a new user."""
        try:
            cursor = self.getCursor()
            sql = "INSERT INTO users (first_name, last_name, email, password_hash) VALUES (%s, %s, %s, %s)"
            values = (user.get("first_name"), user.get("last_name"), user.get("email"), user.get("password"))
            cursor.execute(sql, values)
            self.connection.commit()
            newid = cursor.lastrowid
            user['userID'] = newid
            return user

        except Exception as e:
            print(f"Database error in create_user: {e}")
            raise
        finally:
            self.closeAll()
        
    def update_user(self, user):
        """Update a user in the users database."""
        try:
            cursor = self.getCursor()
            sql = "UPDATE users SET first_name = %s, last_name = %s, email = %s, password_hash = %s WHERE userID = %s"
            values = (user.get("first_name"), user.get("last_name"), user.get("email"), user.get("password"), user.get("userID"))
            cursor.execute(sql, values)
            self.connection.commit()
            return user

        except Exception as e:
            print(f"Database error in update_user: {e}")
            raise
        finally:
            self.closeAll()
                                                                                                                                                                                                        
    def findByUserID_users(self, userID):
        """Get a specific user by userID."""
        try:
            cursor = self.getCursor()
            sql = "SELECT userID, first_name, last_name, email FROM users WHERE userID = %s"
            values = (userID, )
            cursor.execute(sql, values)
            result = cursor.fetchone()

            if result is None:
                return None
            
            returnvalue = self.convertToDictionaryUsers(result)
            return returnvalue
        
        except Exception as e:
            print(f"Database error in findByUserID_users: {e}")
            raise
        finally:
            self.closeAll()

    def delete_user(self, userID):
        """Delete a specific user by userID."""
        try:
            cursor = self.getCursor()
            sql = "DELETE FROM users WHERE userID = %s"
            values = (userID, )
            cursor.execute(sql, values)
            self.connection.commit()
            print("User deleted")
        except Exception as e:
            print(f"Database error in delete_user: {e}")
            raise
        finally:
            self.closeAll()

userDAO = UserDAO()