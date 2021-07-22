import sqlite3
from sqlite3.dbapi2 import connect
import subprocess
import json
import os

github_repo_dir = '/home/long/Documents/PoC-in-GitHub/'
github_PoC_dir = '/home/long/Documents/Github_repo/'


def get_CVE_name():
    conn = sqlite3.connect('/home/long/Documents/database/cve.db')
    assert conn.total_changes == 0
    cur = conn.cursor()
    l = cur.execute(
        "select id,name from CVE where tool = 'github' and status = 'update'").fetchall()
    conn.close()
    return l


def update_status(id: int):
    conn = sqlite3.connect('/home/long/Documents/database/cve.db')
    assert conn.total_changes == 0
    cur = conn.cursor()
    cur.execute("update CVE set status = 'done' where id = {};".format(
        str(id).replace("CVE", '').replace('-', '')))
    conn.commit()
    conn.close()


def json_from_id(id: int):
    id = str(id)
    return github_repo_dir+id[:4]+'/CVE-'+id[:4]+'-'+id[4:]+'.json'


def json_to_repo(file: str):
    repos = []
    with open(file, 'r') as f:
        content = f.read()
        json_content = json.loads(content)
        for j in json_content:
            repos.append(j['html_url'])
        return repos


if __name__ == '__main__':
    CVE_list = get_CVE_name()
    for x in CVE_list:
        print("OK")
        break
        repos = json_to_repo(json_from_id(x[0]))
        os.system("mkdir /home/long/Documents/Github_repo/"+str(x[1]))
        for i in range(len(repos)):
            subprocess.call(
                ['/home/long/Documents/clone_repo.sh {} {} {}'.format(repos[i],  'v'+str(i+1), str(x[1]))],  shell=True)
        
        update_status(x[1])
