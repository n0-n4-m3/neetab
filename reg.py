from libraries import *

def add_user_to_db():
    users = db.Users

    user_name = request.form.get("fullname")
    role = request.form.get("role")
    user_login = request.form.get("user_login")
    user_pasw = request.form.get("user_pasw")

    user_exist = users.find_one({"user_login": user_login})
    print(user_login)

    if user_exist:
            message = 'There already is a user by that name'
            return redirect('/')
    else:
        hashed = bcrypt.hashpw(user_pasw.encode('utf-8'), bcrypt.gensalt())
        user_input = make_user(role, user_name, user_login, hashed)
        print(user_input["user_login"])
        users.insert_one(user_input)
    return redirect('/')