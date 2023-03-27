import os
import sqlite3
import time
import argparse
import textwrap
import re
from datetime import datetime


def copy_model(playbook, hosts_file, host_name):

    os.system('ansible-playbook {playbook} -i {hosts_file} -l {host_name}'.format(playbook=playbook, hosts_file=hosts_file, host_name=host_name))



def build(playbook, hosts_file, host_name, tag):

    os.system('ansible-playbook {playbook} -i {hosts_file} -l {host_name} -t build,test,push -e "tag={tag}"'.format(playbook=playbook, hosts_file=hosts_file, host_name=host_name, tag=tag))



def get_data(playbook, hosts_file, host_name, tag, model_name, owner_name, dataset, task, version, conn):
    
    os.system('ansible-playbook {playbook} -i {hosts_file} -l {host_name} -t log -e "tag={tag}" > modelinfo.txt'.format(playbook=playbook, hosts_file=hosts_file, host_name=host_name, tag=tag))

    rows = []
    p_start = re.compile('TASK \[get result].+')
    p_end = re.compile('PLAY RECAP.+')

    with open('modelinfo.txt', 'r') as f:

        lines = f.readlines()

    ## search task start line
        for line in lines:
            start = p_start.search(str(line))

            ## save index of string data
            if start:
                idx = lines.index(line)
                run = True

                while run:
                    lines[idx] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s\.\-\:]", "", lines[idx])
                    lines[idx] = re.sub(" +", " ", lines[idx])
                    lines[idx] = re.sub("\n", "", lines[idx])
                    lines[idx] = re.sub("changed.+", "", lines[idx])

                    rows.append(lines[idx])

                    end = p_end.search(lines[idx])

                    idx += 1

                    if end:
                        run = False

    data =[]
    p_date = re.compile('\d+-\d+-\d+ \d+:\d+:\d+')

    for row in rows:
        if 'date' in row:
            tmp = p_date.findall(row)
            data.append(tmp[0])

        elif 'size' in row:
            row = row.strip(' size')
            row = row.strip('GB')
            data.append(row)

    tmp = []
    log = []
    time_format = "%Y-%m-%d %H:%M:%S"

    tmp.append(time.mktime(datetime.strptime(data[0], time_format).timetuple()))
    tmp.append(owner_name)
    tmp.append(model_name)
    tmp.append(data[1])
    tmp.append(task)
    tmp.append(dataset)
    tmp.append(version)
    tmp = tuple(tmp)

    log.append(tmp)

    cur = conn.cursor()
    query = "insert into modelinfo_detail values(?,?,?,?,?,?,?)"
    cur.executemany(query, log)
    conn.commit()
    
    cur.execute('select * from modelinfo_detail')
    db_show = cur.fetchall()
    
    for row in db_show:
        print(row)
    


if __name__ == "__main__" :

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        
        ============ register your model ==============

        contained informations :
            * owner name
            * model name
            * distribute date
            * trained dataset
            * model size
            * task
            * version
            * accuracy
            * precision
            * recall
            * F1 score

        '''))
    parser.add_argument(
        '--owner_name',
        default='bhc',
        type=str,
        help='who made this model (person | organization | company)'
    )
    parser.add_argument(
        '--model_name',
        default='test',
        type=str,
        help='name of model'
    )
    parser.add_argument(
        '--task',
        default='classification',
        type=str,
        help='which task the model execute'
    )
    parser.add_argument(
        '--dataset',
        default='imagenet',
        type=str,
        help='dataset used for model training'
    )
    parser.add_argument(
        '--version',
        default='v1.0',
        type=str,
        help='version of model'
    )

    args = parser.parse_args()
    print(args)

    db_path = '../../edge_logs.db3'
    conn = sqlite3.connect(db_path)
    copy_playbook_path = 'copy.yaml'
    build_playbook_path = 'autorun.yaml'
    hosts_file_path = '../../../edge-hosts.ini'
    host_name = 'n02'
    tag = args.dataset

    copy_model(copy_playbook_path, hosts_file_path, host_name)
    build(build_playbook_path, hosts_file_path, host_name, tag)

    get_data(
        build_playbook_path,
        hosts_file_path,
        host_name,
        tag,
        args.model_name,
        args.owner_name,
        args.dataset,
        args.task,
        args.version,
        conn
    )