//Maya ASCII 2025ff03 scene
//Name: skeleton.ma
//Last modified: Fri, Oct 31, 2025 03:11:06 PM
//Codeset: 1252
requires maya "2025ff03";
requires "stereoCamera" "10.0";
requires "mtoa" "5.5.4.2";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2025";
fileInfo "version" "2025";
fileInfo "cutIdentifier" "202409190603-cbdc5a7e54";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 22631)";
fileInfo "UUID" "F6FF2C8E-4935-9B5F-AAA5-1DA18B0D621A";
createNode joint -n "root_jnt";
	rename -uid "89DBF2A6-4C24-F524-1323-65A5496C31C3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 2;
	setAttr -cb on ".oc";
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -cb on ".ds";
createNode joint -n "pelvis_jnt" -p "root_jnt";
	rename -uid "FB529AA6-4777-15FA-42F9-799162588792";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr ".wfcc" -type "float3" 1 0 1 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 0 140.37987730116546 1.2779054165287134 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 1 1 0.99999999999999956 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -90.000000000000057 -27.377912676520626 90 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 1.1102230246251565e-16 0.88799272457843259 0.45985750085844185 0
		 9.9920072216264089e-16 0.4598575008584419 -0.88799272457843259 0 -0.99999999999999956 5.5511151231257807e-16 -8.8817841970012484e-16 0
		 0 140.37987730116546 1.2779054165287134 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "clavicle_left_jnt" -p "pelvis_jnt";
	rename -uid "2E033AF9-4106-3094-2DD1-F0A738390AA0";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr ".wfcc" -type "float3" 0.60000002 0.2 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 70.659512179767034 -29.5459722706618 -2.5018123929152183 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 0.99999999999999944 1 1.0000000000000002 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 92.392920098956182 57.767821002186075 61.217129881997955 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" 0.84589375367077735 0.44300357589353279 -0.29700435896851546 0
		 -0.53288635493177972 0.72523995236233463 -0.43595773215415834 0 0.022268592867004743 0.52704349274326845 0.84954650639544715 0
		 2.5018123929151952 189.53807307024042 60.007820516336814 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode joint -n "shoulder_left_jnt" -p "clavicle_left_jnt";
	rename -uid "4A6E2A3D-4248-8767-67B2-F98619945A5C";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr ".wfcc" -type "float3" 0.60000002 0.1 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 21.179007552552207 2.8421709430404007e-13 2.8421709430404007e-14 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 0.99999999999999944 1.0000000000000004 0.99999999999999967 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 1.5319806602063053 16.602592160631765 -18.441243077299891 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999933 1 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.9241796701841134 0.032288956260864754 -0.38059080456831862 0
		 -0.22986537011945429 0.84279886555703476 -0.48667441255486238 0 0.30504728951134991 0.53725924423816285 0.78631969048372719 0
		 20.417002590565172 198.92044914989739 53.717562954601597 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "elbow_left_jnt" -p "shoulder_left_jnt";
	rename -uid "65EC69EB-47E8-4F81-C7D0-58B89987660B";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr ".wfcc" -type "float3" 0.60000002 0.1 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 70.992591857908764 -1.9895196601282805e-13 -1.1084466677857563e-12 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 1 1 1.0000000000000002 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -3.46037633993157e-05 -58.05377665595838 4.5013633510966014e-05 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999933 1.0000000000000004 0.99999999999999956 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.74785106991145656 0.47297387793291457 0.46584813837278505 0
		 -0.2298657200482016 0.84279868504844979 -0.48667455987273928 0 -0.62280055232715015 0.25687757253934612 0.7390083793484965 0
		 86.026912719322368 201.21272584324208 26.698435301009059 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wrist_left_jnt" -p "elbow_left_jnt";
	rename -uid "1183053D-49B3-243A-67E9-CDB6611D97C0";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr ".wfcc" -type "float3" 0.60000002 0.1 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 117.22806549072232 5.4001247917767614e-13 3.0624391911260318e-12 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 0.99999999999999944 0.99999999999999967 0.99999999999999989 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.74785106991145611 0.47297387793291429 0.46584813837278477 0
		 -0.22986572004820152 0.84279868504844946 -0.48667455987273911 0 -0.62280055232715004 0.25687757253934607 0.73900837934849639 0
		 173.69604692020732 256.65853858096392 81.308911374906984 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wingFinger_a01_left_jnt" -p "wrist_left_jnt";
	rename -uid "AC3A9FEE-4DCA-7B7E-1076-55808C79E53A";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr ".wfcc" -type "float3" 0.60000002 0.1 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 13.53474810856801 -0.52415511620273492 6.0666641781117718 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 0.99999999999999911 1 0.99999999999999967 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 119.53680831774318 -79.544535190149617 -119.12715889541001 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999933 0.99999999999999956 0.99999999999999978 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.64207925786397957 0.07723150603786616 0.76273817335699279 0
		 -0.33589672132121096 0.86599208645996117 -0.3704471605970035 0 -0.68913541428843417 -0.49405768961108959 -0.53009374652947894 0
		 180.16018626647352 264.17675360550618 92.352457207428927 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wingFinger_a02_left_jnt" -p "wingFinger_a01_left_jnt";
	rename -uid "D1500223-4F90-7346-89CD-46ACD6B6C9C0";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 2;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 30.794042971182034 -2.5579538487363607e-13 -5.6843418860808015e-14 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 1 0.99999999999999978 1 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999911 1 0.99999999999999956 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.64207925786398112 0.07723150603786412 0.76273817335699212 0
		 -0.3358967213212109 0.86599208645996106 -0.37044716059700344 0 -0.68913541428843406 -0.49405768961108909 -0.53009374652947905 0
		 160.38797000890548 266.55502392116495 115.84024929354514 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wingFinger_b01_left_jnt" -p "wrist_left_jnt";
	rename -uid "A76F5ED8-43BE-4623-83DB-F5B4449F778B";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr ".wfcc" -type "float3" 0.60000002 0.1 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 37.109214253763014 -0.8601791401388823 3.9896093547778051 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 0.99999999999999911 1 0.99999999999999967 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 21.908471827860264 -58.515435850896274 -25.248462838695637 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999933 0.99999999999999956 0.99999999999999978 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.12663908732627838 0.25473017694123734 0.95868403476675168 0
		 -0.26472930821695045 0.92273276633183943 -0.28014752418781969 0 -0.95597119984449963 -0.28926938810229919 -0.049419491850683284 0
		 199.16120729115073 274.51011087183002 101.96315179944604 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wingFinger_b02_left_jnt" -p "wingFinger_b01_left_jnt";
	rename -uid "577C349A-482A-3E2E-979B-B6B6FC14BD4C";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 2;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 33.72969491866013 5.1159076974727213e-13 -1.1368683772161603e-13 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 1 0.99999999999999978 1 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999911 1 0.99999999999999956 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.12663908732627835 0.2547301769412374 0.95868403476675157 -8.2120181610850895e-20
		 -0.26472930821695073 0.9227327663318392 -0.2801475241878198 -3.5599654531237758e-19
		 -0.95597119984449952 -0.28926938810229946 -0.049419491850683318 -2.6181080399839643e-19
		 194.88970951085773 283.10208202663483 134.29927181551858 0.99999999999999989;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wingFinger_c01_left_jnt" -p "wrist_left_jnt";
	rename -uid "17E3A0A2-4C34-EA7A-980D-56A0EC9B58EC";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr ".wfcc" -type "float3" 0.60000002 0.1 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 37.457033183106603 -3.0257667633699725 -7.029663018696219 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 0.99999999999999956 1.0000000000000002 0.99999999999999989 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -17.412963036155706 32.249645094490873 -30.444963742096601 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999933 0.99999999999999956 0.99999999999999978 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.9761111065265069 -0.15339185787482437 0.15387672225940763 0
		 0.20855898610301091 0.86003860584142133 -0.4656573265589472 0 -0.060911879229527732 0.48662566146891184 0.87148448555822244 0
		 206.78192732838022 270.01886179999588 95.035784385252711 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wingFinger_c02_left_jnt" -p "wingFinger_c01_left_jnt";
	rename -uid "DE1A7900-45C7-0F64-D2C8-5EB7BFC1981D";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr ".wfcc" -type "float3" 0.60000002 0.1 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 74.734635423817053 -1.1652900866465643e-12 0 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 1.0000000000000002 1.0000000000000011 1 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -14.904142101047977 31.750732505092849 -1.4546486914789432 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999956 1.0000000000000002 0.99999999999999978 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.85731545324617997 -0.40503383878272597 -0.31773857661011462 0
		 0.10739131947380148 0.74435283060681823 -0.65909480962096301 0 0.50346530975526349 0.53092980045251692 0.68164230272518334 0
		 279.73123500777712 258.55517722473792 106.53570512352204 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wingFinger_c03_left_jnt" -p "wingFinger_c02_left_jnt";
	rename -uid "7E72B846-4459-A106-365E-3AAE3DA57686";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 2;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 111.73695703179254 2.5579538487363607e-13 -2.8421709430404007e-12 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 1 0.99999999999999978 1 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000002 1.0000000000000011 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.85731545324618008 -0.40503383878272592 -0.31773857661011418 0
		 0.10739131947380141 0.74435283060681778 -0.65909480962096267 0 0.50346530975526338 0.5309298004525167 0.68164230272518345 0
		 375.52505496983582 213.29792858424901 71.032563441492698 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wingFinger_d01_left_jnt" -p "wrist_left_jnt";
	rename -uid "ABD6D86E-4A26-1924-8365-FD859599FDC4";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr ".wfcc" -type "float3" 0.60000002 0.1 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 22.583289118447681 -0.6859977027389732 -9.9380502026251207 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 0.99999999999999911 1 0.99999999999999967 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -64.939801384887531 74.636605877924239 -65.730465782275644 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999933 0.99999999999999956 0.99999999999999978 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.73750273429284841 -0.39974913162339043 -0.54432559068715047 0
		 -0.053318289323454449 0.76901659529641697 -0.63700128428624458 0 0.67323612271934896 0.4988126982395833 0.54583790189099535 0
		 196.93209436069955 264.20882423815715 84.818849824998409 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wingFinger_d02_left_jnt" -p "wingFinger_d01_left_jnt";
	rename -uid "1BC130FC-408B-7635-2D03-75BBC34F1C4A";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 2;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 149.1148773896297 -5.6843418860808015e-14 -4.3769432522822171e-12 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 1 0.99999999999999978 1 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999911 1 0.99999999999999956 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.7375027342928453 -0.39974913162339409 -0.54432559068715214 0
		 -0.053318289323451264 0.76901659529641975 -0.63700128428624236 0 0.67323612271934785 0.49881269823958146 0.54583790189099513 0
		 306.90472415929099 204.60028148952142 3.6518061096438146 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wingFinger_e01_left_jnt" -p "wrist_left_jnt";
	rename -uid "E56FABC4-478C-9CFB-0E16-5098B4A9E801";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr ".wfcc" -type "float3" 0.60000002 0.1 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 7.076595950061062 -0.33190784216887437 -7.3214843669075194 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 0.99999999999999911 1 0.99999999999999967 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 6.072782370524811 121.64014195801136 7.1229254075212687 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999933 0.99999999999999956 0.99999999999999978 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.1558975188414285 -0.51971608063089147 -0.8399947375744431 0
		 -0.22019099159168048 0.81070950903437056 -0.54246291963886362 0 0.96291842377272485 0.26952789743348599 0.011950801819355039 0
		 183.62440551548596 257.8451269855355 79.35642323085149 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wingFinger_e02_left_jnt" -p "wingFinger_e01_left_jnt";
	rename -uid "2D107F36-4A68-3303-ACF1-FDA837C959B5";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 2;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 145.8357224370807 -3.979039320256561e-13 -1.3926637620897964e-12 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 1 0.99999999999999978 1 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999911 1 0.99999999999999956 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.15589751884142805 -0.51971608063089181 -0.83999473757444287 0
		 -0.22019099159168046 0.81070950903437011 -0.54246291963886351 0 0.96291842377272485 0.2695278974334856 0.011950801819355161 0
		 206.35983280187278 182.05195690456057 -43.144816166663219 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wingElbow_01_left_jnt" -p "elbow_left_jnt";
	rename -uid "2FF829C9-4E68-D4EF-E1A5-67B46B2F2E6F";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr ".wfcc" -type "float3" 0.60000002 0.1 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" -4.0192824774293285 -0.093608882881198952 -5.8848856860982739 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 0.99999999999999933 1.0000000000000002 0.99999999999999978 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 2.8116319314087619 121.93465188936695 3.3120043089913538 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.14064904852451809 -0.49351739007928375 -0.85828808149623503 0
		 -0.22567270278342244 0.82810401410098489 -0.51314283883560141 0 0.96399672010207804 0.26586524315745119 0.0050986383728273688 0
		 86.707715547251013 197.72112163026694 20.522637269645987 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode joint -n "wingElbow_02_left_jnt" -p "wingElbow_01_left_jnt";
	rename -uid "56A31184-47E7-94F4-54EC-029F2DCAB873";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 2;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 82.428180250712302 -3.1263880373444408e-13 -7.673861546209082e-13 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 1 0.99999999999999978 1 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999933 1.0000000000000002 0.99999999999999978 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.1406490485245179 -0.49351739007928391 -0.85828808149623503 0
		 -0.2256727027834223 0.82810401410098455 -0.51314283883560141 0 0.96399672010207793 0.26586524315745136 0.0050986383728273731 0
		 98.301160671120471 157.04138124395021 -50.224487418963577 1;
	setAttr -cb on ".ds";
	setAttr ".fbxID" 5;
createNode transform -s -n "persp";
	rename -uid "6C2DFF6E-4400-DA44-FCF8-DBA37EF8DB3E";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 627.27526009356438 608.48871602137024 639.96190312826059 ;
	setAttr ".r" -type "double3" -27.938352729602325 45.000000000000007 2.9236893181567143e-14 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "D7A657E5-45EA-2587-07F3-F88A6582AEE1";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 1076.726695485067;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "B853058C-4DC1-4145-635D-71A414163C58";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "CAF01605-4D70-DA24-EC3A-7CB8E2C3F24E";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "front";
	rename -uid "C6C51D86-4653-BD8B-F05C-A692942A6ED7";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "A3D25CAA-4F36-8001-54EE-7E94C70BBAAE";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "side";
	rename -uid "ABE68475-43B1-B8C0-B5E9-2CBBED935382";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "3A9F19BC-4D77-2A08-EB22-12998B08B3CF";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode displayLayer -n "joints_lyr";
	rename -uid "715A0F25-4680-BBE4-3B0B-57B18706AB88";
	setAttr ".ufem" -type "stringArray" 0  ;
	setAttr ".do" 1;
createNode displayLayerManager -n "layerManager";
	rename -uid "02EC92B3-4D01-2674-AC08-FE9D5CAB2EC2";
	setAttr -s 3 ".dli[1:2]"  1 2;
	setAttr -s 2 ".dli";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "90F485BA-4966-554A-978E-1A823463D21D";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "318F52C7-4ECA-1150-EEF5-E6AE348F629C";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "3B69E0F1-448E-50DC-4660-7E989FE1061E";
createNode displayLayer -n "defaultLayer";
	rename -uid "ECD9BAF7-408B-9F89-C3B4-31A7545A7D36";
	setAttr ".ufem" -type "stringArray" 0  ;
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "5A8AF9DE-416B-919A-7E79-1BB29DBDC248";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "8B352971-431A-63E9-C2F9-11892D53BCBC";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "40B4FD06-4656-681A-909D-0DA63B655757";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n"
		+ "            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n"
		+ "            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n"
		+ "            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n"
		+ "            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n"
		+ "            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n"
		+ "            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n"
		+ "            -camera \"|persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 1\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n"
		+ "            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n"
		+ "            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1762\n            -height 1066\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n"
		+ "            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n"
		+ "            -longNames 0\n            -niceNames 1\n            -selectCommand \"print(\\\"\\\")\" \n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n"
		+ "            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -showUfeItems 1\n"
		+ "            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -ufeFilter \"USD\" \"InactivePrims\" -ufeFilterValue 1\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n"
		+ "                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -showUfeItems 1\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n"
		+ "                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showPlayRangeShades \"on\" \n                -lockPlayRangeShades \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -tangentScale 1\n                -tangentLineThickness 1\n                -keyMinScale 1\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -preSelectionHighlight 0\n                -limitToSelectedCurves 0\n                -constrainDrag 0\n                -valueLinesToggle 0\n                -outliner \"graphEditor1OutlineEd\" \n                -highlightAffectedCurves 0\n                $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n"
		+ "                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -showUfeItems 1\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n"
		+ "                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -hierarchyBelow 0\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n"
		+ "                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n"
		+ "                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n"
		+ "                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n"
		+ "                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"|persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n"
		+ "                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n"
		+ "                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n"
		+ "                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -bluePencil 1\n                -greasePencils 0\n                -excludeObjectPreset \"All\" \n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n"
		+ "                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName; };\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1762\\n    -height 1066\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1762\\n    -height 1066\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 50 -size 500 -divisions 2 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "CD953C37-4A36-DCC1-EAFF-5DBEAF49988E";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 24 -ast 0 -aet 24 ";
	setAttr ".st" 6;
select -ne :time1;
	setAttr ".o" 0;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
	setAttr ".rtfm" 1;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 5 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :standardSurface1;
	setAttr ".bc" -type "float3" 0.40000001 0.40000001 0.40000001 ;
	setAttr ".sr" 0.5;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".ren" -type "string" "arnold";
	setAttr ".dss" -type "string" "standardSurface1";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "<MAYA_RESOURCES>/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".vtn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".vn" -type "string" "ACES 1.0 SDR-video";
	setAttr ".dn" -type "string" "sRGB";
	setAttr ".wsn" -type "string" "ACEScg";
	setAttr ".otn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".potn" -type "string" "ACES 1.0 SDR-video (sRGB)";
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "joints_lyr.di" "root_jnt.do";
connectAttr "root_jnt.s" "pelvis_jnt.is";
connectAttr "pelvis_jnt.s" "clavicle_left_jnt.is";
connectAttr "clavicle_left_jnt.s" "shoulder_left_jnt.is";
connectAttr "shoulder_left_jnt.s" "elbow_left_jnt.is";
connectAttr "elbow_left_jnt.s" "wrist_left_jnt.is";
connectAttr "wrist_left_jnt.s" "wingFinger_a01_left_jnt.is";
connectAttr "wingFinger_a01_left_jnt.s" "wingFinger_a02_left_jnt.is";
connectAttr "wrist_left_jnt.s" "wingFinger_b01_left_jnt.is";
connectAttr "wingFinger_b01_left_jnt.s" "wingFinger_b02_left_jnt.is";
connectAttr "wrist_left_jnt.s" "wingFinger_c01_left_jnt.is";
connectAttr "wingFinger_c01_left_jnt.s" "wingFinger_c02_left_jnt.is";
connectAttr "wingFinger_c02_left_jnt.s" "wingFinger_c03_left_jnt.is";
connectAttr "wrist_left_jnt.s" "wingFinger_d01_left_jnt.is";
connectAttr "wingFinger_d01_left_jnt.s" "wingFinger_d02_left_jnt.is";
connectAttr "wrist_left_jnt.s" "wingFinger_e01_left_jnt.is";
connectAttr "wingFinger_e01_left_jnt.s" "wingFinger_e02_left_jnt.is";
connectAttr "elbow_left_jnt.s" "wingElbow_01_left_jnt.is";
connectAttr "wingElbow_01_left_jnt.s" "wingElbow_02_left_jnt.is";
connectAttr "layerManager.dli[1]" "joints_lyr.id";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of skeleton.ma
