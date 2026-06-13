# Discard courses for which prerequisites are not covered



# Schedule conflict checking in the selected courses and provide plan A (Interval Scheduling -> GREEDY)
def valid_courses (courses) :
    if len(courses) == 1 or len(courses) == 0 :
        return courses
    
    courses.sort(
        key= lambda x : (
            list(x.values())[0][1],
            list(x.values())[0][0],
        )
    )
    
    
    plan = []
    prev_end = -1
    
    for c in courses :
        st = list(c.values())[0][0]
        et = list(c.values())[0][1]
        course = list(c.keys())[0]
        
        if st >= prev_end:
            plan.append(course)
            prev_end = et
    
    print(plan)
    return plan


def get_plan_a (selected_course_dir) :
    mon_courses = valid_courses(selected_course_dir["mon"])
    tue_courses = valid_courses(selected_course_dir["tue"])
    wed_courses = valid_courses(selected_course_dir["wed"])
    thu_courses = valid_courses(selected_course_dir["thu"])
    fri_courses = valid_courses(selected_course_dir["fri"])
    sat_courses = valid_courses(selected_course_dir["sat"])
    sun_courses = valid_courses(selected_course_dir["sun"])
    
    plan_a = [
        c for c in (mon_courses or tue_courses or wed_courses or thu_courses or fri_courses or sat_courses or sun_courses)
    ]
    
    print(plan_a)
    return plan_a


# Modified plan B as per to maximize user's desire score (Line sweep -> GREEDY)

