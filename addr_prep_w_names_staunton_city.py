# Credit to https://github.com/MikeTho16 for compiling this script
#!/usr/bin/python3
import re
import copy
import csv
import time

addr_input = 'VirginiaSiteAddressPoint.txt'

# # change me is listed 3 places. Two of them for output
# file, and one for choosing municipality to export.
# Put all of the street type abbreviations to be expanded here
# Note that the USPS has a standard list of such abbreviations
# This list (Python dictionary) is now complete, filled from
# https://pe.usps.com/text/pub28/28apc_002.htm
street_types = {
    'RD': 'Road',
    'TRL': 'Trail',
    'TR': 'Trail', #unofficial abbreviation
    'LN': 'Lane',
    'DR': 'Drive',
    'AVE': 'Avenue',
    'WAY': 'Way',
    'CIR': 'Circle',
    'RUN': 'Run',
    'HWY': 'Highway',
    'TPKE': 'Turnpike',
    'LOOP': 'Loop',
    'PL': 'Place',
    '': '',
    'CT': 'Court',
    'ST': 'Street',
    'PIKE': 'Pike',
    'HOLW': 'Hollow',
    'ROW': 'Row',
    'SPUR': 'Spur',
    'PARK': 'Park',
    'SQ': 'Square',
    'CRK': 'Creek',
    'VW': 'View',
    'TER': 'Terrace',
    'BLVD': 'Boulevard',
    'HTS': 'Heights',
    'ALY': 'Alley',
    'PATH': 'Path',
    'STA': 'Station',
    'ANX': 'Anex',
    'ARC': 'Arcade',
    'BYU': 'Bayou',
    'BCH': 'Beach',
    'BND': 'Bend',
    'BLF': 'Bluff',
    'BLF': 'Bluffs',
    'BTM': 'Bottom',
    'BR': 'Branch',
    'BRG': 'Bridge',
    'BRK': 'Brook',
    'BRKS': 'Brooks',
    'BG': 'Burg',
    'BGS': 'Burgs',
    'BYP': 'Bypass',
    'CP': 'Camp',
    'CYN': 'Canyon',
    'CPE': 'Cape',
    'CSWY': 'Causeway',
    'CTR': 'Center',
    'CTRS': 'Centers',
    'CIRS': 'Circles',
    'CLF': 'Cliff',
    'CLFS': 'Cliffs',
    'CLB': 'Club',
    'CMN': 'Common',
    'CMNS': 'Commons',
    'COR': 'Corner',
    'CORS': 'Corners',
    'CRSE': 'Course',
    'CTS': 'Courts',
    'CV': 'Cove',
    'CVS': 'Coves',
    'CRES': 'Crescent',
    'CRST': 'Crest',
    'XING': 'Crossing',
    'XRD': 'Crossroad',
    'XRDS': 'Crossroads',
    'CURV': 'Curve',
    'DL': 'Dale',
    'DM': 'Dam',
    'DV': 'Divide',
    'DRS': 'Drives',
    'EST': 'Estate',
    'ESTS': 'Estates',
    'EXPY': 'Expressway',
    'EXT': 'Extension',
    'EXTS': 'Extensions',
    'FALL': 'Fall',
    'FLS': 'Falls', #Just pointing out Fall is not abbreviated, but Falls is.
    'FRY': 'Ferry',
    'FLDS': 'Fields',
    'FLTS': 'Flats',
    'FLT': 'Flat',
    'FRD': 'Ford',
    'FRDS': 'Fords',
    'FRST': 'Forest',
    'FRG': 'Forge',
    'FRGS': 'Forges',
    'FRK': 'Fork',
    'FRKS': 'Forks',
    'FT': 'Fort',
    'FWY': 'Freeway',
    'GDN': 'Garden',
    'GDNS': 'Gardens',
    'GTWY': 'Gateway',
    'GLN': 'Glen',
    'GLNS': 'Glens',
    'GRN': 'Green',
    'GRNS': 'Greens',
    'GRV': 'Grove',
    'GRVS': 'Groves',
    'HBR': 'Harbor',
    'HBRS': 'Harbors',
    'HVN': 'Haven',
    'HL': 'Hill',
    'HLS': 'Hills',
    'INLT': 'Inlet',
    'IS': 'Island',
    'ISS': 'Islands',
    'ISLE': 'Isle',
    'JCT': 'Junction',
    'JCTS': 'Junctions',
    'KY': 'Key',
    'KYS': 'Keys',
    'KNL': 'Knoll',
    'KNLS': 'Knolls',
    'LK': 'Lake',
    'LKS': 'Lakes',
    'LAND': 'Land',
    'LNDG': 'Landing',
    'LGT': 'Light',
    'LGTS': 'Lights',
    'LF': 'Loaf',
    'LCK': 'Lock',
    'Locks': 'Locks',
    'LDG': 'Lodge',
    'MALL': 'Mall',
    'MNR': 'Manor',
    'MNRS': 'Manors',
    'MDW': 'Meadow',
    'MDWS': 'Meadows',
    'MEWS': 'Mews',
    'ML': 'Mill',
    'MLS': 'Mills',
    'MSN': 'Mission',
    'MTWY': 'Motorway',
    'MT': 'Mount',
    'MTN': 'Mountain',
    'MTNS': 'Mountains',
    'NCK': 'Neck',
    'ORCH': 'Orchard',
    'OVAL': 'Oval',
    'OPAS': 'Overpass',
    'PARKS': 'Parks',
    'PKWY': 'Parkway',
    'PKWYS': 'Parkways', #PKWY used for singular and plural; assuming this is correct plural form
    'PASS': 'Pass',
    'PSGE': 'Passage',
    'PNE': 'Pine',
    'PNES': 'Pines',
    'PLN': 'Plain',
    'PLNS': 'Plains',
    'PLZ': 'Plaza',
    'PT': 'Point',
    'PTS': 'Points',
    'PRT': 'Port',
    'PRTS': 'Ports',
    'PR': 'Prairie',
    'RADL': 'Radial',
    'RAMP': 'Ramp',
    'RNCH': 'Ranch',
    'RPD': 'Rapid',
    'RPDS': 'Rapids',
    'RST': 'Rest',
    'RDG': 'Ridge',
    'RDGS': 'Ridges',
    'RIV': 'River',
    'RDS': 'Roads',
    'RTE': 'Route',
    'RUE': 'Rue',
    'SHL': 'Shoal',
    'SHLS': 'Shoals',
    'SHR': 'Shore',
    'SHRS': 'Shores',
    'SKWY': 'Skyway',
    'SPG': 'Spring',
    'SPGS': 'Springs',
    'SPURS': 'Spurs', #SPUR used for singular and plural; assuming this is correct plural form
    'SQS': 'Squares',
    'STRA': 'Stravenue', #only useful in Tuscon, AZ
    'STRM': 'Stream',
    'STS': 'Streets',
    'SMT': 'Summit',
    'TRWY': 'Throughway',
    'TRCE': 'Trace',
    'TRAK': 'Track',
    'TRFY': 'Trafficway',
    'TRLR': 'Trailer',
    'TUNL': 'Tunnel',
    'UPAS': 'Underpass',
    'UN': 'Union',
    'UNS': 'Unions',
    'VLY': 'Valley',
    'VLYS': 'Valleys',
    'VIA': 'Viaduct',
    'VWS': 'Views',
    'VLG': 'Village',
    'VLGS': 'Villages',
    'VL': 'Ville',
    'VIS': 'Vista',
    'WALK': 'Walk',
    'WK': 'Walk', #Not an official abbreviation, but used in Augusta County
    'WALKS': 'Walks', #WALK used for singular and plural; assuming this is correct plural form
    'WALL': 'Wall',
    'WAYS': 'Ways',
    'WL': 'Well',
    'WLS': 'Wells'
    }

# Direction prefix dictionary
street_prefixes = {
    '': '',
    'N': 'North',
    'NE': 'Northeast',
    'NW': 'Northwest',
    'S': 'South',
    'SE': 'Southeast',
    'SW': 'Southwest',
    'E': 'East',
    'W': 'West'
    }

street_suffixes = {
    '': ''
    }

# A dictionary of all unit labels and their replacements
# This dictionary is filled from
# https://pe.usps.com/text/pub28/28apc_003.htm
# "** Does not require a Secondary RANGE to follow" from USPS page.
# my interpretation of this means it does not need a addr:unit identifier.
unit_labels = {
    'APT': 'Apartment',
    'BSMT': 'Basement',  # **
    'BLDG': 'Building',
    'DEPT': 'Department',
    'FL': 'Floor',
    'FRNT': 'Front', # **
    'HNGR': 'Hanger',
    'KEY': 'Key',
    'LBBY': 'Lobby', # **
    'LOT': 'Lot',
    'LOWR': 'Lower',  # **
    'OFC': 'Office',  # **
    'PH': 'Penthouse',  # **
    'PIER': 'Pier',
    'REAR': 'Rear',  # **
    'RM': 'Room',
    'SIDE': 'Side',  # **
    'SLIP': 'Slip',
    'SPC': 'Space',
    'STOP': 'Stop',
    'STE': 'Suite',
    'TRLR': 'Trailer',
    'UNIT': 'Unit',
    'UPPR': 'Upper',  # **
    'STO': 'Stop',       # Not the official abbreviation, used in Rockbridge
    'OFF': 'Office'      # Not the official abbreviation, used in Rockbridge
    }

# The position of a word within the street name impacts how we handle it. For example
# if 'THE' appears as the first work in a street name we want it to be translated
# as 'The', but if appears elsewhere, we want to be translated as 'the'.  All comparisons
# are case insensitive, so for consistency, all patters use upper case letters.  Of
# course the substitutions are case sensitive - otherwise this wouldn't achieve the
# desired outcome.
#
# In the regular expression, the part between ( and ) is the part that gets replaced.
#
# \b - Represents a word boundary so '\b(AND)\b' only matches 'AND' if it is a stand alone
#      word, and doesn't match 'SAND' or 'ANDERSON'.  The word boundary can be the beginning
#      or end of the street name as well as most non alphanumeric characters.
street_name_special_cases = [
    (r' (THE)\b', 'the'),    # Only lowercase 'The' that doesn't occur at start
    (r'\b(ST) ', 'Saint'),   # Only translate ST -> Saint if it doesn't occur at the end of the name
    (r'\b(HANKEY MT)\b', 'Hankey Mountain'), #very specific use case for error in data source for Augusta County.
    (r'\b(MTN)\b', 'Mountain'),
    (r'\b(MT)\b', 'Mount'),
    (r'\b(MCBRYDGE)\b', 'McBrydge'),
    (r'\b(MCCAULEY)\b', 'McCauley'),
    (r'\b(MCCLUNG)\b', 'McClung'),
    (r'\b(MCCLURE)\b', 'McClure'),
    (r'\b(MCCLURES)\b', 'McClures'),
    (r'\b(MCCOMBS)\b', 'McCombs'),
    (r'\b(MCCORKLE)\b', 'McCorkle'),
    (r'\b(MCCORMICK)\b', 'McCormick'),
    (r'\b(MCCOWN)\b', 'McCown'),
    (r'\b(MCCRAY)\b', 'McCray'),
    (r'\b(MCCRORYS)\b', 'McCrorys'),
    (r'\b(MCCUE)\b', 'McCue'),
    (r'\b(MCCULLOCH)\b', 'McCulloch'),
    (r'\b(MCCURDY)\b', 'McCurdy'),
    (r'\b(MCCUTCHEN)\b', 'McCutchen'),
    (r'\b(MCDANIELS)\b', 'McDaniels'),
    (r'\b(MCELWEE)\b', 'McElwee'),
    (r'\b(MCGUSLIN)\b', 'McGuslin'),
    (r'\b(MCFADDIN)\b', 'McFaddin'),
    (r'\b(MCILWEE)\b', 'McIlwee'),
    (r'\b(MCKAMY)\b', 'McKamy'),
    (r'\b(MCKENDREE)\b', 'McKendree'),
    (r'\b(MCKENNY)\b', 'McKenny'),
    (r'\b(MCKETHAN)\b', 'McKethan'),
    (r'\b(MACKEYS)\b', 'McKeys'),
    (r'\b(MCKINLEY)\b', 'McKinley'),
    (r'\b(MCPHEETERS)\b', 'McPheeters'),
    (r'\b(MCARTHUR)\b', 'McArthur'),
    (r'\b(MCMAHON)\b', 'McMahon'),
    (r'\b(W )\b', 'West '),
    (r'\b(VSDB)\b', 'VSDB'), # Staunton City specific (Virginia School for Deaf and Blind)
    (r'\b(APT)\b', 'Apartment'), # i.e. Plaza Apartment Drive
    (r'\b(TPKE)\b', 'Turnpike'),
    (r'\b(PKWY)\b', 'Parkway'),
    (r'\b(LN)\b', 'Lane'),
    (r'\b(RD)\b', 'Road'),
    (r'\b(EXT)\b', 'Extension'),
    (r'\b(OF)\b', 'of'),
    (r'\b(AND)\b', 'and')
    ]

def fix_street_name(street_name):
    """ 'Fixes' the street name, including:
        * Converting from all upper case to title case
        * Handling upper case in the middle of words, e.g. McDonald
        * Handling words that should be all upper case, e.g. IBM
    """
    street_name_temp = title_case(street_name)
    for case in street_name_special_cases:
        pat = re.compile(case[0], flags=re.IGNORECASE)
        street_name_temp = apply_case(pat, case[1], street_name_temp)
    return street_name_temp

def apply_case(pat, replacement, string_in):
    """ For every case where the regular expression pattern (pat)
    matches in string_in, replace group 1 with replacement.
    """
    string_out = ''
    start_pos = 0
    for match in pat.finditer(string_in):
        string_out += string_in[start_pos:match.start(1)] + replacement
        start_pos = match.end(1)
    string_out += string_in[start_pos:]
    return string_out

def make_addr_unit_and_label(unitid):
    """ Makes the addr:unit tag/field and the addr:unit:label tag/field.
    """
    label = ''
    unit = unitid
    for unit_type in unit_labels:
        if unit_type in unit:
            unit = unit.replace(unit_type,'').strip()
            label = unit_labels[unit_type].strip()
            break
    return label, unit

def make_addr_housenumber(preaddrnum, addrnum, addrnumsuf):
    """ Makes the addr:housenumber tag/field by concatenating the preaddrnum, addrnum
    and addrnumsuf from the input data.
    """
    return preaddrnum.strip() + addrnum.strip() + addrnumsuf.strip()


def make_addr_street(street_prefix, street_name, street_type, street_suffix):
    """ Makes the addr:street tag/field by modifying and combining fields
    from the input file.
    """
    street_prefix_expanded = expand_street_prefix(street_prefix)
    street_name_title_case = fix_street_name(street_name)
    street_type_expanded = expand_street_type(street_type)
    street_suffix_expanded = expand_street_suffix(street_suffix)
    addr_street = street_prefix_expanded
    if addr_street != '':
        addr_street = addr_street + ' '
    addr_street = addr_street + street_name_title_case
    if street_type_expanded != '':
        addr_street += ' ' + street_type_expanded
    if street_suffix_expanded != '':
        addr_street += ' ' + street_suffix_expanded
    return addr_street

def title_case(title):
    """ Sets the first character in each word in the given title to upper
    case, and the rest to lower case.  While Python does have a built in
    .title() function, it produces things like "2Nd Street" rather than
    "2nd Street".
    """
    title_fixed = ''
    for word in title.split():
        word_fixed = word[0:1].upper() + word[1:].lower()
        if title_fixed:
            title_fixed += ' '
        title_fixed += word_fixed
    return title_fixed

def expand_street_suffix(street_suffix):
    """ Expands abbreviations in the street suffix field. The field is considered
    as a whole. If the contents of the street suffix field is not recognized as
    an abbreviation, a message is printed to stdout.
    """
    if street_suffix in street_suffixes:
        return street_suffixes[street_suffix]
    print('unhanded street suffix: ' + street_suffix)
    return None

def expand_street_prefix(street_prefix):
    """ Expands abbreviations in the street prefix field.  The field is considered
    as a whole. if the contents of the street prefix field is not blank, and is
    not recognized as an abbreviation, a message is printed to stdout.
    """
    if street_prefix in street_prefixes:
        return street_prefixes[street_prefix]
    print('unhanded street prefix: ' + street_prefix)
    return None

def expand_street_type(street_type_abbr):
    """ Expands abbreviations in the street type field.  The field is considered
    as a whole.  If the contents of the street type field is not blank, and is
    not recognized as an abbreviation, a message is printed to stdout.
    """
    if street_type_abbr in street_types:
        return street_types[street_type_abbr]
    print('unhandled street type abbreviation:' + street_type_abbr)
    return None

def split_county():
    """ Makes a file of just the data from a single county.  The format is the same
    as that of the input file, with the exception that latitude and longitude are
    added so that the data can be visualized in JOSM.
    """
    with open(addr_input, newline='') as csvfile:
        addr_reader = csv.DictReader(csvfile)
        with open('./staunton_original.csv', 'w', newline='') as csvfile_out:
            field_names = copy.deepcopy(addr_reader.fieldnames)
            field_names.append('latitude')
            field_names.append('longitude')
            field_names.append('name')
            writer = csv.DictWriter(csvfile_out, fieldnames=field_names)
            writer.writeheader()
            for row in addr_reader:
                # Unlike the rest of the file, it seems that the 'MUNICIPALITY' field's
                # contents are in title case, but we don't take any chances and force
                # an uppercase comparison.
                if row['MUNICIPALITY'].upper() == 'STAUNTON CITY':
                    new_row = {}
                    for key, value in row.items():
                        new_row[key] = value
                    new_row['latitude'] = row['LAT']
                    new_row['longitude'] = row['LONG']
                    new_row['name'] = row['PLACENAME']
                    writer.writerow(new_row)



def summarize():
    """ Makes a unique list of addr:street, addr:city, addr:unit
    """
    #with open('./1_Complete data in one file.csv', newline='') as csvfile:
    with open('./staunton.csv', newline='') as csvfile: # change me
        addr_reader = csv.DictReader(csvfile)
        streets = {}
        cities = {}
        units = {}
        count = 0
        for row in addr_reader:
            addr_street = row['addr:street']
            if addr_street not in streets:
                streets[addr_street] = addr_street
            if addr_street is None or addr_street == '':
                print('BLANK Street')
            addr_city = row['addr:city']
            if addr_city not in cities:
                cities[addr_city] = addr_city
            addr_unit = row['addr:unit']
            if addr_unit not in units:
                units[addr_unit] = addr_unit
            count += 1
    streets = list(streets.keys())
    streets.sort()
    for street in streets:
        print(street)
    print()

    cities = list(cities.keys())
    cities.sort()
    for city in cities:
        print(city)
    print()

    units = list(units.keys())
    units.sort()
    for unit in units:
        print(unit)

    print(f'Total Records: {count}')

def main():
    with open(addr_input, newline='') as csvfile:
        with open('./staunton.csv', 'w', newline='') as csvfile_out: # change me
            field_names = ['addr:housenumber', 'addr:street', 'addr:unit:label',
                           'addr:unit', 'addr:city', 'addr:state', 'addr:postcode',
                           'latitude', 'longitude', 'name']
            writer = csv.DictWriter(csvfile_out, fieldnames=field_names)
            writer.writeheader()
            addr_reader = csv.DictReader(csvfile)
            streets = {}
            cities = {}
            for row in addr_reader:
                # Unlike the rest of the file, it seems that the 'MUNICIPALITY' field's
                # contents are in title case, but we don't take any chances and force
                # an uppercase comparison.
                if row['MUNICIPALITY'].upper() == 'STAUNTON CITY': # change me
                    addr_street = make_addr_street(
                        row['STREET_PREFIX'],
                        row['STREET_NAME'],
                        row['STREET_TYPE'],
                        row['STREET_SUFFIX'])
                    if addr_street not in streets:
                        streets[addr_street] = addr_street
                    if addr_street is None or addr_street == '':
                        print('BLANK Street')
                    addr_city = row['PO_NAME'].title()
                    if addr_city not in cities:
                        cities[addr_city] = addr_city
                    addr_unit_label, addr_unit = make_addr_unit_and_label(row['UNITID'])
                    writer.writerow({'addr:housenumber': make_addr_housenumber(row['PREADDRNUM'],
                                                                               row['ADDRNUM'],
                                                                               row['ADDRNUMSUF']),
                                     'addr:street': addr_street,
                                     'addr:unit:label': addr_unit_label,
                                     'addr:unit': addr_unit,
                                     'addr:city': addr_city,
                                     'addr:state': 'VA',
                                     'addr:postcode': row['ZIP_5'],
                                     'latitude': row['LAT'],
                                     'longitude': row['LONG'],
                                     'name': row['PLACENAME']})
        streets = list(streets.keys())
        streets.sort()
        for street in streets:
            print(street)

        cities = list(cities.keys())
        cities.sort()
        for city in cities:
            print(city)

if __name__ == '__main__':
    #test_fix_street_name('THE RIGHT THE THE THEODORE END THE')
    #test_fix_street_name('ST ANDREWS')
    #test_fix_street_name('ANDREWS ST')
    #test_fix_street_name('LAKE STREET EXT')


    #summarize()
    #split_county()
    main()
