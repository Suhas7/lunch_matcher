import random

import pandas as pd
prefs=pd.read_csv("prefs.csv")
ppl=set()
nameToObject=dict()
class Person:
	def __init__(self,row):
		self.name=row[1]["Name"]
		ppl.add(self.name)
		days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		self.availability=[]
		for d in days:
			intervals=row[1]["Availability ["+d+"]"]
			if intervals!="Unavailable":
				for i in intervals.split(","):
					self.availability.append((d,i))
		if type(row[1]["Requests"])==type(""):
			self.requests=row[1]["Requests"].split(",")
		else: self.requests=[]
		self.appointments=[]
		self.assignment="Not Assigned"
		nameToObject[self.name]=self

people=[Person(row) for row in prefs.iterrows() if row[1]["Name"] not in ppl]
people.sort(key=lambda x: len(x.requests))
for p in people:
	print("Roden: "+str(p.name))
	if len(p.requests)>0:
		print("     Requested: ")
		for i in p.requests:
			print("        "+(" "*(p.requests.index(i)==0))+str(i))
	print("     Has compatible times with:")
	for g in people:
		if g!=p:
			overlaps=[]
			for i in p.availability:
				for j in g.availability:
					if i==j:
						overlaps.append(i)
			if len(overlaps)>0:
				print("         "+g.name+" at:" )
				meetings=""
				for o in overlaps:
					meetings+= o[0]+" from "+o[1]+", "
					p.appointments.append((g.name,o))
				print("            "+meetings)
matched=set()
appointmentsMade=[]
count=10000
while(len(matched)<(len(people)-(len(people)%2)) and count>0):
	x=random.sample(people,1)[0]
	while x.name in matched:
		x = random.sample(people, 1)[0]
	matchMade=False
	for unmatch in x.appointments:
		if (unmatch[0] not in matched) and (not matchMade):
			x.assignment=unmatch
			nameToObject[unmatch[0]].assignment=(x.name,unmatch[1])
			matchMade=True
			matched.add(x.name)
			matched.add(unmatch[0])
	if not matchMade:
		newMatch=random.sample(x.appointments,1)[0]
		matched.remove(nameToObject[newMatch[0]].assignment[0])
		nameToObject[newMatch[0]].assignment=(x.name,newMatch[1])
		matched.add(x.name)
		x.assignment = newMatch
	count-=1
maxLen=0
for p in people:
	if p.name in matched:
		maxLen=max(maxLen,len(p.name+" meets with: "))


for p in people:
	if p.name in matched:
		print(p.name+" meets with: "+(" "*(maxLen+1-len(p.name+" meets with: ")))+p.assignment[0]+" at "+p.assignment[1][1]+" on  "+p.assignment[1][0])
	else:
		compats=set([x.assignment[1] for x in people if x.assignment[1] in p.availability])
		print(p.name+" is free to join any lunch at: "+str(compats))