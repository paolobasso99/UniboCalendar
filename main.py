import requests
from ics import Calendar, Event
import arrow
from Settings import Settings

settings = Settings()

YEAR = settings.get('YEAR')
COURSE = settings.get('COURSE')


def unibo_calendar():
    print("Options:")
    print("Year: " + YEAR)
    print("Course: " + COURSE)

    # Get data
    print("Getting json data...")
    url = 'https://corsi.unibo.it/laurea/' + \
        str(COURSE) + "/orario-lezioni/@@orario_reale_json?anno=" + str(YEAR)
    events = requests.get(url).json()
    print(str(len(events)) + " events found!")

    # Build calendar
    calendar = Calendar()
    for event in events:
        # Build event
        e = Event(location=event.get("aule")[0].get(
            "des_ubicazione"), alarms=None)
        e.name = event.get("title").title() + " - " + \
            event.get("aule")[0].get("des_risorsa")
        e.begin = arrow.get(event.get("start")).replace(
            tzinfo="Europe/Rome")
        e.end = arrow.get(event.get("end")).replace(tzinfo="Europe/Rome")

        # Add event to calendar
        calendar.events.add(e)

    # Print file
    print("Writing .ics...")
    with open('UniboCalendar.ics', 'w') as file:
        file.writelines(calendar)
        print("Done!")


if __name__ == "__main__":
    unibo_calendar()
