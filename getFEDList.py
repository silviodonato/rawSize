from FEDlist import FEDlist

badFEDs = []
#badFEDs = [11462, ##CTPPS
#    11104, 11106, 11108, 11110, 11112, 11114, 11116, 11118, 11120, 11134, 11122, 11124, 11126, 11128, 11100, 11102 ##HCAL
#    ]

def getList(key, FEDlist=FEDlist, badFEDs = badFEDs):
    if key in FEDlist:
        out = []
        for v in FEDlist[key]:
            if type(v) == range:
                out += list(v)
            else:
                out += [v]
        for badFED in badFEDs:
            if badFED in out:
                out.remove(badFED)
        return out
    
    elif "FPIX" == key:
        return getList("FPIX+")+getList("FPIX-")
    elif "BPIX" == key:
        return getList("BPIX+")+getList("BPIX-")
    
    elif "Pixel" == key:
        return getList("FPIX")+getList("BPIX")
    
    elif "TEC" == key:
        return getList("TEC+")+getList("TEC-")
    elif "Strip" == key:
        return getList("TIBTID")+getList("TOB")+getList("TEC")
    
    elif "Tracker" == key:
        return getList("Pixel")+getList("Strip")
    
    elif "EB" == key:
        return getList("EB+")+getList("EB-")
    elif "EE" == key:
        return getList("EE+")+getList("EE-")
    elif "ES" == key:
        return getList("ES+")+getList("ES-")
    
    elif "ECAL" == key:
        return getList("EB")+getList("EE")+getList("ES")
    
    elif "HBHE" == key:
        return getList("HBHEA")+getList("HBHEB")+getList("HBHEC")
    
    elif "HCAL" == key:
        return getList("HBHE")+getList("HF")+getList("HO")
    
    elif "GEM" == key:
        return getList("GEM+")+getList("GEM-")+getList("GEMPILOT")
    elif "CSC" == key:
        return getList("CSC+")+getList("CSC-")
    elif "DT" == key:
        return getList("DT+")+getList("DT-")+getList("DT0")+getList("DTUP")
    elif "Muon" == key:
        return getList("DT")+getList("CSC")+getList("RPC")+getList("GEM")
    
    elif "L1T" == key:
        return getList("CALOL1")+getList("CALOL2")+getList("MUTF")+getList("UGT")+getList("UGTSPARE")
    
    elif "Others" == key:
        return getList("CTPPS")+getList("TOTDET")+getList("CPM-PRI")+getList("TWINMUX")
    
    elif "All" == key:
        return getList("L1T")+getList("Pixel")+getList("Strip")+getList("ECAL")+getList("HCAL")+getList("Muon")+getList("Others")
    else:
        raise Exception("%s is unknown in getList()." %key)

def getListToBeExcluded(key, FEDlist=FEDlist, badFEDs = badFEDs):
    out = getList("All", FEDlist=FEDlist, badFEDs = badFEDs)
    for el in getList(key, FEDlist=FEDlist, badFEDs = badFEDs):
        out.remove(el)
    return out


if __name__ == '__main__':
    all_ = getList("All")
    print(all_)

    ## Check all FED are included in "All"
    #print(len(all_))
    for i, x in enumerate(all_):
        for j, y in enumerate(all_[i+1:]):
            if x==y:
                print (i, j, j+i+1, x, y, all_[i], all_[j], all_[i+1:][j])
    out = []
    #FEDlist = {"MUTF" : FEDlist["MUTF"]}
    for vs in FEDlist.values():
        for v in vs:
    #        print(v)
            if type(v) == range:
                out += list(v)
            else:
                out += [v]

    Sout = set(out)
    Sall = set(all_)

    print(Sout-Sall)
    print(Sall-Sout)
    hltHcalCalibrationRaw = [700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 1024, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1127, 1128, 1129, 1130, 1131, 1132, 1133, 1134, 1135, 1136, 1137, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1145, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172, 1173, 1174, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1189, 1190, 1191, 1192, 1193, 1194, 1195, 1196, 1197, 1198, 1199]
    print(set(hltHcalCalibrationRaw) - set(getList("HCAL")))
    print(set(getList("HCAL")) - set(hltHcalCalibrationRaw))

#CALOL1
#CALOL2
#MUTF

#CPM-PRI

#CTPPS
#TOTDET

#FPIX+
#FPIX-

#BPIX
#BPIX-

#TIBTID
#TOB
#TEC+
#TEC-

#CSC+
#CSC-
#DT+
#DT-
#DT0
#DTUP
#GEM+
#GEM-
#GEMPILOT
#RPC

#EB+
#EB-
#EE+
#EE-
#ES+
#ES-


#HBHEA
#HBHEB
#HBHEC
#HF
#HO




