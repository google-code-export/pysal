<map version="0.9.0">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node CREATED="1329408682020" ID="ID_1481318209" LINK="../../../../../../../nsf/cyber10/cyber%20infrastructure%20nsf.mm" MODIFIED="1329413769265" TEXT="parallell pysal">
<node CREATED="1329408686020" MODIFIED="1329408690408" POSITION="left" TEXT="plisa implementation"/>
<node CREATED="1329408690900" MODIFIED="1329408696456" POSITION="left" TEXT="fisher jenks optimization">
<node CREATED="1329409285132" MODIFIED="1329409298384" TEXT="original implementation"/>
<node CREATED="1329409298877" MODIFIED="1329409314785" TEXT="other implementation"/>
<node CREATED="1329409316261" MODIFIED="1329409326196" TEXT="parallel implementations">
<node CREATED="1329409326701" MODIFIED="1329409332113" TEXT="multiprocessing">
<node CREATED="1329409371046" LINK="https://mail.google.com/mail/?shva=1#search/xing/13563fbf742a8e4b" MODIFIED="1329409376601" TEXT="xing&apos;s note">
<node CREATED="1329412503382" MODIFIED="1329412514348" TEXT="syncrhonised">
<node CREATED="1329412524646" MODIFIED="1329412534709" TEXT="one process updates all others"/>
<node CREATED="1329412552501" MODIFIED="1329412555643" TEXT="correct but slow"/>
</node>
<node CREATED="1329412515263" MODIFIED="1329412520499" TEXT="asyncrhonise">
<node CREATED="1329412536318" MODIFIED="1329412540797" TEXT="no coordination"/>
<node CREATED="1329412541198" MODIFIED="1329412550813" TEXT="results in wrong classification"/>
</node>
</node>
</node>
<node CREATED="1329409332653" MODIFIED="1329409333849" TEXT="pp">
<node CREATED="1329410334451" MODIFIED="1329410338976" TEXT="dependency">
<node CREATED="1329410326993" MODIFIED="1329410333785" TEXT="sudo easy_install pp"/>
</node>
<node CREATED="1329410638931" MODIFIED="1329410640826" TEXT="example">
<node CREATED="1329410641294" MODIFIED="1329410654758" TEXT="filling in a distance matrix">
<node CREATED="1329410657086" MODIFIED="1329410665685" TEXT="compare sequential versus pp"/>
<node CREATED="1329410679710" LINK="../../pysal/src/pysal/branches/parallel/pysal/esda/pptest1.py" MODIFIED="1329410717611" TEXT="pptest1.py"/>
</node>
<node CREATED="1329410747742" MODIFIED="1329410752531" TEXT="speeds things up"/>
<node CREATED="1329410756916" MODIFIED="1329410788561" TEXT="each job determines distances for subsets of ijs"/>
<node CREATED="1329410788931" MODIFIED="1329410793944" TEXT="results returned by job"/>
<node CREATED="1329410794499" MODIFIED="1329410806764" TEXT="outter loop fills in relevant section of distance matrix"/>
<node CREATED="1329410807179" MODIFIED="1329410822379" TEXT="question as to whether matrix could be directly passsed to the individual jobs"/>
<node CREATED="1329410824075" MODIFIED="1329410828215" TEXT="issue of shared data"/>
<node CREATED="1329412694003" MODIFIED="1329412699288" TEXT="need to consider load balancing">
<node CREATED="1329412700026" MODIFIED="1329412705353" TEXT="currently doing dij 2x"/>
</node>
</node>
</node>
<node CREATED="1329409334261" MODIFIED="1329410839200" TEXT="pyopencl"/>
</node>
<node CREATED="1329411332466" ID="ID_1094534875" MODIFIED="1329411334359" TEXT="todo">
<node CREATED="1329413837000" ID="ID_1847986195" MODIFIED="1329413839997" TEXT="minimum">
<node CREATED="1329413816576" ID="ID_1994966278" MODIFIED="1329413820517" TEXT="implement pp for fj"/>
<node CREATED="1329411335858" ID="ID_1804944538" MODIFIED="1329411343967" TEXT="use same machine to compare all three methods"/>
</node>
<node CREATED="1329413844936" ID="ID_677884127" MODIFIED="1329413847077" TEXT="time permitting">
<node CREATED="1329412445048" ID="ID_1525337724" MODIFIED="1329412451142" TEXT="can pp do shared memory"/>
<node CREATED="1329412451623" ID="ID_1969030895" MODIFIED="1329412455300" TEXT="mp">
<node CREATED="1329412455871" MODIFIED="1329412465524" TEXT="try it with preallocated D"/>
<node CREATED="1329412466391" MODIFIED="1329412471868" TEXT="mimic approach in pp"/>
</node>
</node>
</node>
</node>
<node CREATED="1329408846583" MODIFIED="1329408850017" POSITION="left" TEXT="aag 2012">
<node CREATED="1329408850550" MODIFIED="1329408853778" TEXT="presentation outline">
<node CREATED="1329409094682" MODIFIED="1329409096822" TEXT="project">
<node CREATED="1329410846978" MODIFIED="1329410855839" TEXT="overview"/>
<node CREATED="1329410857082" MODIFIED="1329410860040" TEXT="asu components"/>
</node>
<node CREATED="1329408854471" MODIFIED="1329409090029" TEXT="pysal">
<node CREATED="1329410861570" MODIFIED="1329410863223" TEXT="history"/>
<node CREATED="1329410863594" MODIFIED="1329410867671" TEXT="role in this project"/>
<node CREATED="1329410868042" ID="ID_1730422358" MODIFIED="1329410869388" TEXT="focus">
<node CREATED="1329410869389" ID="ID_393822830" MODIFIED="1329762832030" TEXT="parallelization">
<font NAME="SansSerif" SIZE="15"/>
</node>
<node CREATED="1329758840603" ID="ID_1524725342" MODIFIED="1329758843415" TEXT="role of dt">
<node CREATED="1329758843738" ID="ID_1449188683" LINK="https://mail.google.com/mail/?shva=1#sent/1359bcd4cca8d23c" MODIFIED="1329759425917" TEXT="slides from Rob"/>
</node>
</node>
</node>
<node CREATED="1329409090586" ID="ID_966733301" MODIFIED="1329409093886" TEXT="parallelization">
<node CREATED="1329410878018" MODIFIED="1329410882654" TEXT="in general"/>
<node CREATED="1329410882970" ID="ID_51192086" MODIFIED="1329762927598" TEXT="in python">
<icon BUILTIN="ksmiletris"/>
<node CREATED="1329762900874" ID="ID_1032708725" MODIFIED="1329762903616" TEXT="pycl"/>
<node CREATED="1329762904010" ID="ID_1102966986" MODIFIED="1329762905520" TEXT="mp"/>
<node CREATED="1329762905882" ID="ID_536234036" MODIFIED="1329762906864" TEXT="pp"/>
<node CREATED="1329762907666" ID="ID_1629480917" MODIFIED="1329762909048" TEXT="issues"/>
</node>
<node CREATED="1329410950296" MODIFIED="1329410951389" TEXT="pysal">
<node CREATED="1329410951873" MODIFIED="1329410961239" TEXT="broad set of spatial analyical methods"/>
<node CREATED="1329410961609" MODIFIED="1329410969015" TEXT="mapping these to forms of parallelization">
<node CREATED="1329410969416" MODIFIED="1329410974237" TEXT="triangle">
<node CREATED="1329410974728" MODIFIED="1329410975797" TEXT="pysal"/>
<node CREATED="1329410976176" MODIFIED="1329410978661" TEXT="parallelization"/>
<node CREATED="1329410979015" ID="ID_359971125" MODIFIED="1329410987693" TEXT="python parallel options"/>
</node>
</node>
</node>
</node>
<node CREATED="1329409102138" MODIFIED="1329409108734" TEXT="illustration">
<node CREATED="1329410913913" ID="ID_356463041" MODIFIED="1329410917230" TEXT="plisa">
<node CREATED="1329759016132" FOLDED="true" ID="ID_1127110995" LINK="https://mail.google.com/mail/?shva=1#search/yan+plisa/12ec61f814ce542c" MODIFIED="1329759355301" TEXT="babak">
<node CREATED="1329759096945" ID="ID_285669155" MODIFIED="1329759099398" TEXT="import pysal import numpy from datetime import datetime import pp  print str(datetime.time(datetime.now())) + &apos; - Starting the program...&apos;  def run(pid, perm_start, perm_stop):     # Step 01: Creating a 5-nearest spatial weights object     in_shp_file = &apos;./C8P20k_epsg2163.shp&apos;     shp = pysal.open(in_shp_file)     pnt_coords = numpy.array([s for s in shp])     shp.close()     w = pysal.knnW(pnt_coords, k=5)     print &apos; - Step 01 completed...&apos;         # Step 02: Reading z values      in_dbf_file = &apos;./C8P20k_epsg2163.dbf&apos;     dbf = pysal.open(in_dbf_file)     z = numpy.array(dbf.by_col(&apos;z&apos;))     dbf.close()     print &apos; - Step 02 completed...&apos;         # Step 03: Computing local Moran Is     lm = pysal.Moran_Local(z, w, &quot;r&quot;, 99)     Is = lm.Is     p_values = lm.p_sim     cluster_type = lm.q     sig_level = 0.05     cluster_type[p_values &lt; sig_level] = 0     print &apos; - Step 03 completed...&apos;          #Step 04: Writing an output csv file     out_file = &apos;./local_moran_&apos; + str(pid) + &apos;.csv&apos;     f = open(out_file, &apos;w&apos;)     f.write(&apos;x,y,I,p_value,cluster\n&apos;)     for i in xrange(len(pnt_coords)):         x, y = tuple(pnt_coords[i])         I, p, c = Is[i], p_values[i], cluster_type[i]         f.write(&apos;%f6,%f6,%f6,%f6,%i\n&apos; % (x,y,I,p,c))     f.close()  ppservers = ()          job_server = pp.Server(ppservers=ppservers)  print &quot;Starting pp with&quot;, job_server.get_ncpus(), &quot;workers&quot;         for i in range(job_server.get_ncpus()):     f = job_server.submit(run, (i, 0, 99), (pysal.Moran_Local, ), modules=(&quot;numpy&quot;, &quot;pysal&quot;, &quot;datetime&quot;));     print &apos;Process &apos; + str(i) + &apos; started...&apos;  job_server.wait(); job_server.print_stats(); "/>
</node>
<node CREATED="1329759341115" ID="ID_430775521" LINK="https://mail.google.com/mail/?shva=1#search/yan+plisa/1359bd4fd9df19eb" MODIFIED="1329759349233" TEXT="request for slide"/>
</node>
<node CREATED="1329410917753" ID="ID_1045880028" MODIFIED="1329410923054" TEXT="gpu lisa"/>
<node CREATED="1329410923625" ID="ID_1446380337" MODIFIED="1329762940467" TEXT="fisher jenks">
<icon BUILTIN="ksmiletris"/>
<node CREATED="1329411354538" MODIFIED="1329411357119" TEXT="algorithm"/>
<node CREATED="1329411357626" MODIFIED="1329411364001" TEXT="sequential implementations"/>
<node CREATED="1329411364362" MODIFIED="1329411368985" TEXT="parallel implementations"/>
<node CREATED="1329411369546" MODIFIED="1329411379350" TEXT="comparison and results"/>
</node>
</node>
<node CREATED="1329409109218" MODIFIED="1329409111845" TEXT="future directions">
<node CREATED="1329412574965" ID="ID_938617055" MODIFIED="1329412578522" TEXT="random sampling"/>
</node>
</node>
</node>
</node>
</map>
