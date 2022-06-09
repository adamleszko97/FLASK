from tkinter import E
from flask import Blueprint, render_template, request, flash, session, jsonify
from flask_login import login_required, current_user
from .models import employees
from . import db
from . import engine
from sqlalchemy.orm import sessionmaker
import json


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    result=[]

    if request.method == 'POST':
        Session = sessionmaker(engine)
        session = Session()

        if request.form.get('Search') == 'Search':
            name_form = request.form.get('name_search')
            if(len(name_form) > 2):
                result = session.query(employees).filter(employees.first_name.match(name_form)).all()

                if result:
                    flash('Users found!')

                else:
                    flash('Users not found', category='error')  

            else:
                flash('Please provide more than 2 characters', category='error')

        elif request.form.get('Search All') == 'Search All':
            flash('All employees listed')
            result = session.query(employees).order_by(employees.last_name.asc()).all()


        session.close()
    return render_template("search.html", user=current_user, rows=result)


@views.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():

    Session = sessionmaker(engine)
    session = Session()

    raw_data = session.query(employees.department.distinct()).all()
    department_list = [item[0] for item in raw_data]

    print(department_list)


    if request.method == 'POST':
        name_add = request.form.get('add_name')
        lastname_add = request.form.get('add_lastname')
        phonenumber_add = request.form.get('add_phonenumber')
        department_add = request.form.get('add_department')

        print(name_add)

        if(len(name_add) <= 2):
            
            flash("First name has to be at lest 2 characters long", category='error')

        elif(len(lastname_add) <= 2):
            
            flash("First name has to be at lest 2 characters long", category='error')

        elif (len(phonenumber_add) <=6 ):

            flash("Last name has to be at lest 6 characters long", category='error')
        
        elif department_add == None:
            
           flash("Please choose Department", category='error')

        else:
            new_employee = employees(first_name=name_add, last_name=lastname_add, phone_number=phonenumber_add, department=department_add)
            session.add(new_employee)
            session.commit()
            flash('Employee Added!', category='success')
        session.close()

    return render_template("add_employee.html", dept_list=department_list)


@views.route('/delete-employee', methods=['POST'])
def delete_employee():

    Session = sessionmaker(engine)
    session = Session()

    employee = json.loads(request.data)
    employeeId = employee['employeeId']
    employee = session.query(employees).filter_by(id=employeeId)
    if employee:
        employee.delete()
        session.commit()
        flash('Employee Deleted')
        return jsonify({})
    else:
        flash('user does not exist', category='error')