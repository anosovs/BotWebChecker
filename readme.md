# botWebChecker
Allows you to check sites for availability using three types of checks. If problems arise, a message is sent to the telegram. Allows you to manage settings using bot telegrams.

## Description for files

<dl>
    <dt>checker_exp_date.py</dt>
    <dd>check domain for expiration date</dd>
    <dt>checker_status.py</dt>
    <dd>check domain for returned status code</dd>
    <dt>checker_tag.py</dt>
    <dd>check page for the existing tag</dd>
    <dt>mainbot.py</dt>
    <dd>Allow to manage settings for checked domains</dd>
</dl>

## Bot commands
  /add <domain> - add domain  
  /del <domain or ID> - delete domain (use id or domain name)  
  /domains - list of available domains with id  
  /status_check <domain or ID> - toggle check for status  
  /exp_check <domain or ID> - toggle expiration date check  
  /tag_check <domain or ID> - check existing of tag on index page  
  /tag <domain or ID> - add\\change tag for domain  
  /last - return result of last check  
  /chat_id - available for everybody return chat_id

## Preparing
1. Create and use [virtual enviroment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
2. Install all reqired packages

   > pip3 install -r requirements.txt

3. Run first_run.py. This will create settings.py with params: sqlite db, telegram API token and count of days for warning about domain 
   expiration date. Just follow the suggested steps

    >python3 first_run.py
   
4. Add into Cron desired check modules (checker_exp_date.py, checker_status.py, checker_tag.py) with desired intervals  
     Example:
   ```bash
   echo "*/10 * * * * * cd /bot_home_dir && /usr/bin/python3 checker_exp_date.py >> /path_to_log 2>1&" >> /etc/crontab
   ```
5. Add into Cron mainbot.py for starting when system restarted