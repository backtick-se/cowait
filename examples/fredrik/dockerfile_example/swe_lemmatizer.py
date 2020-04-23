from pipeline.tasks import Task

import lemmy

class SweLemmatizer(Task):
    async def run(self, word, pos_tag='NOUN'):
        lem = lemmy.load('sv')
        result = lem.lemmatize(pos_tag, word)

        return result