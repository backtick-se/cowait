import time
import pandas as pd
from datetime import datetime
from pipeline.tasks import Task, join
from year import ScrapeYear

class Scrape(Task):
    async def run(self, start, end, **inputs):
        assert int(start) >= 2014

        years = range(int(start), int(end)+1)
        date = str(datetime.now())
        tasks = [self.spawn(ScrapeYear, date=date, year=year) for year in years]
        
        return await join(*tasks)
