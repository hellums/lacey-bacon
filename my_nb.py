
# coding: utf-8

# # **Import modules to handle downloading, compressed files, regular expressions, and dataframes.**

# In[1]:

import requests
import gzip
import re
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


# # **Download watchlist from github, compressed datasets from imdb**

# In[ ]:

remote_url ='https://raw.githubusercontent.com/hellums/hallmarkish/root/watchlist.txt'  
local_file = 'watchlist.txt' # export of imdb watchlist
data = requests.get(remote_url)
with open(local_file, 'wb') as file:
    file.write(data.content)


# In[ ]:

remote_url ='https://datasets.imdbws.com/title.basics.tsv.gz'  
local_file = 'movie_info.tsv.gz' # detail and metadata about all imdb movies (pare down!)
data = requests.get(remote_url)
with open(local_file, 'wb') as file:
    file.write(data.content)


# In[ ]:

remote_url ='https://datasets.imdbws.com/title.ratings.tsv.gz'
local_file = 'movie_ratings.tsv.gz'  # ratings and number votes, for some movies (not all)
data = requests.get(remote_url)
with open(local_file, 'wb') as file:
    file.write(data.content)


# In[ ]:

remote_url ='https://datasets.imdbws.com/name.basics.tsv.gz'
local_file = 'cast_crew_info.tsv.gz'  # personal details of cast and crew
data = requests.get(remote_url)
with open(local_file, 'wb') as file:
    file.write(data.content)


# In[ ]:

remote_url ='https://datasets.imdbws.com/title.principals.tsv.gz'
local_file = 'movie_cast_crew.tsv.gz'  # list of major cast and crew for all movies (pare down!)
data = requests.get(remote_url)
with open(local_file, 'wb') as file:
    file.write(data.content)


# In[ ]:

remote_url ='https://datasets.imdbws.com/title.crew.tsv.gz'
local_file = 'movie_crew.tsv.gz'  # list of director and writers for all movies
data = requests.get(remote_url)
with open(local_file, 'wb') as file:
    file.write(data.content)


# # **Decompress datasets to tab-delimited files**

# In[ ]:

compressed_file = "movie_cast_crew.tsv.gz"
uncompressed_file = "movie_cast_crew.tsv"
with gzip.open(compressed_file, 'rb') as f:
    data = f.read()
with open(uncompressed_file, 'wb') as f:
    f.write(data)


# In[ ]:

compressed_file = "movie_crew.tsv.gz"
uncompressed_file = "movie_crew.tsv"
with gzip.open(compressed_file, 'rb') as f:
    data = f.read()
with open(uncompressed_file, 'wb') as f:
    f.write(data)


# In[ ]:

compressed_file = "movie_info.tsv.gz"
uncompressed_file = "movie_info.tsv"
with gzip.open(compressed_file, 'rb') as f:
    data = f.read()
with open(uncompressed_file, 'wb') as f:
    f.write(data)


# In[ ]:

compressed_file = "movie_ratings.tsv.gz"
uncompressed_file = "movie_ratings.tsv"
with gzip.open(compressed_file, 'rb') as f:
    data = f.read()
with open(uncompressed_file, 'wb') as f:
    f.write(data)


# In[ ]:

compressed_file ='cast_crew_info.tsv.gz'
uncompressed_file = 'cast_crew_info.tsv'
with gzip.open(compressed_file, 'rb') as f:
    data = f.read()
with open(uncompressed_file, 'wb') as f:
    f.write(data)


# # **Load movie data into dataframes, and drop unwanted rows**

# In[2]:

local_file = 'watchlist.txt'
header_field = ['tconst']
watchlist_info = pd.read_csv(local_file, names=header_field)
watchlist = []
watchlist = watchlist_info['tconst'].tolist() # refactor this to load direct to list, don't need a df


# In[3]:

local_file = 'movie_info.tsv'
movie_info = pd.read_csv(local_file, sep='\t', usecols=[0, 1, 2, 5, 7, 8],                          dtype={'startYear': str, 'runtimeMinutes': str},                          converters={'genres': lambda x: re.split(',+', x)})  # converting genre string to a list


# In[4]:

movie_info = movie_info[movie_info['tconst'].isin(watchlist) == True]  # drop movies not on/by Hallmark


# In[5]:

movie_info['runtimeMinutes'] = movie_info['runtimeMinutes'].replace(to_replace=r"\N", value='80')  # fix imdb format error


# In[6]:

local_file = 'movie_ratings.tsv'  # only need this temporarily to add ratings and voters to movie_info df
movie_ratings = pd.read_csv(local_file, sep='\t')


# In[7]:

movie_ratings = movie_ratings[movie_ratings['tconst'].isin(watchlist) == True]  # drop ratings not associated w/Hallmark


# In[8]:

local_file = 'cast_crew_info.tsv'
cast_crew_info = pd.read_csv(local_file, sep='\t', usecols=[0, 1, 2, 3]) # refactor to pare based on actor list


# In[9]:

actorlist = cast_crew_info['nconst'].tolist()
actorlist = list(set(actorlist))


# In[10]:

cast_crew_info = cast_crew_info[cast_crew_info['nconst'].isin(actorlist) == True]  # drop people not in Hallmark movies


# In[11]:

local_file = 'movie_crew.tsv'  # may not need separate director/writer associations, but better have than not
movie_crew = pd.read_csv(local_file, sep='\t')


# In[12]:

movie_crew = movie_crew[movie_crew['tconst'].isin(watchlist) == True]  # drop people not associated w/Hallmark


# In[13]:

local_file = 'movie_cast_crew.tsv'
movie_cast_crew = pd.read_csv(local_file, sep='\t', usecols=[0, 2, 3])


# In[14]:

movie_cast_crew = movie_cast_crew[movie_cast_crew['tconst'].isin(watchlist) == True]  # drop movies not on/by Hallmark


# In[15]:

unwantedValues = ['writer', 'producer', 'director', 'composer', 'cinematographer', 
                  'editor', 'production_designer', 'self']  # should only leave actor, actress categories


# In[16]:

movie_cast_crew = movie_cast_crew[movie_cast_crew['category'].isin(unwantedValues) == False] # keep actor, actress rows


# In[17]:

movielist = movie_cast_crew['tconst'].tolist()
movielist = list(set(movielist))


# # **Merge ratings into movie dataframe, and drop ratings df**

# In[18]:

movie_info = pd.merge(movie_info,
                     movie_ratings[['tconst', 'averageRating', 'numVotes']],
                     on='tconst', how='outer')  # adds the ratings and votes columns to the movie_info df


# In[19]:

movie_info = movie_info[:len(watchlist)]  # get rid of the NaN records from the merge, maybe refactor so not needed


# In[20]:

movie_info = movie_info.fillna(value={'averageRating':6.9,'numVotes':699})  # clean up <20 NaN values from csv import


# In[21]:

movie_info['runtimeMinutes'] = movie_info['runtimeMinutes'].astype(int)  # convert runtime to an int for proper processing


# In[22]:

movie_info['numVotes'] = movie_info['numVotes'].astype(int)  # convert column to an int for proper processing


# In[23]:

del movie_ratings # don't need it anymore, after outer join merge with movies


# # **Validate import and data structures**

# In[24]:

get_ipython().magic('matplotlib inline')


# In[25]:

df = movie_info


# In[26]:

df.averageRating.plot(kind='hist',
                      title='Historgram of Ratings',
                      color='c',
                      bins=20);


# In[27]:

df.titleType.value_counts().plot(kind='bar',
                                 rot=0,
                                 title='Bar Graph of Titles',
                                 color='m');


# In[28]:

df.averageRating.plot(kind='box', title='Boxplot, duh!', color='b');


# In[29]:

df.runtimeMinutes.plot(kind='box', title='Boxplot, duh!', color='b');


# In[30]:

df.numVotes.plot(kind='box', title='Boxplot, duh!', color='b');


# In[31]:

null_counts = df.isnull().sum()


# In[32]:

null_counts[null_counts > 0].sort_values(ascending=False)


# In[33]:

pd.crosstab(df.startYear, df.titleType)


# In[34]:

df.groupby('titleType').averageRating.mean()


# In[35]:

df.groupby('titleType').runtimeMinutes.median()


# In[36]:

df.groupby(['titleType'])['runtimeMinutes'].median() # same as above


# In[37]:

df.groupby(['titleType']).agg({ 'numVotes': 'mean', 'runtimeMinutes': 'median' })


# In[38]:

df.head()


# In[39]:

df.info()


# In[40]:

df.to_json('./df.json', orient='records')


# In[41]:

df.to_csv('./df.csv', sep='\t', orient='records')


# In[42]:

movie_info.info()


# In[43]:

cast_crew_info.info()


# In[44]:

movie_cast_crew.info()


# In[45]:

movie_info.head()


# In[46]:

cast_crew_info.head()


# In[47]:

movie_cast_crew.head()


# In[48]:

'nm0000327' in actorlist


# In[49]:

cast_crew_info.head


# In[50]:

movie_cast_crew.loc[movie_cast_crew.tconst == 'tt13831504',:]


# In[51]:

cast_crew_info.loc[cast_crew_info.nconst == 'nm0000327']


# In[52]:

movie_cast_crew.loc[movie_cast_crew.nconst == 'nm0000327',:]


# In[53]:

df3 = movie_cast_crew.groupby('nconst')['tconst'].apply(list).reset_index(name="movieList")


# In[54]:

df3.count()


# In[55]:

df3.head()


# In[56]:

df3.info()


# In[339]:

nm_tt_Dict = dict(zip(df3.nconst, df3.movieList))


# In[342]:

nm_tt_Dict['nm4003706']


# In[59]:

junk = df3.loc[df3.nconst == 'nm0000327',:]  #just an intermediate step


# In[60]:

print(junk)  # confirms it's not very useful 'as is'


# In[61]:

nameDict = dict(zip(df3.nconst, df3.movieList))


# In[62]:

nameDict['nm0000327']  # much more useful, IMHO


# In[63]:

df2 = movie_cast_crew.groupby('tconst')['nconst'].apply(list).reset_index(name="actorList")


# In[64]:

df2.count()


# In[65]:

df2.head()


# In[66]:

df2.info()


# In[67]:

tt_nm_Dict = dict(zip(df2.tconst, df2.actorList))


# In[68]:

list(tt_nm_Dict.items())[91:95]


# In[69]:

tt_nm_Dict['tt13831504']


# In[70]:

list(nm_tt_Dict.items())[91:95]


# In[71]:

nm_tt_Dict['nm4003706']


# In[72]:

df1 = cast_crew_info


# In[73]:

nm_Dict = dict(zip(df1.nconst, df1.primaryName))


# In[74]:

list(nm_Dict.items())[91:95]


# In[75]:

tt_nm_Dict['tt13831504']


# In[76]:

nm_tt_Dict['nm0000327']


# In[77]:

nm_Dict['nm4003706']


# In[78]:

df4 = movie_info


# In[79]:

tt_Dict = dict(zip(df4.tconst, df4.primaryTitle))


# In[80]:

tt_Dict['tt13831504']


# In[81]:

cast_crew_info.head()


# In[82]:

Name_nm_Dict = dict(zip(df1.primaryName, df1.nconst))


# In[83]:

Name_nm_Dict['Alison Sweeney']


# In[84]:

nm_tt_Dict['nm0842081']


# In[85]:

tt_nm_Dict['tt11068326']


# In[86]:

tt_Dict['tt11068326']


# In[87]:

df4.head()


# In[88]:

Title_tt_Dict = dict(zip(df4.primaryTitle, df4.tconst))


# In[89]:

Title_tt_Dict['It Was Always You']


# In[90]:

"It Was Always You" in Title_tt_Dict


# In[91]:

Title_tt_Dict['Sarah, Plain and Tall']


# # **Graph network plot and determine centrality**

# In[92]:

titles = watchlist


# In[93]:

G1 = nx.Graph()
names = {}
node_color = []
for n, star in enumerate(movie_cast_crew.nconst.unique()):
    name = nm_Dict[star]
    names[star] = name
    G1.add_node(name, {'type':'Star', 'color':'green'})
    #G1.add_node(name)
    #node_color.append('cyan')
for n, movie in enumerate(movie_cast_crew.tconst.unique()):
    name = tt_Dict[movie]
    names[movie] = name
    G1.add_node(name, {'type': 'Movie', 'color':'blue'})    
    #G1.add_node(name)
    #node_color.append('magenta')
for row in movie_cast_crew.index:
    star = movie_cast_crew['nconst'][row]
    s_name = names[star]
    movie = movie_cast_crew['tconst'][row]
    m_name = names[movie]
    G1.add_edge(s_name, m_name)


# In[94]:

color_map = [n[1]['color'] for n in G1.nodes(data=True)]
labels = {n:n for n in G1.nodes()}
plt.title('Six Degrees of Lacey Chabert')
nx.draw_networkx(G1, node_color=color_map, alpha=0.5, labels=labels, with_labels=True)


# In[95]:

print(nx.betweenness_centrality(G1)['Lacey Chabert'])


# In[96]:

between_ity = nx.betweenness_centrality(G1)
[(x, between_ity[x]) for x in sorted(between_ity, key=between_ity.get, reverse=True)[:20]]


# In[97]:

between_ity["Autumn Reeser"]


# In[98]:

degree_ity = nx.degree(G1)
[(x, degree_ity[x]) for x in sorted(degree_ity, key=degree_ity.get, reverse=True)[:40]]


# In[99]:

degree_ity['Tyler Hynes']


# In[100]:

G1.edges()


# In[101]:

close_ity = nx.closeness_centrality(G1)  # not useful without removing titles from list


# In[102]:

[(x, close_ity[x]) for x in sorted(close_ity, key=close_ity.get, reverse=True)[:40]]


# In[103]:

nx.is_connected(G1)


# In[104]:

G1.neighbors('Lacey Chabert')


# In[105]:

int(nx.shortest_path_length(G1, 'Lacey Chabert', 'Tyler Hynes')/2)


# In[106]:

nx.shortest_path(G1, 'Lacey Chabert', 'Cindy Busby')


# In[107]:

lacey1 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=1)


# In[108]:

lacey2 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=2)


# In[109]:

lacey3 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=3)


# In[110]:

lacey4 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=4)


# In[269]:

lacey5 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=5)


# In[270]:

lacey6 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=6)


# In[271]:

lacey7 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=7)


# In[272]:

lacey8 = nx.single_source_shortest_path(G1, 'Lacey Chabert', cutoff=8)


# In[111]:

path = nx.single_source_shortest_path(G1, 'Lacey Chabert')


# In[308]:

lacey2


# In[307]:

lacey_totals = [len(lacey1),
                len(lacey2) - len(lacey1),
                len(lacey3) - len(lacey2),
                len(lacey4) - len(lacey3),
                len(lacey5) - len(lacey4),
                len(lacey6) - len(lacey5),
                len(lacey7) - len(lacey6),
                len(lacey8) - len(lacey7),
                len(lacey8)]
print(lacey_totals)


# In[316]:

len(lacey1)-1


# In[314]:

lacey1 # lacey's movie connections, plus herself


# In[325]:

len(lacey2.keys())-len(lacey1.keys())-1


# In[324]:

lacey2.keys()


# In[304]:

print(lacey_totals[7], len(lacey7))


# In[ ]:

print(len_lacey)


# In[267]:

len(lacey2) - len(lacey1)


# In[268]:

len(lacey3) - len(lacey2)


# In[264]:

lacey2


# In[312]:

lacey3.values()


# In[258]:

len(lacey3.keys())


# In[250]:

path['Autumn Reeser']


# In[116]:

sp=nx.all_pairs_shortest_path(G1)


# In[117]:

chabert_num = sp['Lacey Chabert']['Luke Macfarlane']


# In[118]:

chabert_num


# In[119]:

chabert_numbers = sp['Lacey Chabert'] 


# In[120]:

chabert_numbers


# In[121]:

len(chabert_numbers)


# In[122]:

junk = movie_cast_crew[:20]


# In[123]:

junk


# In[124]:

G2 = nx.Graph()
names = {}
node_color = []
for n, star in enumerate(junk.nconst.unique()):
    name = star
    names[star] = name
    #node_color.append('cyan')
    G2.add_node(name, {'type':'star', 'color':'blue'})
for n, movie in enumerate(junk.tconst.unique()):
    name = movie
    names[movie] = name
    #node_color.append('magenta')
    G2.add_node(name, {'type': 'movie', 'color':'green'})
for row in junk.index:
    star = junk['nconst'][row]
    s_name = names[star]
    movie = junk['tconst'][row]
    m_name = names[movie]
    G2.add_edge(s_name, m_name)    


# In[125]:

color_map = [n[1]['color'] for n in G2.nodes(data=True)]
labels = {n:n for n in G2.nodes()}
plt.title('Six Degrees of Lacey Chabert')
nx.draw_networkx(G2, node_color=color_map, alpha=0.5, labels=labels, with_labels=True)


# In[126]:

centrality = nx.betweenness_centrality(G2)
[(x, centrality[x]) for x in sorted(centrality, key=centrality.get, reverse=True)[:20]]


# In[127]:

centrality


# In[128]:

G2.number_of_nodes()


# In[129]:

G2.number_of_edges()


# In[130]:

G2.adj['nm0825555']


# In[131]:

G2.nodes()


# In[147]:

G2.edges()


# In[ ]:

G5 = nx.Graph()
names = {}
node_color = []
for n, star in enumerate(movie_cast_crew.nconst.unique()):
    name = star
    names[star] = name
    G1.add_node(name, {'type':'Star', 'color':'green'})
for n, movie in enumerate(movie_cast_crew.tconst.unique()):
    name = movie
    names[movie] = name
    G1.add_node(name, {'type': 'Movie', 'color':'blue'})    
for row in movie_cast_crew.index:
    star = movie_cast_crew['nconst'][row]
    s_name = names[star]
    movie = movie_cast_crew['tconst'][row]
    m_name = names[movie]
    G1.add_edge(s_name, m_name)


# In[144]:

nx.draw_spring(G1.to_directed(), node_size=0)


# In[133]:

color_map = [n[1]['color'] for n in G2.nodes(data=True)]
labels = {n:n for n in G2.nodes()}
plt.title('Six Degrees of Lacey Chabert')
nx.draw_networkx(G2, node_color=color_map, alpha=0.5, labels=labels, with_labels=True)


# In[148]:

tt_Dict


# In[152]:

for titleID, title in tt_Dict.items():
  print (titleID, title)


# In[153]:

movie_info.head()


# In[154]:

tt_Dict.head()


# In[161]:

print(tt_Dict.values())


# In[158]:

print(tt_Dict.items())


# In[162]:

L1 = list(tt_Dict.values())
for i in L1:
   print (i)


# In[163]:

tt_Dict['tt1335977']


# In[166]:

df3.head()


# In[167]:

print(df3.head())


# In[171]:

tt_Dict['tt0217066']


# In[165]:

movie_info.head()


# In[ ]:

G1 = nx.Graph()
names = {}
node_color = []
for n, star in enumerate(movie_cast_crew.nconst.unique()):
    name = nm_Dict[star]
    names[star] = name
    G1.add_node(name, {'type':'Star', 'color':'green'})
    #G1.add_node(name)
    #node_color.append('cyan')
for n, movie in enumerate(movie_cast_crew.tconst.unique()):
    name = tt_Dict[movie]
    names[movie] = name
    G1.add_node(name, {'type': 'Movie', 'color':'blue'})    
    #G1.add_node(name)
    #node_color.append('magenta')
for row in movie_cast_crew.index:
    star = movie_cast_crew['nconst'][row]
    s_name = names[star]
    movie = movie_cast_crew['tconst'][row]
    m_name = names[movie]
    G1.add_edge(s_name, m_name)


# In[172]:


# Python program to demonstrate
# Lists
 
 
# Creating a List with
# the use of multiple values
List = ["Geeks", "For", "Geeks"]
print("List containing multiple values: ")
print(List[0]) 
print(List[2])
   
# Creating a Multi-Dimensional List
# (By Nesting a list inside a List)
List = [['Geeks', 'For'] , ['Geeks']]
print("\nMulti-Dimensional List: ")
print(List)


# In[173]:

mytuple=1,2,3


# In[174]:

type(mytuple)


# In[175]:

mytuple=1


# In[176]:

type(mytuple)


# In[177]:

mytuple=1,


# In[178]:

type(mytuple)


# In[181]:

mytuple = mytuple + (10,)


# In[182]:

mytuple


# In[183]:

print(mytuple)


# In[189]:

describe(mytuple)


# In[190]:

id(mytuple)


# In[191]:

mytuple = mytuple + (15,)


# In[192]:

mytuple


# In[197]:

id(mytuple)


# In[198]:

listx = list(mytuple) 
#use different ways to add items in list
listx.append(30)
mytuple = tuple(listx)
id(mytuple)


# In[228]:

lacey = 'nm0000327'


# In[200]:

hex(id(mytuple))


# In[227]:

df1.head()


# In[229]:

print(df1['primaryName'].where(df1['nconst'] == lacey).dropna())


# In[230]:

df1.loc[df1['nconst'] == lacey]


# In[234]:

df1.loc[df1['nconst'].isin(['nm0000327', 'nm0000001'])]


# In[246]:

df1.loc[(df1['birthYear'] == '1982') & (df1['deathYear'] > '2015')]


# In[247]:

print(df3.head())


# In[248]:

data=df3.head()


# In[249]:

print(data)


# In[ ]:

G10 = nx.Graph()
names = {}
node_color = []
for n, star in enumerate(movie_cast_crew.nconst.unique()):
    name = nm_Dict[star]
    names[star] = name
    G10.add_node(name, {'type':'Star', 'color':'green'})
    #G1.add_node(name)
    #node_color.append('cyan')
for n, movie in enumerate(movie_cast_crew.tconst.unique()):
    name = tt_Dict[movie]
    names[movie] = name
    G10.add_node(name, {'type': 'Movie', 'color':'blue'})    
for row in movie_cast_crew.index:
    star = movie_cast_crew['nconst'][row]
    s_name = names[star]
    movie = movie_cast_crew['tconst'][row]
    m_name = names[movie]
    G10.add_edge(s_name, m_name)


# In[330]:

tt_Dict['tt13831504']


# In[331]:

tt_Dict


# In[333]:

nm_Dict['nm4003706']


# In[335]:

Name_nm_Dict['Erin Krakow']


# In[337]:

tt_nm_Dict['tt13831504']


# In[338]:

tt_nm_Dict


# In[343]:

nm_Dict


# In[344]:

m = nx.Graph()


# In[388]:

edge_attribute_dict = {}


# In[390]:

for name_ID, titles in nm_tt_Dict.items():
    m.add_node(name_ID)
    for title in titles:
        for name_ID2, titles2 in nm_tt_Dict.items():
            if (title in titles2) and (titles2 != titles):
                m.add_edge(name_ID, name_ID2)
                name_ID_tuple = tuple(sorted((name_ID, name_ID2)))
                if name_ID_tuple not in edge_attribute_dict:
                    edge_attribute_dict[name_ID_tuple] = 1
                else:
                    edge_attribute_dict[name_ID_tuple] += 1
                    


# In[392]:

len(m.edges())


# In[393]:

for k,v in edge_attribute_dict.items():
    edge_attribute_dict[k] = {'weight':v}


# In[394]:

edge_attribute_dict


# In[360]:

nx.set_edge_attributes(m, edge_attribute_dict)


# In[405]:

centrality = nx.betweenness_centrality(m)
[(nm_Dict[x], centrality[x]) for x in sorted(centrality, key=centrality.get, reverse=True)[:30]]


# In[404]:

between_ity = nx.betweenness_centrality(m)
[(nm_Dict[x], between_ity[x]) for x in sorted(between_ity, key=between_ity.get, reverse=True)[:30]]


# In[403]:

degree_ity = nx.degree(m)
[(nm_Dict[x], degree_ity[x]) for x in sorted(degree_ity, key=degree_ity.get, reverse=True)[:30]]


# In[407]:

pos = nx.spring_layout(m,k=1,iterations=20)
max_c = max(centrality.values())
color_map = {x[0]:x[1]/max_c for x in centrality.items()}
nx.draw(m, pos, node_color=list(color_map.values()), cmap=plt.cm.Blues)
plt.show()


# In[ ]:



