from dataclasses import dataclass, field
from typing import Optional, List, Dict, Union


@dataclass
class SelectorRule:
    selector: str
    attribute: Optional[str] = None  # e.g., "src", "href"
    text: bool = True                # True = extract text, False = inner HTML
    multiple: bool = False           # True = list of values

@dataclass
class ScraperConfig:
    title: Optional[Union[str, SelectorRule]] = None
    date: Optional[Union[str, SelectorRule]] = None
    content: Optional[Union[str, SelectorRule]] = None
    images: Optional[SelectorRule] = None
    tags: Optional[SelectorRule] = None
    custom_fields: Dict[str, SelectorRule] = field(default_factory=dict)  # extensibility
