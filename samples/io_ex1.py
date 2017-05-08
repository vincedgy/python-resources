# Open a fil an read it entierly then display it line by line and close the file
# f = open('io_ex1.txt')
# text = f.read()
# for line in text.split('\n'):
#     print line
# f.close()

# The same but simpler
# f = open('io_ex1.txt')
# for line in f:
#     print line
# f.close()

try:    
    for line in open('io_ex1.txt'):
        print line
except Exception as err:
    print type(err), err.args, err
else:
    print('Ends normally')
finally:
    print('The End')