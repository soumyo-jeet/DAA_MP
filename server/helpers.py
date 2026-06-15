def time(time_str):
    hh, mm = time_str.split(":")
    return [int(hh), int(mm)]


def load_files(file_name):

    courses = {}

    try:
        with open(file_name, "r") as file:
            next(file)

            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 11:
                    continue

                course_id = parts[0]

                prereq = parts[7]
                completed = parts[10]

                if prereq == "None" or prereq == "":
                    prereq_list = []
                else:
                    prereq_list = [p.strip() for p in prereq.split(";")]

                if completed == "None" or completed == "":
                    completed_list = []
                else:
                    completed_list = [c.strip() for c in completed.split(";")]

                courses[course_id] = {
                    "name": parts[1],
                    "department": parts[2],
                    "credits": int(parts[3]),
                    "day": parts[4],
                    "start": time(parts[5]),
                    "end": time(parts[6]),
                    "prereq": prereq_list,
                    "limit": int(parts[8]),
                    "enrolled": int(parts[9]),
                    "completed": completed_list
                }

        return courses

    except Exception as e:
        print("Error in loading the file:", e)
        return {}


def graph(file_name):

    courses = load_files(file_name)
    Graph = {}

    for course_id, data in courses.items():

        Graph[course_id] = {
            "prerequisite": data["prereq"]
        }

    return Graph


def schedule_map(file_name, selected):

    '''
    A map of selected course ids to the schedule wrt a.txt
    # Ex:
    {
        mon : [
            {
                c1 : [st, et]
            },
            {
                c2 : [st, et]
            },
            .
            .
            . 
        ],
        tue : [...],
        .
        .
        . all 7 days
    }

    - If there is no lectures on a particular day of a course just leave it.
    '''

    courses = load_files(file_name)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    schedule = {}
    for day in days:
        schedule[day] = []

    for course_id in selected:

        if course_id not in courses:
            continue

        data = courses[course_id]
        course_day = data["day"]
        st = data["start"][0]
        et = data["end"][0]

        for day in days:

            if day == course_day:
                schedule[day].append({course_id: [st, et]})

    return schedule


def prereq_map(file_name, selected):

    '''
    A map of selected course ids to the prerequisites wrt a.txt
    # Ex:
    {
        c1 : [p1, p2, ...],
        .
        .
        .
    }
    '''

    courses = load_files(file_name)

    result = {}

    for course_id in selected:

        if course_id not in courses:
            continue

        result[course_id] = courses[course_id]["prereq"]

    return result