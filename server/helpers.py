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
'''
