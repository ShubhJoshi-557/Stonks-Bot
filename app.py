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
with open("help2.txt", encoding="utf8") as f2:
    help_content2 = f2.read()
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
            welcome_embed=discord.Embed(title="Welcome!", description="$stonk is a prefix command for Stonks Bot. For More Information, type: ```$stonk help```", color=0x5E4A9D)
            await message.channel.send(embed=welcome_embed)
            return
        if(message.content=="$stonk help"):
            help_embed=discord.Embed(title="Help Page 1/2", description=help_content, color=discord.Color.blue())
            await message.channel.send(embed=help_embed)
            return
        if(message.content=="$stonk help 2"):
            help_embed2=discord.Embed(title="Help Page 2/2", description=help_content2, color=discord.Color.blue())
            await message.channel.send(embed=help_embed2)
            return
        msg = message.content.split(' ')
        if(len(msg)<3):
            invalid_embed=discord.Embed(title="⚠️", description="Invalid Command! For More information, type: ```$stonk help ```", color=discord.Color.red())
            await message.channel.send(embed=invalid_embed)
            return
        currency = msg[1].split("-")
        Dict = {'ns': 'INR', 'bo': 'INR', 'to': 'CAD', 'l': 'GBp', 'sz': 'CNY', 't': 'JPY', 'hk': 'HKD', 'ss': 'CNY', }
        if(len(currency)<2):
            temp = currency[0].split(".")
            print(currency)
            if(len(temp)>1):
                if temp[1].lower() in Dict.keys():
                    currency.append(Dict[temp[1].lower()])
                else:
                    currency.append(" ")
            else:
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
            invalid_duration_embed=discord.Embed(title="⚠️", description="Enter Valid Duration!", color=discord.Color.red())
            await message.channel.send(embed=invalid_duration_embed)
            return
        
        if(df.empty):
            invalid_name_embed=discord.Embed(title="⚠️", description=str(msg[1])+" is either Delisted or Spelt Incorrectly!\n\n For More Info Regarding Stock Names, type:```$stonk help 2```", color=0xEDBC27)
            await message.channel.send(embed=invalid_name_embed)
        else:
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x = df.index, 
                    open = df['Open'],
                    high = df['High'],
                    low = df['Low'],
                    close = df['Close'],
                    name = "Data",
                ))
            fig.update_layout(template='plotly_dark', title="Stock Price", yaxis_title="Price(in "+currency[1]+")", width=1500,height=750)
            fig.write_image("foo.png")
            output_embed=discord.Embed(description=str(msg[1])+" Current Stock Price 💸: ```"+str(format(curr_df['Open'][0],".2f"))+" "+currency[1]+"```", color=0x1AC255)
            await message.channel.send(embed=output_embed)
            await message.channel.send(file=discord.File('foo.png'))
    print('we have logged in as {0.user}'.format(client))

keep_alive()
client.run(os.getenv('TOKEN'))
# plt.show()
