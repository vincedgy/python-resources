x_list=[1,2,3]
y_list=[4,5,6]

# for i in range(len(x_list)):
#     x = x_list[i]
#     y = y_list[i]
#     print (x,y)


for x, y in zip(x_list,y_list):
    print(x,y)