import os
from flask import render_template, redirect, flash, url_for
from FormEntry import db,app, login_manager, bcrypt
from FormEntry.forms import RegistrationAccountForm, RegistrationForm, LoginForm, UpdateForm
from FormEntry.models import Pinfo, User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods=['GET','POST'])
def home():
    db.create_all()
    return render_template('home.html')

@app.route("/about")
def about():  
    return render_template('home.html')


def save_picture(form_picture, form_citizenship, form_firstname):
    print('function in ')
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_filename =  str(form_citizenship) + form_firstname + f_ext
    picture_path = os.path.join (app.root_path, 'static/form_pics', picture_filename)
    form_picture.save(picture_path)
    return picture_filename
 


@app.route("/registerform/<user_id>", methods=['GET','POST'])
@login_required
def register_form(user_id):
    form = RegistrationForm()
    userinfo = Pinfo.query.filter_by(user_id=user_id).first()
    if form.validate_on_submit():
        if userinfo:
            flash('Data already registered. You can only update them','danger')
            return ( redirect(url_for('register_form',user_id=current_user.id)))
        if form.picture.data :
            picture_name = save_picture(form.picture.data,form.citizenship.data,form.firstname.data)

        user = Pinfo( citizenship=form.citizenship.data, firstname = form.firstname.data,lastname=form.lastname.data,
                             sex=form.sex.data, dob=form.dob.data, picture=picture_name, user_id = current_user.id)
        db.session.add(user)
        db.session.commit()
        flash('Your form has been submitted','success')
        return redirect(url_for('submission'))
    return render_template('register_form.html',form=form, title='Register!!', userinfo=userinfo)

@app.route("/registeraccount", methods=['GET','POST'])  
def register_account():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationAccountForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been registered.','success')
        return redirect(url_for('login'))
    return render_template('register_account.html',form=form, title='Account Register')

@app.route("/login", methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash('Successfully logged in.','success')
        else:
            flash('Invalid Email or Password', 'danger')
        return redirect(url_for('home' ))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/<id>/update", methods=['GET','POST'])
@login_required
def update_info(id):
    form = UpdateForm()
    userinfo = Pinfo.query.filter_by(user_id=id).first()
    if form.validate_on_submit():
        print('validated to update')
        if form.picture.data :
            picture_name =  save_picture(form.picture.data,form.citizenship.data,form.firstname.data)
        userinfo.picture = picture_name
        userinfo.citizenship = form.citizenship.data
        userinfo.firstname = form.firstname.data
        userinfo.lastname = form.lastname.data
        userinfo.sex = form.sex.data
        userinfo.dob = form.dob.data
        db.session.add(userinfo)
        db.session.commit()
        flash('Account updated','success')
    form.picture.data = userinfo.picture
    form.citizenship.data = userinfo.citizenship
    form.firstname.data = userinfo.firstname
    form.lastname.data = userinfo.lastname
    form.sex.data = userinfo.sex
    form.dob.data = userinfo.dob
    return render_template('upd\del.html', form=form, userinfo=userinfo, id=id)

@app.route("/<id>/delete", methods=['POST'])
@login_required
def delete_info(id):
    userinfo = Pinfo.query.filter_by(user_id=id).first()
    db.session.delete(userinfo)
    db.session.commit()
    flash('Your info is deleted!','danger')
    return redirect(url_for('home'))


@app.route("/submitted")
def submission():
    return render_template('form_submitted.html', title='Form Submitted')

@app.route("/fbsignup/<id>", methods=['GET'])
def fb_signup(id):  
    userinfo = Pinfo.query.filter_by(user_id=id).first()
    if userinfo:
        return render_template('fb.html', userinfo=userinfo)
    else:
        return render_template('fb2.html')


@app.route("/fb_login")
def fb_login():
    return render_template('fb_login.html', title='Form Submitted')



    