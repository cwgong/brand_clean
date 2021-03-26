
from brand_reg_tool import BrandRegTool
import tool
import traceback
traceback.format_exc()

# def __init__(self, standard_brand_file, del_brand_file=None, exchange_brand_file=None, rule_brand_file=None):
#
bReg = BrandRegTool("brand_recall_info.txt", "del_brand_info.txt", "exchange_brand_info.txt", "rule_brand.cfg")

idx = 0
err_lst = []
r_lst = []
with open("../douyin_data.txt","r",encoding="utf-8") as f1:
    for line in f1:
        try:
            line = line.strip()
            if line == "": continue
            lst1 = line.split("\001")
            if len(lst1) != 5:
                print(lst1)
                continue

            idx += 1

            lst1 = [tmp.strip() for tmp in lst1]
            product_id, product_name, brand_word, cat1_id, cat1 = lst1
            '''
            if product_id not in ["3416468988480342466"]:
                #["3430512378675096131"]:
                #['3420540042093967614','3430630092982850935', '3429622676191327009', '3404061549483132357', '3431098226802049044', '3430532274658141732', '3430162766265223134', '3427225824267505184', '3431448580613892761', '3428720073454567789', '3431693217630920222', '3427554312073687200', '3430328180395910029', '3429621468214990761']:
    
                #['3427554312073687200', '3427225824267505184']:
                #['3430162766265223134', '3427554312073687200', '3427225824267505184', '3430328180395910029']:
                #['3420540042093967614','3430630092982850935', '3429622676191327009', '3404061549483132357', '3431098226802049044', '3430532274658141732', '3430162766265223134', '3427225824267505184', '3431448580613892761', '3428720073454567789', '3431693217630920222', '3427554312073687200', '3430328180395910029', '3429621468214990761']:
                continue
            '''

            '''
            flag = False
            if "转接头" in product_name:
                ok = 1
                flag = True
            
            if cat1 == "生鲜" and "苹果" in product_name:
                ok = 2
                flag = True
            
            if flag == False: continue
            '''
            #if product_id not in ["3431813551977835032", "3434084541613109981", "3400284318290021202", "3428544113082017102"]: continue
            #if product_id not in ["3400471044862127146"]: continue
            #if product_id not in ["3436340101679086536", "3432625045128778267", "3424086933435992400", "3434855073778387047", "3436340101679086536"]: continue
            #if product_id not in ['3432742510454288500', '3436868129337275480', '3436867686989178116']: continue
            #if product_id not in ['3355592858823480484', "3411798860086001815", "3423538998570802670", "3422411309952710608", "3418828334392561031"]: continue
            #if product_id not in ["3355592858823480484", "3422411309952710608"]: continue
            #if  product_id not in ["3418828334392561031"]: continue

            #if not product_id in ["3434101983466937016", "3425415609368885164", "3354685409459341232", "3426111097860667817"]: continue
            #if not product_id in ["3401616162600130251", "3403150395785271393"]: continue
            #if not product_id in ["3355592858823480484"]: continue
            #if not product_id in ["3357085538191592175"]: continue
            #if not product_id in ["3357085538191592175"]: continue
            #if not product_id in ["3423645268946595861"]: continue
            #if not product_id in ["3425211641489445438"]: continue
            #if not product_id in ["3384173514230777960"]: continue
            #if not product_id in ["3416648243235438963", "3415864514741168743","3421897522199802328"]: continue
            #if not product_id in ["3410543769668440301"]: continue
            #if not product_id in ["3369894145832411458"]: continue
            #if not product_id in ["3411824198245607566","3419769275710372814","3386404760302309717","3405190000600595627"]: continue
            #if not product_id in ["3431124812649647120"]: continue
            #if not product_id in ["3387292659109519153"]: continue
            #if not product_id in ["3422982723139202889","3413488532390605772","3413320736608270373","3411621218049227867", \
            #                      "3406644899288878464", "3406652086916644253", "3357449486631852237", "3335530570338930486"]: continue

            #if not product_id in ["3406652086916644253","3426119120834405366", "3439916115256551356"]: continue
            #if not product_id in ["3403154995695201307", "3432747672921060805", "3428673070716598496"]: continue
            #if not product_id in ["3428673070716598496"]: continue
            #if not product_id in ["3426338026752718371","3429242762678128160", "3426479986016664307"]: continue
            #if not product_id in ["3421462080472118360", "3422028681793655131", "3432809430239046014"]: continue
            #if not product_id in ['3424420989549853529','3411470013725554286','3428487241272543721']: continue
            #if not product_id in ['3436183522203855290']: continue
            #if not product_id in ["3428672918245219245", "3362265244507489411", "3410191786361363072", "3434095375659760539"]: continue
            #if product_id not in ["3436468699433974384", "3436466895673531644", "3416966128797393478"]: continue
            # 3424397096529326919, 3436263342140993605
            #if product_id not in ["3402370457641553915", "3404610871496934818", "3428881596437124874", "3428920805193557904"]: continue
            #if product_id not in ['3423892227301234703', '3427763444793893865', '3414494108830584464']: continue
            #if product_id not in ['3427763444793893865']: continue
            #if product_id not in ['3433127554154940773', '3437234251769206601', '3430784172820714938']: continue
            #if product_id not in ["3430563441088331398", "3438910448597088145", "3439075478487596833", "3429425470184269665", "3438319907765406722"]: continue
            #if product_id not in ["3416639799329698434", "3412575954961329774","3424608896516508143"]: continue
            # , '3426092167767142874'
            #if product_id not in ['3428887287268797774']: continue
            #if product_id not in ['3405572190379349468']: continue
            #if product_id not in ['3437618367790475775']: continue
            #if product_id not in ['3440634871582745367']: continue
            #if product_id not in ["3429238866731774171"]: continue
            #if product_id not in ['3438953329433176688']: continue
            #if product_id not in ['3432952349587588647', '3433740841158611445', '3431638171190989599']: continue
            #if product_id not in ['3428881596437124874']: continue
            #if product_id not in ['3428881596437124874']: continue
            #if product_id not in ['3441826054807927445', '3442840691447871683']: continue
            #if product_id not in ['3440384032548979330']: continue
            #if product_id not in ['3424959619133473558']: continue
            #if product_id not in ["3357822597537647801","3358532770371601788"]: continue
            #if product_id not in ['3424455613311237097']: continue
            #if product_id not in ['3439050979910239656']: continue
            #if product_id not in ['3437107475004923216']: continue
            #if product_id not in ['3428902753563498418', '3431848201643237653']: continue
            #if product_id not in ['3430423402069020499', '3411631702064428611', '3424437956700685219']: continue
            #if product_id not in ['3436708788206465508', '3437419920965657389', '3427246350033630127', '3430960113974937748']: continue
            #if product_id not in ['3422415789603574805', '3434491393169593291']: continue
            #if product_id not in ['3437816449425644426', '3414438832601481898','3437647891395697844']: continue
            #if product_id not in ['3443204155395712887', '3437797195104012647', '3443562735579839684']: continue
            #if product_id not in ['3442635987057016816', '3433881703310056899', '3442599881313769465', '3433542658482637940']: continue
            #欧莱雅
            # if product_id not in ['3432438564116398463','3432833046225811113','3432834362540978803','3434283866851027682','3419992457243408647','3424513874685250253','3428893446251907671','3430023044536603436','3430029141142060908','3430034937208821558','3430036376014465289','3432804475977513344','3432928460945921397','3432930604260393110']: continue
            # 华为
            # if product_id not in ['3424649106000334259', '3433944016717227017', '3435554983788061479', '3437073991431526603', '3434646170998319124', '3424636130786713955', '3437373043545104752', '3436569070663821265', '3427551408558323088', '3330738832093135104', '3435707912650131812', '3427573151830308119', '3425734115696185216', '3433728237669380022', '3418851733374407528', '3417336816687257917', '3430936740729358133', '3420358369129704588', '3423876692664526612', '3433891190876066403', '3418153384459567341', '3426876757242969366', '3431847044057312144', '3425754293427416655', '3433105065848753216', '3424652713798069575', '3413891329455963456', '3426871371353995061', '3439305220574856604', '3409402674142411900', '3425143201210721121', '3419614723459688465', '3424074248250075457', '3440965708442420712', '3407133647239813656', '3432030436971399278', '3405136500340471476', '3432218358995659341', '3432218069177652686', '3409182928608345853', '3416408403671699786', '3423680889400516635', '3437641466124628726', '3440004481960536018', '3420388092568285193', '3432407496562723102', '3419050345547042843', '3432403652466317623', '3433949185760748246', '3427557891928904989', '3434241999417515403', '3416292089514876929', '3435592036571597546', '3435201233202360968', '3426125273400244440', '3420329779679858791', '3439635387537032117', '3409456777845442484', '3419592256603179276', '3433105089353656363', '3413883113225455318', '3418854501480830953', '3419220342500127566', '3438697046687781304', '3424626812997769778', '3427232455814421465', '3428690043185796908', '3439251166070973383', '3420323066646004035', '3428846897538945827', '3440438857781384128', '3416108529055073724', '3438171368536075548', '3420549460957250587', '3440369189016195765', '3420364184632835919', '3431874828225886885', '3418844502679500804', '3422021988204590412', '3433898462247276877', '3279700062028090004', '3439611344184307272', '3438366783113946165', '3424640215443208745', '3437970525060787230', '3361726668493432671', '3427567933587623647', '3419247115061344837', '3432657446479500661', '3439650329711499725', '3432969190145978325', '3412388488228791128', '3422022162150759037', '3420184236123134819', '3420351473677135001', '3439104551028920413', '3428847464449491818']: continue

            if product_id not in ['3439305220574856604']: continue

            # 错误数据修改检查
            #if product_id not in['3428324266330949292', '3436468699433974384', '3436479902847755010', '3433672641364501589', '3428286026349728666', '3436466895673531644', '3436641213170719204', '3420552448081802724', '3420548868109131775', '3429083984204857258', '3420550818141762938', '3436479872833340115', '3420543467187741997', '3434033693537265765', '3425252769978829443', '3439056047954896445', '3425247908193292203', '3420548599673707932', '3428524186581239150', '3430340630423939156', '3429491091244759599', '3428526791336323169', '3416641100662839276', '3425213196267606198', '3416800630780653509', '3439056082339811925', '3423096413045843787', '3439056333578585891', '3429587259874275151', '3429792604391395409', '3416966128797393478', '3414078961586676361', '3430921012156491974', '3423666217792193103', '3439099519474781724', '3425220798242285876', '3439100462312348858', '3439093203716988219', '3428473918283985381', '3434259696863823807', '3433901387153590762', '3434221798072399812', '3427763444793893865', '3423892227301234703', '3425875634608569733', '3423891996874547341', '3410161545471459561', '3429646863282902254', '3397878632616736113', '3436858074827215280', '3397871423421865794', '3353202531273689108', '3420124802365706195', '3353209774736025490', '3353213071123466902', '3353208393912460611', '3353216807669487792', '3353214254386970114', '3432924241266358144', '3423698556605828457', '3414630364478622121', '3308157949050021354', '3426479745498483991', '3427019610002699593', '3432261534171192101', '3423288554732788101', '3428503284980307387', '3435543157704669546', '3437044021049072987', '3435705430150664909', '3436480119877803561', '3438175416458823049', '3436553310281310259', '3424027628410144240', '3424113727614650869', '3424113229373249000', '3424108584391337712', '3438764241467875323', '3438763696074189359', '3436267388000150042', '3422366844013649477', '3423645268946595861', '3427586796941395013', '3407322862066004272', '3413094915817769512', '3404541318771424396', '3404543485607563746', '3427790051210306712', '3430787271161473220', '3430599907516500484', '3426472632269314703', '3436531985709967985', '3405120529496181589', '3417216890421001137', '3435233460405539048', '3420720482259972699', '3404803084168354977', '3402370796918844468', '3414071045961950125', '3419389972116040126', '3420156374670258855', '3404610871496934818', '3402370457641553915', '3417149858866453184', '3420189583357424565', '3423285941387829795', '3420153063250481238', '3420157119964549014', '3417028646341370761', '3428527613939980345', '3426467792487114953', '3426467811822843466', '3426562518250820848', '3427541674132388666', '3427570669481788654', '3428332654519556467', '3427433181136160336', '3427435659189742291', '3427418732841066058', '3427430271270669522', '3427539423594683051', '3434087056433937235', '3427413744236534977', '3427428085014917103', '3427414059941817613', '3427412223843251850', '3427433494668781425', '3427427168156802347', '3427422347056000422', '3427434250440467146', '3427411712716998795', '3427429171784198407', '3428511677346369201', '3424040210516827396', '3428514909451858657', '3423891250431027413', '3423872554320960751', '3427428480294512048', '3428513745373131206', '3424269125948709751', '3424093000077317705', '3431151053280820711', '3427418011311734830', '3428513146342637172', '3428513425540656294', '3424255899479502592', '3423908520494538635', '3421817807606793688', '3423934026157836659', '3429088852550221987', '3423922629462079838', '3421808702418735743', '3423908271268979381', '3421702348265914756', '3429080309868670429', '3421708631803046202', '3423952410647879565', '3409416373007706153', '3409418312185475036', '3413558553284330328', '3437961164070472057', '3413540658303105511', '3409414878317139899', '3437965444114431666', '3423497507156689817', '3413907553736854483', '3437602789851796280', '3409416048670570604', '3409417008620958266', '3409418831809399539', '3413903499287771194', '3413904699689172311', '3423494760525136093', '3409419143194496704', '3419398179798537715', '3418471787523144240', '3423496377605472792', '3409415649238586321', '3413908844374536846', '3413906527239692530', '3413915593915657669', '3420523240181913923', '3423497202096589084', '3438489318337961877', '3409417459567349635', '3413909542264784461', '3432245206844633330', '3423494496384633296', '3417337802340360860', '3423496783337270126', '3438689627215636159', '3438410973847906415', '3397500561678034929', '3424415120502186314', '3429445968142142757', '3419241662600378103', '3390471351520358645', '3390816651875381307', '3428871097507018510', '3434106699475202685', '3436533229170127389', '3436618842992946276', '3424257600286522570', '3424385032108770286', '3427583929287334694', '3432649597376457551', '3433938839184494517', '3424261139457017851', '3432646777688466617', '3433749499812675700', '3434088175163816981', '3436581440186369155', '3432658354873491293', '3426646900567340708', '3424397968525140863', '3434106489013423645', '3424417860666156403', '3424248074166504224', '3433932828453301310', '3433743018816053476', '3433755553569050363', '3427583334434374754', '3427587258541313979', '3424252794335527969', '3427585705902223023', '3431471863606463777', '3432842314706501279', '3433857004974798920', '3431500629158312901', '3424416265110974894', '3426104288190058467', '3424398554670753907', '3433748335968796144', '3431070073761177780', '3432658561023490390', '3427587142577204586', '3433577112693512713', '3432854982678942884', '3424247605897612180', '3424394461684337580', '3427584459715795962', '3424257031345988584', '3431499493156248293', '3424262043547628963', '3427585825515413087', '3430934614762458133', '3424415401822580923', '3427587348962106320', '3431488498123865887', '3424985479131597686', '3426155771820408495', '3426517406036702501', '3426520021696930953', '3426515385279734613', '3423679164828532640', '3426532889393765509', '3426538805736386596', '3426519023091870991', '3426519564282951464', '3417953936915727287', '3415115599146286917', '3412984685482133258', '3413065613445307790', '3431663844458668036', '3434678142592243481', '3412988102128611273', '3432434518349482467', '3424693172364786510', '3424691965504139964', '3425402314297601264', '3434678155611353578', '3439655354831666943', '3422980403714219787', '3422988998086373841', '3422981995142186214', '3422984958644454629', '3423551855555433655', '3436646809588655059', '3435408482579411678', '3435407812447043665', '3435404906901682198', '3409606670056574040', '3436311952580829071', '3421450390451960834', '3432777673276057594', '3425389566977268035', '3426842352407463969', '3433096658425149139', '3423336916181989992', '3435557245088364655', '3424615319665278137', '3422954885166009335', '3437837535760527192', '3422169934912949940', '3401777185227433274', '3432780512207451396', '3391085422338787617', '3385473018812826954', '3427574365301120550', '3388821925164918022', '3420765441952477720', '3381977883823181673', '3422569152123172644', '3432975390048714065', '3385663004417861231', '3431713809851640349', '3414793261850693402', '3402714037820209679', '3425143836723273077', '3435545466190878696', '3401659331291313950', '3436620769319386585', '3423338563184535534', '3434893640428845050', '3423947001254028570', '3420866171703056408', '3422086599687723075', '3403480079597193469', '3386228039754096387', '3382139316737324640', '3420580635977344506', '3414494108830584464', '3392896451116977405', '3424848351680714902', '3425261035760821616', '3401843140884331826', '3414252549090484535', '3432930544030248982', '3427225532209712071', '3422579329048137679', '3428888245046540500', '3413695305043018499', '3420439898346412016', '3431688188241023999', '3416246805485213998', '3418900405973874375', '3384741469918218947', '3385260772266491466', '3386023455253250982', '3436113703207061599', '3429244452764529065', '3425349282188939174', '3425140566223120567', '3425239758517983087', '3436128106379875884', '3425137817326626251', '3437787724818578702', '3425158089689711899', '3425162120516523184', '3426438524692478171', '3425182388467186630', '3426460252932075832', '3425186174363383479', '3423660325097095972', '3425344985074126581', '3429245118501271518', '3425253167380709661', '3425252164388452705', '3425235150018117430', '3426680526772305907', '3426681042025754871', '3436101593546777433', '3425145698709051848', '3425152355933488555', '3425216726730689447', '3426457124048366511', '3425238416198109669', '3429243286664150297', '3425146242047571152', '3425151690213600236', '3436091367238047918', '3437787273813465827', '3436103438277163193', '3425242696250459860', '3429244978923191227', '3425214896957176186', '3425237434798076822', '3424990132871245817', '3425157756829718140', '3426456514137867515', '3425189582537400362', '3425142378581887058', '3425311643360462658', '3425146396641212102', '3437776484754976597', '3425216080363281601', '3425159762604632118', '3437747992050969560', '3425137454519306670', '3432942439059573696', '3344850750386872658', '3414403886600033185', '3380454089681987262', '3405275401721928535', '3420052058622059693', '3420050102146994887', '3422204681080977263', '3417204971886800011', '3435381074170105196', '3422407757989557624', '3418266290559815476', '3423469830269992629', '3415684373075335293', '3419217149074511430', '3414933825434872295', '3420730500128589204', '3415692262972260274', '3417203094986095806', '3400362992049722105', '3422205604641510461', '3422764051179165866', '3419203967937288038', '3419942440201798676', '3406776441260628275', '3427619574101758973', '3417007276731544756', '3419204777421201156', '3433479507422667067', '3419234281816480688', '3419237477272126459', '3434089910422879392', '3419417601640693573', '3408831613210129789', '3429950280819679652', '3420165681864385336', '3430517773145610811', '3422206564566741114', '3436508266929199244', '3404165743208738134', '3406775895791434287', '3408810728889652941', '3406837034625697304', '3420737576087254515', '3433305396008328850', '3404030722347015685', '3419962023105161847', '3415690897130685654', '3414399050424959677', '3414767084025035026', '3406776821356835166', '3427806924752724412', '3438148027477552923', '3423099256314164073', '3430921377656505658', '3416347550427520611', '3432254647165948463', '3423689015453481779', '3433924079529402240', '3419948272884805884', '3435382296138668691', '3419971046948903460', '3420591755622529083', '3411838193354558170', '3423393049257060964', '3410529645710439299', '3423505233828015528', '3419935800299771381', '3383610461198110716', '3410667935025503860', '3411832197622179888', '3423505470026062367', '3435182163463698976', '3421075506261574428', '3406987856722422173', '3428913014265482518', '3416346783733945553', '3417343926963702282', '3428299894799112640', '3420061307716674380', '3384547410410920403', '3426654024676592244', '3412558208114532625', '3414408434928464594', '3422066741906427060', '3420593808642027304', '3412555620396728993', '3434981698046167246', '3434240446904297319', '3425347807010262919', '3420493409486538358', '3423393768664084359', '3416995925132972961', '3383435537917551321', '3422779760164656575', '3423387225281454875', '3433713370640062735', '3436339365125689185', '3436262607584106678', '3436263342140993605', '3415775806528604375', '3415777131526021510', '3408299395828030912', '3424397096529326919', '3436304936726563790', '3429247448520994467', '3411822422276607257', '3436507487275251285', '3436339588413664476', '3431481656232573555', '3435408022900498096', '3418314873082392516', '3434818480589943064', '3424615955177847854', '3424849897751448753', '3424617054689440509', '3411090735943026441', '3423117720403732279', '3415955608892004807', '3426655961706838716', '3417393379259062449', '3418307760616557597', '3426114503769729871', '3429412746746281869', '3431301978322564721', '3424955788022645146', '3425189642549496293', '3424955242679272202', '3414598235975721034', '3422363244948515710', '3419648990973709278', '3426491575985908290', '3425193675523778317', '3424624274529514211', '3428891706907583862', '3430175116443663082', '3423136102838618621', '3431129005007444104', '3425190688491445480', '3422738410341857728', '3414174969096198410', '3428132195628410558', '3417762907465864783', '3428135365339416821', '3419074644324537909', '3423308689656947248', '3429432037625493602', '3419933560356892953', '3420695657206430729', '3414171554639181129', '3434094323443065515', '3415561661564738640', '3414173794422660195', '3414177077967069138', '3430034202769366719', '3424262185306731998', '3422029865174565408', '3439471560296129800', '3422960105698806033', '3420895860807099399', '3418325125169287477', '3420715472155459933', '3435398318522507080', '3421974949722722000', '3435241635984869764', '3427015364570162790', '3420135715994998118', '3417768574675245273', '3423538088037718752', '3413460396101794486', '3435753042027361762', '3436500907511175286', '3425965313643156544', '3426519284204107607', '3417032574046996908', '3436115127089382908', '3415688141909180425', '3435753052773198485', '3417027100153116725', '3431331626532133400', '3438162731172246768', '3417384744185423887', '3424474908594418196', '3435240366796865131', '3435004306754024059', '3428115140313249889', '3433144029775319634', '3429285562069216456', '3436173450589394232', '3429022205193908607', '3437599259497786191', '3436498248741865895', '3436486841417760025', '3436486506368370469', '3436630548876010816', '3436486057535912241', '3436505187437674069', '3436487161392804778', '3436503675617576383', '3438743863987166586', '3436505133574424956', '3436486646047095945', '3436485862114877286', '3436499904518819936', '3436492117743152494', '3436492792145251438', '3438740144537117352', '3436492553791391700', '3415496410316071553', '3431261893401129383', '3357830341363659230', '3435422198448394637', '3418325966940975457', '3414229875958108077', '3421711974554332305', '3413465111933912787', '3415478191022864081', '3404541318771424396', '3429076171457966149', '3434820696977586768', '3429122703301417428', '3428887287268797774', '3428921593437500404', '3423507533757819344', '3428923412238697837', '3428914749407117536', '3428897749809119457', '3428901795785761038', '3433529320545620358', '3390087727205723453', '3429256598957224027', '3428891185069055213', '3428881596437124874', '3428873522041248138', '3432639012387570550', '3414195907061775367', '3428920805193557904', '3429411565454127233', '3412422966036802596', '3429397001421382257', '3429407272877600729', '3425334260683389284', '3357275616264194311', '3431848201643237653', '3428917395132183813', '3416293504706562658', '3429085528245597901', '3433211716203325709', '3437293290196710704', '3422045947822253203', '3404899675835350410', '3434116421125330198', '3415112483189476592', '3431529283024198777', '3414949001701772041', '3438187045082769153', '3428923770868484750', '3438190977116935814', '3411860705467575106', '3384344045907231341', '3427609508845891094', '3420591386137888117', '3426711916515610409', '3424109103939737171', '3430910077605966852', '3430915794240935585', '3436497252368126595', '3437264930544459086', '3428923753688635446', '3404541318771424396', '3424085419342597172', '3419055615354535947', '3414601483012982183', '3430343906435435105', '3433721329046700734', '3373394643004867674', '3423329756496720722', '3422198359031701054', '3414767556513419029', '3424612242321188402', '3425907677446970229', '3432562267697351692', '3423858299441925951', '3427554634221381022', '3422545581367792670', '3426270134057227030', '3422226521132238414', '3423868678112967390', '3414592023305521378', '3415717341286241026', '3422546775226058539', '3422666705887980520', '3424821952546736067', '3424187375423720631', '3416448971743312731', '3422547722409013904', '3424652990798264248', '3425781214282415038', '3432556555466351923', '3427741802311099212', '3431263937847528820', '3429227983712463688', '3413449248472187365', '3429846351679200695', '3433882143535799483', '3430983558053938634', '3417267525937984401', '3413164081971080691', '3414826122645496808', '3418669092037617923', '3419612191576448834', '3418706063116118967', '3435533227748659463', '3430143870455963301', '3418688524617186399', '3432410107911265445', '3418137619740138363', '3415675626416424644', '3414822804783260496', '3414820019538894030', '3432950361000907924', '3349435028819040477', '3414828291645928194', '3430318519932316973', '3421143033884866451', '3431120001631967920', '3432056889716948176', '3431124318719989423', '3421145252378098902', '3421787914751837456', '3421676971476823775', '3430355633390664104', '3431119952894155049', '3432072304337778910', '3432050376491305658', '3421687360860113600', '3421679466852796529', '3421677263509390590', '3430355657021361381', '3431120182666493470', '3432055032235883578', '3421679022181058943', '3431879292735362790', '3402498393988331062', '3382143003966717054', '3438029338170259206', '3423129589520700650', '3427484722631194501', '3435949356409303017', '3350957719296278787', '3361865808228820467', '3435949231830093985', '3423511815865396229', '3436687966230213804', '3436687961801007222', '3433179201203734402', '3437793138624885851', '3434967470967023585', '3434968903397324831', '3422753599518859339', '3424441777074132393', '3422731890581488052', '3424819897547519091', '3416794690840861151', '3426855679833597851', '3415918324238915868', '3422768303339389960', '3422753245041437504', '3424819083651220433', '3422754499171896020', '3416837571836303368', '3416822827213522021', '3422734248518520431', '3422732382380365962', '3424817520140538441', '3419602944629317739', '3422730264936351700', '3422764875930312574', '3415919720145275563', '3428203534917727406', '3422740304422411586', '3422766995379203217', '3424822278964303815', '3422742200650446585', '3426854599506720450', '3416831058476449605', '3422737766096759517', '3415918672173223905', '3416828021976517252', '3419601540057555710', '3422747163485162329', '3435949991930233033', '3427370227627865926', '3426853845857388959', '3422740892715470180', '3415915588386742486', '3422745939419524783', '3426858301911093643', '3428099238196831768', '3426857382645465683', '3425053599577836459', '3416790902721627662', '3419599326001954709', '3425058238167647585', '3416836442217938156', '3415915884697485694', '3422765346254377378', '3418153335067392283', '3425059743411110626', '3416302749581710319', '3416303331591765572', '3416302341559821270', '3416303149013690112', '3416302150475719071', '3416301602867381733', '3416302932159779310', '3430139384345824767', '3436924756341985066', '3425183913205758898', '3436922211573858383', '3415980747293600201', '3418499290388111916', '3436084707891276558', '3404541318771424396', '3433750824843646762', '3436320392158035582', '3425000825049736678', '3436508294729045413', '3427399353831178328', '3438957074627874593', '3436321465815980501', '3432816272121962060', '3428739740109771919', '3429657768255173325', '3433868455466649900', '3436505631849366377', '3436684790076722274', '3433737377384927597', '3436719063940889897', '3432823829225962529', '3433755147786922048', '3433866153263542906', '3436510150171724158', '3432976695643212653', '3438946680932812610', '3433765356831933100', '3429691140109169970', '3436513478762958127', '3432979790125226196', '3436708476846496622', '3436718829865181499', '3432826352393429605', '3433774116535164913', '3436512533970852925', '3436698789547759590', '3431525020319543239', '3433749405306594495', '3433870585711746777', '3431546407167885836', '3436687768577793273', '3436311213821266035', '3436505223844223165', '3431523830588439236', '3438958756233384281', '3433865648596505322', '3417234392412724626', '3436507863210693596', '3436321171702974117', '3433870998078923420', '3425959902126942504', '3438918677746053834', '3433749867015573664', '3433910679231431963', '3436499067092481247', '3413664411343268425', '3416265237379337548', '3408984992934659966', '3403990330327086120', '3426473217148243583', '3400107939737028281', '3413682437321012785', '3422011306763485943', '3413298890257082183', '3404393876872644783', '3414563663636497278', '3407170521681536045', '3412559419295288843', '3412742724204524433', '3382514284612434853', '3412049458500909194', '3411797627430430245', '3411301801331438887', '3380121319961168891', '3413663047691175210', '3422380965983586552', '3400138240739688302', '3417758251763262943', '3412371407143878127', '3419608721242856401', '3412380385772977440', '3412361470695082040', '3380658381948908674', '3410313991065834753', '3405312815156846064', '3411454652775033948', '3416065693198743544', '3411815380677727409', '3404404633618254038', '3409405130863705994', '3405320954119907417', '3415740115350360004', '3404965470439373292', '3415516023242281016', '3433660164526457824', '3433660372782056747', '3404836247766755551', '3413293257449466551', '3437764461094679156', '3413205034526211358', '3412774919321353745', '3411426634555898352', '3407875495507936048', '3408246599967705637', '3413083162639789808', '3427017230733418527', '3430228268710785985', '3427049713571094175', '3427179357133756473', '3436891676403223112', '3436118857176248272', '3430208741625224641', '3419428238244582356', '3417898587630263376', '3429411118542677865', '3438548294865972274', '3414593698342814802', '3422413251135295170', '3438676012093858618', '3409550831211958178', '3438535652436767143', '3417391326222797010', '3419812906253056414', '3433887366199256271', '3435936915952678900', '3432005070961686946', '3405469673830107874', '3424458967798160155', '3430394073759015694', '3428672918245219245', '3429770787693934882', '3418116101953951792', '3423521468661778936', '3439849193148136034', '3436172576588716852', '3436172514194248502', '3436172518606652637', '3436171741217572799', '3435533654988849107', '3435533442497014492', '3436151290714023397', '3435533324209248864', '3435533330710423106', '3435533706645890093', '3435534219768670429', '3435533917107672800', '3436175009670935053', '3435533483307588647', '3433001078130642628', '3435533813835536599', '3435533371453899923', '3435534063119812474', '3435534078160536488', '3435533304940609401', '3435533421022161981', '3437203815407999266', '3437100665317532605', '3435533932005851007', '3435533519630293265', '3435533446791956492', '3435533584214153781', '3435534090936442917', '3435533766783813225', '3432996018650794287', '3437224021073247909', '3435534071642635033', '3435534254245863383', '3437249988277747154', '3437103910249183542', '3435533377963447078', '3436826839509815131', '3436826798875399269', '3437098878502067591', '3435533453058304747', '3435533365120505783', '3435533427397509095', '3437105366167630646', '3437098910848536546', '3435533895439904598', '3435533966474662392', '3436831890466831524', '3436830054485757270', '3433010140486466759', '3437101331045833751']: continue

            '''
            if idx > 100: break
            #print(bReg.brand_recognition(product_name, brand_word))
            p_name = tool.s_name_dealing(product_name)
            b_name = tool.s_name_dealing(brand_word)
            print(bReg.brand_recognition("%s %s") % (p_name, b_name))
            '''
            #if idx >= 100: break
            pre_brand_id, pre_brand, match_type, \
            b_cat1_id, b_cat1_name, cat1_id, \
            cat1_name = bReg.brand_recognition(line)
            if pre_brand != None and match_type != None:
                s1 = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ('', pre_brand, product_name, brand_word, cat1_id, cat1, \
                                                                  pre_brand_id, product_id, b_cat1_id, b_cat1_name, match_type)
                r_lst.append((pre_brand, s1))
            else:
                s1 = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ('', '',  product_name, brand_word, cat1_id, cat1, \
                                                                  '', product_id, '', '','')
                r_lst.append(('', s1))
                #err_lst.append(product_id)
                #print("error", lst1)
        except Exception as e:
            print(traceback.format_exc())
    #print(err_lst)


#a = bReg.english_brand_recognition("vero moda".lower(), "Vero Moda2020春季新款棉收腰宽摆风衣外套女 320121527 VERO MODA".lower())
#print(a)

lst9 = sorted(r_lst, key= lambda x: x[0], reverse=True)
for tmp in lst9:
    print(tmp[1])