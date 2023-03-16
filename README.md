# yuyuyu
A text-to-speech bot for Discord using VITS model based on Python and node.js. Current state is "usable" but it is **VERY EXPERIMENTAL** and **VERY BUGGY**. Only usable using Japanese/Chinese language at the moment.

# How to use
Note : Make sure you have adequate CPU power. Tested on 2 cores AMD EPYC 7443.

Please make sure you have install **Python 3.10.6** (I have not tested this to run in other version) and **node.js** 16. Additionally run `pip install -r requirements` for python requirements and `npm install` for node requirements. After you have done all those, the next step is :

1. Get your VITS model. Google is your best friend if you don't have one.
2. Rename your model and config to model.pth and model.json.
3. Edit config.json and replace it with your own bot token
4. Run `node index.js` to run the bot.
5. Once running, use `/speak` to use the bot.

# Testing and debugging

In order to test whether your voice generating script is working or not, please run `python tts.py "こんばんは"` and see if it will generate `temp.ogg` file in root directory. You might also need to change `commands/speak.js` directory as it was hardcoded. If you having issues, feel free to open one.
