
y = [1,2,3]
x = [1,2,3]

lst = [(x,y) for x in [1,2,3] for y in [1,2,3]]
lst2 =  [['x' for x in range(4)] for y in range(3)]


print(lst2)

