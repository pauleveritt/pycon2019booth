"""Download the calendars and generate output

"""
from dataclasses import dataclass, field
from typing import Optional, List

from jinja2 import Environment, FileSystemLoader


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
        BoothEvent(start='10:00', finish='10:30', who='Michael &amp; Matt', title='Special Book Announcement'),
        BoothEvent(start='10:30', finish='11:00', who='Someone Else', title='Another Thing'),
    ]
    theater.friday = [
        BoothEvent(start='10:00', finish='10:30', who='Michael &amp; Matt', title='Special Book Announcement'),
        BoothEvent(start='10:30', finish='11:00', who='Someone Else', title='Another Thing'),
    ]
    theater.saturday = [
        BoothEvent(start='10:00', finish='10:30', who='Michael &amp; Matt', title='Special Book Announcement'),
        BoothEvent(start='10:30', finish='11:00', who='Someone Else', title='Another Thing'),
    ]
    return theater


def main():
    theater = make_theater()
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('page.jinja2')
    output = template.render(theater=theater)
    with open('public/index.html', 'w') as o:
        o.write(output)


if __name__ == '__main__':
    main()
