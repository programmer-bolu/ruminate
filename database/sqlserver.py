from mysql import connector
import random
from datetime import datetime
import numpy as np

data = connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Ilerioluwa1@",
    database = "InkSpire"
)

connect = data.cursor()

# categories = [
#         "Artificial Intelligence",
#         "Gadgets & Reviews",
#         "Software Development",
#         "Cybersecurity",
#         "Tech News",
#         "Health & Wellness",
#         "Travel",
#         "Home & Garden",
#         "Minimalism",
#         "Relationships",
#         "Entrepreneurship",
#         "Marketing & Sales",
#         "Leadership & Management",
#         "Finance & Investing",
#         "Startups",
#         "Productivity",
#         "Mindfulness & Meditation",
#         "Motivation & Inspiration",
#         "Career Development",
#         "Education & Learning",
#         "Writing & Literature",
#         "Photography",
#         "Music",
#         "Art & Design",
#         "Film & Theater",
#         "Recipes",
#         "Restaurant Reviews",
#         "Cooking Tips & Techniques",
#         "Nutrition",
#         "Wine & Spirits",
#         "Movies & TV Shows",
#         "Music & Concerts",
#         "Books & Literature",
#         "Video Games",
#         "Celebrity News",
#         "Trends & Styles",
#         "Beauty Tips & Tutorials",
#         "Fashion Industry News",
#         "Skincare",
#         "Makeup Reviews",
#         "Workout Routines",
#         "Sports News",
#         "Nutrition & Diet",
#         "Fitness Tips",
#         "Athlete Interviews",
#         "Space Exploration",
#         "Environmental Issues",
#         "Wildlife & Conservation",
#         "Health & Medicine",
#         "Research & Discoveries",
#         "Car Reviews",
#         "Maintenance Tips",
#         "Industry News",
#         "Motorcycles",
#         "Electric Vehicles",
#         "Parenting Tips",
#         "Child Development",
#         "Family Activities",
#         "Education & Schooling",
#         "Work-Life Balance",
#         "Personal Finance",
#         "Investing Tips",
#         "Market News",
#         "Retirement Planning",
#         "Real Estate",
#         "Home Improvement",
#         "Craft Projects",
#         "Tutorials & How-Tos",
#         "Sustainable Living",
#         "Upcycling Ideas",
#         "Destination Guides",
#         "Travel Tips",
#         "Cultural Experiences",
#         "Adventure Sports",
#         "Budget Travel",
#         "Game Reviews",
#         "Industry News",
#         "Tips & Tricks",
#         "Esports",
#         "Game Development",
#         "Pet Care Tips",
#         "Animal Behavior",
#         "Pet Health",
#         "Wildlife Conservation",
#         "Pet Training",
#         "Sustainable Practices",
#         "Renewable Energy",
#         "Eco-Friendly Products",
#         "Organic Gardening",
#         "Climate Change",
#         "Historical Events",
#         "Biographies",
#         "Archaeology",
#         "War & Conflict",
#         "Cultural History",
#         "Human Rights",
#         "Equality & Justice",
#         "Politics & Government",
#         "Community Development",
#         "Mental Health Awareness"
#     ]

   
# connect.execute('CREATE DATABASE IF NOT EXISTS InkSpire')

# connect.execute('CREATE TABLE allusers (id INTEGER PRIMARY KEY AUTO_INCREMENT, email VARCHAR(255), name VARCHAR(255), age VARCHAR(255), password VARCHAR(255))')
# connect.execute('CREATE TABLE confirmedUsers (id INTEGER PRIMARY KEY AUTO_INCREMENT, email VARCHAR(255), name VARCHAR(255), user_id VARCHAR(255), age VARCHAR(255), password VARCHAR(255), profilePicture VARCHAR(255))')
# connect.execute('CREATE TABLE blogs (id INTEGER PRIMARY KEY AUTO_INCREMENT, blog_details LONGTEXT, date_created VARCHAR(255), date_updated VARCHAR(255), views INTEGER, comments LONGTEXT, stars LONGTEXT)')
# connect.execute('ALTER TABLE blogs ADD COLUMN (title LONGTEXT, description LONGTEXT, author_id VARCHAR(255), author_name VARCHAR(255), categories VARCHAR(255))')
# connect.execute('ALTER TABLE blogs ADD COLUMN (image_link VARCHAR(255), image_description VARCHAR(255))')
# connect.execute('ALTER TABLE blogs CHANGE COLUMN `categories` `categories` LONGTEXT NULL DEFAULT NULL')
# connect.execute('ALTER TABLE blogs DROP COLUMN blog_details')
# connect.execute('CREATE TABLE verification_codes (id INTEGER PRIMARY KEY AUTO_INCREMENT, email VARCHAR(255), code VARCHAR(255) )')
# connect.execute('CREATE TABLE categories (id INTEGER PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), posts_under_category VARCHAR(255))')
# for i in categories:
#     value = [i, 0]
#     connect.execute('INSERT INTO categories (name, posts_under_category) VALUES(%s, %s)', value)
#     data.commit()


def check_email(email):
    connect.execute('SELECT * FROM allusers')
    data = connect.fetchall()
    emin = []
    for user in data:
        if user[1] == email:
            emin.append(user)

    if len(emin) >= 1:
        return False
    else:
        return True  

def get_age(email):
    connect.execute(f'SELECT age FROM allusers WHERE email="{email}"')
    data2 = connect.fetchall()
    birthdate = data2[0][0]
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
    today = datetime.today()
    age = today.year - birthdate.year
    if((today.month, today.day) <  (birthdate.month, birthdate.day)):
        age -= 1
    
    return age
    
def create_verification_code(email):
    connect.execute(f'SELECT * FROM verification_codes')
    data2 = connect.fetchall()
    check = []
    for i in data2:
        if email == i[1]:
            check.append(i)

    if len(check) == 0:
        code = random.randint(100000, 999999)
        dat = [email, code]
        connect.execute('INSERT INTO verification_codes (email, code) VALUES (%s, %s)', dat)
        data.commit()
    else:
        pass

def confirm_verification_code(email, code):
    connect.execute(f'SELECT code FROM verification_codes WHERE email="{email}"')
    dat = connect.fetchall()
    dat = dat[0][0]
    if code == dat:
        connect.execute(f'DELETE FROM verification_codes WHERE email="{email}"')
        data.commit()
        return True
    else:
        return False

def save_user(email, name, password):
    if checkId() == None:
        dat = [email, name, 'jqhwo9q87q28q9nqw', password]
        connect.execute("INSERT INTO confirmedusers (email, name, user_id ,password) VALUES (%s,%s,%s,%s)", dat)
        data.commit()

    elif checkId()[0] == True:
        dat = [email, name, get_age(email), checkId()[1], password]
        connect.execute("INSERT INTO confirmedusers (email, name, age, user_id ,password) VALUES (%s,%s, %s,%s,%s)", dat)
        data.commit()

def checkId():
    idvar = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    userId = []
    new = []
    for i in range(10):
        userId.append(random.choice(idvar))
        
    connect.execute(f'SELECT user_id FROM confirmedusers')
    data = connect.fetchall()
    fet = ''
    for i in userId:
        fet += str(i)

    for i in data:
        if fet == i:
            new.append(i)

    if len(new) > 0:
        checkId()
    else:
        return [True, fet]

def encrypt(password):
    passer = []
    encrypted = ''
    encryptPasswordKey = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    j = 0

    for i in range(0, len(password) * 3):
        passer.append(str(random.choice(encryptPasswordKey)))
        if i % 3 == 0:
            passer.append(str(password[j]))
            j+=1

    for i in passer:
        encrypted += i

    return encrypted

def decrypt(value):
    breaker = []
    password = ''
    for i in value:
        breaker.append(i)
    breaker = np.array(breaker)
    final = breaker[1::4]
    for i in final:
        password += i

    return password

def check_all(email, password):
    connect.execute(f'SELECT * FROM allusers')
    data2 = connect.fetchall()
    j = 0
    for i in data2:
        if email == i[1]:
            if password == decrypt(i[4]):
                return [False, i]
            else:
                return 'Wrong Password'
        else:
            j += 1
            if j == len(data2):
                return 'No User With Email'

def check_login(email, password):
    connect.execute(f'SELECT * FROM confirmedusers')
    data = connect.fetchall()
    j = 0
    if len(data) >= 1:
        for i in data:
            if email == i[1]:
                if password == decrypt(i[5]):
                    return [True, i]
                else:
                    return 'Wrong Password'
            else:
                j += 1
                if j == len(data):
                    return check_all(email, password)
    else:
        return check_all(email, password)

def get_user(email):
    connect.execute(f'SELECT * FROM allusers WHERE email="{email}"')
    data2 = connect.fetchall()
    return {'name': data2[0][2], 'password': data2[0][4]}

def check_confirmed_user(email):
    connect.execute(f'SELECT * FROM confirmedusers')
    data = connect.fetchall()
    for i in data:
        if email == i[1]:
            return True
        
    return False

def get_categories(post_categories):
    connect.execute('SELECT * FROM categories')
    category = connect.fetchall()
    for i in category:
        if i[1] in post_categories:
            connect.execute(f'UPDATE categories SET posts_under_category = "{int(i[2]) + 1}" WHERE name = "{i[1]}"')
            data.commit()

def categories():
    connect.execute('SELECT * FROM categories')
    category = connect.fetchall()
    cat = []
    for i in category:
        if int(i[2]) >= 1:
            cat.append(i[1])
    return cat

def get_id(email):
    connect.execute(f'SELECT user_id FROM confirmedusers WHERE email="{email}"')
    data = connect.fetchall()
    return data[0][0]

def get_user_data(id):
    connect.execute(f'SELECT * FROM confirmedusers WHERE user_id="{id}"')
    data = connect.fetchall()
    return {'name': data[0][2], 'email': data[0][1], 'age': data[0][4], 'profile_picture': data[0][6]}

def fetch_user_blogs(id):
    connect.execute(f'SELECT * FROM blogs WHERE author_id="{id}"')
    data = connect.fetchall()
    return data

def get_blog(id, title):
    connect.execute(f'SELECT * FROM blogs WHERE author_id="{id}" AND title="{title}"')
    data = connect.fetchall()
    return data

def get_all_blogs():
    connect.execute(f'SELECT * FROM blogs')
    data = connect.fetchall()
    return data