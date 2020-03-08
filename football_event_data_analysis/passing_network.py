
from itertools import groupby
import warnings
warnings.filterwarnings("ignore")


def create_pass_node(graph, source_player_id, dest_player_id, source_player_name, dest_player_name):
    graph.add_edge(source_player_id, dest_player_id)
    graph.node[source_player_id]['label'] = source_player_name
    graph.node[dest_player_id]['label'] = dest_player_name
    graph[source_player_id][dest_player_id]['weight'] = 1

    return graph


def group_consecutive_passes(game_event_id):
    """Group consecutive passes"""
    consecutive_passes = []
    for k, g in groupby(enumerate(game_event_id), lambda ix: ix[0] - ix[1]):
        consecutive_passes.append([i[1] for i in g])

    return consecutive_passes


def create_passing_graph(df, team_id, players_dict):
    team_df = df[(df['team'] == team_id) & (df['outcome'] == '1')]
    team_df['game_event_id'] = team_df['game_event_id'].astype('int32')
    game_event_id = team_df['game_event_id']

    consecutive_passes = group_consecutive_passes(game_event_id)

    G = nx.DiGraph()  # graph to store pass network
    # loop over all grouped events only multi events are considered
    for pass_event in consecutive_passes:
        for source_id, dest_id in zip(pass_event, pass_event[1:]):  # only two or morw consecutive events are considered

            # source player id and name
            source_player_id = team_df[team_df['game_event_id'] == source_id]['player_id'].item()
            source_player_name = players_dict[source_player_id]

            # destination player id and name
            dest_player_id = team_df[team_df['game_event_id'] == dest_id]['player_id'].item()
            dest_player_name = players_dict[dest_player_id]
            # print(source_player_name)

            if G.has_edge(source_player_id, dest_player_id) is True:
                G[source_player_id][dest_player_id]['weight'] += 1
            else:
                create_pass_node(G, source_player_id, dest_player_id, source_player_name, dest_player_name)

            # TODO: check the second part in the source
            # https://sites.temple.edu/tudsc/2018/10/23/create-a-network-from-xml-and-visualize-it-a-soccer-player-passing-network/

    return G


def team_pass_pattern(df, team_id, players_dict):
    team_df = df[(df['team'] == team_id) & (df['outcome'] == '1')]
    team_df['game_event_id'] = team_df['game_event_id'].astype('int32')
    game_event_id = team_df['game_event_id']

    pass_pattern = {}
    consecutive_passes = group_consecutive_passes(game_event_id)

    for pass_event in consecutive_passes:
        if len(pass_event) < 2:
            continue

        codes = {}  # dict to store player ids and Alphabet
        alphabets = [chr(x) for x in range(ord('A'), ord('Z') + 1)]

        pattern = ""
        for event_id in pass_event:  # only two or morw consecutive events are considered

            # source player id and name
            player_id = team_df[team_df['game_event_id'] == event_id]['player_id'].item()
            #player_name = players_dict[player_id]

            if player_id in pass_pattern:
                pattern = pattern + codes[player_id]
            else:
                player_code = alphabets.pop(0)
                codes[player_id] = player_code
                pattern = pattern + player_code

        if pattern in pass_pattern:
            pass_pattern[pattern] += 1
        else:
            pass_pattern[pattern] = 1

    return pass_pattern
