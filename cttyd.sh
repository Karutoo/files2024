#!/bin/bash

# ユーザー名とパスワードを読み取る
USERNAME=$(cat /usr/local/src/himo/username.txt)
PASSWORD=$(cat /usr/local/src/himo/password.txt)
cd /home/admin
# ttyd を実行する
/usr/local/bin/ttyd -W -p 443 -c "$USERNAME:$PASSWORD" bash
