# Apple Spyder
A hard-working bot that captures Apple software updates and pushes notifications, developed by Hackl0us.

## License
Open source license (GPLv3) for this project has legal effects, so please be sure to comply with it.

## Configuration
### SQLite database initialization
Initialize the SQLite 3 database with the file under `res/init_db.sql`.

Put the database file at under the `res` folder, name the file `apple-spyder.db`.

### Configuration
Please put the configuration file at under the `res` folder, name the file `config.yaml`.

```yaml
# All the following parameters are randomly generated. Please replace them with real ones
weibo:
  enable: false
  app-key: 6677073540
  app-secret: 2h152qzt4xcg9fyx2qt44xwlwn2w7kwb
  redirect-uri: https://hackl0us.com
  access-token: 2.00WM2onwpur1qlgeq91xryamuhfk2i
  rip: 213.1.207.236 # Your real IP address

telegram:
  enable: true
  bot-name: Apple Spyder Test Bot
  bot-token: 4934421727:ZRXNwextc2K_o4j150Nf7u-O2k6CMQVRj4
  chat-id: 4543069976

url:
  apple-developer-rss: https://developer.apple.com/news/releases/rss/releases.rss
```


### Docker Compose
```yaml
services:
  apple-spyder:
    image: hackl0us/apple-spyder
    container_name: apple-spyder
    restart: always
    volumes:
      - /folder_to_config/res:/usr/src/app/res
    ports:
      - 5001:8888
```

## API Call
After you successfully run the App, you can refer to the APIs below to perform the corresponding requests:

* `/apple-spyder/software-release`: Check Apple Developer RSS feed.
* `/apple-spyder/accessory-ota-update`: Check for Apple accessories OTA updates.