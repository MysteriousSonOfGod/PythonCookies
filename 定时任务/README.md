终端 crontab -e

*/1 * * * * /usr/local/python3/bin/python3 /home/xnotes/demo.py > /home/xnotes/listen.log 2>&1
'2>&1'要不要都无所谓
一分钟执行一次
日记保存在listen.log
vim /var/spool/mail/xnotes