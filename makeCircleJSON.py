import subprocess

dets = ['BPIX+', 'BPIX-', 'CALOL1', 'CALOL2', 'CPM-PRI', 'CSC+', 'CSC-', 'CTPPS', 'DT+', 'DT-', 'DT0', 'DTUP', 'EB+', 'EB-', 'EE+', 'EE-', 'ES+', 'ES-', 'FPIX+', 'FPIX-', 'GEM+', 'GEM-', 'GEMPILOT', 'HBHEA', 'HBHEB', 'HBHEC', 'HF', 'HO', 'MUTF', 'RPC', 'TEC+', 'TEC-', 'TIBTID', 'TOB', 'TOTDET', 'TWINMUX', 'UGT', 'UGTSPARE']

#dets = ['BPIX+', 'BPIX-', ,, , ,, 'DTUP', , , , , , , , , , , , , ]
#dets = ['BPIX+', 'EB-']

groups = {
    "BPIX": ['BPIX+', 'BPIX-'],
    "FPIX": ['FPIX+', 'FPIX-'],
    "L1T": ['CALOL1', 'CALOL2', 'MUTF', 'UGT', 'UGTSPARE'],
    "TEC": ['TEC+', 'TEC-'],
    "TIBTOB": ['TIBTID', 'TOB'],
    "CSC": ['CSC+', 'CSC-'],
    "DT": ['DT+', 'DT-', 'DT0', 'DTUP'],
    "RPC": ['RPC'],
    "EB": ['EB+', 'EB-'],
    "EE": ['EE+', 'EE-'],
    "ES": ['ES+', 'ES-'],
    "GEM": ['GEM+', 'GEM-', 'GEMPILOT'],
    "HBHE": ['HBHEA', 'HBHEB', 'HBHEC'],
    "HF": ['HF'],
    "HO": ['HO'],
    "CPM-PRI": ['CPM-PRI'],
    "TOTDET": ['TOTDET'],
    "TWINMUX": ['TWINMUX'],
    "CTPPS": ['CTPPS'],
}

def getType(var):
    for group in groups:
        if var in groups[group]:
            return group
    raise Exception("%s not defined in %s"%(str(var),str(groups)))

def getSizes(fName):
    print("Doing %s."%fName)
    output = subprocess.check_output("edmEventSize -v %s"%fName, shell=True)

    events = 0
    var = 0
    for line in output.decode().split("\n"):
        if " Events " in line:
            if events !=0 : raise Exception("Two nevents!")
            events = int(line.split(" ")[3])
        if "FEDRawDataCollection" in line:
            if var !=0 : raise Exception("Two FEDRawDataCollection!")
            var, uncompressed, compressed = line.split(" ")
            compressed = float(compressed)*events/1000 ##already contains Byte/Event
            uncompressed = float(uncompressed)*events/1000
            var = var.split("_")[1][len("FED"):-len("Selector")]
    return var, events, round(compressed,3), round(uncompressed,3)

#fName = "RawStudy_TWINMUX.root"
#var, compressed, uncompressed = getSizes("RawStudy_TWINMUX.root")
#print(var, compressed, uncompressed)


outDict = dict()
outDict["resources"] =[
    {
      "size_compr": "event size"
    },
    {
      "size_uncompr": "uncompressed event size"
    }
]
outDict["modules"] = []


files = subprocess.check_output("ls RawStudy_*root", shell=True).decode().split("\n")
files.remove("")
for det in dets:
    fName = "RawStudy_%s.root"%det
    fName = fName.replace("+","p").replace("-","m")
    var, events, compressed, uncompressed = getSizes(fName)
#    print(var, events, compressed, uncompressed)
    outDict["modules"].append({
      "events": events,
      "label": det,
      "size_compr": compressed,
      "size_uncompr": uncompressed,
      "type": getType(det)
    })

var, events, compressed, uncompressed = getSizes("RawStudy_Default.root")

outDict["total"] = {
  "events": events,
  "label": "EventSize",
  "size_compr": compressed,
  "size_uncompr": uncompressed,
  "type": "Job"
}


#import pprint
#pprint.pprint(outDict)

import json
json_object = json.dumps(outDict, indent = 4)  
print(json_object) 
