import discord
import yfinance as yf
import pandas as pd
import os
import plotly.graph_objs as go
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
with open("help.txt", encoding="utf8") as f:
    help_content = f.read()

client = discord.Client()
@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$stonk'):
        temp = message.content.split(" ")
        if(len(temp)==1):
            await message.channel.send("For More Information, type: ```$stonk help```")
            return
        if(message.content=="$stonk help"):
            await message.channel.send(help_content)
            return
        msg = message.content.split(' ')
        if(len(msg)<3):
            await message.channel.send("Invalid Command! For More information, type: ```$stonk help ```")
            return
        currency = msg[1].split("-")
        if(len(currency)<2):
            currency.append("USD")
        
        duration = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '1D', '5D', '1MO', '3MO', '6MO', '1Y']
        if(msg[2] in duration):
            if(msg[2]=="1d" or msg[2]=="1D" or msg[2]=="5d" or msg[2]=="5D"):
                df = yf.download(tickers = msg[1], 
                period=msg[2], interval="1m")
            else:
                df = yf.download(tickers = msg[1], 
                    period=msg[2])  
            curr_df = yf.download(tickers = msg[1], 
                    period="1d",interval="1m")
        else:
            await message.channel.send("Enter Valid Duration")
            return
        
        if(df.empty):
            await message.channel.send(str(msg[1])+" is either Delisted or Spelt Incorrectly!")
        else:
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x = df.index, 
                    open = df['Open'],
                    high = df['High'],
                    low = df['Low'],
                    close = df['Close'],
                    name = "Data",
                ))
            fig.update_layout(template='plotly_dark', title="Stock Price", yaxis_title="Price(in USD)", width=1500,height=750)
            fig.write_image("foo.png")
            await message.channel.send(str(msg[1])+" Current Stock Price 💸: ```"+str(format(curr_df['Open'][0],".2f"))+" "+currency[1]+"```")
            await message.channel.send(file=discord.File('foo.png'))
    print('we have logged in as {0.user}'.format(client))

keep_alive()
client.run(os.getenv('TOKEN'))

# plt.show()
