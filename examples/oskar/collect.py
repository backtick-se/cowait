import boto3
import json
import pandas as pd
import aiohttp
import asyncio
from lxml import html

from pipeline.tasks import Task, join
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


async def fetch_runner_data(session, url):
    async with session.get(url) as response:
        content = await response.content.read()

        data = {}

        data = parse_table(data, content)
        data = parse_info(data, content)

        return data

class Collect(Task):
    async def run(self, year, urls, **inputs):
        async with aiohttp.ClientSession() as session:
            reqs = [fetch_runner_data(session, url) for url in urls]
            data = await join(*reqs)
        
        s3 = boto3.resource('s3').Object('backtick-running', f'{year}/{uuid()}.json')
        s3.put(Body=(bytes(json.dumps(data).encode('UTF-8'))))

        return {
            'processed': len(data)
        }