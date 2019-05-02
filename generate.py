"""Download the calendars and generate output

"""
from dataclasses import dataclass, field
from datetime import time
from typing import Optional, List

from jinja2 import Environment, FileSystemLoader

from pycon2019booth.spreadsheetloader import get_theater_slots


@dataclass
class BoothEvent:
    start: str
    finish: str
    title: str
    who: str


@dataclass
class Facility:
    title: str
    thursday: Optional[List[BoothEvent]] = field(default_factory=list)
    friday: Optional[List[BoothEvent]] = field(default_factory=list)
    saturday: Optional[List[BoothEvent]] = field(default_factory=list)


def make_theater() -> Facility:
    theater = Facility(title='Theater')
    theater.thursday = [
        BoothEvent(start='10:00', finish='10:30', who='Michael &amp; Matt', title='Something we can have on the '
                                                                                  'laptop in public'),
        BoothEvent(start='10:30', finish='11:00', who='Someone Else', title='Another Thing'),
    ]
    theater.friday = [
        BoothEvent(start='10:00', finish='10:30', who='Michael &amp; Matt', title='Blackjack and Hookers'),
        BoothEvent(start='10:30', finish='11:00', who='Someone Else', title='Another Thing'),
    ]
    theater.saturday = [
        BoothEvent(start='10:00', finish='10:30', who='Michael &amp; Matt', title='NASA Stuff'),
        BoothEvent(start='10:30', finish='11:00', who='Someone Else', title='Another Thing'),
    ]
    return theater


def main():
    theater = get_theater_slots()
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('page.jinja2')
    output = template.render(theater=theater)
    with open('public/index.html', 'w') as o:
        o.write(output)


if __name__ == '__main__':
    main()
