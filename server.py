from flask import Flask, url_for, request, redirect, abort, jsonify, render_template
from PatternDAO import patternDAO
from UserDAO import userDAO
from werkzeug.security import generate_password_hash

app = Flask(__name__, static_url_path='', static_folder='static')

# Flask application for managing sewing patterns and user accounts

###### Page Routes
@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/users')
def users():
    """Render the users page."""
    return render_template('users.html')

@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')

###### Pattern API Routes
# Get all patterns
@app.route('/patterns', methods = ['GET'])
def getAll():
    """Return a list of all sewing patterns."""
    try:
        return jsonify(patternDAO.getAll())
    
    except Exception as e:
        print(f"Error with getAll(), getting patterns: {e}")
        return jsonify({"error: Unable to get all patterns"}), 500


# Get a pattern by patternID
@app.route('/patterns/<patternID>', methods = ['GET'])
def findByID(patternID):
    """Find a pattern by its patternID."""
    try:
        pattern = patternDAO.findByID(patternID)

        if not pattern:
            return jsonify({"error": f"Pattern ID, {patternID} does not exist."}), 404
        return jsonify(pattern)
    
    except Exception as e:  
        print(f"Error finding pattern by ID: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
        

# Get patterns by brand
@app.route('/patterns/brand/<brand>', methods = ['GET'])
def findByBrand(brand):
    """Find patterns by a specific brand."""
    try:
        brand = patternDAO.findByBrand(brand)

        if not brand:
            return jsonify({"error": f"Pattern brand, {brand} does not exist."}), 404
        return jsonify(brand)
    
    except Exception as e:  
        print(f"Error finding pattern by brand: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# Find patterns by category
@app.route('/patterns/category/<category>', methods = ['GET'])
def findByCategory(category):
    """Find patterns by category."""
    try:
        category = patternDAO.findByCategory(category)

        if not category:
            return jsonify({"error": f"Pattern category, {category} does not exist."}), 404
        return jsonify(category)
    
    except Exception as e:  
        print(f"Error finding pattern by category: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Get patterns by fabric type
@app.route('/patterns/fabric_type/<fabric_type>', methods=['GET'])
def findByFabric(fabric_type):
    """Find patterns by fabric type"""
    try:
        fabric_type = patternDAO.findByFabric(fabric_type)
        
        if not fabric_type:
            return jsonify({"error": f"Pattern fabric type, {fabric_type} does not exist."}), 404
        return jsonify(fabric_type)
    
    except Exception as e:  
        print(f"Error finding pattern by fabric_type: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# Get patterns by format
@app.route('/patterns/format/<format>')
def findByFormat(format):
    """Find patterns by pattern format"""
    try:
        format = patternDAO.findByFormat(format)

        if not format:
            return jsonify({"error": f"Pattern format, {format} does not exist."}), 404
        return jsonify(format)
    except Exception as e:  
        print(f"Error finding pattern by format: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# Get patterns by userID
@app.route('/patterns/userID/<userID>')
def findByUserID(userID):
    """Find patterns by a specific userID."""
    try:
        userID = patternDAO.findByUserID(userID)

        if not userID:
            return jsonify({"error": f"Pattern userID, {userID} does not exist."}), 404
        return jsonify(userID)
    
    except Exception as e:  
        print(f"Error finding by userID: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# Create a pattern
@app.route('/patterns', methods=['POST'])
def create():
    """Create a new sewing pattern."""
    if not request.json:
        abort(400)
    
    # Used Chat GPT - how to handle missing fields
    required_fields = ["patternID", "brand", "category", "fabric_type", "description", "format", "userID"]

    # Return an error if all fields are not in the request.
    for field in required_fields:
        if field not in request.json:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    pattern_id = request.json["patternID"]
    user_id = request.json["userID"]

    # Check if patternID already exists.
    # If it does, return an error message. 
    if patternDAO.findByID(pattern_id):
        return jsonify({"error": "pattern_id_exists"}), 400
    
    # Check that the userID exists in the users database.
    # If not, return an error message.
    if not userDAO.findByUserID_users(user_id):
        return jsonify({"error": "user_id_not_found"}), 400
    
    try:
        pattern = {
            "patternID": request.json["patternID"],
            "brand": request.json["brand"],
            "category": request.json["category"],
            "fabric_type": request.json["fabric_type"],
            "description": request.json["description"],
            "format": request.json["format"],
            "userID": request.json["userID"]
        }
        
        result = patternDAO.create(pattern)
        return jsonify(result), 201
    
    except Exception as e:
        print(f"Error creating pattern: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# Update an existing pattern.
@app.route('/patterns/<patternID>', methods=['PUT'])
def update_pattern(patternID):
    """Update an existing pattern by its patternID"""

    user_id = request.json["userID"]

    if not userDAO.findByUserID_users(user_id):
        return jsonify({"error": "user_id_not_found"}), 400
    
    try:
        # Find the pattern to update
        foundPattern = patternDAO.findByID(patternID)
        print (foundPattern)
        if not foundPattern:
            return jsonify({"error": f"Pattern with ID {patternID} not found"}), 404
        
        currentPattern = foundPattern
        
        # Update fields found in the request. 
        if 'patternID' in request.json:
            currentPattern['patternID'] = request.json['patternID']
        if 'brand' in request.json:
            currentPattern['brand'] = request.json['brand']
        if 'category' in request.json:
            currentPattern['category'] = request.json['category']
        if 'fabric_type' in request.json:
            currentPattern['fabric_type'] = request.json['fabric_type']
        if 'description' in request.json:
            currentPattern['description'] = request.json['description']
        if 'format' in request.json:
            currentPattern['format'] = request.json['format']
        if 'userID' in request.json:
            currentPattern['userID'] = request.json['userID']
        patternDAO.update(currentPattern)
        return jsonify(currentPattern)
    
    except Exception as e:
        print(f"Error updating pattern: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


#  Delete a pattern
@app.route('/patterns/<patternID>', methods=['DELETE'])
def delete(patternID):
    try:
        patternDAO.delete(patternID)
        return jsonify({"done": True})
    except Exception as e:
        print(f"Error deleting a pattern: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


######## User Routes

# Get all users.
@app.route('/users', methods = ['GET'])
def get_all_users():
    """Return a list of all users"""
    try:
        print("in get all")
        users = userDAO.get_all_users()
        return jsonify(users)
    
    except Exception as e:
        print(f"Error fetching users {e}")
        return jsonify({"error": "Something went wrong with get_all_users."}), 500

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user account."""
    if not request.json:
        abort(400)

    try:
        user = {
            #"userID": request.json["userID"],
            "first_name": request.json["first_name"],
            "last_name": request.json["last_name"],
            "email": request.json["email"],
            "password": generate_password_hash(request.json["password"]),
        }

        new_user = userDAO.create_user(user)
        return jsonify(new_user), 201
    
    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "Failed to create user."}), 500

# Get user by userID
@app.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Return user information by userID."""
    try:
        user = userDAO.findByUserID_users(user_id)
        if user:
            return jsonify(user)
        return jsonify({"error": "User not found"}), 404
    
    except Exception as e:
        print(f"Error getting user: {e}")
        return jsonify({"error": "Internal Server Error with get_user_by_id."}), 500

# Update a user by userID
@app.route('/users/<userID>', methods=['PUT'])
def update_user(userID):
    """Update a user by userID"""
    try:
        foundUser = userDAO.findByUserID_users(userID)

        print(f"This is foundUser {foundUser}")
        if foundUser == {}:
            return jsonify({}), 404
        

        #if 'userID' in request.json:
        #    foundUser['userID'] = request.json['userID']
        if 'first_name' in request.json:
            foundUser['first_name'] = request.json['first_name']
        if 'last_name' in request.json:
            foundUser['last_name'] = request.json['last_name']
        if 'email' in request.json:
            foundUser['email'] = request.json['email']
        if 'password' in request.json:
            foundUser['password'] = generate_password_hash(request.json['password'])
        userDAO.update_user(foundUser)
        return jsonify(foundUser)
    except Exception as e:
        print(f"Error updating user: {e}")
        return jsonify({"error": "Internal Server Error with update_user."}), 500


#  Delete user by userID
@app.route('/users/<userID>', methods=['DELETE'])
def delete_user(userID):
    """Delete a user by userID"""
    try:
        userDAO.delete_user(userID)
        return jsonify({"done": True})
    except Exception as e:
        print(f"Error finding by delete_user: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
