from datetime import datetime
from xml.etree.ElementTree import Element
from typing import Optional

import dateutil.parser
from defusedxml.ElementTree import parse as defused_xml_parse, ParseError

from .exceptions import FeedXMLError, FeedParseError

ns = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'feed': 'http://www.w3.org/2005/Atom'
}


def parse_xml(xml_content):
    try:
        return defused_xml_parse(xml_content)
    except ParseError:
        raise FeedXMLError('Not a valid XML document')


def get_child(element: Element, name,
              optional: bool=True) -> Optional[Element]:
    child = element.find(name, namespaces=ns)

    if child is None and not optional:
        raise FeedParseError(
            'Could not parse feed: "{}" required in "{}"'
            .format(name, element.tag)
        )

    elif child is None:
        return None

    return child


def get_text(element: Element, name, optional: bool=True) -> Optional[str]:
    child = get_child(element, name, optional)
    if child is None:
        return None

    if child.text is None:
        if optional:
            return None

        raise FeedParseError(
            'Could not parse feed: "{}" text is required but is empty'
            .format(name)
        )

    return child.text.strip()


def get_int(element: Element, name, optional: bool=True) -> Optional[int]:
    text = get_text(element, name, optional)
    if text is None:
        return None

    return int(text)


def get_datetime(element: Element, name,
                 optional: bool=True) -> Optional[datetime]:
    text = get_text(element, name, optional)
    if text is None:
        return None

    return dateutil.parser.parse(text)
