"""Download the calendars and generate output

"""

from jinja2 import Environment, FileSystemLoader

from pycon2019booth.models import Facility, BoothEvent
from pycon2019booth.spreadsheetloader import get_theater_slots, get_service

def main():
    theater = get_theater_slots(get_service())
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('page.jinja2')
    output = template.render(theater=theater)
    with open('../public/index.html', 'w') as o:
        o.write(output)


if __name__ == '__main__':
    main()
