# Utility functions for parsing and analyzing labor data


# Parses a "Participants" entry that is a string of charged, charging, and
# involved parties in a case. 
# Charged parties follow 'Charged Party / Respondent,'
# Charging parties follow 'Charging Party,'
# Involved parties follow 'Involved Party,' 
# Returns a list [charged, charging, involved] where each entry is a list 
# of parties, which are strings. Lists can be empty.
# TODO: trim leading spaces and line breaks 
def get_charged_and_charging(S):
	charged = []
	chargers = []

	# split by charged
	S = S.split("Charged Party / Respondent,")
	for s in S:
		if len(s) > 0:
			if "Charging Party, " in s:
				SS = s.split("Charging Party,")
				if len(SS[0]) > 0:
					charged += [SS[0]]
				chargers += SS[1:]
			else:
				charged += [s]

	return [charged, chargers]


# Returns a list of unions present in a given string. Good for parsing case
# names to determine which union(s) are involved. 
# TODO
def unions_involved(S):
	unions = []
	return unions