from libraries import *

def add_problem_to_db():
#     priority = request.form.get('priority')
#     print(session["priority"])
    problems = db.Problems
    problem = make_problem(request.form.get('priority'), request.form.get('who'), request.form.get('problem_name'), request.form.get('problem_dscr'), request.form.get('make_date'), request.form.get('dead_date'), request.form.get('git'))
    problems.insert_one(problem)
    session["priority"] = request.form.get('priority')
    return redirect('/')