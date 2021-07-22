#!/usr/bin/env python3
import glob
import csv

plugins_dir = '/opt/gvm/var/lib/openvas/plugins'
extension = '.nasl'


def get_folder_depth():
    for i in range(1, 20):
        if glob.glob(plugins_dir+'/*'*i+extension) == []:
            return i


def process_content(content: str):
    CVEs_list = []
    while content.find('\"') != -1:
        i = content.find('\"')
        j = content[i+1:].find('\"')
        cve = content[i+1:i+1+j]
        if cve.find('CVE-') != -1:
            CVEs_list.append(cve)
        content = content[i+j+1+1:]
    return CVEs_list


def get_content_in_file(file):
    with open(file, 'r', errors='ignore') as f:
        content = f.read()
        start = content.find('script_cve_id(')
        end = content[start:].find(");")
        content = content[start + 13:start+end+1]
        content.replace('\n', '')
        return content


if __name__ == '__main__':
    l = []
    for i in range(1, get_folder_depth()):
        for file in glob.glob(plugins_dir+i*'/*'+extension):
            l.extend(process_content(get_content_in_file(file)))
    print(len(l))
    l = list(set(l))
    print(len(l))
    with open('openvasCVEs.txt', 'w') as f:
        for cve in l:
            f.write(cve + '\n')


# rint(process_content(get_content_in_file('/opt/gvm/var/lib/openvas/plugins/2020/gb_hw_vuln_full_linux_kernel_mitigation_missing.nasl')))
# print(get_CVEs_in_file('/opt/gvm/var/lib/openvas/plugins/2020/gb_hw_vuln_full_linux_kernel_mitigation_missing.nasl'))
