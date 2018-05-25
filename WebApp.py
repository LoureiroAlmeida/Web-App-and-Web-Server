#Flask
from flask import Flask, request, render_template

#Requests
import requests

#Create a object of Flask(Framework)
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/show_users")
def show_users():
    #Get the data from the WebServer
    users = requests.get("http://127.0.0.1:5001/users")

    if users.status_code != 200:
        # This means something went wrong.
    	raise Exception('GET /tasks/ %s' % (users.status_code))
    
    
    return render_template("show_users.html", users=users.json())

@app.route("/show_kegs")
def show_kegs():
    #Get the data from the table Keg
    kegs = requests.get("http://127.0.0.1:5001/kegs")
    
    if kegs.status_code != 200:
        # This means something went wrong.
    	raise Exception('GET /tasks/ %s' % (kegs.status_code))
    
    return render_template("show_kegs.html", kegs=kegs.json())

@app.route("/show_users/<int:user_id>")
def show_task_user(user_id):
    #Get the data from the data User
    user = requests.get("http://127.0.0.1:5001/users/{}".format(user_id))
    
    if user.status_code != 200:
        # This means something went wrong.
    	raise Exception('GET /tasks/ %s' % (user.status_code))
    
    return render_template("show_task_user.html", user=user.json())

@app.route("/show_kegs/<int:keg_id>")
def show_task_keg(keg_id):
    #Get the data from the table Keg
    keg = requests.get("http://127.0.0.1:5001/kegs/{}".format(keg_id))
    
    if keg.status_code != 200:
        # This means something went wrong.
    	raise Exception('GET /tasks/ %s' % (keg.status_code))
    
    return render_template("show_task_keg.html", keg=keg.json())

@app.route("/insert_user", methods=['GET', 'POST'])
def insert_user():
    if (request.method == "GET"):
        return render_template("insert_user.html")
    
    elif(request.method == "POST"):  
        user = {
        'username': request.form.get('username'),
        'fullname': request.form.get('fullname'),
        'email': request.form.get('email'),
        'password': request.form.get('password'),
        'nfc_id': request.form.get('nfc_id'),
        'user_flow': request.form.get('user_flow'),
        }
        
        user = requests.post("http://127.0.0.1:5001/users", json=user)
        
        if user.status_code != 201:
            # This means something went wrong.
            raise Exception('GET /tasks/ %s' % (user.status_code))
    
        return show_users()
    
@app.route("/insert_keg", methods=['GET', 'POST'])
def insert_keg():
    if (request.method == "GET"):
        return render_template("insert_keg.html")
    
    elif(request.method == "POST"):
        keg = {
        'keg_id': request.form.get('keg_id'),
        'keg_flow': 0.0,
        }
        
        keg = requests.post("http://127.0.0.1:5001/kegs", json=keg)
        
        if keg.status_code != 201:
            # This means something went wrong.
            raise Exception('GET /tasks/ %s' % (keg.status_code))
    
        return show_kegs()
    
@app.route("/update_user/<int:user_id>", methods=['GET', 'POST'])
def update_user(user_id):
    if (request.method == "GET"):
        user = requests.get("http://127.0.0.1:5001/users/{}".format(user_id))
    
        if user.status_code != 200:
            # This means something went wrong.
            raise Exception('GET /tasks/ %s' % (user.status_code))
        
        return render_template("update_user.html", user=user.json())
    elif(request.method == "POST"):
        user = {
        'username': request.form.get('username'),
        'fullname': request.form.get('fullname'),
        'email': request.form.get('email'),
        'password': request.form.get('password'),
        'nfc_id': request.form.get('nfc_id'),
        'user_flow': request.form.get('user_flow'),
        }
       
        user = requests.put("http://127.0.0.1:5001/users/{}".format(user_id), json=user)
        
        if user.status_code != 200:
            # This means something went wrong.
            raise Exception('GET /tasks/ %s' % (user.status_code))
       
        return show_users()
    
@app.route("/update_keg/<int:keg_id>", methods=['GET', 'POST'])
def update_keg(keg_id):
    if (request.method == "GET"):
        keg = requests.get("http://127.0.0.1:5001/kegs/{}".format(keg_id))
    
        if keg.status_code != 200:
            # This means something went wrong.
            raise Exception('GET /tasks/ %s' % (keg.status_code))
        
        return render_template("update_keg.html", keg=keg.json())
    elif(request.method == "POST"):
        keg = {
        'keg_id': request.form.get('keg_id'),
        'keg_flow': request.form.get('keg_flow'),
        }
       
        keg = requests.put("http://127.0.0.1:5001/kegs/{}".format(keg_id), json=keg)
       
        if keg.status_code != 200:
            # This means something went wrong.
            raise Exception('GET /tasks/ %s' % (keg.status_code))
        
        return show_kegs()

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    status = requests.delete("http://127.0.0.1:5001/users/{}".format(user_id))

    return render_template("delete_user.html", status=status.json())

@app.route("/delete_keg/<int:keg_id>")
def delete_keg(keg_id):
    status = requests.delete("http://127.0.0.1:5001/kegs/{}".format(keg_id))
        
    return render_template("delete_keg.html", status=status.json())



if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=5000)