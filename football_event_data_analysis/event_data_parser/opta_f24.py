import pandas as pd
from datetime import datetime
from lxml import etree
from itertools import groupby


# https://imrankhan17.github.io/Parsing-Opta-files/

# TODO: improve code by including try catch construct
# Class to parse event data
# based on work in https://imrankhan17.github.io/Parsing-Opta-files/
class EventParser:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.all_events = None

    def _read_xml_file(self):
        """Read event xml file"""
        xml_tree = etree.ElementTree(file=self.xml_file)
        self.all_events = xml_tree.getroot()

    def get_match_details(self):
        """Print match details"""
        self._read_xml_file()
        match_details = self.all_events[0].attrib
        print("%s v %s, %s %s" % (match_details["home_team_name"],
                                  match_details["away_team_name"],
                                  match_details["competition_name"],
                                  match_details["season_name"]))
        print("Date: %s" % datetime.strftime(datetime.strptime(match_details["game_date"],
                                                               '%Y-%m-%dT%H:%M:%S'), "%A %d %B %Y"))
        print("Kick-off: %s" % datetime.strftime(datetime.strptime(match_details["game_date"],
                                                                   '%Y-%m-%dT%H:%M:%S'), "%I%p").lstrip("0"))
        team_info_dict = {match_details["home_team_id"]: {},
                          match_details["away_team_id"]: {}
                          }
        team_info_dict[match_details["home_team_id"]]['name'] = match_details["home_team_name"]
        team_info_dict[match_details["away_team_id"]]['name'] = match_details["away_team_name"]

        # get the player ids of the first 11
        for game in self.all_events:
            for team in game:
                if team.attrib.get("type_id") == '34':
                    for q in team:
                        qualifier = q.attrib.get("qualifier_id")
                        if qualifier == "30": # match day squad
                            team_info_dict[team.attrib.get("team_id")]['squad'] = q.attrib.get("value")
                        if qualifier == "131": # first 11
                            team_info_dict[team.attrib.get("team_id")]['first_team'] = q.attrib.get("value")

        return team_info_dict

    def get_all_events(self):
        """Extract all game event."""
        opta_event_id = []  # The unique ID for this event within Opta’s entire database of all events in all games
        game_event_id = []  # unique ID for this event within this game for each team
        event_type = []
        event_name = []
        event_start_x = []
        event_start_y = []
        event_outcome = []
        event_min = []
        event_sec = []
        event_period = []
        event_team = []
        player_id = []

        for game in self.all_events:
            for event in game:
                opta_event_id.append(int(event.attrib.get('id')))
                game_event_id.append(int(event.attrib.get('event_id')))
                event_type.append(int(event.attrib.get("type_id")))     # TODO: create event identifier
                event_name.append(int(event.attrib.get("type_id")))  # TODO: create event identifier
                event_start_x.append(float(event.attrib.get("x")))
                event_start_y.append(float(event.attrib.get("y")))
                event_outcome.append(int(event.attrib.get("outcome")))
                event_min.append(float(event.attrib.get("min")))
                event_sec.append(float(event.attrib.get("sec")))
                event_period.append(event.attrib.get("period_id"))
                event_team.append(int(event.attrib.get("team_id")))
                player_id.append(event.attrib.get("player_id"))

        # event quantifiers: to be determined after better understanding of xml file
        event_df = pd.DataFrame({"opta_event_id": opta_event_id, "game_event_id": game_event_id,
                                 "event_type": event_type, "team": event_team,"player_id": player_id,
                                 "period": event_period, "outcome": event_outcome,"min": event_min, "sec": event_sec,
                                 "x_start": event_start_x, "y_start": event_start_y})
        return event_df

    def get_passes(self):
        """Extract all passes."""
        opta_event_id = []  # The unique ID for this event within Opta’s entire database of all events in all games
        game_event_id = []  # unique ID for this event within this game for each team
        pass_start_x = []
        pass_start_y = []
        pass_outcome = []
        pass_min = []
        pass_sec = []
        pass_period = []
        pass_team = []
        pass_end_x = []
        pass_end_y = []
        pass_length = []
        pass_angle = []
        pass_zone = []
        pass_real = []
        pass_player = []

        for game in self.all_events:
            for event in game:
                if event.attrib.get("type_id") == '1':
                    opta_event_id.append(int(event.attrib.get('id')))
                    game_event_id.append(int(event.attrib.get('event_id')))
                    pass_start_x.append(float(event.attrib.get("x")))
                    pass_start_y.append(float(event.attrib.get("y")))
                    pass_outcome.append(event.attrib.get("outcome"))
                    pass_min.append(float(event.attrib.get("min")))
                    pass_sec.append(float(event.attrib.get("sec")))
                    pass_period.append(int(event.attrib.get("period_id")))
                    pass_team.append(int(event.attrib.get("team_id")))
                    pass_player.append(int(event.attrib.get("player_id")))

                    # pass quantifiers
                    for q in event:
                        qualifier = q.attrib.get("qualifier_id")
                        if qualifier == "140":
                            pass_end_x.append(float(q.attrib.get("value")))
                        if qualifier == "141":
                            pass_end_y.append(float(q.attrib.get("value")))
                        if qualifier == "212":
                            pass_length.append(float(q.attrib.get("value")))
                        if qualifier == "213":
                            pass_angle.append(float(q.attrib.get("value")))
                        if qualifier == "56":
                            pass_zone.append(q.attrib.get("value"))

        # pass_start_point = [Point(pass_start_x[i],pass_start_y[i]) for i in range(len(pass_start_x))]
        # pass_end_point = [Point(pass_end_x[i],pass_end_y[i]) for i in range(len(pass_end_x))]

        pass_df = pd.DataFrame({"opt_event_id": opta_event_id, "game_event_id": game_event_id, "team": pass_team,
                                "player_id": pass_player, "period": pass_period, "min": pass_min, "sec": pass_sec,
                                "pass_zone": pass_zone, "x_start": pass_start_x,"y_start": pass_start_y,
                                "x_end": pass_end_x, "y_end": pass_end_y, "pass_length": pass_length,
                                "pass_angle": pass_angle, "outcome": pass_outcome})
        return pass_df

    def get_goals(self):
        """Extract all goal events"""
        opta_event_id = []  # The unique ID for this event within Opta’s entire database of all events in all games
        game_event_id = []  # unique ID for this event within this game for each team
        goal_shot_x = []
        goal_shot_y = []
        goal_zone = []
        goal_outcome = []
        goal_min = []
        goal_sec = []
        goal_period = []
        goal_team = []
        goal_mouth_y = []
        goal_mouth_z = []
        goal_assisted = []
        body_part = []
        player_id = []

        body_dict = {"15": "head",
                     "72": "left foot",
                     "20": "right foot",
                     "21": "other body part"}

        for game in self.all_events:
            for event in game:
                if event.attrib.get("type_id") == '16':
                    opta_event_id.append(int(event.attrib.get('id')))
                    game_event_id.append(int(event.attrib.get('event_id')))
                    goal_shot_x.append(float(event.attrib.get("x")))
                    goal_shot_y.append(float(event.attrib.get("y")))
                    goal_outcome.append(int(event.attrib.get("outcome")))
                    goal_min.append(int(event.attrib.get("min")))
                    goal_sec.append(int(event.attrib.get("sec")))
                    goal_period.append(int(event.attrib.get("period_id")))
                    goal_team.append(int(event.attrib.get("team_id")))
                    player_id.append(int(event.attrib.get("player_id")))

                    for q in event:
                        qualifier = q.attrib.get("qualifier_id")
                        if qualifier == "103":
                            goal_mouth_z.append(float(q.attrib.get("value")))
                        if qualifier == "102":
                            goal_mouth_y.append(float(q.attrib.get("value")))
                        if qualifier == "56":
                            goal_zone.append(q.attrib.get("value"))
                        if qualifier in ["15", "72", "20", "21"]:
                            body_part.append(body_dict[qualifier])

        goal_df = pd.DataFrame(
            {'opta_event_id': opta_event_id, 'game_event_id': game_event_id, 'goal_shot_x': goal_shot_x,
             'goal_shot_y': goal_shot_y,
             'goal_outcome': goal_outcome, 'goal_min': goal_min, 'goal_sec': goal_sec, 'goal_period': goal_period,
             'goal_team': goal_team,
             'player_id': player_id, 'goal_post_z': goal_mouth_z, 'goal_post_y': goal_mouth_y, 'goal_zone': goal_zone,
             'body_part': body_part})

        return goal_df

    def get_all_shots(self):
        """Extract all shots"""
        shots_df = pd.DataFrame()

        shot_dict = {'13': 'Shot off target',
                     '14': 'Post',
                     '15': 'Shot saved',
                     '16': 'Goal'}

        body_dict = {"15": "head",
                     "72": "left foot",
                     "20": "right foot",
                     "21": "other body part"}

        shot_play_dict = {'22': 'regular play',
                          '23': 'fast break',
                          '24': 'set piece',
                          '25': 'from corner',
                          '26': 'free kick',
                          '96': 'corner situation',
                          '112': 'scramble',
                          '160': 'throw-in set piece',
                          '9': 'penalty',
                          '28': 'own goal'}

        i = 0  # pandas index counter
        for game in self.all_events:
            for event in game:
                # handle other shots
                if event.attrib.get("type_id") in ['13', '14', '15', '16']:
                    shots_df.at[i, 'opta_event_id'] = int(event.attrib.get('id'))
                    shots_df.at[i, 'game_event_id'] = int(event.attrib.get('event_id'))
                    shots_df.at[i, 'shot_type'] = shot_dict[event.attrib.get("type_id")]
                    shots_df.at[i, 'shot_x'] = float(event.attrib.get("x"))
                    shots_df.at[i, 'shot_y'] = float(event.attrib.get("y"))
                    shots_df.at[i, 'shot_min'] = int(event.attrib.get("min"))
                    shots_df.at[i, 'shot_sec'] = int(event.attrib.get("sec"))
                    shots_df.at[i, 'shot_period'] = int(event.attrib.get("period_id"))
                    shots_df.at[i, 'shot_team_id'] = int(event.attrib.get("team_id"))
                    shots_df.at[i, 'player_id'] = int(event.attrib.get("player_id"))

                    for q in event:
                        qualifier = q.attrib.get("qualifier_id")
                        if qualifier in body_dict.keys():
                            shots_df.at[i, 'body_part'] = body_dict[qualifier]
                        if qualifier in shot_play_dict.keys():
                            shots_df.at[i, 'shot_play'] = shot_play_dict[qualifier]

                    # parse goals, off target or hits the post
                    if event.attrib.get("type_id") in ['13', '14', '16']:
                        for q in event:
                            qualifier = q.attrib.get("qualifier_id")
                            if qualifier == '102':
                                shots_df.at[i, 'goal_mouth_y'] = float(q.attrib.get("value"))
                            if qualifier == '103':
                                shots_df.at[i, 'goal_mouth_z'] = float(q.attrib.get("value"))

                    # handle saved shots
                    if event.attrib.get("type_id") == '15':
                        for q in event:
                            qualifier = q.attrib.get("qualifier_id")
                            if qualifier == '146':
                                shots_df.at[i, 'saved_x'] = float(q.attrib.get("value"))
                            if qualifier == '147':
                                shots_df.at[i, 'saved_y'] = float(q.attrib.get("value"))

                i = i + 1  # increment pandas index

        return shots_df
