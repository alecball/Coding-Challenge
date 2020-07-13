import json
import sys

def find_children(node, unordered):
    a = {}
    a['task'] = node
    subtasks = []
    for item in unordered:
        if item.get('parentID') == node.get('ID'):
            subtasks.append(find_children(item, unordered))
    #order children
    a['subtasks'] = []
    if len(subtasks) > 0:
        for item in subtasks:
            if item.get('task').get('previousID') == None:
                next = item
                a.get('subtasks').append(item)
                subtasks.remove(item)
                break
        while next.get('task').get('nextID') != None:
            for item in subtasks:
                if item.get('task').get('ID') == next.get('task').get('nextID'):
                    next = item
                    a.get('subtasks').append(item)
                    subtasks.remove(item)
                    break
    return a

input = sys.argv[1]
output = sys.argv[2]

with open(input) as f:
   unordered = json.load(f)
   
o = []
   
for item in unordered:
    if item.get('parentID') == None:
        o.append(item)

b = []
for item in o:
    b.append(find_children(item, unordered))
    
ordered = []
for entry in b:
    if entry.get('task').get('previousID') == None:
        next = entry
        ordered.append(entry)
        b.remove(entry)
        break
        
while next.get('task').get('nextID') != None:
    for entry in b:
        if entry.get('task').get('ID') == next.get('task').get('nextID'):
            next = entry
            ordered.append(entry)
            b.remove(entry)
            break    
    
with open(output, 'w') as f:
    json.dump(ordered, f, indent = 2)