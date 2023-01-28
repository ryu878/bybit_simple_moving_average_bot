# Bybit USDT Perpetual Futures Bot
Simple Bybit Futures bot: if price lower the selected moving average it will open short, if higher then long.

![image](https://user-images.githubusercontent.com/81808867/213633538-a9b29301-716a-4287-8066-ef893290780d.png)


You can set any length for your SMA (bybit max limit is 200 candles, but here there are no limits).

![image](https://user-images.githubusercontent.com/81808867/213634321-12b145e7-1f06-4e74-8d7e-be95b2d15e58.png)


[![Latest release](https://badgen.net/github/release/Naereen/Strapdown.js)](https://aadresearch.xyz)

## Disclaimer
<hr>
This project is for informational and educational purposes only. You should not construe this information or any other material as legal, tax, investment, financial or other advice. Nothing contained herein constitutes a solicitation, recommendation, endorsement or offer by us or any third party provider to buy or sell any securities or other financial instruments in this or any other jurisdiction in which such solicitation or offer would be unlawful under the securities laws of such jurisdiction.

If you intend to use real money, use it at your own risk.

Under no circumstances will we be responsible or liable for any claims, damages, losses, expenses, costs or liabilities of any kind, including but not limited to direct or indirect damages for loss of profits.
<hr>

## Install

First create python virtual environment and activate it:

<code>python3 -m venv .smabot && source .smabot/bin/activate</code>

And then install necessary libraries:

<code>pip install pandas</code>

<code>pip install pybit</code>

## Run

To run the bot type in console:

<code>python3 bybit_sma_bot.py</code>

If you are using windows use python instead of python3 as well.

## Contacts
Discord: https://discord.gg/zSw58e9Uvf

Telegram: https://t.me/aadresearch
