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



# Modified plan B as per to maximize user's desire score (Line sweep -> GREEDY)
