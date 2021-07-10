from pymongo import MongoClient
import os
import discord
from discord.ext import commands
import pytz
from random import randint
import datetime
from asyncio import sleep
client = commands.Bot(command_prefix=">",intents=discord.Intents.all())

cluster = MongoClient("mongodb+srv://ekfar1:1234@cluster0.dhafo.mongodb.net/bd?retryWrites=true&w=majority")
bd = cluster["bd"]
collection = bd["dzdatabase"]
daynow = ""

@client.event
async def on_ready():
    global daynow
    while True:
          Emos = pytz.timezone("Europe/Moscow")
          Emos2 = datetime.datetime.now(Emos)
          daynow = Emos2.strftime("%d/%m/%Y") #day/mouth/year
          await client.change_presence(status=discord.Status.online,
              activity=discord.Game(daynow)) 
          await sleep(10)
          
@client.command()
async def adddz(ctx,timeout,book="NULL",*,dz="NULL"):
    collection.insert_one({"timeout":timeout,'book': book,'dz': dz})
    await ctx.channel.send("Вот так выглядит :")   
    x = collection.find_one({"dz":dz})
    
    embed = discord.Embed(title=f'ДАТА '+x['timeout'])
    embed.add_field(name="Предмет ",value=x['book'])
    embed.add_field(name="ДЗ ",value=x['dz'],inline=False)
    await ctx.channel.send(embed=embed)
    
@client.command()
async def starttimeout(ctx):
    await ctx.channel.send("Поиск начат")
    while True:       
        await sleep(10)
        Emos = pytz.timezone("Europe/Moscow")
        Emos2 = datetime.datetime.now(Emos)
        DAYTOMORROW = int(Emos2.strftime("%d")) + 1
        daytom = Emos2.strftime(str(DAYTOMORROW)+"/%m/%Y") #day/mouth/year
        print(daytom)
        data = collection.find({"timeout":daytom})
        for d in data:
            embed = discord.Embed(title=f'ДАТА '+d['timeout'])
            embed.add_field(name="Предмет ",value=d['book'])
            embed.add_field(name="ДЗ ",value=d['dz'],inline=False)
            await ctx.channel.send(embed=embed)
@client.command()
async def tomorrow(ctx,tomorrow):
    await ctx.channel.send("ДЗ на "+tomorrow)     
    data = collection.find({"timeout":tomorrow})
    for d in data:
        embed = discord.Embed(title=f'ДАТА '+d['timeout'])
        embed.add_field(name="Предмет ",value=d['book'])
        embed.add_field(name="ДЗ ",value=d['dz'],inline=False)
        await ctx.channel.send(embed=embed)

@client.command()
async def deletedz(ctx,dz):
    await ctx.channel.send("Удаляю вот это :")
    x = collection.find_one({"dz":dz})
    
    embed = discord.Embed(title=f'ДАТА '+x['timeout'])
    embed.add_field(name="Предмет ",value=x['book'])
    embed.add_field(name="ДЗ ",value=x['dz'],inline=False)
    await ctx.channel.send(embed=embed)
    
    collection.delete_one({"dz":dz})
@client.command()
async def ekfar(ctx):
    embed = discord.Embed(title="Помощь")
    embed.add_field(name="Добавить дз ",value="adddz day//mouth//year book dz",inline=False)
    embed.add_field(name="Удалить дз ",value="deletedz dz",inline=False)
    embed.add_field(name="Дз на день ",value="tomorrow day//mouth//year",inline=False)
    embed.add_field(name="Включить уведомление ",value="starttimeout",inline=False)
    await ctx.channel.send(embed=embed)
    
client.run('ODU0MDM4OTQ5MDgxMTIwODA4.YMeHwA._5b56gapDJD40xOX3zvzvfs51n0')
