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
    task_list= mongo.db.tasks.find().sort([("due_date", -1)]) # Sorts so closest deadline first
    print(task_list)
    return render_template("tasks.html", tasks=task_list) #second part will store in var tasks, all of the items in the "task" collection

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

@app.route('/edit_task/<task_id>')#taskes task_id param and places in route
def edit_task(task_id):#task id is passed when edit button clicked
    the_task = mongo.db.tasks.find_one({"_id":ObjectId(task_id)})#has to use bson format to find in mongo
    all_categories = mongo.db.categories.find()
    return render_template('edit-task.html', task= the_task, categories= all_categories)

@app.route('/edit_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks # accesses the task collection
    tasks.update({'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'category_name':request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    }) #Gets the form values and places them into key,value pairs they are obtaining the values from form names
    return redirect(url_for('get_tasks'))

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))

if __name__ == '__main__':
    app.run(host = host, port = port, debug=True)
    