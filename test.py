file_array = []

def replaceList (list_of_strings, old, new):
    for i in range(len(list_of_strings)):
        list_of_strings[i] = list_of_strings[i].replace(old, new)
    return list_of_strings

with open('./messages/command.txt', 'r') as file:
    file_array = file.readlines()
file_array = replaceList(file_array, '\n', '')
    
print(len(file_array))
for i in range(len(file_array)):
    print(f'{i}: {file_array[i]}')