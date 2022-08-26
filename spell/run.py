import subprocess
import os
file = 'corpus_filelist_2_only_filenames.txt'

ip_file = open(file, 'r')
lines = ip_file.readlines()
op_file = open('result.txt', 'a')
lag = 'es'
for line in lines:
    position = line.split('-')
    year = position[0]
    month = position[1]
    day = position[2][0:2]
    print(year, month, day)
    path = f"/data/tv/{year}/{year}-{month}/{year}-{month}-{day}/{line}"
    obj = subprocess.Popen(f"python3 cospell.py --file {path} --language 'es'", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for s_line in obj.stdout.readlines():
        op_file.write(str(s_line))
    obj.stdout.close()
