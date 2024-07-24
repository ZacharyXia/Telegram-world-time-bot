# Telegram-world-time-bot

A convenient Telegram bot designed to enhance communication in global chat groups. This bot can be easily added to any group and is capable of managing multiple time zones.

## Features

- Add multiple time zones to a group chat
- Display current time for all added time zones
- Remove time zones from the group
- Easy-to-use commands

## Commands

- `/start`: Initializes the bot
- `/info`: Displays information about the bot
- `/addtimezone [country name]`: Adds a new time zone for the specified country
- `/showTimeZone`: Displays the current time for all added time zones
- `/removetimezone [city name]`: Removes the specified city's time zone from the group

## Setup

1. Clone this repository
2. Install the required dependencies:
```
pip install python-telegram-bot pytz
```
3. Replace the token in the `ApplicationBuilder().token()` line with your own Telegram bot token
4. Run the script:
```
python bot.py
```

## Usage

1. Add the bot to your Telegram group
2. Use the `/addtimezone` command followed by a country name to add a time zone
3. Select the specific city/time zone from the provided options
4. Use `/showTimeZone` to display the current time for all added time zones
5. Remove unwanted time zones using the `/removetimezone` command

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
