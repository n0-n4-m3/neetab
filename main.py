from traceback import print_tb
from libraries import *
from reg import *
from add_problem import *

"""Загрузка начальной сраницы"""

display = "background-image:none;position:absolute;left:0;right:0;top:0;bottom:0;margin:auto;display:none"
blur = ".blur {filter: blur(0px)}"
make_new_problem = ".form_for_add_card {display: none;}"
user_login = ""

def header():
    print("dsfsdfs")
    if "user" in session:
        users = db.Users
        print(session["user"])
        user_login = users.find_one({"_id": ObjectId(session["user"])})["user_login"]
        header_bloc = ".first {display: inline;} .second {display: none;}"
        if users.find_one({"_id": ObjectId(session["user"])})["user_role"] == "Тимлид":
            make_new_problem = ".form_for_add_card {display: inline;}"
    else:
        user_login = ""
        header_bloc = ".first {display: none;} .second {display: inline;}"
    return render_template("header.html",user_login=user_login,header_bloc=header_bloc)

@app.route('/', methods=["GET"])
def index():
    if(display != "background-image:none;position:absolute;left:0;right:0;top:0;bottom:0;margin:auto;display:block"):
        data = db.Problems
        massiv0 = data.find({"status": 0})
        size0 = data.count_documents({"status": 0})

        massiv1 = data.find({"status": 1})
        size1 = data.count_documents({"status": 1})

        massiv2 = data.find({"status": 2})
        size2 = data.count_documents({"status": 2})
        return render_template('index.html', massiv0=massiv0, size0=size0, massiv1=massiv1, size1=size1, massiv2=massiv2, size2=size2, display=display,blur=blur,card=[],header=header)
    else:
        data = db.Problems
        users = db.Users
        massiv0 = data.find({"status": 0})
        size0 = data.count_documents({"status": 0})

        massiv1 = data.find({"status": 1})
        size1 = data.count_documents({"status": 1})

        massiv2 = data.find({"status": 2})
        size2 = data.count_documents({"status": 2})

        id_card = session["ObjId"]
        card = data.find_one({"_id": ObjectId(id_card)})

        admins = []
        workers = []
        buyers = []
        if(len(card["members"]) > 0):
            for i in card["members"]:
                user_role = users.find_one({"_id": ObjectId(i)})["user_role"]
                if user_role == "Заказчик":
                    buyers.append(users.find_one({"_id": ObjectId(i)})["user_name"])
                if user_role == "Рабочий":
                    workers.append(users.find_one({"_id": ObjectId(i)})["user_name"])
                if user_role == "Тимлид":
                    admins.append(users.find_one({"_id": ObjectId(i)})["user_name"])
        else:
            workers.append("Ну блин, никто не пдключился(")
        git_have = get_git(card['git'])
        return render_template('index.html', massiv0=massiv0, size0=size0, massiv1=massiv1, size1=size1, massiv2=massiv2, size2=size2, display=display,blur=blur, card=card, buyers=buyers, admins=admins, workers=workers,git=git_have,header=header)

@app.route('/join_to_problem', methods=['POST','GET'])
def join():
    users = db.Users
    print(session["user"])
    user_problems = users.find_one({"_id": ObjectId(session["user"])})

    problem = db.Problems
    id_problem = request.form.get("id_problem")
    find_join = problem.find_one({"_id": ObjectId(id_problem)})

    if len(find_join["members"]) == 0:
        find_join["status"] = 1

    find_join["members"].append(session["user"])
    problem.replace_one({"_id": ObjectId(id_problem)}, find_join)

    user_problems["my_problems"].append(id_problem)
    users.replace_one({"_id": ObjectId(session["user"])}, user_problems)
    return redirect('/')

""""Регистрация пользователей"""
@app.route('/add_to_db', methods=['POST'])
def add_user():
    add_user_to_db()# reg.py
    return redirect('/')

@app.route('/reg', methods=['POST'])
def reg():
    return render_template("reg.html")
"""Логин"""

@app.route('/login', methods=['POST'])
def login_page():
    return render_template("login.html")

@app.route('/login_page', methods=['POST'])
def login_def():
    message = 'Please login to your account'
    # if "user" in session:
    #     return redirect("/")
    if request.method == "POST":
        login = request.form.get("user_login")
        password = request.form.get("user_pasw")

        login_found = db.Users.find_one({"user_login": login})
        if login_found:
            login_val = login_found['user_login']
            id = login_found["_id"]
            passwordcheck = login_found['user_pas']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["user"] = str(id)
                return redirect('/')
            else:
                if "user" in session:
                    return redirect("/")
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'login not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

"""Добавления задачи"""
@app.route('/add_probem', methods=['POST'])
def asdasd():
    add_problem_to_db()# add_problem.py
    return redirect('/')

@app.route('/print_card', methods=['POST'])
def print_card():
    global display
    global blur
    session["ObjId"] = request.form.get("problem_id")
    if(session["ObjId"] != ''):
        display = "background-image:none;position:absolute;left:0;right:0;top:0;bottom:0;margin:auto;display:block"
        blur = ".blur {filter: blur(4px)}"
    else:
        blur = ".blur {filter: blur(0px)}"
        display = "background-image:none;position:absolute;left:0;right:0;top:0;bottom:0;margin:auto;display:none"
    return redirect('/')

@app.route('/close', methods=['POST'])
def close():
    global display
    global blur
    session["ObjId"] = ""
    print(session["ObjId"])
    if(session["ObjId"] != ''):
        display = "background-image:none;position:absolute;left:0;right:0;top:0;bottom:0;margin:auto;display:block"
        blur = ".blur {filter: blur(4px)}"
    else:
        blur = ".blur {filter: blur(0px)}"
        display = "background-image:none;position:absolute;left:0;right:0;top:0;bottom:0;margin:auto;display:none"
        print(display)
    return redirect('/')

@app.route('/add', methods=['POST'])
def add():
    return render_template('create_problem.html')

@app.route('/my_problems', methods=['POST'])
def my_problems():
    data = db.Problems
    users = db.Users
    massiv0 = data.find({"status": 0})
    size0 = data.count_documents({"status": 0})

    massiv1 = data.find({"status": 1})
    size1 = data.count_documents({"status": 1})

    massiv2 = data.find({"status": 2})
    size2 = data.count_documents({"status": 2})
    return render_template('my_problems.html', massiv0=massiv0, size0=size0, massiv1=massiv1, size1=size1, massiv2=massiv2, size2=size2)

@app.route('/about_us', methods=['POST'])
def about():
    return render_template('about_us.html')

#         user_data = records.find_one({"email": email})
#         new_email = user_data['email']
#         return render_template('logged_in.html', email=new_email)
app.run(host='0.0.0.0', port=3000)