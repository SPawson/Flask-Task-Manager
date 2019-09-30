import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId # Allows mongo docs to be read

host = os.environ.get('IP')
port = int(os.environ.get('PORT'))
M_URI = os.environ.get('MONGO_URI')
app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'task_manager' #config is a dictionary and by using [] you are accessing the value for the key in [] e.g. config[key] = value
app.config["MONGO_URI"] = M_URI #Telling the app the connection link

mongo = PyMongo(app) #creates instance of PyMongo

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find()) #second part will store in var tasks, all of the items in the "task" collection

@app.route('/add_task')
def add_task():
    _categories= mongo.db.categories.find()
    category_list= [category for category in _categories]

    return render_template('addtask.html', categories= category_list)

@app.route('/insert_task', methods=["POST"])#When using post , it must be specified as a parameter, default is get
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict()) #uses flask request object to process form-data
    return redirect(url_for('get_tasks'))#On insert find the url for func get tasks and redirect there

if __name__ == '__main__':
    app.run(host = host, port = port, debug=True)