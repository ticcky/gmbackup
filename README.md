GMBackup
========
This Python script allows you to download your mail periodically from some remote IMAP server, such as Google's GMail, for the purpose of the backup. It remembers where it ended last, and uses the IMAP capabilities to download only the new mail from the last run. So it's ideal for having it run by cron at night.
