import requests
from bs4 import BeautifulSoup
import os

base_url = 'https://tardis.fandom.com'
listep = 'https://tardis.fandom.com/wiki/List_of_Doctor_Who_television_stories'

NEWHO_START = 38 #USE THIS INFO IF YOU WANT TO SPLIT YOUR DATASET INTO CLASSIC AND NEW WHO

def get_roles_and_edges():

	#filter some tables that contains info about missing stories
	def filter_no_ep_info(x):
		return 'Story completely missing' not in str(x)
    	
    	#filter two special stories. Reasoning in README
	def skip_mid(x):
    		return '/wiki/The_Curse_of_Fatal_Death_(TV_story)' not in str(x) and\
			'/wiki/Scream_of_the_Shalka_(webcast)' not in str(x)
			
	response = requests.get(listep)
	soup = BeautifulSoup(response.text,'lxml')
	ep_table = list(filter(lambda x: filter_no_ep_info(x),soup.find_all('table')))
	ep_table = list(filter(lambda x: skip_mid(x),ep_table))
	
	def filter_char_lines(x):
		x = str(x.find('h3'))
		return 'Doctor' in x or 'Companion(s)' in x or 'Main enemy' in x or 'Featuring' in x
	
	finalchars = []	
	with open('rawcharacters.csv','a') as chars, open('rawdoctorwho.csv','a') as edges:
		chars.write('Id,Label\n')
		edges.write('Source,Target,Story\n')
		for table in ep_table:
			for row in table.findAll('tr')[1:]:
				try:
					epurl = row.find('td').find('a')['href']
				except TypeError:
					try:
						epurl = row.find_all('td')[1].find('a')['href']
					except: pass #last tables
				except: pass
				eptitle = epurl.split('/')[2]
				response = requests.get(base_url+epurl)
				soup = BeautifulSoup(response.text,'lxml')
				character_lines = list(filter(lambda x: filter_char_lines(x),\
							soup.find('aside').find_all('div')))
				allcharacters = []
				for line in character_lines:
					role = str(line.find('h3')).split('>')[1].split(':')[0]
					characters = [a['title'] for a in line.find('div',class_='pi-data-value pi-font').findAll('a')]
					allcharacters+=characters
					for char in characters:
						#chars.write(char + ',' + role + '\n')
						if (char,role) not in finalchars:
							finalchars.append((char,role))
							chars.write(char + ',' + role + '\n')
					
					for source in allcharacters:
						for target in allcharacters:
							if source!=target:
								edges.write(source + ',' + target + ',' + eptitle + '\n')
								
#filtering some garbage rows in new-who datasets
def clean_rows():
	def nouser(x):
		role = x.split(',')[1]
		return False if role!='Doctor' and role!='Companion(s)' and role!='Featuring' and role!='Main enemy' else True
		
	def is_a_real_edge(x,notusers):
		source,target,_ = x.split(',')[0:3]
		return source not in notusers and target not in notusers
	
	clean_chars = []
	clean_edges = []
	with open('rawcharacters.csv','r') as f, open('rawdoctorwho.csv','r') as e:
		elements = f.read().split('\n')[:-1]
		chars = elements[1:]
		clean_chars = list(filter(lambda x: nouser(x),chars))
		notusers = list(map(lambda x: x[0],filter(lambda x: x not in clean_chars,chars)))
		edges = e.read().split('\n')[:-1]
		clean_edges = list(filter(lambda x: is_a_real_edge(x,notusers),edges))
		
	with open('doctorwho_roles.csv','a') as f, open('doctorwho_multigraph.csv','a') as e:
		f.write('Id,Label\n')
		for c in clean_chars:
			f.write(str(c)+'\n')
		for edge in clean_edges:
			e.write(str(edge)+'\n')

def get_doctorwho_dataset():
	try:
		print("Getting info from doctor who wiki...")
		get_roles_and_edges()
		print("Cleaning some garbage rows...")
		clean_rows()
		print("Dataset saved")
		os.remove('rawcharacters.csv')
		os.remove('rawdoctorwho.csv')
		print("Raw files removed")
		print("Task successfully completed")
	except Exception as e:
		print(e)
		print("Error")

if __name__ == "__main__":
	get_doctorwho_dataset()
