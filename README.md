## AWESOME BOT

Deploy on Heroku.\
Make sure in heroku you enter valid info in env.

```
API_ID
API_HASH
BOT_TOKEN
OWNER_ID
```

<p align="center"><a href="https://heroku.com/deploy?template=https://github.com/xbitcode/menuBot"> <img src="https://img.shields.io/badge/Deploy%20To%20Heroku-red?style=for-the-badge&logo=heroku" width="220" height="38.45"/></a></p>


## Setup 

Install python3.1x and pip \
run pip install -r r*.txt 

## Config

`config.py` This file contains all import data you use values in this file also can pass in .env.

WELCOME_MSG | Message shown when user send /start message.\
CUSTOM_MSG  | Message show above buttons \
BUTTON_TYPE , BUTTON_MODE | Configure look and ui of bot check below for details.

`msg.yml` : This file contains text that is show in 3 buttons. \
You can edit message with custom font, emoji & link as below example
```
MESSAGE TEXT  [LINK TEXT](https://t.me/line_here)
```

#### OWNER CMD
_Owner can restart bot if needed with /reboot or reload, reboot re** any word starting with re will reLOAD the bot._

`/admin` : This command is only for admin.\
Admin can choose 2 settings.

-----
**BUTTON_TYPE**

Type:  Is used to configure how the buttons will show 2 options are grid|list \
Grid: All menu buttons in single line.\
List: 1 menu in 1 line for if we have 3 menu it will show 3 lines.

----
**BUTTON_MODE**

Mode: We can display button/option in 3 ways we use inline|chat \
Inline| Menu/Option Buttons will not be shown inside chat windows and always visible below the chat.\
Chat| Show menu with in chat when user send /start command (not optimized better to use inline mode.)


----


Every time owner change button bot will restart to apply new changes and config.py file is updated.\
Note: `When deployed on heroku it will actually not work on bot dyno crash/restart default buttons will be used in config.py`
