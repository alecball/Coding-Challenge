import json
import sys

def find_subtasks(task, unordered):
    ''' Finds the ordered subtask 'tree' of a given task.
    
    Parameters:
        task [dict(str:str)]:The task description
        unordered [list(dict(str:str))]:The list of all task descriptions
    
    Returns:
        ordered_subtasks [list(dict(str:*))]:The ordered heirarchical list of 
            the subtasks of the given task
    '''
    
    ordered_subtasks = {}
    ordered_subtasks['task'] = task
    # find subtasks
    subtasks = []
    for item in unordered:
        if item.get('parentID') == task.get('ID'):
            subtasks.append(find_subtasks(item, unordered))
    # order subtasks
    ordered_subtasks['subtasks'] = []
    if len(subtasks) > 0:
        for subtask in subtasks:
            if subtask.get('task').get('previousID') == None:
                next = subtask
                ordered_subtasks.get('subtasks').append(subtask)
                subtasks.remove(subtask)
                break
        while next.get('task').get('nextID') != None:
            for subtask in subtasks:
                if subtask.get('task').get('ID') == \
                                        next.get('task').get('nextID'):
                    next = subtask
                    ordered_subtasks.get('subtasks').append(subtask)
                    subtasks.remove(subtask)
                    break
    return ordered_subtasks


# Command line input arguments
input = sys.argv[1]
output = sys.argv[2]

# open and read input file
with open(input) as f:
   unordered = json.load(f)

# find list of all tasks on level one
base_tasks = []
for task in unordered:
    if task.get('parentID') == None:
        base_tasks.append(task)

# find list of all tasks in heirarchical form
all_tasks = []
for task in base_tasks:
    all_tasks.append(find_subtasks(task, unordered))

# order list of all tasks on level one
ordered = []
# find first task
for task in all_tasks:
    if task.get('task').get('previousID') == None:
        next = task
        ordered.append(task)
        all_tasks.remove(task)
        break
# follow given ordering
while next.get('task').get('nextID') != None:
    for task in all_tasks:
        if task.get('task').get('ID') == next.get('task').get('nextID'):
            next = task
            ordered.append(task)
            all_tasks.remove(task)
            break    

# open and write to output file
with open(output, 'w') as f:
    json.dump(ordered, f, indent = 2)
