list = ['first', 'second', 'thrid', 'fourth']
print("the last element in the list is: " + list[-1])

# append can add new element to the end of list
list.append('fifth')
print(list)

# pop can delete element from the end of list
list.pop()
print(list)

# pop with index can delete element in that index
list.pop(1)
print(list)

# sort the list reverse
list.sort(reverse=True)
print(list)

test = [1,2,3]

test2 = test[1:3]

test[1] = 5
print(test)
print(test2)

print(test[-1])
