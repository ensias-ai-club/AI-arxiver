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


@bot.command(name = "latest", help = "pulls a link for the most recent paper based on a search term")
async def latest(ctx, arg):
    search = query(arg, arxiv.SortCriterion.SubmittedDate)
    results = search.results()
     
    for result in results:
        cat = result.categories
        if all(x in cat for x in ['cs.AI', 'cs.LG']):
            response = f'{result.entry_id} \n **{result.title}** \n {result.summary}'
            await ctx.send(response)
            break

@bot.command(name = "best", help = "pulls a link for the most relevant paper based on a search term")
async def best(ctx, arg):
    search = query(arg, arxiv.SortCriterion.Relevance)
    results = search.results()
     
    for result in results:
        cat = result.categories
        if all(x in cat for x in ['cs.AI', 'cs.LG']):
            response = f'{result.entry_id} \n **{result.title}** \n {result.summary}'
            await ctx.send(response)
            break


bot.run(TOKEN)
