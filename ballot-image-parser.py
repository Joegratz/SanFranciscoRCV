# Files available from https://sfelections.sfgov.org/june-5-2018-election-results-detailed-reports
# You will have to go get the Master Lookup file and the Ballot Image file from there and place them in the same directory as this script.
MASTER_LOOKUP_FILE = '20180615_masterlookup.txt'
BALLOT_IMAGE_FILE = '20180615_ballotimage.txt'
CONTEST_ID = 20 # 2018 SF mayoral race

import collections

class Candidate():
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.firstPlaceTallies = collections.Counter()
		self.secondPlaceTallies = collections.Counter()
		self.thirdPlaceTallies = collections.Counter()
		
	def __str__(self):
		return self.name
	
	def __name__(self):
		return self.name

class Voter():
	def __init__(self, id, precinctID):
		self.id = id
		self.precinct = precinctID
		self.firstChoice = None
		self.secondChoice = None
		self.thirdChoice = None
		
candidates = {}
voters = {}

# These field definitions are from https://sfelections.org/results/20180605/data/BallotImageRCVhelp.pdf
with open (MASTER_LOOKUP_FILE, "r") as mlf:
    for line in mlf.readlines():
		Record_Type = line[0:10].strip()
		Id = int(line[10:17])
		Description = line[17:67].strip()
		List_Order = int(line[67:74])
		Candidates_Contest_Id = int(line[74:81])
		Is_WriteIn = int(line[81])
		Is_Provisional = int(line[82])
		
		if Candidates_Contest_Id == CONTEST_ID:
			candidates[Id] = Candidate(Id, Description)

with open(BALLOT_IMAGE_FILE, "r") as bif:
	for line in bif.readlines():
		Contest_Id = int(line[0:7])	
		Pref_Voter_Id = int(line[7:16])
		Serial_Number = int(line[16:23])
		Tally_Type_Id = int(line[23:26])
		Precinct_Id = int(line[26:33])
		Vote_Rank = int(line[33:36])
		Candidate_Id = int(line[36:43])
		Over_Vote = int(line[43])
		Under_Vote = int(line[44])
		
		if Contest_Id == CONTEST_ID:
			try:
				voter = voters[Pref_Voter_Id]
			except KeyError:
				voter = Voter(Pref_Voter_Id, Precinct_Id)
				voters[Pref_Voter_Id] = voter
			if Vote_Rank == 1 and Candidate_Id != 0:
				voter.firstChoice = candidates[Candidate_Id]
			elif Vote_Rank == 2 and Candidate_Id != 0:
				voter.secondChoice = candidates[Candidate_Id]
			elif Vote_Rank == 3 and Candidate_Id != 0:
				voter.thirdChoice = candidates[Candidate_Id]

# Tally up, for each candidate, how many of the voters who voted for them as the voter's first choice voted for each of the candidates as second choice, and how many voted for each of the candidates as third choice.
for voterID, voter in voters.iteritems():
	if voter.firstChoice:
		voter.firstChoice.firstPlaceTallies.update([voter.firstChoice])
	if voter.firstChoice and voter.secondChoice:
		voter.firstChoice.secondPlaceTallies.update([voter.secondChoice])
	if voter.firstChoice and voter.thirdChoice:
		voter.firstChoice.thirdPlaceTallies.update([voter.thirdChoice])
	
# Output the results of the tallies.
for candidateID, candidate in candidates.iteritems():
	print('== FIRST PLACE VOTES BY %s VOTERS ==' % candidate.name)
	for tallyCandidateID, tallyCandidate in candidates.iteritems():
		print '{}: {:,}'.format(tallyCandidate.name, candidate.firstPlaceTallies[tallyCandidate])
	print('== SECOND PLACE VOTES BY %s VOTERS ==' % candidate.name)
	for tallyCandidateID, tallyCandidate in candidates.iteritems():
		print '{}: {:,}'.format(tallyCandidate.name, candidate.secondPlaceTallies[tallyCandidate])
	print('== THIRD PLACE VOTES BY %s VOTERS ==' % candidate.name)
	for tallyCandidateID, tallyCandidate in candidates.iteritems():
		print '{}: {:,}'.format(tallyCandidate.name, candidate.thirdPlaceTallies[tallyCandidate])
	print '======================================'

