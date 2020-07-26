# song-link-bot
The telegram bot to share music links

# Build
```docker build -t muzsharebot .```
# Run
```
docker volume create muzsharebot_db
docker run -d --name muzsharebot --restart=always -v muzsharebot_db:/app/databases muzsharebot
```
