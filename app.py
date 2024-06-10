from flask import Flask, render_template, request, url_for, jsonify, redirect, session
import json
import random
from database import sqlserver as sv
import numpy as np
from process_image import image_url as ig
from datetime import datetime, timedelta
import os
app = Flask(__name__)

app.secret_key = os.urandom(24)

def is_less_than_24_hours(time_str):
    # Parse the given time string
    given_time = datetime.strptime(time_str, '%d/%m/%Y, %H:%M')
    
    # Get the current time
    current_time = datetime.now()
    
    # Calculate the difference between the given time and current time
    time_difference = current_time - given_time
    
    # Check if the time difference is less than 24 hours
    if time_difference < timedelta(hours=24):
        return True
    else:
        return False
# """LANDING PAGE"""
@app.route('/')
def index():
    categories = sv.categories()
    random.shuffle(categories)
    blogs = sv.get_all_blogs()
    recent = []
    random.shuffle(blogs)
    for i in range(len(blogs)):
        blogs[i] = list(blogs[i])
        blogs[i][10] = eval(blogs[i][10])
        if is_less_than_24_hours(blogs[i][1]):
            recent.append(blogs[i])

    random.shuffle(recent)
        
    return render_template('index.html', categories = categories, blogs=blogs, recent=recent)

@app.route('/login')
def login():
    return render_template('login_page.html')

@app.route('/register')
def register():
    return render_template('signup.html')

@app.get('/submit_sign_up')
def submitsignup():
    name = request.args.get('name')
    email = request.args.get('email')
    age = request.args.get('date')
    password = request.args.get('password')
    password = sv.encrypt(password)
    if email == None or name == None or age == None or password == None:
        return redirect(url_for('register'))
    
    if sv.check_email(email) == True or sv.check_email(email) == None:
        userData = [email, name, age, password]
        push_to_server = 'INSERT INTO allusers (email, name, age, password) VALUES (%s, %s, %s, %s)'
        sv.connect.execute(push_to_server, userData)
        sv.create_verification_code(email)
        return jsonify(f'["true", "{email}"]')
    
    else:
        return jsonify('false')

@app.route('/Oauth/')
def confirm():
    email = request.args.get('email')

    if email == None:
        return redirect(url_for('register'))
    else:
        return render_template('confirmemail.html', email=email)

@app.get('/verify/')
def verify():
    email = request.args.get('email')
    code = request.args.get('code')
    session['blog_token'] = os.urandom(24).hex()
    

    if email == None or code == None:
        return redirect(url_for('register'))
    
    if sv.confirm_verification_code(email, code) == True:
        res = sv.get_user(email)
        name = res['name']
        token = session.get('blog_token')
        password = res['password']
        sv.save_user(email, name, password)
        id = sv.get_id(email)
        return jsonify(f'["true", "{id}", "{token}"]')
    else:
        return jsonify('false')

@app.post('/authlogin/another/vesel/ruminate/login/attack/disabled/true')
def AuthLog():
    element = request.json['data']
    email = element['email']
    password = element['password']
    session['blog_token'] = os.urandom(24).hex()
    
    if sv.check_login(email, password) == None:
        return jsonify('["res1" , "No User"]')

    elif sv.check_login(email, password)[0] == True:
        id = sv.get_id(email)
        token = session.get('blog_token')
        return jsonify(f'["res2", "{id}", "{token}" ]')
    
    elif sv.check_login(email, password)[0] == False:
        return jsonify(f'["res3" , "{sv.check_login(email, password)[1]}"]')
    
    elif sv.check_login(email, password) == 'Wrong Password':
        return jsonify(f'["res4" , "wrong password", "{password}"]')
    
    elif sv.check_login(email, password) == 'No User With Email':
        return jsonify('["res4" , "No User With Email"]')
    


    # return jsonify('true')

@app.get('/OauthLogin')
def OauthLogin():
    email = request.args.get('email')
    if email == None:
        return redirect(url_for('login'))
    
    if sv.check_email(email) == False:
        sv.create_verification_code(email)
        return jsonify('true')
    else:
        return jsonify('false')

@app.route('/forgotpassword/')
def forgotpassword():
    return render_template('forgotpassword.html')

@app.get('/forgotpassword/oauth/')
def forget():
    email = request.args.get('email')
    if email == None:
        return redirect(url_for('login'))
    return render_template('resetpasswordcode.html', email=email)

@app.get('/forgotpassword/oauth/process')
def conf():
    email = request.args.get('email')
    code = request.args.get('class')

    if email == None or code == None:
        return redirect(url_for('login'))

    elif sv.confirm_verification_code(email, code) == True:
        return jsonify(f'"{email}"')
    
    else:
        return jsonify('false')
    
@app.get('/changepassword')
def changepassword():
    email = request.args.get('email')
    details = sv.get_user(email)
    if email == None:
        return redirect(url_for('login'))
    
    return render_template('change_password.html', email=email, details=details)

@app.get('/newpassword')
def newpassword():
    email = request.args.get('email')
    oldpassword = sv.decrypt(sv.get_user(email)['password'])
    newpassword = request.args.get('password')
    name = sv.get_user(email)['name']
    if email == None or newpassword == None:
        return redirect(url_for('login'))
    
    if newpassword == oldpassword:
        return jsonify(f'false')
    else:
        if sv.check_confirmed_user(email) != True:
            sv.save_user(email, name, sv.encrypt(newpassword))
            sv.connect.execute(f'UPDATE allusers SET password="{sv.encrypt(newpassword)}" WHERE email="{email}"')
            sv.data.commit()
            return jsonify('true')
        else:
            sv.connect.execute(f'UPDATE confirmedusers SET password="{sv.encrypt(newpassword)}" WHERE email="{email}"')
            sv.connect.execute(f'UPDATE allusers SET password="{sv.encrypt(newpassword)}" WHERE email="{email}"')
            sv.data.commit()
            return jsonify('true')
    
@app.get('/blog')
def get_blog():
    author_id = request.args.get('author_id')
    title = request.args.get('blog_title')
    comments = sv.get_post_comment('author_id=' + author_id + '&blog_title=' + title)
    post_has_comment = len(comments)
    recent = []
    categories = sv.categories()
    random.shuffle(categories)
    blog = sv.get_blog(author_id, title)
    blog[0] = list(blog[0])
    blog[0][10] = eval(blog[0][10])
    for i in sv.get_all_blogs():
        if is_less_than_24_hours(i[1]):
            recent.append(i)
    random.shuffle(recent)

    return render_template('blog.html', blog=blog, categories=categories, recent=recent, comment=comments, hascomment = post_has_comment)

@app.get('/blogger/create/blog')
def create_blog():
    user_id = request.args.get('userId')
    return render_template('createblog.html', author_id=user_id, author_name = sv.get_user_data(user_id)['name'])

@app.route('/post', methods=['POST'])
def post():
    image = request.files.get('image')
    postinfo = json.loads(request.form.get('data'))
    title = postinfo['title']
    description = postinfo.get('description')
    date = postinfo.get('date')
    author = postinfo.get('Author')
    authorID = postinfo.get('user_id')
    categories = postinfo.get('categories')
    value = [date, title, description, authorID, author, categories]
    
    try:
        if image != None:
            imagelink = ig.upload_to_imgbb(image.read())['data']['url']
            imageDescription = postinfo.get('imagedescription')
            if imagelink.startswith('http'):
                value = [date, title, description, authorID, author, str(categories), imagelink, imageDescription]
                sv.get_categories(categories)
                sv.connect.execute('INSERT INTO blogs (date_created, title, description, author_id, author_name, categories, image_link, image_description) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', value)
                sv.data.commit()

                return jsonify('true')
            else:

                return jsonify('image error')
        else:
            value = [date, title, description, authorID, author, str(categories)]
            sv.get_categories(categories)
            sv.connect.execute('INSERT INTO blogs (date_created, title, description, author_id, author_name, categories) VALUES(%s, %s, %s, %s, %s, %s)', value)
            sv.data.commit()

            return jsonify('true')
    except:
        return jsonify('Network Error') 

@app.route('/category')
def category():
    return render_template('categories.html')

@app.get('/home')
def home():
    toke = request.args.get('token')
    id = request.args.get('user_id')
    if len(sv.fetch_user_blogs(id)) > 0:
        user_has_blogs = True
        blog = sv.fetch_user_blogs(id)
        for i in range(len(blog)):
            blog[i] = list(blog[i])
            blog[i][10] = eval(blog[i][10])
        return render_template('profile.html', user_name=sv.get_user_data(id)['name'], user_has_blogs=user_has_blogs, id=id, blogs=blog, bloglen = len(blog))
    else:
        user_has_blogs = False
        return render_template('profile.html', user_name=sv.get_user_data(id)['name'], user_has_blogs=user_has_blogs, id=id)

@app.post('/receive_comment/async')
def comment():
    comment = request.json.get('message')
    name = request.json.get('name')
    email = request.json.get('email')
    blog_aut = request.json.get('blog_aut')
    blog_tit = request.json.get('blog_tit')
    blog_id = 'author_id=' + blog_aut + '&blog_title=' + blog_tit
    date = request.json.get('time')
    blog = sv.get_blog(blog_aut, blog_tit)
    
    if blog[0][4] == None:
        sv.connect.execute(f'UPDATE blogs SET comments="1" WHERE author_id="{blog_aut}" AND title="{blog_tit}"')
    else:
        sv.connect.execute(f'UPDATE blogs SET comments="{int(blog[0][4]) + 1}" WHERE author_id="{blog_aut}" AND title="{blog_tit}"')
    post_comment = [name, email, comment, blog_id, date]
    send_to_server = 'INSERT INTO blog_comments (name, email, comment, blog_id, date) VALUES (%s, %s, %s, %s, %s)'
    sv.connect.execute(send_to_server, post_comment)
    sv.data.commit()
    return jsonify('true')

@app.route('/blog/allblogs')
def logout():
    blogs = sv.get_all_blogs()
    titles = []
    for i in blogs:
        titles.append([i[6], i[8]])
    random.shuffle(blogs)
    random.shuffle(titles)
    return render_template('blog_page.html', blogs=blogs, titles=titles)

@app.get('/blog/category')
def categ():
    category = request.args.get('category')
    blog = sv.get_categories(category)
    return render_template('blog_category.html', blogs=blog)

@app.route('/aboutus/ruminate')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contact/ruminate')
def contact():
    return render_template('contactus.html')

app.run(debug=True)