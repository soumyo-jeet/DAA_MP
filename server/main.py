from flask import Flask, request, jsonify
from logics import *
from helpers import *

app = Flask(__name__)
# API to accept a.txt from user

# API to validate selected course by means of prerequisites and schedule conflicts and to provide plan A
# courses = ["CS101", "CS102", "CS103", "CS404", "CS201"]
# schedule = schedule_map('sample.txt', courses)
# print(schedule)
# get_plan_a(schedule)


@app.route('/plan_a', methods=['GET'])
def plan_a():
    selected_courses = request.get_json()
    
    print("Got: ", selected_courses)
    schedule = schedule_map('sample.txt', selected_courses)
    plan, conflicts = get_plan_a(schedule)
    return jsonify({
        'plan': plan,
        'conflicts': conflicts
    })
    
    


# API to accept weighted courses (preferences) and provide plan B
# priorities = {
#     "CS101": 10, 
#     "CS102": 20, 
#     "CS103": 50, 
#     "CS404": 60, 
#     "CS201": 70
# }

# get_plan_b(schedule, priorities=priorities)


@app.route('/plan_b', methods=['POST'])
def plan_b():
    data = request.get_json()

    print("TYPE:", type(data))
    print("DATA:", data)

    selected_courses = data['courses']
    priorities = data['priorities']

    print("COURSES:", selected_courses)
    print("PRIORITIES:", priorities)

    schedule = schedule_map('sample.txt', selected_courses)

    plan, score = get_plan_b(schedule, priorities)

    return jsonify({
        'plan': plan,
        'score': score
    })

if __name__ == '__main__':
    app.run(debug=True)