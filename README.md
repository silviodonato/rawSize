## Raw event size study
### Short instructions

- Run `rawStudy.py` in CMSSW (eg. CMSSW_13_2_6_patch2) to get as output several RAW files containing each of them one detector (eg. `RawStudy_BPIXp.root`). These files will be used to measure the contribution of each detector to the total event size.
- Use `makeCircleJSON.py` to make an `events.json` which can be used in [Circles](https://github.com/fwyzard/circles/tree/master) ([link](https://sdonato.web.cern.ch/sdonato/eventContentSize/circles/web/piechart.php?local=false&dataset=event&resource=size_compr&colours=default&groups=eventSize&threshold=0)) 



### Long instructions

- Make `FEDlist.txt` from [OMS](https://cmsoms.cern.ch/cms/runs/report?cms_run=370293)
- Create `FEDlist.py` using `convertFedList.py`
- `FEDlist.py` will be used in `rawStudy.py` through `getFEDList.py`
- Run `rawStudy.py` selecting a proper RAW root file
- You should get files like this 
```
edmEventSize -v RawStudy_BPIXp.root

File RawStudy_BPIXp.root Events 100
Branch Name | Average Uncompressed Size (Bytes/Event) | Average Compressed Size (Bytes/Event) 
FEDRawDataCollection_FEDBPIXpSelector__RAWSizeStudy. 119913 93922.8
EventAuxiliary 120.07 27.38
EventSelections 79.21 4.66
EventProductProvenance 30.56 3.78
BranchListIndexes 26.31 3.12
```
- Run `makeCircleJSON.py > events.json` to create the `events.json`
- Load `events.json` in `circles/web/data` in your [Circles](https://github.com/fwyzard/circles/tree/master) website (see ([link](https://sdonato.web.cern.ch/sdonato/eventContentSize/circles/web/piechart.php?local=false&dataset=event&resource=size_compr&colours=default&groups=eventSize&threshold=0)).
- Copy `eventSize.json` in your `circles/web/groups`
- Adapt `circle/web/piechart.html` and  `circle/web/piechart.php` as follow
```
         if (config.resource.startsWith("time_")) {
           current.unit = " ms";
           current.title = "Time";
+        } else if (config.resource.startsWith("size_")) {
+          current.unit = " kB";
+          current.title = "Size";
         } else if (config.resource.startsWith("mem_")) {
           current.unit = " kB";
           current.title = "Memory";
```
