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

# Parses a party string to return [type, name]
# The types this function looks for are: 
#     Legal Representative
#    Employer
#    Union 
#    Individual
#    Additional Service
#    Notification
#    Union as an Employer
# Any other types return ["", party]
# 
# From the data we have, it does seem we would want to also parse parties of
# the form "Individual\n[some other party]" where [some other party] is 
# Empoloyer, Amicus, Petitioner, Intervenor, etc. But these cases are fairly
# few, i.e. less than 100 total in all ULP cases.
def parse_party(party):
    party_types = ["Legal Representative","Employer","Union","Individual","Additional Service","Notification","Union as an Employer"]
    for party_type in party_types:
        if party.startswith(party_type):
            if party.startswith(party_type+","):
                return [s.strip() for s in party.split(",", 1)]
            else:
                return [party_type, party.split(party_type, 1)[1]]
    return ["", party]

# Determines whether a case is employer vs union, vice versa, or something
# else. Input is a list of charged parties and a list of charging parties.
# Possible outputs are:
#     "Union charged employer"
#    "Employer charged union"
#    "Union charged union"
#    "Employer charged employer"
#    "Other"
# Note: Our filtering here is pretty strict, since cases where an empolyer
# a union are both charging or charged fall into "Other." In practice a very
# large fraction of cases are "Other" and we may want to consider a less
# granular metric, e.g. whether the case was brought by a union, by an employer
# or neither. 
def who_charging_who(charged, charging):
    emp_charged = False
    emp_charging = False
    union_charged = False
    union_charging = False
    individual_charging = False
    individual_charged = False
    for p in charged:
        p = parse_party(p)
        if p[0] == "Employer":
            emp_charged = True
        elif p[0] == "Union":
            union_charged = True
        elif p[0] == "Individual":
            individual_charged = True
    for p in charging:
        p = parse_party(p)
        if p[0] == "Employer":
            emp_charging = True
        elif p[0] == "Union":
            union_charging = True
        elif p[0] == "Individual":
            individual_charging = True

    match [emp_charged, emp_charging, union_charged, union_charging, individual_charged, individual_charging]:
        case [True, False, False, True, False, False]:
            return "Union charging Employer"
        case [True, False, False, False, False, True]:
            return "Individual charging Employer"
        case [False, False, True, False, False, True]:
            return "Individual charging Union"
        case [False, True, True, False, False, False]:
            return "Employer charging Union"
        case [True, False, False, False, False, False]:
            return "Other charging Employer"
        case [False, False, True, True, False, False]:
            return "Union charging Union"
        case [True, False, False, True, False, True]:
            return "Union charging Employer" #Individual is charging here too
        case _:
            return "Other"


# Determines who is defending in a case: an employer, a union, or other.
# Some cases have employers and union both defending, which we categorize
# as "other"
def who_being_charged(charged):
    employer_charged = False
    union_charged = False
    for p in charged:
        p = parse_party(p)
        if p[0] == "Employer":
            employer_charged = True
        elif p[0] == "Union":
            union_charged = True
    match [employer_charged, union_charged]:
    	case [True, False]:
    		return "Employer"
    	case [False, True]:
    		return "Union"
    	case _:
    		return "Other"

# Returns a list of unions present in a given string. Good for parsing case
# names to determine which union(s) are involved. 
# TODO
def unions_involved(S):
    unions = []
    return unions