#!flask/bin/python
#Flask
from flask import Flask, jsonify, abort, make_response, request

#ORM
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from sqlalchemy_declarative import User, Base, Keg

app = Flask(__name__)

#Insert data in the table User
def insert_data_User(username, fullname, email, password, nfc_id, user_flow):
    new_user = User(username=username, fullname=fullname, email=email, password=password, nfc_id=nfc_id, user_flow=user_flow)
    session.add(new_user)
    session.commit()
    
#Insert data in the table Keg
def insert_data_Keg(keg_id, keg_flow):
    new_keg = Keg(keg_id=keg_id, keg_flow=keg_flow)
    session.add(new_keg)
    session.commit()

#Update data in the table User
def update_data_User(user_id, username, fullname, email, password, nfc_id, user_flow):
    user = session.query(User).filter_by(id=user_id).one()
    
    if(username != user.username and username != ''):
        user.username = username
    if(fullname != user.fullname and fullname != ''):
        user.fullname = fullname
    if(email != user.email and email != ''):
        user.email = email
    if(password != user.password and password != ''):
        user.password = password
    if(nfc_id != user.nfc_id and nfc_id != ''):
        user.nfc_id = nfc_id
    if(user_flow != user.user_flow and user_flow != ''):
        user.user_flow = user_flow
        
    session.add(user)
    session.commit()
    
#Update data in the table Keg
def update_data_Keg(id, keg_id, keg_flow):
    keg = session.query(Keg).filter_by(id=id).one()
    
    if(keg_id != keg.keg_id and keg_id != ''):
        keg.keg_id = keg_id
    if(keg_flow != keg.keg_flow and keg_flow != ''):
        keg.keg_flow = keg_flow
        
    session.add(keg)
    session.commit()
    
#Remove data from table User
def remove_data_User(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    session.delete(user)
    session.commit()

#Remove data from table Keg
def remove_data_Keg(keg_id):
    keg = session.query(Keg).filter_by(id=keg_id).one()
    session.delete(keg)
    session.commit()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/users', methods=['GET'])
def get_users():
    users = session.query(User).all()

    list_users = []
    for row in users:
        list_users.append({
                    'id': row.id,
                    'username': row.username,  
                    'fullname': row.fullname,
                    'email': row.email,
                    'password': row.password,
                    'nfc_id': row.nfc_id,
                    'user_flow': row.user_flow,
                })
        
    return jsonify({'users': list_users})

@app.route('/kegs', methods=['GET'])
def get_kegs():
    kegs = session.query(Keg).all()
    
    list_kegs = []
    for row in kegs:
        list_kegs.append({
                        'id': row.id,
                        'keg_id': row.keg_id,
                        'keg_flow': row.keg_flow,
                        })
        
    return jsonify({'kegs': list_kegs})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    users = session.query(User).all()
    for row in users:
        if(user_id == row.id):
            user = {
                    'id': row.id,
                    'username': row.username,  
                    'fullname': row.fullname,
                    'email': row.email,
                    'password': row.password,
                    'nfc_id': row.nfc_id,
                    'user_flow': row.user_flow,
                }   
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user})

@app.route('/kegs/<int:keg_id>', methods=['GET'])
def get_one_keg(keg_id):
    kegs = session.query(Keg).all()
    for row in kegs:
        if(keg_id == row.id):
            keg = {
                    'id': row.id,
                    'keg_id': row.keg_id,  
                    'keg_flow': row.keg_flow,
                }   
    if len(keg) == 0:
        abort(404)
    return jsonify({'keg': keg})

@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'fullname' in request.json or not 'email' in request.json or not 'password' in request.json or not 'nfc_id' in request.json or not 'user_flow' in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'fullname': request.json['fullname'],
        'email': request.json['email'],
        'password': request.json['password'],
        'nfc_id': request.json['nfc_id'],
        'user_flow': request.json['user_flow'],
    }
    insert_data_User(user['username'], user['fullname'], user['email'], user['password'], user['nfc_id'], user['user_flow'])
    return jsonify({'user': user}), 201

@app.route('/kegs', methods=['POST'])
def create_keg():
    if not request.json or not 'keg_id' in request.json or not 'keg_flow' in request.json:
        abort(400)
    keg = {
        'keg_id': request.json['keg_id'],
        'keg_flow': request.json['keg_flow'],
    }
    insert_data_Keg(keg['keg_id'], keg['keg_flow'])
    return jsonify({'keg': keg}), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    users = session.query(User).all()
    if not request.json:
        abort(400)
    for row in users:
        if(user_id == row.id):
            user = {
                    'username': request.json['username'],
                    'fullname': request.json['fullname'],
                    'email': request.json['email'],
                    'password': request.json['password'],
                    'nfc_id': request.json['nfc_id'],
                    'user_flow': request.json['user_flow'],
                    }
    if len(user) == 0:
        abort(404)
    update_data_User(user_id, user['username'], user['fullname'], user['email'], user['password'], user['nfc_id'], user['user_flow'])
    return jsonify({'user': user})

@app.route('/kegs/<int:keg_id>', methods=['PUT'])
def update_keg(keg_id):
    kegs = session.query(Keg).all()
    if not request.json:
        abort(400)
    for row in kegs:
        if(keg_id == row.id):
            keg = {
                    'keg_id': request.json['keg_id'],  
                    'keg_flow': request.json['keg_flow'],
                }
    if len(keg) == 0:
        abort(404)
    
    update_data_Keg(keg_id, keg['keg_id'], keg['keg_flow'])
    return jsonify({'keg': keg})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    users = session.query(User).all()
    for row in users:
        if(user_id == row.id):
            remove_data_User(user_id)
            return jsonify({'result': True})  

@app.route('/kegs/<int:keg_id>', methods=['DELETE'])
def delete_keg(keg_id):
    kegs = session.query(Keg).all()
    for row in kegs:
        if(keg_id == row.id):
            remove_data_Keg(keg_id)
            return jsonify({'result': True})
        

if __name__ == '__main__':
    path_to_database = "BeerBase.db"    
    engine = create_engine('sqlite:///'+path_to_database) 
    Base.metadata.bind = engine
     
    DBSession = sessionmaker(bind=engine)

    session = DBSession()
    app.run('0.0.0.0',debug=True, port=5001)

