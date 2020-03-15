import boto3
import os
import json
import pandas as pd
import aiohttp
import asyncio
from lxml import html

from pipeline.tasks import Task, join, sleep
from pipeline.utils import uuid

def parse_table(data, content):
    splits = pd.read_html(content)[0]

    # Add split times and paces from table
    for i, km in enumerate(["5km", "10km", "15km", "20km", "21km"]):
        row = splits.iloc[i]

        data[f"{km}_time"] = str(row[2])
        data[f"{km}_min/km"] = str(row[3])
        data[f"{km}_plac"] = str(row[4])

    return data


def parse_info(data, content):
    tree = html.fromstring(content)    # Parse html tree

    elements = tree.xpath("//div[contains(@class, 'infobox')]")
    for e in elements:
        key, value = e.text_content().strip().split("\n")

        data[key.strip()] = value.strip()

    return data


async def fetch_runner_data(session, url, current_retry=0):
    try:
        async with session.get(url) as response:
            content = await response.content.read()

            data = {}
            try:
                data = parse_table(data, content)
            except:
                print("Couldnt parse table for", url)
                pass
            data = parse_info(data, content)

            return data
    except:
        print("couldn't fetch", url)
        if current_retry < 3:
            await sleep(0.1)
            return await fetch_runner_data(session, url, current_retry=current_retry+1)

    return False

class Collect(Task):
    async def run(self, date, year, urls, **inputs):
        async with aiohttp.ClientSession() as session:
            reqs = [fetch_runner_data(session, url) for url in urls]
            data = await join(*reqs)
            data = list(filter(lambda x: x != False, data))     # remove failed requests
        
        s3 = boto3.resource('s3').Object('backtick-running', f'{date}/{year}/{uuid()}.json')
        s3.put(Body=(bytes(json.dumps(data).encode('UTF-8'))))

        return f"{year} finished {len(data)}"