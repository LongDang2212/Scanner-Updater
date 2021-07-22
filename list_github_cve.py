import os


plugins_dir = '/home/long/Documents/PoC-in-GitHub/'
extension = '.json'

def process_line(line:str):
	string = line.replace(".json", '')
	return string

l = []
for i in os.listdir(plugins_dir):
    if i == '.git' or i == 'README.md':
        continue
    for j in os.listdir(plugins_dir+i+'/'):
        l.append(process_line(j))

	
l = list(set(l))
print(len(l))
with open('githubCVEs.txt', 'w') as f:
	for cve in l:
		f.write(cve+ '\n') 
