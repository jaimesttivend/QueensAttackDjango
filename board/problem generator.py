import random
response = ""
for item in  range(100):

    temp = random.randint(1,100).__str__()+" "+random.randint(1,100).__str__()+"\n"
    response += temp
with open("test.txt","a") as f:
    f.write(response)