GMBackup
========
This Python script allows you to download your mail periodically from some remote IMAP server, such as Google's GMail, for the purpose of the backup. It remembers where it ended last, and uses the IMAP capabilities to download only the new mail from the last run. So it's ideal for having it run by cron at night.

Configuration
-------------

You need to change the configuration parameters in the beginning of the script (gmb.py):

 * BACKUP_DIR -- file path where the backups will be stored
 * BACKUP_IMAP_FOLDER -- name of the IMAP folder which you want to backup (e.g. "[Gmail]/Todos", for the Spanish Gmail account folder with all mail)
 * SERVER -- name of the imap server (e.g. "imap.gmail.com", for Gmail)
 * USER  -- your username
 * PASSWORD -- your password

Requirements
------------

 * Python 2.6+
