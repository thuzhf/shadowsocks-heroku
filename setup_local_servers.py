#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Fang Zhang <thuzhf@gmail.com>
# @Date:   2016-12-22 20:12:43

import argparse, hashlib, requests, subprocess, json
import multiprocessing as mp

def gen_name_list(root_str, length, times):
    results = []
    tmp_str = ''
    for i in range(times):
        head_char = chr(ord('a') + i % 26)
        tmp_str = hashlib.sha512('{}{}'.format(root_str, tmp_str).encode('utf-8')).hexdigest()[:length]
        results.append('{}{}'.format(head_char, tmp_str[1:]))
    return results

def setup_local(name_list, start_port):
    cli = 'pkill -f "node local.js -s"'
    print('Run: {}'.format(cli))
    subprocess.run(cli, shell=True)
    cli = 'npm install'
    print('Run: {}'.format(cli))
    subprocess.run(cli, shell=True)
    for i, app_name in enumerate(name_list):
        cli = 'node local.js -s {0}.herokuapp.com -l {1} > /tmp/{0} &'.format(app_name, start_port + i)
        print('Run: {}'.format(cli))
        subprocess.Popen(cli, shell=True)

def get_IP(url, queue):
    r = requests.get(url)
    IP = r.json()['origin']
    queue.put(IP)

def get_IPs(name_list):
    urls = []
    for name in name_list:
        url = 'https://{}.herokuapp.com'.format(name)
        urls.append(url)
    queue = mp.SimpleQueue()
    pool = []
    for url in urls:
        p = mp.Process(target=get_IP, args=(url, queue))
        p.start()
        pool.append(p)
    IPs = set()
    for i in range(len(pool)):
        IPs.add(queue.get())
    return IPs
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file', default='./extra_config.json')
    args = parser.parse_args()
    with open(args.config_file) as f:
        cfg = json.load(f)
    app_name_list = gen_name_list(cfg['root_str'], cfg['length'], cfg['times'])
    setup_local(app_name_list, cfg['start_port'])
    print('Getting IPs...')
    IPs = get_IPs(app_name_list)
    print(len(IPs), IPs)

if __name__ == '__main__':
    main()
