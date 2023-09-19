import http.client
import json
import csv
from os import name
import pickle


class Graph:

    # Do not modify. 
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
        self.nodes creates an empty list of each actor & their ID
        self.edges create an empty list of 2 actor's name per row; source and target
        """
        self.nodes = [] 
        self.node_weights = dict()
        self.edges = [] 
        self.edge_weights = dict()
        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0], n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0], e[1]) for e in edges_CSV]


    def add_node(self, id: str, name: str, weight: int = None) -> None:
        """
        (id and name) are data pairs and they need to stay together
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        if (id, name) not in self.nodes:
            self.nodes.append((id, name))
            if weight:
                self.node_weights[(id, name)] = weight


    def add_edge(self, source: str, target: str, weight: int = None) -> None:
        """
        Add an edge between two nodes if it does not already exist.
        An edge is represented by a tuple containing two strings: e.g.: ('source', 'target').
        Where 'source' is the id of the source node and 'target' is the id of the target node
        e.g., for two nodes with ids 'a' and 'b' respectively, add the tuple ('a', 'b') to self.edges
        """
        if (source, target) not in self.edges and (target, source) not in self.edges:
            self.edges.append((source, target))
            if weight:
                self.edge_weights[(source, target)] = weight


    def total_nodes(self) -> int:
        """
        Returns an integer value for the total number of nodes in the graph
        """
        return len(self.nodes)

    def total_edges(self) -> int:
        """
        Returns an integer value for the total number of edges in the graph
        """
        return len(self.edges)


    def max_degree_nodes(self) -> dict:
        """
        Return the node(s) with the highest degree
        Return multiple nodes in the event of a tie
        Format is a dict where the key is the node_id and the value is an integer for the node degree
        e.g. {'a': 8}
        or {'a': 22, 'b': 22}
        """
        flat_list=[]
        for row in self.edges:
            flat_list.extend(row)

        dictionary={}
        for x in flat_list:
            if x in dictionary:
                dictionary[x]+=1
            else:
                dictionary[x]=1

        max_degree = max(dictionary.values())

        def my_filter_function(pair):
            key, value = pair
            if value == max_degree:
                return True
            else:
                return False

        max_degree_dict = dict(filter(my_filter_function, dictionary.items()))
 
        return max_degree_dict



    def print_nodes(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.nodes)


    def print_edges(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.edges)


    # Do not modify
    def write_edges_file(self, path="edges.csv")->None:
        """
        write all edges out as .csv
        :param path: string
        :return: None
        """
        edges_path = path
        edges_file = open(edges_path, 'w', encoding='utf-8')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(e[0] + "," + e[1] + "\n")

        edges_file.close()
        print("finished writing edges to csv")


    # Do not modify
    def write_nodes_file(self, path="nodes.csv")->None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w', encoding='utf-8')

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")


class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key:str):
        self.api_key=api_key


    def get_movie_cast(self, movie_id:str, limit:int=None, exclude_ids:list=None) -> list:
        """
        Get the movie cast for a given movie id, with optional parameters to exclude an cast member
        from being returned and/or to limit the number of returned cast members
        documentation url: https://developers.themoviedb.org/3/movies/get-movie-credits

        :param string movie_id: a movie_id
        :param list exclude_ids: a list of ints containing ids (not cast_ids) of cast members  that should be excluded from the returned result
            e.g., if exclude_ids are [353, 455] then exclude these from any result.
        :param integer limit: maximum number of returned cast members by their 'order' attribute
            e.g., limit=5 will attempt to return the 5 cast members having 'order' attribute values between 0-4
            If after excluding, there are fewer cast members than the specified limit, then return the remaining members (excluding the ones whose order values are outside the limit range). 
            If cast members with 'order' attribute in the specified limit range have been excluded, do not include more cast members to reach the limit.
            If after excluding, the limit is not specified, then return all remaining cast members."
            e.g., if limit=5 and the actor whose id corresponds to cast member with order=1 is to be excluded,
            return cast members with order values [0, 2, 3, 4], not [0, 2, 3, 4, 5]
        :rtype: list
            return a list of dicts, one dict per cast member with the following structure:
                [{'id': '97909' # the id of the cast member
                'character': 'John Doe' # the name of the character played
                'credit_id': '52fe4249c3a36847f8012927' # id of the credit, ...}, ... ]
                Note that this is an example of the structure of the list and some of the fields returned by the API.
                The result of the API call will include many more fields for each cast member.
        """

        #searching on TMBD website
        import requests

        movie_search_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlMDcyMDJiYzhjZTZmOGUyZWVhYjQ1ZDBiZjBkYTQ0NiIsInN1YiI6IjY1MDY0NjhjZmEyN2Y0MDBlYjE3M2E4NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.65BaAttDZJJR0E-aTzfsIudfCregYOHax0eRGyrbOqg"
        }

        movie_search_response = requests.get(movie_search_url, headers=headers)

        #the response is a string that is formatted like a dictionary. items downloaded from the internet are typically string/text file. json transforms the string into an actual dictionary
        #movie_search_subset = list((i['id'],i['order'],i["name"]) for i in movie_search_response)

        movie_search_json = json.loads(movie_search_response.text)

        movie_search_json = movie_search_json['cast']

        cast_searched = []

        for x in movie_search_json:
            if limit is not None and x['order'] >= limit:
                continue
            if exclude_ids is not None and x['id'] in exclude_ids:
                continue
            filtered_cast = {'id':str(x['id']), 'name':x['name'].replace(',' , ' '),}
            cast_searched.append(filtered_cast)
        
        return cast_searched

    def get_movie_credits_for_person(self, person_id:str, vote_avg_threshold:float=None)->list:
        """
        Using the TMDb API, get the movie credits for a person serving in a cast role
        documentation url: https://developers.themoviedb.org/3/people/get-person-movie-credits

        :param string person_id: the id of a person
        :param vote_avg_threshold: optional parameter to return the movie credit if it is >=
            the specified threshold.
            e.g., if the vote_avg_threshold is 5.0, then only return credits with a vote_avg >= 5.0
        :rtype: list
            return a list of dicts, with each dict having 'id', 'title', and 'vote_avg' keys, 
            one dict per movie credit with the following structure:
                [{'id': '97909' # the id of the movie
                'title': 'Long, Stock and Two Smoking Barrels' # the title (not original title) of the credit
                'vote_avg': 5.0 # the float value of the vote average value for the credit}, ... ]
        """
        
        import requests

        person_search_url = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?language=en-US"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlMDcyMDJiYzhjZTZmOGUyZWVhYjQ1ZDBiZjBkYTQ0NiIsInN1YiI6IjY1MDY0NjhjZmEyN2Y0MDBlYjE3M2E4NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.65BaAttDZJJR0E-aTzfsIudfCregYOHax0eRGyrbOqg"
        }

        person_search_response = requests.get(person_search_url, headers=headers)

        person_search_json = json.loads(person_search_response.text)

        person_search_json = person_search_json['cast']

        credit_searched = []
        
        for x in person_search_json:
            if vote_avg_threshold is not None and x['vote_average'] < vote_avg_threshold:
                continue
            filtered_credit = {'id':str(x['id']), 'title':x['title'], 'vote_avg':x['vote_average']}
            credit_searched.append(filtered_credit)
    
        return credit_searched
        

# You should modify __main__ as you see fit to build/test your graph using  the TMDBAPIUtils & Graph classes.
# Some boilerplate/sample code is provided for demonstration. We will not call __main__ during grading.

if __name__ == "__main__":

    graph = Graph()
    graph.add_node(id='2975', name='Laurence Fishburne', weight=4)
    tmdb_api_utils = TMDBAPIUtils(api_key='<your API key>')

    # call functions or place code here to build graph (graph building code not graded)

    # BEGIN BUILD BASE GRAPH:
#   Find all of Laurence Fishburne's movie credits that have a vote average >= 8.0
    credits = tmdb_api_utils.get_movie_credits_for_person('2975', 8)
    nodes = []

#   FOR each movie credit:
    for credit in credits:
#   |   get the movie cast members having an 'order' value between 0-2 (these are the co-actors)
        members = tmdb_api_utils.get_movie_cast(credit['id'], 3, [2975])
#   |
#   |   FOR each movie cast member:
        for member in members:
#   |   |   using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
            graph.add_node(member['id'], member['name'], weight=3)
            nodes.append(member)
#   |   |   using graph.add_edge(), add an edge between the Laurence Fishburne (actor) node
#   |   |   and each new node (co-actor/co-actress)
            graph.add_edge('2975', member['id'], weight=3)
#   |   END FOR
#   END FOR
# END BUILD BASE GRAPH
    print("BASE GRAPH")
    print("edges:", graph.total_edges(), "nodes:", graph.total_nodes())
    print("")
#
#
# BEGIN LOOP - DO 2 TIMES:
#   IF first iteration of loop:
#   |   nodes = The nodes added in the BUILD BASE GRAPH (this excludes the original node of Laurence Fishburne!)
#   ELSE
#   |    nodes = The nodes added in the previous iteration:
#   ENDIF
    for ITERATION in range(2):
#
        new_nodes = []
#   FOR each node in nodes:
        for node in nodes:
#   |  get the movie credits for the actor that have a vote average >= 8.0
            credits = tmdb_api_utils.get_movie_credits_for_person(node['id'], 8)

#   |
#   |   FOR each movie credit:
            for credit in credits:
#   |   |   try to get the 3 movie cast members having an 'order' value between 0-2
                members = tmdb_api_utils.get_movie_cast(credit['id'], 3, [int(node['id'])])
#   |   |   
#   |   |   FOR each movie cast member:
                for member in members:
#   |   |   |   IF the node doesn't already exist:
                    if member['id'] not in graph.nodes:
#   |   |   |   |    add the node to the graph (track all new nodes added to the graph)
                        graph.add_node(member['id'], member['name'], weight=2-ITERATION)
                        new_nodes.append(member)
#   |   |   |   ENDIF
#   |   |   |
#   |   |   |   IF the edge does not exist:
#   |   |   |   |   add an edge between the node (actor) and the new node (co-actor/co-actress)
                    if (member['id'], node['id']) not in graph.edges and (node['id'], member['id']) not in graph.edges:
                        graph.add_edge(member['id'], node['id'], weight=2-ITERATION)
#   |   |   |   ENDIF
#   |   |   END FOR
#   |   END FOR
        nodes = new_nodes
        print("ITERATION", ITERATION + 1)
        print("edges:", graph.total_edges(), "nodes:", graph.total_nodes())
        print("")

#   END FOR
# END LOOP


    # Suggestion: code should contain steps outlined above in BUILD CO-ACTOR NETWORK

    graph.write_edges_file()
    graph.write_nodes_file()

    print(graph.node_weights)
    
    with open('graph.txt', 'wb') as file:
        pickle.dump(graph, file)

    # If you have already built & written out your graph, you could read in your nodes & edges files
    # to perform testing on your graph.
    # graph = Graph(with_edges_file="edges.csv", with_nodes_file="nodes.csv")
    # print("edges:", graph.total_edges(), "nodes:", graph.total_nodes())

