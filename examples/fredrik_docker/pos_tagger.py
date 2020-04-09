from pipeline.tasks import Task

import spacy
import en_core_web_sm

class Tagger(Task):
    async def run(self, sentence):
        nlp = en_core_web_sm.load()
        doc = nlp(sentence)
        results = [(t.text, t.tag_) for t in doc]

        return results