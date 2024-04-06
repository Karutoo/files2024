import re
import sys
import json
import subprocess

PID = sys.argv[1]
result = ""

with open(f'/usr/local/src/himo/typescript_{PID}', 'r') as input_file:
    result = ""
    for line in input_file:
        output_line = re.sub(r'\x1b\[[^mGK]*[mGK]', '', line)
        result += output_line
    result = result.split("2004l\n")

try:
    with open(f'/usr/local/src/himo/lastcommand', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        last_line = lines[-1].strip()
        if last_line:
            parts = last_line.split('@w@a@w@')
            log_dict = {}
            for element in parts:
                key_value = element.split('@c@w@c@')
                if len(key_value) == 2:
                    key, value = key_value[0], key_value[1]
                    log_dict[key] = value
            else:
                try:
                    data = {
                        'StudentID': log_dict['StudentID'],
                        'ip_addr': log_dict['GlobalIP'],
                        'path': log_dict['CurrentDir'],
                        'command': log_dict['Command'],
                        'output': result[-1],
                        'ExitCode': log_dict['ExitCode']
                    }
                except KeyError as e:
                    exit(1)
                data_json = json.dumps(data)
                #print(result)
                cmd = ['curl', '-X', 'POST', 'https://supabasepusher.himohimo.workers.dev/', '-H', 'Content-Type: application/json', '-H', 'table: logdata', '-d', data_json]
                try:
                    result = subprocess.run(cmd, text=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError as e:
                    print(f"log取得のエラーコード: {e.returncode}")
                    print(f"学生の方は無視していただいて大丈夫です。: {e.stderr}")
except subprocess.CalledProcessError as e:
    print(f"コマンドがエラーを返しました。エラーコード: {e.returncode}")
    print(f"エラーメッセージ: {e.stderr}")