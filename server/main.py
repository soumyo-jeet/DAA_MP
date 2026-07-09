import os

from flask import Flask, request, jsonify
from logics import *
from helpers import *
import tempfile

app = Flask(__name__)
COURSE_FILE_NAME = 'a.txt'
FALLBACK_FILE_NAME = 'sample.txt'
TMP_COURSE_FILE = os.path.join(tempfile.gettempdir(), "a.txt")


def get_course_file():
    if os.path.exists(TMP_COURSE_FILE):
        return TMP_COURSE_FILE
    return os.path.join(os.path.dirname(__file__), FALLBACK_FILE_NAME)

# # API to accept a.txt from user
@app.route('/upload', methods=['POST'])
def upload_dataset():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded.'}), 400

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    if not uploaded_file.filename.lower().endswith('.txt'):
        return jsonify({'error': 'Only .txt files are allowed.'}), 400

    uploaded_file.save(TMP_COURSE_FILE)

    return jsonify({
        "message": "Upload successful",
        "path": TMP_COURSE_FILE
    })

# def get_course_file():
#     course_path = os.path.join(os.path.dirname(__file__), COURSE_FILE_NAME)
#     if os.path.exists(course_path):
#         return course_path
#     return os.path.join(os.path.dirname(__file__), FALLBACK_FILE_NAME)


# # API to accept a.txt from user
# @app.route('/upload', methods=['POST'])
# def upload_dataset():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded.'}), 400

#     uploaded_file = request.files['file']

#     if uploaded_file.filename == '':
#         return jsonify({'error': 'No selected file.'}), 400

#     if not uploaded_file.filename.lower().endswith('.txt'):
#         return jsonify({'error': 'Only .txt files are allowed.'}), 400

#     save_path = os.path.join(os.path.dirname(__file__), COURSE_FILE_NAME)
#     uploaded_file.save(save_path)

#     return jsonify({
#         'message': 'Dataset file saved successfully.',
#         'filename': uploaded_file.filename,
#         'saved_to': save_path
#     })


# API to validate selected course by means of prerequisites and schedule conflicts and to provide plan A
# courses = ["CS101", "CS102", "CS103", "CS404", "CS201"]
# schedule = schedule_map('sample.txt', courses)
# print(schedule)
# get_plan_a(schedule)


@app.route('/plan_a', methods=['POST'])
def plan_a():
    data = request.get_json() or {}
    selected_courses = data.get('courses', [])
    completed_courses = data.get('completed', [])

    print("Got selected courses:", selected_courses)
    print("Got completed courses:", completed_courses)

    course_file = get_course_file()
    
    eligibility_result = eligibility(course_file, selected_courses, completed_courses)
    required_course_value = eligibility_result.get("Required Course", "None")

    try:
        if isinstance(required_course_value, str) and required_course_value != "None":
            required_course_map = json.loads(required_course_value)
        else:
            required_course_map = {}
    except Exception:
        required_course_map = {}

    cancelled_courses = list(required_course_map.keys())
    eligible_courses = [c for c in selected_courses if c not in cancelled_courses]
    schedule = schedule_map(course_file, eligible_courses)
    plan, conflicts = get_plan_a(schedule)

    return jsonify({
        'plan': plan,
        'conflicts': conflicts,
        'eligibility': eligibility_result
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
@app.route('/courses', methods=['GET'])
def get_available_courses():
    courses = load_files(get_course_file())

    return jsonify({
        'courses': courses
    })
    
    
@app.route('/courseId', methods=['GET'])
def get_course_by_id():
    c_id = request.args.get('id')
    courses = load_files('sample.txt')
    asked_course = courses.get(c_id, {})

    return jsonify({
        'course': asked_course
    })

if __name__ == '__main__':
    app.run(debug=True)