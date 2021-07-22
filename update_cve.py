import sys
import subprocess
import os
import time
import sqlite3

db_path = '/home/long/Documents/database/'
db_file = 'cve.db'


def insert_data(conn: sqlite3.Connection, data: str, tool: str, stt: str):
    id = data.replace('CVE', '').replace('-', '')
    if id == '\n':
        return
    if int(id) < 10000000:
        return
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO CVE(id, name, tool, status) VALUES({},'{}', '{}', '{}');".format(id, data, tool, stt))
    conn.commit()


def check_exist(conn, data):
    id = data.replace('CVE', '').replace('-', '')
    if id == '\n':
        return
    if int(id) < 10000000:
        return
    r = conn.cursor().execute("select id from CVE where id = {}".format(id)).fetchall()
    return True if r != [] else False


def update_repo_github():
    assert os.path.isdir('/home/long/Documents/PoC-in-GitHub')

    with open('git_update.sh', 'rb') as f:
        script = f.read()
        p = subprocess.call(script, shell=True)


if __name__ == '__main__':
    conn = sqlite3.connect(db_path + db_file)
    assert conn.total_changes == 0
    update_repo_github()
    subprocess.call(
        "python3 /home/long/Documents/list_github_cve.py", shell=True)
    with open('/home/long/Documents/githubCVEs.txt', 'r') as f:
        for line in f:
            if check_exist(conn, line):
                continue
            insert_data(conn, line, 'github', 'update')
    subprocess.call(
        "python3 /home/long/Documents/clone_github_cve.py", shell=True)
    subprocess.call(
        "/home/long/Documents/update_openvas_metasploit.sh", shell=True)
    with open('/home/long/Documents/openvasCVEs.txt', 'r') as f:
        for line in f:
            if check_exist(conn, line):
                continue
            insert_data(conn, line, 'openvas','done')

    with open('/home/long/Documents/metasploitCVEs.txt', 'r') as f:
        for line in f:
            if check_exist(conn, line):
                continue
            insert_data(conn, line, 'metasploit', 'done')

    conn.close()


# with open('/home/long/Documents/githubCVEs.txt', 'r') as f:
#     for line in f:
#         if check_exist(conn, line):
#             continue
#         insert_data(conn, line, 'github')

#  with open('/home/long/Documents/metaslpoitCVEs.txt', 'r') as f:
#         for line in f:
#             if check_exist(conn, line):
#                 continue
#             insert_data(conn, line, 'metasploit')
#     print(check_exist(conn, "CVE-2020-0796"))
