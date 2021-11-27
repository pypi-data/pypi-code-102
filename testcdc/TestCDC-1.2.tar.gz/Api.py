from flask import Flask, jsonify


app = Flask(__name__)

# Characters
# Wheel of Time
db=dict({})

@app.route('/')
def getTitle():
    return "Flask is running\nWelcome to The Wheel of Time"


# Using the GET method
#@app.route("/characters", methods=['GET'])
#def getCharacters():
#    return jsonify({'Characters': db})


# To get character based on user choice
@app.route("/characters/<int:characterId>", methods=['GET'])
def getCharacterById(characterId):
    return jsonify({'Character': db[characterId]})


# Using the POST method
# curl -i -H "Content-Type: Application/json" -X POST http://127.0.0.1:5000/characters
# Use the above link in windows cmd
#@app.route("/characters", methods=['POST'])
#def addCharacter():
#    character = {'id': "7", 'name': "Trollocs", 'gender': "Male",
#                 'description': "Wretched, horrifying amalgams of man and beast, these towering Shadowspawn are the "
#                                "core of the Dark One's army. While their appearances are varied — some with horns, "
#                                "others with beaks or snarled snouts — one thing is universal: their murderous rage. "
#                                "They possess a ferocious bloodlust, and can only be controlled by the equally "
#                                "terrifying Fades."}
#
#    db.append(character)
#    return jsonify({'Added Character': character})


# Using the PUT method to update database
# curl -i -H "Content-Type: Application/json" -X PUT http://127.0.0.1:5000/characters/4
@app.route("/characters/<int:characterId>", methods=['PUT'])
def updateCharacter(characterId):
    db[characterId]['description'] = "This is the updated description for the character selected"
    return jsonify({'Characters': db[characterId]})


# Using the DELETE method to delete a character
# curl -i -H "Content-Type: Application/json" -X DELETE http://127.0.0.1:5000/characters/3
@app.route("/characters/<int:characterId>", methods=['DELETE'])
def deleteCharacter(characterId):
    db.remove(db[characterId])
    return jsonify({'Result': True})

@app.route("/dataset", methods=['GET'])
def getCharacters():
    return jsonify({'Data ': db})

@app.route("/dataset", methods=['POST'])
def addCharacter(datadict):
    db.append(datadict)
    return jsonify({'Added Data': datadict})

if __name__ == '__main__':
    app.run(debug=True)


def AddUpdate(datadict):
    print(addCharacter(datadict))
    
    
def DispData():
    print(getCharacters())
    
