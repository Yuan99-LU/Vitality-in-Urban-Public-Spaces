
import random

with open("proxy_list.txt") as f:
    content = f.readlines()

#print(content)

content =[x.strip() for x in content]

print(content[4:5])
print(content[-3:-2])

sr = random.SystemRandom()
proxyip_gaoni =sr.choice(content)
proxyip=proxyip_gaoni.split(" ")[0]
print(proxyip)
