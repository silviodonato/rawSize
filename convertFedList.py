import json

fName = 'FEDlist.txt' ##take list of FED from OMS ( https://cmsoms.cern.ch/cms/runs/report?cms_run=362722 )
outFile = 'FEDlist.py'
# Read the input text file
with open(fName, 'r') as file:
    lines = file.readlines()

#lines = lines[2:]

# Initialize variables
output = """
FEDlist = {
"""
current_key = None
current_values = []

# Process each line in the input file
for i, line in enumerate(lines):
    line = line.strip()
    print(i%4, line)
    if i%4==0:
        name = line
    elif i%4==1:
        continue
    elif i%4==2:
        continue
    elif i%4==3:
        values = line
        output += "  '%s' : ["%name
        for value in values.split(" "):
            if "-" in value:
                a, b = value.split("-")
                output += "\n    range(%d, %d),"%(int(a), int(b)+1)
            else:
                output += "\n    %s,"%value
        output += "\n  ],\n"
output += "}\n"

print(output)

ofile = open(outFile, 'w')
ofile.write(output)
ofile.close()


'''


CALOL1
CALOL2
MUTF

CPM-PRI

CTPPS

FPIX+
FPIX-

BPIX
BPIX-

TIBTID
TOB
TOTDET
TEC+
TEC-

CSC+
CSC-
DT+
DT-
DT0
DTUP
GEM+
GEM-
GEMPILOT
RPC

EB+
EB-
EE+
EE-
ES+
ES-


HBHEA
HBHEB
HBHEC
HF
HO
'''
