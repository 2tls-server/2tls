# 2tls
**The server is currently in active development. Available on [2tls.fun](2tls.fun)**

*[Discord server](https://discord.gg/fa5nJEsXH7)*
## TODO

 - [ ] Replay uploading and leaderboards
 - [ ] Custom level background
 - [ ] Support for uploading CHS, MMWS, SUS and USCv1 charts
 - [ ] Website
 - [ ] Move static assets from github and calculate hashes
## Installation guide
### Dependencies:
 
 - Python 3.12+
 - A process manager (I use pm2)
 - A reverse proxy (I use Caddy)
 - An S3 bucket (won't be passed to client)
 - SQL Database (check [here](https://www.sqlalchemy.org/features.html) if your one will work)
 - Redis or Redis-compatible server

### Steps:

 - **Install python dependencies**
 `python3 -m pip install -r requirements.txt`
NOTE: using `venv` is recommended, but not necessary.
 - **Get an S3 bucket link**
You can use `MinIO` if you have enough storage or if you are not deploying to prod.
There are many S3 providers out there and you can get an "external" S3 bucket too.
 - **Configure env**
Create a file in project root directory called `env.py`;
Import envhelper in there (`from envhelper import BaseEnv`);
Create env (`env = BaseEnv(...)`).
- **Add engine to your S3**
Use [Nanashi](github.com/sevenc-nanashi)'s [pjsekai-engine-extended](https://github.com/sevenc-nanashi/sonolus-pjsekai-engine-extended). You need to compile it and locate files in `S3/engine` folder. Check `sonolus_server/static.py:85` for more info.
I plan on forking this engine when needed.
 - **Configure reverse proxy and process manager**
If you plan on hosting 2tls on your local machine, you might not use reverse proxy at all or use ngrok. 
If you want to deploy 2tls to prod, you should **absolutely** use reverse proxy: it will provide HTTPS support and also it's just not recommended to use anything without a reverse proxy.
If you use Caddy: edit `/etc/caddy/Caddyfile`, add contents from local caddy file (make sure to change the domain name).
If you use PM2: you can launch 2tls using `start.sh` (2 * cpu-cores + 1 workers), `start1worker.sh` and `start2workers.sh`.
 - **Done. You're awesome**
## Some notes
- This is my first open-source project and almost my first project in prod.
- PR and Issues are welcome.
## License
This project is licensed under the [MIT License](LICENSE). 
It uses code and assets from various third-party sources. For a full list of third-party licenses and credits, please see the [NOTICE file](NOTICE.md).
