import pandas as pd

# Import Data
usfests = pd.read_csv('USfestivals.csv')

# Rename Columns
usfests.columns = ['band', 'year', 'warped', 'lollapalooza', 'firefly', 'austincitylimits', 'outsidelands', 'governorsball', 'riotfest', 'bealestreet', 'voodoo', 'coachella', 'electricdaisycarnival', 'sasquatch', 'bonnaroo', 'newportfolk', 'hangoutfest', 'pitchfork', 'madeinamerica', 'ultra', 'festival']

# Map Festival Values
festivals_list = {'warped': 'Vans Warped Tour', 
 'lollapalooza': 'Lollapalooza Chicago',
 'firefly': 'Firefly Music Festival',
 'austincitylimits': 'Austin City Limits',
 'outsidelands': 'Outside Lands Music and Arts Festival',
 'governorsball': 'Governors Ball Music Festival',
 'riotfest': 'Riot Fest Chicago',
 'bealestreet': 'The Beale Street Music Festival',
 'voodoo': 'VooDoo Music and Arts Festival',
 'coachella': 'Coachella Valley Music and Arts Festival',
 'electricdaisycarnival': 'Electric Daisy Carnival Las Vegas',
 'sasquatch': 'Sasquatch! Music Festival',
 'bonnaroo': 'Bonnaroo Music and Arts Festival',
 'newportfolk': 'Newport Folk Festival',
 'hangoutfest': 'Hangout Music Festival',
 'pitchfork': 'Pitchfork Music Festival',
 'madeinamerica': 'Budweiser Made in America Festival',
 'ultra': 'Ultra Music Festival Miami'} 

# Get Festival by Name & Year
def festbyyear(fest, year):
	try:
		return usfests[usfests['year'] == year][usfests[usfests['year'] == year][fest] == 1]['band']
	except:
		return " "

# Get Festival by Name
def makefestvars(fest):
	try:
		return usfests[usfests[fest] == 1]['band']
	except:
		return " "

# Get Intersection
def intersect(a, b):
	try:
		return list(set(a) & set(b))
	except:
		return " "

# Map Festival Names
def match_fest(fest):
     if fest in festivals_list:
         return festivals_list[fest]