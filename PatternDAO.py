import mysql.connector
import db_config as cfg


class PatternDAO:
    """A data access object class to interact with the patterns table in the MySQL database, sewing_patterns."""
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
#
    def convertToDictionaryPatterns(self, resultLine):
        """Converts the result from a query to the patterns table into a dictionary."""
        attkeys=['patternID', 'brand','category', 'fabric_type', 'description', 'format', 'userID']
        pattern = {}
        currentkey = 0
        for attrib in resultLine:
            pattern[attkeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return pattern

    def convertToDictionaryUsers(self, resultLine):
        """Converts the result from a query to the users table into a dictionary."""
        attkeys=['userID', 'first_name','last_name', 'email', 'password']
        user = {}
        currentkey = 0
        for attrib in resultLine:
            user[attkeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return user

    def getAll(self):
        """Gets all the patterns from the database."""
        try:
            cursor = self.getCursor()
            sql = "SELECT * from patterns"
            cursor.execute(sql)
            results = cursor.fetchall()

            if not results:
                return None
            
            patterns = []
            for row in results:
                patterns.append(self.convertToDictionaryPatterns(row))
            return patterns
        
        except Exception as e:
            print(f"Database error in getAll: {e}")
            raise

        finally:
            self.closeAll()

    def findByID(self, patternID):
        """Get a pattern by patternID. """
        try:
            cursor = self.getCursor()
            sql = "SELECT * FROM patterns WHERE patternID = %s"
            values = (patternID, )
            cursor.execute(sql, values)
            result = cursor.fetchone()

            if not result:
                return None
            
            returnvalue = self.convertToDictionaryPatterns(result)
            return returnvalue
        
        except Exception as e:
            print(f"Database error in findByID: {e}")
            raise
        finally:
            self.closeAll()

# View by Category
    def findByCategory(self, category):
        """Get patterns filtered by category. """
        try:
            cursor = self.getCursor()
            sql = "SELECT * FROM patterns WHERE category = %s"
            values = (category, )
            cursor.execute(sql, values)
            results = cursor.fetchall()

            if not results:
                return None
            
            patterns = []
            for row in results:
                patterns.append(self.convertToDictionaryPatterns(row))
            return patterns
        
            #returnvalue = self.convertToDictionaryPatterns(result)
            #return returnvalue
        
        except Exception as e:
            print(f"Database error in findByCategory: {e}")
            raise
        finally:
            self.closeAll()

    def findByBrand(self, brand):
        """Get patterns filtered by brand."""
        try:
            cursor = self.getCursor()
            sql = "SELECT * FROM patterns WHERE brand = %s"
            values = (brand, )
            cursor.execute(sql, values)
            results = cursor.fetchall()

            if not results:
                return None
            
            patterns = []
            for row in results:
                patterns.append(self.convertToDictionaryPatterns(row))
            return patterns
        
        except Exception as e:
            print(f"Database error in findByBrand: {e}")
            raise
        finally:
            self.closeAll()

    def findByFabric(self, fabric_type):
        """Get patterns filtered by fabric type"""
        try:
            cursor = self.getCursor()
            sql = "SELECT * FROM patterns WHERE fabric_type = %s"
            values = (fabric_type, )
            cursor.execute(sql, values)
            results = cursor.fetchall()

            if not results:
                return None
            
            patterns = []
            for row in results:
                patterns.append(self.convertToDictionaryPatterns(row))
            return patterns
        
        except Exception as e:
            print(f"Database error in findByFabric: {e}")
            raise
        finally:
            self.closeAll()

    def findByFormat(self, format):
        """Get patterns filtered by pattern format."""
        try:
            cursor = self.getCursor()
            sql = "SELECT * FROM patterns WHERE format = %s"
            values = (format, )
            cursor.execute(sql, values)
            results = cursor.fetchall()

            if not results:
                return None

            patterns = []
            for row in results:
                patterns.append(self.convertToDictionaryPatterns(row))
            return patterns
        
        except Exception as e:
            print(f"Database error in findByFormat: {e}")
            raise
        finally:
            self.closeAll()

    def findByUserID(self, userID):
        """Get the patterns owned by a specific userID."""
        try:
            cursor = self.getCursor()
            sql = "SELECT * FROM patterns WHERE userID = %s"
            values = (userID, )
            cursor.execute(sql, values)
            results = cursor.fetchall()

            if not results:
                return None
            
            patterns = []
            for row in results:
                patterns.append(self.convertToDictionaryPatterns(row))
            return patterns
        
        except Exception as e:
            print(f"Database error in findByUserID: {e}")
            raise
        finally:
            self.closeAll()
    
    def create(self, pattern):
        """Insert a new sewing pattern into the patterns table."""
        try:
            cursor = self.getCursor()
            sql = "INSERT INTO patterns (patternID, brand, category, fabric_type, description, format, userID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = [pattern['patternID'], pattern['brand'], pattern['category'], pattern['fabric_type'], pattern['description'], pattern['format'], pattern['userID']]
            cursor.execute(sql, values)
            self.connection.commit()
            newid = cursor.lastrowid
            return newid
        
        except Exception as e:
            print(f"Database error in create: {e}")
            raise
        finally:
            self.closeAll()
    
    def update(self, pattern):
        """Update a sewing pattern."""
        try:
            cursor = self.getCursor()
            sql = "UPDATE patterns SET brand = %s, category = %s, fabric_type = %s, description = %s, format = %s, userID= %s WHERE patternID = %s"
            values = (pattern.get("brand"), pattern.get("category"), pattern.get("fabric_type"), pattern.get("description"), pattern.get('format'), pattern.get('userID'), pattern.get("patternID"))
            cursor.execute(sql, values)
            self.connection.commit()
            return pattern
        except Exception as e:
            print(f"Database error in update: {e}")
            raise
        finally:
            self.closeAll()

    def delete(self, patternID):
        """Delete a sewing pattern by patternID."""
        try:
            cursor = self.getCursor()
            sql = "DELETE FROM patterns WHERE patternID = %s"
            values = (patternID, )
            cursor.execute(sql, values)
            self.connection.commit()
            print("Pattern deleted")

        except Exception as e:
            print(f"Database error in delete: {e}")
            raise
        finally:
            self.closeAll()

patternDAO = PatternDAO()