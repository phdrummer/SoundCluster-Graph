import operator
import networkx as nx


def get_all_followings(client, user_id=None):
    """
    Returns your followings if no user_id provided, else the users followings
    :param client: SC Client
    :param user_id: Optional userID to get
    :return:
    """
    # start paging through results, 200 at a time
    if user_id:
        response = client.get('/users/{}/followings'.format(user_id), limit=200,
                              linked_partitioning=1)
    else:
        response = client.get('/me/followings', limit=200,
                              linked_partitioning=1)
    followers = response.collection
    previous_result = followers
    # if there are more than 200 followers, keeps getting them
    while hasattr(previous_result, 'next_href'):
        next_followers = client.get(previous_result.next_href, limit=200, linked_partitioning=1)
        followers.extend(next_followers.collection)
        previous_result = followers
    return followers


def get_stats(g):
    """
    Generate stats based ond a graph and return a dict
    :param G: NX Graph
    :return: Dictionary of stats
    """
    degree = g.degree()
    info = nx.info(g)
    frequency_list = sorted(degree.items(), key=operator.itemgetter(1), reverse=True)
    cent = nx.degree_centrality(g)
    centrality = sorted(cent.items(), key=operator.itemgetter(1), reverse=True)
    page = nx.pagerank(g)
    page_rank = sorted(page.items(), key=operator.itemgetter(1), reverse=True)
    return locals()


def get_my_user_id(client):

    return client.get('/me').id


def get_neighbors(G, node):
    return G.neighbors(node)