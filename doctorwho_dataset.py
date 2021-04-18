import networkx as nx
import pandas as pd

def load_simple_graph_with_roles(default_url = True,\
					edges_url='datasets/doctorwho.csv',\
					roles_url='datasets/roles/doctorwho_roles.csv',\
					era='all'):
	"""
		Read an edgelist and list of nodes info and return a graph with edges in edgelist and nodes attributes as in the nodes info file.
		The Doctor Who simple graph is an undirected weighted graph where nodes are characters\
		with information about their roles in the series and exist an edge between node i and node j with weight w\
		iff i and j appear in the same episode w times.

		Parameters
		----------
		default_url = bool, optional
			choose if you want to use default url or not(default is True). It's important to set this bool to False\
			if you want to load particular era dataset in no default location
		edges_url : str, optional
			The csv edgelist location(default is the location in the github repo).
		roles_url: str, optional
			The csv roles location(default is the location in the github repo)
		era: str, optional
			The doctor who era you want in the graph(default is all). You can choose 'all','classic','new'.

		Returns
		-------
		networkx.Graph
			The doctor who simple graph
	"""
	if era == 'classic' and default_url:
		edges_url = 'datasets/classic-who.csv'
		roles_url = 'datasets/roles/classic-who_roles.csv'
        
	if era == 'new' and default_url:
		edges_url = 'datasets/new-who.csv'
		roles_url = 'datasets/roles/new-who_roles.csv'
        
	df = pd.read_csv(edges_url)
	g = nx.from_pandas_edgelist(df,'Source','Target',['Weight'])
	roles = pd.read_csv(roles_url).set_index('Id')['Label'].map(lambda x: eval(x)).to_dict()
	nx.set_node_attributes(g,roles,'roles')
	return g

def load_multigraph_with_roles(default_url = True,\
					edges_url='datasets/multigraph/doctorwho_multigraph.csv',\
					roles_url='datasets/roles/doctorwho_roles.csv',\
					era='all'):
	"""
		Read an edgelist and list of nodes info and return a multigraph with edges in edgelist, edges and nodes attributes as in the csv files.
		The Doctor Who multigraph is an undirected multigraph where nodes are characters\
		with information about their roles in the series and exist an edge between node i and node j\
		iff i and j appear in the same episode and the edge is marked with the title of the episode.

		Parameters
		----------
		default_url = bool, optional
			choose if you want to use default url or not(default is True). It's important to set this bool to False\
			if you want to load particular era dataset in no default location
		edges_url : str, optional
			The csv edgelist location(default is the location in the github repo).
		roles_url: str, optional
			The csv roles location(default is the location in the github repo)
		era: str, optional
			The doctor who era you want in the graph(default is all). You can choose 'all','classic','new'.

		Returns
		-------
		networkx.MultiGraph
			The doctor who multigraph
	"""
	if era == 'classic' and default_url:
		edges_url = 'datasets/multigraph/classic-who_multigraph.csv'
		roles_url = 'datasets/roles/classic-who_roles.csv'
        
	if era == 'new' and default_url:
		edges_url = 'datasets/multigraph/new-who_multigraph.csv'
		roles_url = 'datasets/roles/new-who_roles.csv'
        
	df = pd.read_csv(edges_url)
	g = nx.from_pandas_edgelist(df,'Source','Target',edge_attr='Story',create_using=nx.MultiGraph)
	roles = pd.read_csv(roles_url).set_index('Id')['Label'].map(lambda x: eval(x)).to_dict()
	nx.set_node_attributes(g,roles,'roles')
	return g
