#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from discord.ext import commands
from dotenv import load_dotenv

import arxiv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


bot = commands.Bot(command_prefix='!')

def query(term, priority):
    query = arxiv.Search(
        query = term,
        sort_by = priority,
        sort_order = arxiv.SortOrder.Descending
    )
    return query

mlcat = ['cs.AI', 'cs.LG', 'cs.CV', 'cs.CL', 'cs.NE', 'stat.ML', 'cs.RO']
mathcat = ['math.MP', 'math.IT', 'math.GM', 'math.OC', 'math.PR', 'math.NA']


@bot.group(pass_context = True, help = "pulls the most recent paper based on a search term")
async def latest(ctx):
    if ctx.invoked_subcommand == None:
        await ctx.send('please specify a valid subcommand')


@latest.group(name = "summary", help = "provide a summary for the paper")
async def summary(ctx, arg, arg1 = mlcat):
    try :
        search = query(arg, arxiv.SortCriterion.SubmittedDate)
        results = search.results()
     
        for result in results:
            cat = result.categories
            if any(x in cat for x in arg1):
                response = f'{result.entry_id} \n **{result.title}** \n {result.summary}'
                await ctx.send(response)
                break
    except:
        await ctx.send('timeout : paper probably not available')

@latest.group(name = "download", help = "provide a pdf download for the paper")
async def download(ctx, arg, arg1 = mlcat):
    try : 
        search = query(arg, arxiv.SortCriterion.SubmittedDate)
        results = search.results()
     
        for result in results:
            cat = result.categories
            if any(x in cat for x in arg1):
                response = result.pdf_url 
                await ctx.send(response)
                break
    except:
        await ctx.send('timeout : paper probably not available')

@bot.group(pass_context = True, help = "pulls the most relevant paper based on a search term")
async def best(ctx):
    if ctx.invoked_subcommand == None:
        await ctx.send('please specify a valid subcommand')



@best.group(name = "summary", help = "provide summary for the paper")
async def summary(ctx, arg, arg1 = mlcat):
    try : 
        search = query(arg, arxiv.SortCriterion.Relevance)
        results = search.results()
     
        for result in results:
            cat = result.categories
            if any(x in cat for x in arg1):
                response = f'{result.entry_id} \n **{result.title}** \n {result.summary}'
                await ctx.send(response)
                break
    except :
        await ctx.send('timeout : paper probably not available')

@best.group(name = "download", help = "provide a pdf download for the paper")
async def download(ctx, arg, arg1 = mlcat):
    try : 
        search = query(arg, arxiv.SortCriterion.Relevance)
        results = search.results()
     
        for result in results:
            cat = result.categories
            if any(x in cat for x in arg1):
                response = result.pdf_url
                await ctx.send(response)
                break
    except:
        await ctx.send('timeout : paper probably not available')




bot.run(TOKEN)
