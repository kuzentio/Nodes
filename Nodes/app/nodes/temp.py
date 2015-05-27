
nodes = ['A', 'B', 'C', 'D']
weights = {'A': {'B': 1,},
           'B': {
                 'A': 1,
                 'C': 3,
                },
             'C': {'B': 3,
                   'D': 7,
                   },
             'D': {
                 'C': 7,
             }
    }

for node in nodes:
    print node,
    for nod in nodes:
        if nod in weights[node]:
            print weights[node][nod],
        else:
            print '0',
    print ''

print ''
print ''


for node in nodes:
    print node,
    for nod in nodes:
        print weights[node].get(nod, 0),
    print ''










