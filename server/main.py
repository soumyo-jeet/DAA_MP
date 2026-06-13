from logics import *


# API to accept a.txt from user

# API to validate selected course by means of prerequisites and schedule conflicts and to provide plan A
courses = {
    "mon" : [
        {
            'c1' : [14, 20]
        },
        {
            'c2' : [15, 25]
        },
        {
            'c3' : [4, 10]
        },
    ],
    
    "tue" : [
        {
            'c4' : [14, 20]
        },
        {
            'c5' : [15, 25]
        },
        {
            'c6' : [4, 10]
        },
    ],
    
    "wed" : [
        {
            'c7' : [14, 20]
        },
        {
            'c8' : [15, 25]
        },
        {
            'c9' : [4, 10]
        },
    ],
    
    "thu" : [
        {
            'c10' : [14, 20]
        }
    ],
    
    "fri" : [
        {
            'c11' : [14, 20]
        }
    ],
    
    "sat" : [],
    "sun" : []
}

get_plan_a(courses)
# API to accept weighted courses (preferences) and provide plan B
