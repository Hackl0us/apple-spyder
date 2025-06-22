# Apple Spyder
A hard-working bot that captures Apple software updates and pushes notifications, developed by Hackl0us.

An _AWS Lambda_ implementation.

## License
Open source license (GPLv3) for this project has legal effects, so please be sure to comply with it.

## Configuration
### DynamoDB
The function utilizes _AWS DynamoDB_ to store software release records.

* **Partition Key**: `platform`
* **Sort Key**: `channel`

### Environment Variables
The function requires to setup environment variables.

| Variable name        | Date Type | Sample                                      | Description                                                                                                                                                                                                                                                                       |
|----------------------|-----------|---------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `CUTOFF_DAYS`        | `int`     | `13`                                        | Only process RSS feed entries whose published timestamp falls within the last N days relative to the current time. When set this value to `0`, the function only process the feed entries whose published timestamp is equal to the feed updated timestamp. Default value is `7`. |
| `TELEGRAM_BOT_TOKEN` | `string`  | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` | Telegram bot API token. You can create a bot and obtain the token by talking to @BotFather.                                                                                                                                                                                       |
| `TELEGRAM_CHAT_ID`   | `string`  | `-1001001001001`                            | The Telegram user or channel ID where notifications should be sent.                                                                                                                                                                                                               |
| `TELEGRAM_ENABLED`   | `bool`    | `True`                                      | Set to `True` to enable Telegram notifications. Default value is `False`.                                                                                                                                                                                                         |
| `WEIBO_ACCESS_TOKEN` | `string`  | `2.00HTd1N5dlsLWSZgG1w94D8zDnt72`           | Weibo OAuth access token.                                                                                                                                                                                                                                                         |
| `WEIBO_ENABLED`      | `bool`    | `False`                                     | Set to `True` to enable Weibo notifications. Default value is `False`.                                                                                                                                                                                                            |
| `WEIBO_REDIRECT_URI` | `string`  | `https://weibo.com`                         | Weibo secure domain.                                                                                                                                                                                                                                                              |
| `WEIBO_RIP`          | `string`  | `36.51.224.123`                             | User's real IP address.                                                                                                                                                                                                                                                           |

### API Call
Create a _Function URL_ for this function to enable this feature.