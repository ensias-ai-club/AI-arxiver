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
    if term.startswith('http') or term.startswith('arxiv.org'):
        arxiv_id = ""
        try:
            arxiv_id = term.replace("https://arxiv.org/abs/", "")
        except:
            arxiv_id = term.replace("https://arxiv.org/pdf/", "")
        query = arxiv.Search(
            id_list = [arxiv_id],
            sort_by = priority,
            sort_order = arxiv.SortOrder.Descending
        )

    else:
        query = arxiv.Search(
            query = term,
            sort_by = priority,
            sort_order = arxiv.SortOrder.Descending
        )
    return query

mlcat = ['cs.AI', 'cs.LG', 'cs.CV', 'cs.CL', 'cs.NE', 'stat.ML', 'cs.RO', 'math.MP', 'math.IT', 'math.GM', 'math.OC', 'math.PR', 'math.NA', 'math.ST', 'stat.ME', 'stat.TH', 'stat.CO']


@bot.group(pass_context = True, help = "pulls the most recent paper based on a search term")
async def latest(ctx):
    if ctx.invoked_subcommand == None:
        await ctx.send('please specify a valid subcommand')


@latest.group(name = "summary", help = "provide a summary for the paper")
async def summary(ctx, arg):
    try :
        search = query(arg, arxiv.SortCriterion.SubmittedDate)
        results = search.results()
     
        for result in results:
            cat = result.categories
            if any(x in cat for x in mlcat):
                response = f'{result.entry_id} \n **{result.title}** \n {result.summary}'
                await ctx.send(response)
                break
    except:
        await ctx.send('timeout : paper probably not available')

@latest.group(name = "download", help = "provide a pdf download for the paper")
async def download(ctx, arg):
    try : 
        search = query(arg, arxiv.SortCriterion.SubmittedDate)
        results = search.results()
     
        for result in results:
            cat = result.categories
            if any(x in cat for x in mlcat):
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
async def summary(ctx, arg):
    try : 
        search = query(arg, arxiv.SortCriterion.Relevance)
        results = search.results()
     
        for result in results:
            cat = result.categories
            if any(x in cat for x in mlcat):
                response = f'{result.entry_id} \n **{result.title}** \n {result.summary}'
                await ctx.send(response)
                break
    except :
        await ctx.send('timeout : paper probably not available')

@best.group(name = "download", help = "provide a pdf download for the paper")
async def download(ctx, arg):
    try : 
        search = query(arg, arxiv.SortCriterion.Relevance)
        results = search.results()
     
        for result in results:
            cat = result.categories
            if any(x in cat for x in mlcat):
                response = result.pdf_url
                await ctx.send(response)
                break
    except:
        await ctx.send('timeout : paper probably not available')




bot.run(TOKEN)
