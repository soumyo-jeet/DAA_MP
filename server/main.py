import os

from flask import Flask, request, jsonify
from logics import *
from helpers import *

app = Flask(__name__)

# API to accept a.txt from user
@app.route('/upload', methods=['POST'])
def upload_dataset():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded.'}), 400

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    if not uploaded_file.filename.lower().endswith('.txt'):
        return jsonify({'error': 'Only .txt files are allowed.'}), 400

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    save_path = os.path.join(project_root, 'sample.txt')

    uploaded_file.save(save_path)

    return jsonify({
        'message': 'Dataset file saved successfully.',
        'filename': uploaded_file.filename,
        'saved_to': save_path
    })


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
    
    
# All courses api
@app.route('/courseId', methods=['GET'])
def get_available_courses():
    c_id = request.get_json()['id']
    
    courses = load_files('sample.txt')
    
    asked_course = {}
    if c_id in list(courses):
        asked_course = courses[c_id]
    

    return jsonify({
        'course': asked_course
    })


if __name__ == '__main__':
    app.run(debug=True)