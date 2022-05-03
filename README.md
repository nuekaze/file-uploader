# file-uploader
Python backend to upload files to some directory.

## Running
You can run server.py in a screen or something. Then proxy_pass some url in nginx to the backend.

## Delete after a while
You can do something like the following in crontab.
This will delete content older than 7 days.

<code>0 0 * * * find /storage/tempfiles/* -mtime +7 --exec rm {} \;</code>
