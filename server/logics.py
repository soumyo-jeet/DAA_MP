# Discard courses for which prerequisites are not covered
from helpers import graph, load_files
import json


def get_all_prereqs(course, Graph, visited=None):

    if visited is None:
        visited = set()

    if course not in Graph:
        return set()

    prereq_set = set()

    for pre in Graph[course]["prerequisite"]:

        if pre not in visited:
            visited.add(pre)
            prereq_set.add(pre)
            prereq_set |= get_all_prereqs(pre, Graph, visited)

    return prereq_set


def eligibility(file, selected=None, completed=None):

    courses = load_files(file)
    Graph = graph(file)

    if selected is None:
        selected = list(courses.keys())

    if completed is None:
        completed = []
        for data in courses.values():
            completed.extend(data["completed"])
        completed = list(set(completed))

    result = {}
    completed_set = set(completed)

    for course in selected:

        required_prereqs = get_all_prereqs(course, Graph)

        missing = []

        for req in required_prereqs:
            if req not in completed_set:
                missing.append(req)

        if missing:
            result[course] = missing

    if not result:
        return {
            "Eligible": True,
            "Required Course": "None"
        }

    return {
        "Eligible": False,
        "Required Course": json.dumps(result)
    }
# FILE="sample.txt"
# eligibility(FILE)
# eligibility(FILE, selected=["CS301", "CS401"])
# # eligibility(FILE, selected=["CS301"], completed=["CS101", "CS201"])



# Schedule conflict checking in the selected courses and provide plan A (Interval Scheduling -> GREEDY)
def valid_courses (courses, day) :
    if len(courses) == 0 :
        return courses, []
    
    courses.sort(
        key= lambda x : (
            list(x.values())[0][1],
            list(x.values())[0][0],
        )
    )
    
    
    plan = []
    conflicts = []
    prev_end = -1
    prev_course = ''
    
    for c in courses :
        st = list(c.values())[0][0]
        et = list(c.values())[0][1]
        course = list(c.keys())[0]
        
        if st >= prev_end:
            plan.append(course)
            prev_end = et
            prev_course = course
        
        else :
           conflicts.append(f"Course {course} has a schedule conflict with course {prev_course} on {day}.") 
    
    print(plan)
    return plan, conflicts


def get_plan_a (selected_course_dir) :
    plan_a = []
    conflict_msgs = []
    
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    for day in days:
        courses, conflicts = valid_courses(selected_course_dir[day], day)
        plan_a.extend(courses)
        conflict_msgs.extend(conflicts)
        
        
    print(plan_a)
    print(conflict_msgs)
    return plan_a, conflict_msgs


# Modified plan B as per to maximize user's desire score (DP)
def solve (courses, priorities, id, prev_end) :
    if id >= len(courses) :
        return 0, []

    take = 0
    take_courses = []
    skip = 0
    skip_courses = []
    
    if list(courses[id].values())[0][0] >= prev_end :
        profit, chosen = solve(courses, priorities, id + 1, list(courses[id].values())[0][1])
        take = priorities[list(courses[id].keys())[0]] + profit
        take_courses = [list(courses[id].keys())[0]] + chosen
    
    skip, skip_courses = solve(courses, priorities, id + 1, prev_end)
    
    if take > skip :
        return take, take_courses
    else :
        return skip, skip_courses



def get_plan_b (selected_course_dir, priorities) :
    plan_b = []
    profit = 0
    
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    for day in days:
        courses = sorted(
            selected_course_dir[day],
            key= lambda x : (
                list(x.values())[0][1],
                list(x.values())[0][0],
            )
        )
        
        max_profit, valid_courses = solve(courses, priorities, 0, -1)
        plan_b.extend(valid_courses)
        profit = profit + max_profit
        
    total_ws = sum(list(priorities.values()))  
    print(total_ws)
    print(plan_b)
    print(profit / total_ws * 100)
    return plan_b, profit / total_ws * 100