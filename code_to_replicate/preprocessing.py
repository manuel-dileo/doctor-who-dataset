import pandas as pd

def write_list_of_roles(roles_url):	
	roles = pd.read_csv(roles_url)
	roles['Label'] = roles['Label'].map(lambda x: [x])
	roles.groupby('Id').sum().to_csv(roles_url)
	
def write_simple_graph(multigraph_url):

	df = pd.read_csv(multigraph_url)[['Source','Target']]
	df['Weight'] = [1 for i in range(len(df))]
	
	df = pd.DataFrame({'Weight' : \
				df.groupby( [ 'Source', 'Target'] ).size(),
				'Type': 'undirected'})\
		.reset_index()
		
	df.to_csv('new-who.csv',index=False)

#Two edges edge1 and edge2 are the same if story1 = story2 and {source1,target1} = {source2,target2}
def drop_multigraph_duplicate_edges(multigraph_url):
	df = pd.read_csv(multigraph_url)
    
	unique_edges = []
	for _,row in df.iterrows():
		source,target,story = row['Source'],row['Target'],row['Story']
		if (source,target,story) not in unique_edges and (target,source,story) not in unique_edges:
			unique_edges.append((source,target,story))
        
	dfunique = pd.DataFrame(unique_edges, columns =['Source', 'Target', 'Story'])
	dfunique.to_csv(multigraph_url,index=False)
