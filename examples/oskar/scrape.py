import time
import pandas as pd
from pipeline.tasks import Task, join
from year import ScrapeYear

class Scrape(Task):
    async def run(self, start, end, **inputs):
        years = range(start, int(end)+1)
        tasks = [self.spawn(ScrapeYear, year=year) for year in years]
        
        return await join(*tasks)
