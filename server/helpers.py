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
        . all selected courses
    ], 
    tue : [
        {
            c1 : [st, et]
        }, 
        {
            c2 : [st, et]
        },
        .
        .
        . all selected courses
    ],
    .
    .
    . all 7 days   
}

- If there is no lectures on a particular day of a course insert it in the list of that day in such a way it does not make a conflict with the other courses, ie, give it a ool interval.
'''





'''
A map of selected course ids to the prerequisites wrt a.txt
# Ex: 
{
    c1 : [p1, p2, ...],
    .
    .
    . 
}
Structure of the txt file as follows---

Selected: CS301,CS302
Prereq: CS301:CS201,CS202 | CS302:CS101 | CS201:CS100
Completed: CS100,CS101
'''

def load_files(file_name):

    try:
        with open(file_name,'r') as file:
            line=file.readlines()
            
        lines=[]
        for l in line:
            if l.strip():
                lines.append(l)

        select=lines[0].split(":")[1].strip()
        preq=lines[1].split(":",1)[1].strip()
        complete=lines[2].split(":")[1].strip()


        if select.lower()=="none":
            selected=[]
        else:
            selected=[x.strip() for x in select.split(",")]

        prerequisite={}

        for item in preq.split("|"):
            course,preres=item.strip().split(":")

            if preres.lower()=="none":
                prerequisite[course.strip()]=[]
            else:
                prerequisite[course.strip()]=[x.strip() for x in preres.split(",")]


        if complete.lower()=="none":
            completed=[]
        else:
            completed=[x.strip() for x in complete.split(",")]


        return selected,prerequisite,completed
    except Exception as e:
        return{
            "Unexpected Error":str(e)
        }



def eligibility(selected,prerequisite,completed):

    required=set()
    stack=selected[:]
    while len(stack)>0 :

        course=stack.pop()
        if course in prerequisite:
            for prereq in prerequisite[course]:
                if prereq not in required:
                    required.add(prereq)
                    stack.append(prereq)
    

    missing=[]
    for course in required:
        if course not in completed:
            missing.append(course)


    if len(missing)==0:
        return{
            "Eligible": True,
            "Required Course": "None"
        }
    
    return{
        "Eligible": False,
        "Required Course": missing
    }

        

# s,p,c=load_files("sample.txt")
# print(eligibility(s,p,c))


    


