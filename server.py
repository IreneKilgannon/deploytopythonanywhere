from flask import Flask, request, abort, jsonify, render_template
from flask_cors import CORS, cross_origin
from PatternDAO import patternDAO
from UserDAO import userDAO

app = Flask(__name__, static_url_path='', static_folder='static')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

##### Pattern Routes
# Get all patterns
@app.route('/patterns', methods = ['GET'])
@cross_origin()
def getAll():
    try:
        return jsonify(patternDAO.getAll())
    except Exception as e:
        print(f"Error with getAll(), getting patterns: {e}")
        return jsonify({"error: Unable to get all patterns"}), 500


# Find By patternID
@app.route('/patterns/<patternID>', methods = ['GET'])
@cross_origin()
def findByID(patternID):
    try:
        
        pattern = patternDAO.findByID(patternID)

        if not pattern:
            return jsonify({"error": f"Pattern ID, {patternID} does not exist."}), 404
        return jsonify(pattern)
    
    except Exception as e:  
        print(f"Error finding pattern by ID: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
        


# Find by Brand
@app.route('/patterns/brand/<brand>', methods = ['GET'])
@cross_origin()
def findByBrand(brand):
    try:
        brand = patternDAO.findByBrand(brand)

        if not brand:
            return jsonify({"error": f"Pattern brand, {brand} does not exist."}), 404
        return jsonify(brand)
    
    except Exception as e:  
        print(f"Error finding pattern by brand: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Find by Category
@app.route('/patterns/category/<category>', methods = ['GET'])
@cross_origin()
def findByCategory(category):
    try:
        category = patternDAO.findByCategory(category)

        if not category:
            return jsonify({"error": f"Pattern category, {category} does not exist."}), 404
        return jsonify(category)
    
    except Exception as e:  
        print(f"Error finding pattern by category: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Find by Fabric Type
@app.route('/patterns/fabric_type/<fabric_type>', methods=['GET'])
@cross_origin()
def findByFabric(fabric_type):
    try:
        fabric_type = patternDAO.findByFabric(fabric_type)
        
        if not fabric_type:
            return jsonify({"error": f"Pattern fabric type, {fabric_type} does not exist."}), 404
        return jsonify(fabric_type)
    except Exception as e:  
        print(f"Error finding pattern by fabric_type: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
# Find by patterns by userID
@app.route('/patterns/userID/<userID>')
@cross_origin()
def findByUserID(userID):
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
@cross_origin()
def create():
    if not request.json:
        abort(400)
    
    # Chat GPT - handling missing fields
    # Do not add to db if required field missing. 
    required_fields = ["patternID", "brand", "category", "fabric_type", "description", "format", "userID"]

    for field in required_fields:
        if field not in request.json:
            return jsonify({"error": f"Missing required field: {field}"}), 400
                           
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


# Update a pattern
@app.route('/patterns/<patternID>', methods=['PUT'])
@cross_origin()
def update_pattern(patternID):
    try:
        foundPattern = patternDAO.findByID(patternID)
        print (foundPattern)
        if not foundPattern:
            return jsonify({{"error": f"Pattern with ID {patternID} not found"}}), 404
        currentPattern = foundPattern
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


#  Delete
@app.route('/patterns/<patternID>', methods=['DELETE'])
@cross_origin()
def delete(patternID):
    patternDAO.delete(patternID)
    return jsonify({"done": True})


if __name__ == "__main__":
    app.run(debug=True)
