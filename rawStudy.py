import FWCore.ParameterSet.Config as cms
process = cms.Process( "RAWSizeStudy" )

process.source = cms.Source( "PoolSource",
    fileNames = cms.untracked.vstring(
        'file:/scratchssd/sdonato/RAWprime/456a5920-f13b-4d65-b777-603fa57ea934.root',
    ),
    inputCommands = cms.untracked.vstring(
        'keep *'
    )
)

process.hltFEDToExclude = cms.EDProducer( "EvFFEDExcluder",
    src = cms.InputTag( "rawDataCollector" ),
    fedsToExclude = ( cms.vuint32( 50, 51, 52,) )
)

process.hltFEDTest = cms.EDProducer( "EvFFEDSelector",
    inputTag = cms.InputTag( "rawDataCollector" ),
#    fedList = cms.vuint32( 1356, 1358, 1360, 1376, 1377 ),
    fedList = cms.vuint32(
        1462, 1463, 
#        11462, 
        582, 583,
        577, 578, 579, 580, 581,
        584, 585, 586, 587, 1024,
        1356, 1358, 1360, 1376, 1377,
        1390, 1391, 1393, 1394, 1395
    )

)

process.hltFEDTest = cms.EDProducer( "EvFFEDSelector",
    inputTag = cms.InputTag( "rawDataCollector" ),
#    fedList = cms.vuint32( 1356, 1358, 1360, 1376, 1377 ),
    fedList = cms.vuint32(
        1462, 1463, 
#        11462, 
        582, 583,
        577, 578, 579, 580, 581,
        584, 585, 586, 587, 1024,
        1356, 1358, 1360, 1376, 1377,
        1390, 1391, 1393, 1394, 1395
    )

)


process.hltTriggerType = cms.EDFilter("HLTTriggerTypeFilter",
    SelectedTriggerType = cms.int32(1)
)


#process.HLT_Dummy = cms.Path( process.HLTBeginSequence + process.hltFEDTest + process.HLTEndSequence )
#process.HLT_Dummy = cms.Path( process.HLTBeginSequence + process.HLTEndSequence )
process.HLT_Dummy = cms.Path( process.hltTriggerType )
process.schedule = cms.Schedule( *(process.HLT_Dummy, ))

###########################

# add a single "keep *" output
process.hltOutputFull = cms.OutputModule( "PoolOutputModule",
    fileName = cms.untracked.string( "RawStudy_Default.root" ),
    fastCloning = cms.untracked.bool( False ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string( 'RECO' ),
        filterName = cms.untracked.string( '' )
    ),
#    SelectEvents = cms.untracked.PSet(  SelectEvents = cms.vstring( 'HLT_Dummy')),
    outputCommands = cms.untracked.vstring( 
        'drop *',
        'keep FED*_rawDataCollector_*_*',
    )
)
process.FullOutput = cms.FinalPath( process.hltOutputFull )
process.schedule.append( process.FullOutput )

###########################

from getFEDList import getList, getListToBeExcluded, FEDlist

#for detector in ["Pixel"]:
#for detector in ["Others", "BPIX+"]:
#        return getList("L1T")+getList("Pixel")+getList("Strip")+getList("ECAL")+getList("HCAL")+getList("Muon")+getList("Others")
#for detector in ["L1T", "Others", "ECAL", "Muon", "HO"]: #, "HF", "HBHEA" , "HBHEB" , "HBHEC"
detectors = ["L1T", "Others", "ECAL", "Muon", "HCAL", "Pixel", "Strip", "All"]
detectors += FEDlist.keys()
for detector in detectors: 
#    fedModule = process.hltFEDTest.clone(
#        fedList = sorted(getList(detector))
#    )
    fedModule = process.hltFEDToExclude.clone(
        fedsToExclude = sorted(getListToBeExcluded(detector))
    )
    detector = detector.replace("+","p").replace("-","m")
    setattr(process, "FED%sSelector"%detector, fedModule)
    process.HLT_Dummy.insert(2, fedModule)
    outputModule = process.hltOutputFull.clone(
        fileName = "RawStudy_%s.root"%detector,
        outputCommands = cms.untracked.vstring( 
            'drop *',
            'keep FED*_FED%sSelector_*_*'%detector,
        )
    )
    setattr(process, "FED%sOutputModule"%detector, outputModule)
    finalPath = cms.FinalPath( outputModule )
    setattr(process, "FED%sOutput"%detector, finalPath)
    process.schedule.append( finalPath )

#print(fedModule.dumpPython())

# limit the number of events to be processed
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( 100 )
)

# enable TrigReport, TimeReport and MultiThreading
process.options.wantSummary = True
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
