#!/usr/bin/env python3

import re
import ics
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup

def get_team_HTML(team_url):
    """
    Get the HTML content for a specific team's page.

    :param team_url: The URL of the team's page
    :returns: The HTML content of the team's page
    """

    # Send the GET request
    response = requests.get(team_url)

    # DEBUG: Check if the request was successful (Status Code 200)
    # print(f"Status Code: {response.status_code}")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup  # Return the parsed HTML content


def parse_schedule(soup):
    """
    Parse the schedule from the team's HTML content.

    :param soup: The BeautifulSoup object containing the team's HTML content
    :returns: A list of games with their details (date, time, opponent, court)
    """

    games = []
    schedule_div = soup.find('div', class_='games-schedule')
    games_list = schedule_div.find_all('div', class_='grid')
    for game in games_list:
        new_game = {}

        game_info = game.find_all('div')
        for cell in game_info:
            heading_found = cell.find('h5')
            heading = cell.find('h5').text.strip() if cell.find('h5') else ""

            if heading == "Opponent":
                # Extract the opponent's name and URL
                opponent_link = cell.find('a')
                if opponent_link:
                    opponent_name = opponent_link.text.strip()
                    opponent_url = opponent_link['href']
                    value = opponent_name  # Get the opponent's name as the value
                    # new_game['Opponent'] = opponent_name
                    # new_game['Opponent URL'] = opponent_url
                else:
                    value = "Opponent Unknown"
            else:
                value = heading_found.next_sibling.strip() if heading else ""  # Get the text after the heading

            new_game[heading] = value
        games.append(new_game)

    return games


def download_ics(games, team_name):
    """
    Download the ICS file containing the games schedule.

    :param games: A list of games with their details
    :param team_name: The name of the team
    """

    games_calendar = ics.Calendar()
    for game in games:
        game_start_time = datetime.strptime(game['Date'] + " " +game['Time'], "%d/%m/%Y %I:%M%p").replace(tzinfo=ZoneInfo("Australia/Sydney"))

        event = ics.Event()
        event.name = f"{team_name} vs {game['Opponent']}"
        event.location = game['Court']
        event.begin = game_start_time
        event.end = game_start_time + timedelta(minutes=45)  # Assuming each game lasts 45 minutes

        games_calendar.events.add(event)

    # User selects download location
    # download_location = input("Enter the download location for the ICS file: ")
    with open(f"{team_name}_schedule.ics", 'w') as f:
        f.writelines(games_calendar.serialize_iter())


def main():
    # Prompt user for a team URL
    team_url = input("Enter the team URL: ")

    # Make a request to that URL
    team_soup = get_team_HTML(team_url)

    # Parse the schedule
    # <div class="widget col-sm-12 games-schedule">
    games = parse_schedule(team_soup)

    # Get the team name from the soup
    name_soup = get_team_HTML(team_url)
    team_name_HTML = name_soup.find('div', class_='team-overview').find('h1').text
    team_name = re.match(r"^(\s|\n)*(.*)\n@", team_name_HTML).group(2).strip()  # Extract the team name from the heading

    # Convert to ICS & download
    download_ics(games, team_name)


if __name__ == "__main__":
    main()