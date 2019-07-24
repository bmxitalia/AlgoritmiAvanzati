import pprint

pp = pprint.PrettyPrinter(indent=4)

G = {
    '51510': {   'coords': ['866.5724777', '262.7346869'],
                     'population': '139966',
                     'risk': '3.66E-05'},
        '51570': {   'coords': ['868.0485307', '299.3604592'],
                     'population': '17411',
                     'risk': '3.58E-05'},
        '51610': {   'coords': ['864.0781087', '261.6556678'],
                     'population': '12332',
                     'risk': '3.60E-05'},
        '51670': {   'coords': ['869.9458502', '298.459424'],
                     'population': '22591',
                     'risk': '5.43E-05'},
        '51730': {   'coords': ['868.570008', '300.7480681'],
                     'population': '32420',
                     'risk': '3.55E-05'},
        '51760': {   'coords': ['865.4240502', '293.7359636'],
                     'population': '204214',
                     'risk': '3.62E-05'},
        '53033': {   'coords': ['125.2748602', '39.14977304'],
                     'population': '1931243',
                     'risk': '3.95E-05'},
        '53053': {   'coords': ['117.1097129', '47.2671922'],
                     'population': '795225',
                     'risk': '3.69E-05'},
        '53061': {   'coords': ['129.5998572', '27.06356013'],
                     'population': '713335',
                     'risk': '3.57E-05'},
        '54011': {   'coords': ['776.4021975', '287.8419288'],
                     'population': '96319',
                     'risk': '3.87E-05'},
        '54039': {   'coords': ['789.7869289', '287.7146937'],
                     'population': '193059',
                     'risk': '5.96E-05'},
}

P = ['51510',
'51570',
'51610',
'51670',
'51730',
'51760',
'53033',
'53053',
'53061',
'54011',
'54039']


# P = ['42342','43829','42934',...]

def mergeSort(arr, G): 
    if len(arr) > 1: 
        mid = len(arr)//2 #Finding the mid of the array 
        L = arr[:mid] # Dividing the array elements  
        R = arr[mid:] # into 2 halves 
  
        mergeSort(L, G) # Sorting the first half 
        mergeSort(R, G) # Sorting the second half 
  
        i = j = k = 0
          
        # Copy data to temp arrays L[] and R[] 
        while i < len(L) and j < len(R): 
            if G[L[i]]['coords'][0] < G[R[j]]['coords'][0]: 
                arr[k] = L[i] 
                i+=1
            else: 
                arr[k] = R[j] 
                j+=1
            k+=1
          
        # Checking if any element was left 
        while i < len(L): 
            arr[k] = L[i] 
            i+=1
            k+=1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+=1
            k+=1


mergeSort(P, G)

pp.pprint(P)

for coord in P:
    print(G[coord]['coords'][0])