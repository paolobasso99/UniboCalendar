import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
import arrow

YEAR = 1


def unibo_calendar():
    # Start calendar
    calendar = Calendar()

    # Get HTML
    url = 'https://corsi.unibo.it/laurea/IngegneriaGestionale/orario-lezionii?anno=' + YEAR
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, features="html.parser")

    # Get data
    url = soup.find("div", {"id" : "calendar"}).get("data-url")
    result = requests.get(url).json()
    events = result.get("events")

    # Build calendar
    for event in events:
        if event.get("lettere") != "L-Z":  # If not "L-Z"

            # Build event
            e = Event(location=event.get("aule")[0].get("des_ubicazione"), alarms=None)
            e.name = event.get("title").title() + " - " + event.get("aule")[0].get("des_risorsa")
            e.begin = arrow.get(event.get("start")).replace(tzinfo="Europe/Rome")
            e.end = arrow.get(event.get("end")).replace(tzinfo="Europe/Rome")

            # Add event to calendar
            calendar.events.add(e)

    # Print file
    with open('UniboCalendar.ics', 'w') as file:
        file.writelines(calendar)


if __name__ == "__main__":
    unibo_calendar()
