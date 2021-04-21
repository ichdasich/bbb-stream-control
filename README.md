# Description

This is a small orchestration script allows you to let your BBB users stream their rooms automatically (via a setting in each room's configuration).
It is build around https://github.com/aau-zid/BigBlueButton-liveStreaming and uses custom patches to Greenlight from this fork: https://github.com/ichdasich/greenlight/tree/streaming
Streaming is supported with a local rtmp instance on nginx, producing HLS, which is then made available via HTTP using a small site relying on https://github.com/videojs/video.js 

# Architecture
- A cron job executes the controller every minute (YMMV)
- If the controller detects a running room with streaming enabled, for which no docker process can be found, it starts a container for streaming.
- nginx consumes the procued rtmp (with the room-path as streaming key) and then produces HLS, which is made available via HTTPS
- A regex based nginx location and a small index.html then provide a web-view of the streams (if they are running)

# Configuration overview

## config.json
- `daemon` = True/False -  If using crontab model of execution or systemd
- `bbb_url` = Your BBB server or loadbalancer endpoint
- `bbb_secret` = Your BBB secret
- `rtmp_path` = `'rtmp://192.168.178.23:1935/live/'`; The IP and port on which nginx listens for rtmp connections; Firewall from the internet
- `web_stream` = `'https://bbb.example.com/streams/'`; The base-URL of your streams. Individual streams will look like `https://bbb.example.com/streams/xyz-123-zyx-412/`, depending on the room's path.
- `bbb_res` = Resolution for the stream, e.g., `'1920x1080'`; The higher the resolution, the higher the load on the machine.
- `postgresql` = configure postgresql
     - `user` = postgresql username
     - `password` =  postgresql password
     - `host` = postgresql host (defaults to password)
     - `port` = postgresql port (defaults to 5433)

## index.html
- Set URL in `src` variable according to your infrastructure (could be done better, i know)
- Update `poster=` according to your infrastructure (background for videos before playing)

# Installation Instructions

1. Git clone the latest greenlite streaming fork

`git clone -b streaming https://github.com/ichdasich/greenlight.git`

2. Compile it with docker / run it - follow the Customize install instructions from BBB page. Make sure to merge it with the newest upstream release for greenlight! Also, make sure to add `streaming` to the enabled features list in `.env`

3. Git clone bbb-stream-controll
`git clone https://github.com/ichdasich/bbb-stream-controll`

4. Install psycopg
`apt-get install python3-psycopg2`

5. Install docker python
`apt-get install python3-docker`

6. Install RTMP for nginx
`apt-get install libnginx-mod-rtmp`

7. Create folders for nginx:
```
mkdir /var/www/html/hls/
mkdir /var/www/html/streams/
chown www-data:www-data /var/www/html/hls/
```

8. Activate rtmp in nginx by adding the following lines to `/etc/nginx/nginx.conf`. Make sure to replace the listen IP. Do not listen publicly or firewall accordingly.

```
rtmp {
        server {
                listen LISTENIP:1935;
                chunk_size 4096;
                allow publish 10.0.0.0/8;
                allow publish 172.16.0.0/12;
                allow publish 192.168.0.0/16;
                deny publish all;

                allow play all;

                application live {
                        live on;
                        hls on;
                        hls_path /var/www/html/hls/;
                        hls_fragment 3;
                        hls_playlist_length 60;
                        record off;
                }
        }
}
```

9. In your greenlight vhost (the nginx proxy), add, before the `location / {` statement, the following:
```
        location ~ "/streams/[^/]+/$" {
                try_files $uri $1/index.html;

        }
```

10. Restart nginx: `service nginx restart`

11. Install and configure controller.py; Adjust configuration variables as indicated above
```
mkdir /opt/bbb-stream-control/
cp ./controller.py /opt/bbb-stream-control/
chmod +x /opt/bbb-stream-control/controller.py
```

12. Pull the container (to speed up things on first try): `docker image pull aauzid/bigbluebutton-livestreaming`


13. Install `CRON` or `DAEMON` method for execution

  - Install the cronjob running the script every minute:    

    `cp bbb-stream-control.cron /etc/cron.d/bbb-stream-control`

    **OR**

  - Install SystemD service that runs every 10-30 seconds

```
cp bbb-stream-control.service /etc/systemd/system
systemctl enable bbb-stream-control
systemctl start bbb-stream-control
```
  - set `DAEMON=True` in `controller.py`

14. Place `var_www_html/index.html` into `/var/www/html/streams/` and adjust according to the config instructions above (change HLS URL)

15. Place `var_www_html/video.min.js` and `var_www_html/video-js.css` into `/var/www/html/`


# Caveats
- This is a hacky sollution, which (mostly) works; Use at your own judgement
- Cron and containers currently run as root; Planning to fix that in the future
- There is no authentication in front of active streams
- Streaming can be rather resource heavy on your frontend; Be careful. Technically, this setup also works with dedicated hosts for the streaming containers and serving the HLS content.


