# Utility functions for parsing and analyzing labor data


# Parses a "Participants" entry that is a string of charged, charging, and
# involved parties in a case. 
# Charged parties follow 'Charged Party / Respondent,'
# Charging parties follow 'Charging Party,'
# Involved parties follow 'Involved Party,' 
# Returns a list [charged_parties, charging_parties, involved_parties] 
# where each entry is a (possibly empty) list of parties, which are strings.
def get_charged_charging_and_involved(participants):
	if not isinstance(participants, str):
		return [[],[],[]]
    
	charged_parties = []
	charging_parties = []
	involved_parties = []

	# split by charged
	split_on_charged = participants.split("Charged Party / Respondent,")
	for S in split_on_charged:
		if len(S) > 0:
			if "Charging Party," in S:
				split_on_charging = S.split("Charging Party,")
				if len(split_on_charging[0]) > 0:
					if "Involved Party," in split_on_charging[0]:
						split_on_involved = split_on_charging[0].split("Involved Party,")
						if len(split_on_involved[0]) > 0:
							charged_parties += [split_on_involved[0].strip()]
						involved_parties += [p.strip() for p in split_on_involved[1:]]
					else:
						charged_parties += [split_on_charging[0].strip()]
				for SS in split_on_charging[1:]:
					if "Involved Party," in SS:
						split_on_involved = SS.split("Involved Party,")
						if len(split_on_involved[0]) > 0:
							charging_parties += [split_on_involved[0].strip()]
						involved_parties += [p.strip() for p in split_on_involved[1:]]
					else:
						charging_parties += [SS.strip()]
			elif "Involved Party," in S:
				split_on_involved = S.split("Involved Party,")
				if len(split_on_involved[0]) > 0:
					charged_parties += [split_on_involved[0].strip()]
				involved_parties += [p.strip() for p in split_on_involved[1:]]
			else:
				charged_parties+= [S.strip()]

	return [charged_parties, charging_parties, involved_parties]


# Returns a list of unions present in a given string. Good for parsing case
# names to determine which union(s) are involved. 
# TODO
def unions_involved(S):
	unions = []
	return unions