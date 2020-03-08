
import pandas as pd
from bs4 import BeautifulSoup
import logging


class Players:
    """Parse player xml file and extract player details."""
    def __init__(self, filename):
        self.filename = filename
        self.players = None     # place holder for xml tree

    def read_players_xml_file(self):
        """Read xml file."""
        infile = open(self.filename, mode="r", encoding="utf-8")
        contents = infile.read()
        # Parse players xml file using beautifulsoup
        soup = BeautifulSoup(contents, 'xml')
        self.players = soup.find_all('Player')

    def players_details_dict(self):
        """Convert xml file and return a pandas dataframe"""
        self.read_players_xml_file()

        player_ids = []     # list to hold player ids
        player_names = []   # list to hold player names

        # Loop over all players and extract player name and id
        # save player_id => player_name as key => value pair in a python dictionary
        for player in self.players:
            player_ids.append(player.attrs['uID'][1:])
            player_names.append(player.Name.string.strip())
        player_dict = dict(zip(player_ids, player_names))

        return player_dict

    def player_details(self):
        """Extract player personal details from file."""
        self.read_players_xml_file()

        df = pd.DataFrame()  # DataFrame to store player details
        i = 0   # index for pandas dataframe
        # Loop over all players in the players xml
        for player in self.players:

            # extract players unique identifier
            # TODO: check how to improve this code
            player_uid = player.attrs['uID']
            player_uid = player_uid[1:]
            df.at[i, 'player_id'] = player_uid

            # get player positions
            # TODO: check for players with multiple positions
            df.at[i, 'position'] = player.Position.string.strip().encode('utf-8', 'ignore')

            # loop over Stat tags in xml doc [other personal information about the current player]
            stats = player.find_all('Stat')
            for stat in stats:
                try:
                    field = stat.attrs['Type'].strip()  # get field name in xml tag
                    value = stat.string.strip()         # get value corresponding to the above field
                    df.at[i, field] = value
                except AttributeError as error:
                    logging.info('Value none found {}'.format(error))
            i = i + 1

        return df

