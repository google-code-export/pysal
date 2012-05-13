<map version="0.9.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="parallell pysal" ID="ID_1481318209" CREATED="1329408682020" MODIFIED="1329413769265" LINK="../../../../../../../nsf/cyber10/cyber%20infrastructure%20nsf.mm">
<hook NAME="MapStyle" max_node_width="600"/>
<node TEXT="plisa implementation" POSITION="left" ID="ID_528827780" CREATED="1329408686020" MODIFIED="1329408690408"/>
<node TEXT="fisher jenks optimization" POSITION="left" ID="ID_1199434912" CREATED="1329408690900" MODIFIED="1329408696456">
<node TEXT="original implementation" ID="ID_717263138" CREATED="1329409285132" MODIFIED="1329409298384"/>
<node TEXT="other implementation" ID="ID_1377887472" CREATED="1329409298877" MODIFIED="1329409314785"/>
<node TEXT="parallel implementations" ID="ID_1671283558" CREATED="1329409316261" MODIFIED="1329409326196">
<node TEXT="multiprocessing" ID="ID_1925429952" CREATED="1329409326701" MODIFIED="1329409332113">
<node TEXT="xing&apos;s note" ID="ID_1001833446" CREATED="1329409371046" MODIFIED="1329409376601" LINK="https://mail.google.com/mail/?shva=1#search/xing/13563fbf742a8e4b">
<node TEXT="syncrhonised" ID="ID_118152479" CREATED="1329412503382" MODIFIED="1329412514348">
<node TEXT="one process updates all others" ID="ID_1197658743" CREATED="1329412524646" MODIFIED="1329412534709"/>
<node TEXT="correct but slow" ID="ID_2082491" CREATED="1329412552501" MODIFIED="1329412555643"/>
</node>
<node TEXT="asyncrhonise" ID="ID_1794181482" CREATED="1329412515263" MODIFIED="1329412520499">
<node TEXT="no coordination" ID="ID_309199785" CREATED="1329412536318" MODIFIED="1329412540797"/>
<node TEXT="results in wrong classification" ID="ID_1561072515" CREATED="1329412541198" MODIFIED="1329412550813"/>
</node>
</node>
</node>
<node TEXT="pp" ID="ID_1832111801" CREATED="1329409332653" MODIFIED="1329409333849">
<node TEXT="dependency" ID="ID_645039258" CREATED="1329410334451" MODIFIED="1329410338976">
<node TEXT="sudo easy_install pp" ID="ID_1959385903" CREATED="1329410326993" MODIFIED="1329410333785"/>
</node>
<node TEXT="example" ID="ID_300367727" CREATED="1329410638931" MODIFIED="1329410640826">
<node TEXT="filling in a distance matrix" ID="ID_1384908022" CREATED="1329410641294" MODIFIED="1329410654758">
<node TEXT="compare sequential versus pp" ID="ID_1894534420" CREATED="1329410657086" MODIFIED="1329410665685"/>
<node TEXT="pptest1.py" ID="ID_430751389" CREATED="1329410679710" MODIFIED="1329410717611" LINK="../../pysal/src/pysal/branches/parallel/pysal/esda/pptest1.py"/>
</node>
<node TEXT="speeds things up" ID="ID_1445087306" CREATED="1329410747742" MODIFIED="1329410752531"/>
<node TEXT="each job determines distances for subsets of ijs" ID="ID_1575912565" CREATED="1329410756916" MODIFIED="1329410788561"/>
<node TEXT="results returned by job" ID="ID_388706391" CREATED="1329410788931" MODIFIED="1329410793944"/>
<node TEXT="outter loop fills in relevant section of distance matrix" ID="ID_849938239" CREATED="1329410794499" MODIFIED="1329410806764"/>
<node TEXT="question as to whether matrix could be directly passsed to the individual jobs" ID="ID_1643687489" CREATED="1329410807179" MODIFIED="1329410822379"/>
<node TEXT="issue of shared data" ID="ID_1543089314" CREATED="1329410824075" MODIFIED="1329410828215"/>
<node TEXT="need to consider load balancing" ID="ID_170237974" CREATED="1329412694003" MODIFIED="1329412699288">
<node TEXT="currently doing dij 2x" ID="ID_372834904" CREATED="1329412700026" MODIFIED="1329412705353"/>
</node>
</node>
</node>
<node TEXT="pyopencl" ID="ID_503622223" CREATED="1329409334261" MODIFIED="1329410839200"/>
</node>
<node TEXT="todo" ID="ID_1094534875" CREATED="1329411332466" MODIFIED="1329411334359">
<node TEXT="minimum" ID="ID_1847986195" CREATED="1329413837000" MODIFIED="1329413839997">
<node TEXT="implement pp for fj" ID="ID_1994966278" CREATED="1329413816576" MODIFIED="1329413820517"/>
<node TEXT="use same machine to compare all three methods" ID="ID_1804944538" CREATED="1329411335858" MODIFIED="1329411343967"/>
</node>
<node TEXT="time permitting" ID="ID_677884127" CREATED="1329413844936" MODIFIED="1329413847077">
<node TEXT="can pp do shared memory" ID="ID_1525337724" CREATED="1329412445048" MODIFIED="1329412451142"/>
<node TEXT="mp" ID="ID_1969030895" CREATED="1329412451623" MODIFIED="1329412455300">
<node TEXT="try it with preallocated D" ID="ID_505350834" CREATED="1329412455871" MODIFIED="1329412465524"/>
<node TEXT="mimic approach in pp" ID="ID_1559775600" CREATED="1329412466391" MODIFIED="1329412471868"/>
</node>
</node>
</node>
</node>
<node TEXT="aag 2012" POSITION="left" ID="ID_1150394529" CREATED="1329408846583" MODIFIED="1329408850017">
<node TEXT="presentation outline" ID="ID_881412052" CREATED="1329408850550" MODIFIED="1329408853778">
<node TEXT="project" ID="ID_496676089" CREATED="1329409094682" MODIFIED="1329409096822">
<node TEXT="overview" ID="ID_651371948" CREATED="1329410846978" MODIFIED="1329410855839"/>
<node TEXT="asu components" ID="ID_607588777" CREATED="1329410857082" MODIFIED="1329410860040"/>
</node>
<node TEXT="pysal" ID="ID_1093811235" CREATED="1329408854471" MODIFIED="1329409090029">
<node TEXT="history" ID="ID_1309337511" CREATED="1329410861570" MODIFIED="1329410863223"/>
<node TEXT="role in this project" ID="ID_211454277" CREATED="1329410863594" MODIFIED="1329410867671"/>
<node TEXT="focus" ID="ID_1730422358" CREATED="1329410868042" MODIFIED="1329410869388">
<node TEXT="parallelization" ID="ID_393822830" CREATED="1329410869389" MODIFIED="1329762832030">
<font NAME="SansSerif" SIZE="15"/>
</node>
<node TEXT="role of dt" ID="ID_1524725342" CREATED="1329758840603" MODIFIED="1329758843415">
<node TEXT="slides from Rob" ID="ID_1449188683" CREATED="1329758843738" MODIFIED="1329759425917" LINK="https://mail.google.com/mail/?shva=1#sent/1359bcd4cca8d23c"/>
</node>
</node>
</node>
<node TEXT="parallelization" ID="ID_966733301" CREATED="1329409090586" MODIFIED="1329409093886">
<node TEXT="in general" ID="ID_714987274" CREATED="1329410878018" MODIFIED="1329410882654"/>
<node TEXT="in python" ID="ID_51192086" CREATED="1329410882970" MODIFIED="1329762927598">
<icon BUILTIN="ksmiletris"/>
<node TEXT="pycl" ID="ID_1032708725" CREATED="1329762900874" MODIFIED="1329762903616"/>
<node TEXT="mp" ID="ID_1102966986" CREATED="1329762904010" MODIFIED="1329762905520"/>
<node TEXT="pp" ID="ID_536234036" CREATED="1329762905882" MODIFIED="1329762906864"/>
<node TEXT="issues" ID="ID_1629480917" CREATED="1329762907666" MODIFIED="1329762909048"/>
</node>
<node TEXT="pysal" ID="ID_1849788006" CREATED="1329410950296" MODIFIED="1329410951389">
<node TEXT="broad set of spatial analyical methods" ID="ID_1477874514" CREATED="1329410951873" MODIFIED="1329410961239"/>
<node TEXT="mapping these to forms of parallelization" ID="ID_10570977" CREATED="1329410961609" MODIFIED="1329410969015">
<node TEXT="triangle" ID="ID_873798731" CREATED="1329410969416" MODIFIED="1329410974237">
<node TEXT="pysal" ID="ID_1099349793" CREATED="1329410974728" MODIFIED="1329410975797"/>
<node TEXT="parallelization" ID="ID_1186454881" CREATED="1329410976176" MODIFIED="1329410978661"/>
<node TEXT="python parallel options" ID="ID_359971125" CREATED="1329410979015" MODIFIED="1329410987693"/>
</node>
</node>
</node>
</node>
<node TEXT="illustration" ID="ID_409096192" CREATED="1329409102138" MODIFIED="1329409108734">
<node TEXT="plisa" ID="ID_356463041" CREATED="1329410913913" MODIFIED="1329410917230">
<node TEXT="babak" ID="ID_1127110995" CREATED="1329759016132" MODIFIED="1329759355301" LINK="https://mail.google.com/mail/?shva=1#search/yan+plisa/12ec61f814ce542c">
<node TEXT="import pysal import numpy from datetime import datetime import pp  print str(datetime.time(datetime.now())) + &apos; - Starting the program...&apos;  def run(pid, perm_start, perm_stop):     # Step 01: Creating a 5-nearest spatial weights object     in_shp_file = &apos;./C8P20k_epsg2163.shp&apos;     shp = pysal.open(in_shp_file)     pnt_coords = numpy.array([s for s in shp])     shp.close()     w = pysal.knnW(pnt_coords, k=5)     print &apos; - Step 01 completed...&apos;         # Step 02: Reading z values      in_dbf_file = &apos;./C8P20k_epsg2163.dbf&apos;     dbf = pysal.open(in_dbf_file)     z = numpy.array(dbf.by_col(&apos;z&apos;))     dbf.close()     print &apos; - Step 02 completed...&apos;         # Step 03: Computing local Moran Is     lm = pysal.Moran_Local(z, w, &quot;r&quot;, 99)     Is = lm.Is     p_values = lm.p_sim     cluster_type = lm.q     sig_level = 0.05     cluster_type[p_values &lt; sig_level] = 0     print &apos; - Step 03 completed...&apos;          #Step 04: Writing an output csv file     out_file = &apos;./local_moran_&apos; + str(pid) + &apos;.csv&apos;     f = open(out_file, &apos;w&apos;)     f.write(&apos;x,y,I,p_value,cluster\n&apos;)     for i in xrange(len(pnt_coords)):         x, y = tuple(pnt_coords[i])         I, p, c = Is[i], p_values[i], cluster_type[i]         f.write(&apos;%f6,%f6,%f6,%f6,%i\n&apos; % (x,y,I,p,c))     f.close()  ppservers = ()          job_server = pp.Server(ppservers=ppservers)  print &quot;Starting pp with&quot;, job_server.get_ncpus(), &quot;workers&quot;         for i in range(job_server.get_ncpus()):     f = job_server.submit(run, (i, 0, 99), (pysal.Moran_Local, ), modules=(&quot;numpy&quot;, &quot;pysal&quot;, &quot;datetime&quot;));     print &apos;Process &apos; + str(i) + &apos; started...&apos;  job_server.wait(); job_server.print_stats(); " ID="ID_285669155" CREATED="1329759096945" MODIFIED="1329759099398"/>
</node>
<node TEXT="request for slide" ID="ID_430775521" CREATED="1329759341115" MODIFIED="1329759349233" LINK="https://mail.google.com/mail/?shva=1#search/yan+plisa/1359bd4fd9df19eb"/>
</node>
<node TEXT="gpu lisa" ID="ID_1045880028" CREATED="1329410917753" MODIFIED="1329410923054"/>
<node TEXT="fisher jenks" ID="ID_1446380337" CREATED="1329410923625" MODIFIED="1329762940467">
<icon BUILTIN="ksmiletris"/>
<node TEXT="algorithm" ID="ID_1368864221" CREATED="1329411354538" MODIFIED="1329411357119"/>
<node TEXT="sequential implementations" ID="ID_1819237026" CREATED="1329411357626" MODIFIED="1329411364001"/>
<node TEXT="parallel implementations" ID="ID_474052859" CREATED="1329411364362" MODIFIED="1329411368985"/>
<node TEXT="comparison and results" ID="ID_979966051" CREATED="1329411369546" MODIFIED="1329411379350"/>
</node>
</node>
<node TEXT="future directions" ID="ID_1580283090" CREATED="1329409109218" MODIFIED="1329409111845">
<node TEXT="random sampling" ID="ID_938617055" CREATED="1329412574965" MODIFIED="1329412578522"/>
</node>
</node>
<node TEXT="book chapter call" ID="ID_617674810" CREATED="1329827263566" MODIFIED="1329827279110" LINK="../../../../../../../nsf/cyber10/publications/SpringerBook-CyberGIS-WangGoodchild-cfp.pdf">
<node TEXT="extended abstract (1000 words) May 7, 2012" ID="ID_1847540535" CREATED="1329827472247" MODIFIED="1329827504893"/>
<node TEXT="Acceptance Notice June 1, 2012" ID="ID_683816748" CREATED="1329827505401" MODIFIED="1329827529157"/>
<node TEXT="Final Draft August 31, 2012" ID="ID_1848942453" CREATED="1329827529851" MODIFIED="1329827545478"/>
<node TEXT="Publication January 2013" ID="ID_393832269" CREATED="1329827546251" MODIFIED="1329827558685"/>
</node>
<node TEXT="things to add from aag" ID="ID_835812419" CREATED="1330357928342" MODIFIED="1330357933738">
<node TEXT="look if there are particular tails = process that hang multiprocessing" ID="ID_1542480223" CREATED="1330357934147" MODIFIED="1330357953378"/>
<node TEXT="see if chunking can be done more efficiently" ID="ID_553924735" CREATED="1330357953721" MODIFIED="1330357966114"/>
<node TEXT="explore changing the number of processors" ID="ID_7345540" CREATED="1330357968434" MODIFIED="1330358018644"/>
</node>
</node>
<node TEXT="hardware" POSITION="right" ID="ID_661799284" CREATED="1336095222203" MODIFIED="1336095227613">
<node TEXT="sr got a new macpro" ID="ID_1700257172" CREATED="1336095228026" MODIFIED="1336095237020">
<node TEXT="make this a dedicated compute machine" ID="ID_66753785" CREATED="1336095237593" MODIFIED="1336095243041"/>
<node TEXT="add a high end graphics card" ID="ID_493673298" CREATED="1336095245760" MODIFIED="1336095252293"/>
<node TEXT="increase memory" ID="ID_1406587467" CREATED="1336095252720" MODIFIED="1336095259079"/>
<node TEXT="build a mini cluster?" ID="ID_1451045607" CREATED="1336095259520" MODIFIED="1336095264739"/>
</node>
<node TEXT="phil noticed that machine left behind by torrens has good nvidia card" ID="ID_532929761" CREATED="1336095270147" MODIFIED="1336095287579"/>
</node>
<node TEXT="other papers" POSITION="right" ID="ID_1728908725" CREATED="1336095510140" MODIFIED="1336095512071">
<node TEXT="maxp" ID="ID_801500141" CREATED="1336095512710" MODIFIED="1336095518889">
<node TEXT="xing takes lead for his student paper" ID="ID_1580409921" CREATED="1336095519358" MODIFIED="1336095524710">
<node TEXT="started draft by end of may" ID="ID_436436308" CREATED="1336095525387" MODIFIED="1336095537051"/>
<node TEXT="before internship" ID="ID_1250828780" CREATED="1336095537492" MODIFIED="1336095541391"/>
<node TEXT="finish over summer" ID="ID_440582643" CREATED="1336095541872" MODIFIED="1336095546154"/>
</node>
</node>
<node TEXT="distributed" ID="ID_234870389" CREATED="1336095548724" MODIFIED="1336095555750">
<node TEXT="moving over to rob&apos;s cluster" ID="ID_1152534493" CREATED="1336095556182" MODIFIED="1336095562535"/>
</node>
<node TEXT="gpu cluster?" ID="ID_1026935367" CREATED="1336095566007" MODIFIED="1336095572101">
<node TEXT="talk to georgia tech guy about kenyland" ID="ID_1663685363" CREATED="1336669779178" MODIFIED="1336669788691"/>
</node>
<node TEXT="fisher-jenks sampling" ID="ID_1422028249" CREATED="1336767540929" MODIFIED="1336767540930" LINK="../../../../../../papers/sampling/fjsampling/paper/Fisher-jenksSampling.mm"/>
</node>
<node TEXT="meetings" POSITION="right" ID="ID_555874811" CREATED="1336669859869" MODIFIED="1336669896769">
<node TEXT="2012-05-10" ID="ID_229418527" CREATED="1336669961932" MODIFIED="1336669964903">
<node TEXT="who" ID="ID_781207445" CREATED="1336671318049" MODIFIED="1336671319628">
<node TEXT="xk" ID="ID_381127249" CREATED="1336671320281" MODIFIED="1336671322204"/>
<node TEXT="ps" ID="ID_1992209945" CREATED="1336671322761" MODIFIED="1336671323460"/>
<node TEXT="sr" ID="ID_147381817" CREATED="1336671323768" MODIFIED="1336671324515"/>
<node TEXT="rp" ID="ID_1542977114" CREATED="1336671325080" MODIFIED="1336671326027"/>
</node>
<node TEXT="update on parallel paper" ID="ID_628267017" CREATED="1336671327375" MODIFIED="1336671332675">
<node TEXT="sr will add results in" ID="ID_735422709" CREATED="1336671333529" MODIFIED="1336671338859"/>
<node TEXT="opencl now not best" ID="ID_1744452746" CREATED="1336671339336" MODIFIED="1336671344683"/>
<node TEXT="need to test on my home machine" ID="ID_43945922" CREATED="1336671345417" MODIFIED="1336671350440"/>
<node TEXT="compare across hardware" ID="ID_1365935116" CREATED="1336671351161" MODIFIED="1336671355051"/>
</node>
<node TEXT="maxp" ID="ID_757799740" CREATED="1336671356304" MODIFIED="1336671358435">
<node TEXT="xing gave overview of algorithm" ID="ID_295647956" CREATED="1336671358758" MODIFIED="1336671364562"/>
<node TEXT="first stage can be parallelized" ID="ID_868706452" CREATED="1336671365665" MODIFIED="1336671372091">
<node TEXT="generation" ID="ID_1227796403" CREATED="1336671372496" MODIFIED="1336671376059"/>
<node TEXT="compare solutions from different processes on distributed env" ID="ID_103805285" CREATED="1336671376416" MODIFIED="1336671389490">
<node TEXT="map reduce" ID="ID_1939195395" CREATED="1336671389927" MODIFIED="1336671391714"/>
</node>
</node>
<node TEXT="second stage" ID="ID_106660397" CREATED="1336671393238" MODIFIED="1336671395441">
<node TEXT="currently kicking out regions that don&apos;t change in the outter loop" ID="ID_238977894" CREATED="1336671395855" MODIFIED="1336671409594">
<node TEXT="may want to revisit" ID="ID_573822366" CREATED="1336671409982" MODIFIED="1336671412986"/>
</node>
<node TEXT="could parallelize the local swapping streams" ID="ID_518890492" CREATED="1336671414230" MODIFIED="1336671434481"/>
</node>
<node TEXT="options" ID="ID_401623357" CREATED="1336671435958" MODIFIED="1336671437559">
<node TEXT="parallelilze different instances of maxp (embarrasingly parallel)" ID="ID_1120200743" CREATED="1336671438038" MODIFIED="1336671454495"/>
<node TEXT="parallelize the initial feasible solutions" ID="ID_1024801662" CREATED="1336671454934" MODIFIED="1336671492320"/>
<node TEXT="parallelize the swap streams" ID="ID_82402655" CREATED="1336671463117" MODIFIED="1336671473272"/>
<node TEXT="parallelize first and second stages" ID="ID_3737219" CREATED="1336671473821" MODIFIED="1336680517726"/>
</node>
</node>
<node TEXT="distributed paper" ID="ID_1664856702" CREATED="1336671495540" MODIFIED="1336671498431">
<node TEXT="on the cluster hardware" ID="ID_1117879001" CREATED="1336671499220" MODIFIED="1336671502695"/>
<node TEXT="compare" ID="ID_1171462657" CREATED="1336671503299" MODIFIED="1336671546442">
<node TEXT="opencl" ID="ID_1707689373" CREATED="1336671504724" MODIFIED="1336671506215"/>
<node TEXT="multiprocessing" ID="ID_1405539706" CREATED="1336671506844" MODIFIED="1336671512703"/>
<node TEXT="pp" ID="ID_469033711" CREATED="1336671513084" MODIFIED="1336671513822"/>
<node TEXT="all on the cluster gpu" ID="ID_500565033" CREATED="1336671514212" MODIFIED="1336671518005"/>
</node>
<node TEXT="ask shun at gt about the Keeneland gpu cluster" ID="ID_1935184633" CREATED="1336671519748" MODIFIED="1336671952821">
<node TEXT="maybe another paper" ID="ID_1797990637" CREATED="1336671538771" MODIFIED="1336671541172"/>
</node>
</node>
</node>
</node>
</node>
</map>
