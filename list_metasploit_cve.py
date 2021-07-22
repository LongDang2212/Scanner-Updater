#!/usr/bin/env python3
import glob
import csv

plugins_dir = '/opt/metasploit-framework/embedded/framework/modules/*'
extension = '.rb'


def get_folder_depth():
    for i in range(1, 20):
        if glob.glob(plugins_dir+'/*'*i+extension) == []:
            return i


def process_content(content: str):
    CVE_list = []
    while content.find("'CVE',") != -1:
        i = content.find("'CVE',")
        start = content[i+6:].find("'")
        end = content[i+6+start+1:].find("'")
        # print(content)
        # print(start)
        # print(end)
        string = 'CVE-'+content[i+6+1+start:i+7+start+end]
        CVE_list.append(string)
        content = content[i+5+start+end:]
    return CVE_list


def get_content_in_file(file):
    with open(file, 'r', errors='ignore') as f:
        content = f.read()
        i = content.find("'References'")
        j = content[i:].find("'Payload'")
        content = content[i:i+j]
    return content


l = []
for i in range(1, get_folder_depth()):
    for file in glob.glob(plugins_dir+'/*'*i+extension):
        l.extend(process_content(get_content_in_file(file)))


l = list(set(l))
print(len(l))
with open('metasploitCVEs.txt', 'w') as f:
    for cve in l:
        f.write(cve + '\n')
