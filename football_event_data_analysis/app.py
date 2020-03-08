
import opta_data_parser.player_details as pdt
import opta_data_parser.events as ope


if __name__ == "__main__":

    # file paths
    path = 'C:\\Users\\ndah\\Dropbox\\PROJECTS\\Football-analytics\\Event_analytics\\Data\\PSG_challenge\\psgchallenge\\'
    player_data = path + 'players.xml'
    event_xml = path + 'f24-24-2016-853139-eventdetails.xml'

    # players details
    players = pdt.players(player_data)
    players_dict = players.players_details_dict()

    # event details
    events = ope.EventParser(event_xml)
    team_dict = events.get_match_details()
    passes = events.get_passes(team_dict, players_dict)