import stanza
from typing import List
import os
from app.core.models.named_entity_model import NamedEntity

class NERService:
    def __init__(self, lang: str = "ar"):
        self.lang = lang
        self._download_if_needed(lang)
        self.nlp = stanza.Pipeline(lang=lang, processors="tokenize,ner", use_gpu=False)

    def _download_if_needed(self, lang: str):
        # Default stanza model directory
        stanza_dir = os.path.expanduser("~/.stanza_resources")
        lang_dir = os.path.join(stanza_dir, lang)
        if not os.path.exists(lang_dir):
            print(f"Downloading stanza models for language: {lang}")
            stanza.download(lang, processors="tokenize,ner", verbose=False)

    def extract_named_entities(self, text: str) -> List[NamedEntity]:
        doc = self.nlp(text)
        return [NamedEntity(ent.text, ent.type) for ent in doc.ents]
