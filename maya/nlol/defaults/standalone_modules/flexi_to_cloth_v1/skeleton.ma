//Maya ASCII 2025ff03 scene
//Name: skeleton.ma
//Last modified: Fri, Oct 10, 2025 10:01:20 PM
//Codeset: 1252
requires maya "2025ff03";
requires "stereoCamera" "10.0";
requires "mtoa" "5.5.2";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2025";
fileInfo "version" "2025";
fileInfo "cutIdentifier" "202409190603-cbdc5a7e54";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 22631)";
fileInfo "UUID" "5119A4E8-4A6C-CF21-0AFE-15A1CF653008";
createNode transform -s -n "persp";
	rename -uid "BFB476F2-4F84-BF07-CE6F-6197BD3E6B50";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 115.3433444890499 142.50489402125669 233.87276800533135 ;
	setAttr ".r" -type "double3" -16.538352729890622 25.800000000000459 -4.4158729975578581e-16 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "93DF5B91-4059-6405-1C08-53B91601D8AC";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 308.1639680492201;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "F730E69A-4937-5FB4-7A0C-59AA561CF6A2";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "CF50D2CD-449B-C3E2-7EB4-C9AE584F8D41";
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
	rename -uid "11DAF669-48B0-BC7F-E5CA-49990F26CBFC";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "2FFA096A-4A8D-2B9B-E05D-04BABDD3B81C";
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
	rename -uid "DA4C54A7-418B-67BB-02C0-CCA1D400E444";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "494864D5-4629-116B-3AC0-94A793D24928";
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
createNode joint -n "root";
	rename -uid "033E1CF2-4135-A10D-3C75-89B91DF588C8";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -k true -sn "jointTRSData" -ln "jointTRSData" -dt "string";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 2;
	setAttr -cb on ".oc";
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -90 0 0 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0 -1 0 0 1 0 0 0 0 0 1;
	setAttr -cb on ".ds" 3;
	setAttr -k on ".jointTRSData" -type "string" ",2,2,2&cr;&lf;";
	setAttr ".fbxID" 2;
createNode joint -n "pelvis" -p "root";
	rename -uid "ABEFFFBC-4EFC-F58C-155A-599B313CEF95";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0 0.60000002 1 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -3.4314998759166203e-17 -2.28086614608765 95.896781921386705 ;
	setAttr ".r" -type "double3" 1.0227239633638709e-16 3.2246852130739906e-15 -3.8166656177562201e-14 ;
	setAttr ".s" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -90 -86.366893050032402 90 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0 0.99799027986901889 -0.063367194090933859 0 0 -0.063367194090933859 -0.997990279869019 0
		 -1 0 0 0 -3.4314998759166203e-17 95.896781921386705 2.28086614608765 1;
	setAttr -cb on ".ds" 3;
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "spine_01" -p "pelvis";
	rename -uid "D08C62F4-42BF-D9F6-A960-EDB73737384E";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0 0.60000002 1 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 3.6770534515381428 3.5527136788005009e-15 -4.6633694517662424e-16 ;
	setAttr ".r" -type "double3" 1.1109600217509716e-16 -8.7589156280487821e-16 -7.1562480332929123e-14 ;
	setAttr ".s" -type "double3" 1.0000000000000004 1.0000000000000002 1 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0 -14.457321828304902 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0 0.98220797016103478 0.18779644126591288 0 0 0.18779644126591283 -0.98220797016103467 0
		 -1 0 0 0 4.3202194641745802e-16 99.566445524580601 2.0478615863412908 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "spine_02" -p "spine_01";
	rename -uid "618F43C5-4E1B-812A-53CA-2AA0459BA1C7";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0 0.60000002 1 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 6.7950572967527023 -2.1316282072803006e-14 1.8559423937125883e-16 ;
	setAttr ".r" -type "double3" 6.4116438275598201e-18 2.1200832928722492e-16 -4.4925334875672175e-14 ;
	setAttr ".s" -type "double3" 1.0000000000000007 1.0000000000000004 1 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0 3.4644695084247501 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000002 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0 0.99176140629857323 0.12809884065314342 0 0 0.12809884065314334 -0.9917614062985729 0
		 -1 0 0 0 2.464277070461992e-16 106.24060495915199 3.3239491648694433 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "spine_03" -p "spine_02";
	rename -uid "6EEA97DD-4E22-B7B7-C72D-32B94CFA08B5";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0 0.60000002 1 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 7.2382278442380112 -5.6843418860808015e-14 1.2292061026365016e-16 ;
	setAttr ".r" -type "double3" 6.382989047489964e-17 6.6618430715655257e-16 -1.2722218725854064e-14 ;
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999967 1 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0 10.946079405533503 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000007 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0 0.99804167658749665 -0.062552472328610137 0 0 -0.062552472328610276 -0.9980416765874961 0
		 -1 0 0 0 1.2350709678254904e-16 113.41919998506297 4.2511577600996908 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "spine_04" -p "spine_03";
	rename -uid "F2079E92-4DFE-A1FB-BF31-B39C4A9C7848";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0 0.60000002 1 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 8.5238933563234269 -3.0198066269804258e-14 2.5229931328786596e-16 ;
	setAttr ".r" -type "double3" -6.400419807445853e-15 3.5842148044301092e-16 -2.7034717606098121e-14 ;
	setAttr ".s" -type "double3" 0.99999999999999967 0.99999999999999944 0.99999999999999989 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0.00044952872062768381 3.0332133116374183e-21 5.8669839318741479 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999978 0.99999999999999956 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0 0.98641974755132933 -0.16424396987644246 0 -7.8457562571503343e-06 -0.16424396987138754 -0.98641974752096862 0
		 -0.99999999996922195 1.2886181543573122e-06 7.7392089065274968e-06 0 -1.2879221650531692e-16 121.92640080146103 3.7179671567962762 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "thigh_l" -p "pelvis";
	rename -uid "9E728990-4857-4A0C-53C1-E9B9638B1698";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -k true -sn "blendParent1" -ln "blendParent1" -dt "string";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -2.3657112121582031 -0.11004376411438344 -9.9692029953002894 ;
	setAttr ".r" -type "double3" -1.1131941385122309e-14 -1.0336802714756426e-14 -4.8702243559910092e-14 ;
	setAttr ".s" -type "double3" 0.99999999999999967 1 1.0000000000000002 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 8.4265142315496018 -4.8646858739326779 -3.8181082597372664 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.084802811748175166 0.99639255941280735 0.0032172451567538257 0
		 -0.14601293308005989 -0.0092329884397984591 -0.98923959448549648 0 -0.98564126663455098 -0.084360058506769975 0.14626918347954523 0
		 9.9692029953002894 93.542798291234803 2.5405972345779313 1;
	setAttr -cb on ".ds";
	setAttr -k on ".blendParent1" -type "string" "1.000000";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "calf_l" -p "thigh_l";
	rename -uid "3FD44830-4316-8986-A74F-188A2AB39D65";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -41.999999999999943 3.6415315207705135e-14 -4.9737991503207013e-14 ;
	setAttr ".r" -type "double3" 1.1131941385122307e-14 -1.5207027070747442e-14 -4.2937488199757462e-14 ;
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999956 1.0000000000000002 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0 -5.0048445558743646 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999956 1 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.071741321700524607 0.99339912429517119 0.089506215483889734 0
		 -0.1528544283548903 0.077727475054326922 -0.98518727323995547 0 -0.98564126663455121 -0.084360058506769989 0.14626918347954526 0
		 13.530921088723685 51.694310795896961 2.4054729379942277 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "calf_twist_02_l" -p "calf_l";
	rename -uid "6131AFCD-41CB-2320-4DA2-D980B2FC7EA6";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -14.550000000000033 1.2378986724570495e-14 3.907985046680551e-14 ;
	setAttr ".r" -type "double3" -1.4112158393778797e-14 -1.4908850069360232e-16 -4.541170456376661e-14 ;
	setAttr ".s" -type "double3" 1.0000000000000007 1.0000000000000009 1.0000000000000007 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -0.0046559128746534624 0.25816272471229068 2.6643342814062101 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999978 0.99999999999999956 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.074327277331800293 0.99630839617945488 0.042953876970129701 0
		 -0.14927420055585572 0.031472133300899985 -0.98829485371214099 0 -0.98599831079614642 -0.079869171322944035 0.14638390136669566 0
		 14.574757319466281 37.240353537402186 1.1031575027036227 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "calf_twist_01_l" -p "calf_l";
	rename -uid "9C0AFC7E-452B-1BD3-6115-F581AF8FA1CF";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -29.100000000000065 5.0670110065542673e-06 3.5527136788005009e-15 ;
	setAttr ".r" -type "double3" -1.4112158393778797e-14 -1.4908850069360232e-16 -4.541170456376661e-14 ;
	setAttr ".s" -type "double3" 1.0000000000000007 1.0000000000000009 1.0000000000000007 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -0.0046559128746534624 0.25816272471229068 2.6643342814062101 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999978 0.99999999999999956 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.074327277331800293 0.99630839617945488 0.042953876970129701 0
		 -0.14927420055585572 0.031472133300899985 -0.98829485371214099 0 -0.98599831079614642 -0.079869171322944035 0.14638390136669566 0
		 15.618592775693882 22.786396672753387 -0.19916292454172613 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "foot_l" -p "calf_l";
	rename -uid "97FFF0FA-4742-00C7-6E14-188C949F500E";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -43.660000000000096 3.2585045772748344e-14 1.0658141036401503e-14 ;
	setAttr ".s" -type "double3" 1.0000000000000007 1.0000000000000016 1.0000000000000007 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 5.0506192817532529 4.8392267506332249 4.4739331954552535 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999978 0.99999999999999956 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -2.7755575615628914e-17 1.0000000000000007 1.4051260155412137e-16 0
		 -0.23330465503120951 4.5102810375396984e-17 -0.97240369083049638 0 -0.97240369083049594 -2.4980018054066022e-16 0.23330465503120948 0
		 16.66314719416858 8.3225050291696903 -1.5023684300324369 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "ball_l" -p "foot_l";
	rename -uid "45FEB49E-4842-9AD1-D7F0-79B10B1E243D";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -7.4987628789477672 -13.883342298259635 1.0658141036401503e-14 ;
	setAttr ".s" -type "double3" 0.99999999999999933 1 0.99999999999999967 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 5.7237061894714536 -90 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000007 1.0000000000000016 1.0000000000000007 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32912071597032444 -1.9965012056348068e-17 0.9442878556452915 0
		 -2.7755575615628914e-17 1.0000000000000007 1.4051260155412137e-16 0 -0.9442878556452915 -2.5305294306823485e-16 0.32912071597032455 0
		 19.902195579744234 0.82374215022191688 11.997844861858377 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "thigh_twist_01_l" -p "thigh_l";
	rename -uid "57A62F29-460D-3A20-1237-8BBA0E7AB062";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -13.999999999999901 2.2204460492503131e-14 4.6185277824406512e-14 ;
	setAttr ".r" -type "double3" 1.8239884774341768e-15 -1.9828770592249113e-14 -5.1684013573782148e-14 ;
	setAttr ".s" -type "double3" 1.0000000000000004 0.99999999999999967 0.99999999999999944 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0.25820470285919334 -1.3073006136480412 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999956 1 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.077006867933141696 0.99671390879602706 0.025126207506777003 0
		 -0.14790967986487863 0.013501832400190579 -0.98890870515134344 0 -0.9859983107964212 -0.079869171364069541 0.14638390134239529 0
		 11.156442359774685 79.5933024594556 2.4955558023833628 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "thigh_twist_02_l" -p "thigh_l";
	rename -uid "7FDE08FE-4C3E-B10B-CCEE-F58A1DE4C93F";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -27.999999999999972 -2.2688979859353253e-06 -8.0748641622108153e-06 ;
	setAttr ".r" -type "double3" 1.8239884774341768e-15 -1.9828770592249113e-14 -5.1684013573782148e-14 ;
	setAttr ".s" -type "double3" 1.0000000000000004 0.99999999999999967 0.99999999999999944 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0.25820470285919334 -1.3073006136480412 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999956 1 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.077006867933141696 0.99671390879602706 0.025126207506777003 0
		 -0.14790967986487863 0.013501832400190579 -0.98890870515134344 0 -0.9859983107964212 -0.079869171364069541 0.14638390134239529 0
		 12.343690014456982 65.643807329820945 2.4505154335687602 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "thigh_r" -p "pelvis";
	rename -uid "B3F8F70C-42F5-AB43-87BC-A5A4C106D7DA";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -k true -sn "blendParent1" -ln "blendParent1" -dt "string";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -2.3657096820641783 -0.11004663225838307 9.9692 ;
	setAttr ".r" -type "double3" -1.1131941385122309e-14 -1.0336802714756426e-14 -4.8702243559910092e-14 ;
	setAttr ".s" -type "double3" 0.99999999999999967 1 1.0000000000000002 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 8.4265142315495751 -4.8646858739326886 176.18189174026273 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.084802811748175361 -0.99639255941280758 -0.0032172451567539229 0
		 -0.14601293308005944 0.0092329884397983411 0.9892395944854967 0 -0.98564126663455098 0.084360058506770169 -0.14626918347954479 0
		 -9.9692000000000007 93.5428 2.5405999999999991 1;
	setAttr -cb on ".ds";
	setAttr -k on ".blendParent1" -type "string" "1.000000";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "calf_r" -p "thigh_r";
	rename -uid "F47E98F4-434F-A8DD-8B02-BF9E090A3463";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 42.000010943528366 -8.3993744759425226e-06 -1.8054284705470991e-05 ;
	setAttr ".r" -type "double3" 1.1131941385122307e-14 -1.5207027070747442e-14 -4.2937488199757462e-14 ;
	setAttr ".s" -type "double3" 0.99999999999999989 0.99999999999999956 1.0000000000000002 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 1.4787793329194398e-06 -1.1848489498583665e-23 -5.0048445558743122 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999956 1 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.071741321700524996 -0.99339912429517152 -0.089506215483888957 0
		 -0.15285445379386534 -0.077727472877029441 0.98518726946481094 0 -0.98564126268944408 0.084360060512882723 -0.14626920890680295 0
		 -13.530899999999994 51.694300000000005 2.4054700000000024 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "calf_twist_02_r" -p "calf_r";
	rename -uid "A103A69D-48A3-B0CA-59AF-B7807F4AAC5C";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 14.549947207860029 1.0651635995229114e-05 6.6888925775998587e-05 ;
	setAttr ".r" -type "double3" -1.4112158393778797e-14 -1.4908850069360232e-16 -4.541170456376661e-14 ;
	setAttr ".s" -type "double3" 1.0000000000000007 1.0000000000000009 1.0000000000000007 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -0.0046573899735469207 0.25816279345283011 2.6643342747501424 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999978 0.99999999999999956 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.074327277331800223 -0.99630839617945499 -0.042953876970131602 0
		 -0.14927420055752269 -0.031472133300766869 0.98829485371189374 0 -0.98599831079589395 0.079869171322997409 -0.14638390136836629 0
		 -14.5748 37.240399999999958 1.1031599999999979 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "calf_twist_01_r" -p "calf_r";
	rename -uid "57ECD250-40D8-EF6E-053F-8080B6B1F8BF";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 29.099987745081069 9.8313939655980676e-07 2.867921894633696e-05 ;
	setAttr ".r" -type "double3" -1.4112158393778797e-14 -1.4908850069360232e-16 -4.541170456376661e-14 ;
	setAttr ".s" -type "double3" 1.0000000000000007 1.0000000000000009 1.0000000000000007 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -0.0046573899735469207 0.25816279345283011 2.6643342747501424 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999978 0.99999999999999956 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.074327277331800223 -0.99630839617945499 -0.042953876970131602 0
		 -0.14927420055752269 -0.031472133300766869 0.98829485371189374 0 -0.98599831079589395 0.079869171322997409 -0.14638390136836629 0
		 -15.618600000000001 22.786399999999951 -0.19916300000000131 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "foot_r" -p "calf_r";
	rename -uid "DB6A0F1D-43E5-152E-3E9A-A9A34A6CFCFD";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 43.659982342061078 -3.8680790006573318e-06 -2.460062180276168e-05 ;
	setAttr ".s" -type "double3" 1.0000000000000007 1.0000000000000016 1.0000000000000007 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 5.0506178022056583 4.8392268659861823 4.473933070640463 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999978 0.99999999999999956 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -5.2735593669694936e-16 -1.0000000000000009 -7.9276862852140084e-16 0
		 -0.23330465503120701 -5.9847959921199845e-16 0.97240369083049705 0 -0.97240369083049638 7.9103390504542404e-16 -0.23330465503120695 0
		 -16.6631 8.3225099999999443 -1.5023700000000022 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "ball_r" -p "foot_r";
	rename -uid "59B1BAD9-4893-A1F1-0BD7-4D8C4EB931DE";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 7.4987679999999433 13.883312242950694 6.0290256435280298e-05 ;
	setAttr ".s" -type "double3" 0.99999999999999933 1 0.99999999999999967 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 2.6411008011161406e-13 5.7237061894716019 -89.999999999999901 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000007 1.0000000000000016 1.0000000000000007 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32912071597032444 -1.2597519809831787e-15 -0.94428785564529161 0
		 -9.4853566236799065e-16 -1.0000000000000009 9.329484420948499e-16 0 -0.94428785564529116 6.5942722013977645e-16 -0.32912071597032455 0
		 -19.902200000000029 0.82374199999998687 11.997799999999994 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "thigh_twist_01_r" -p "thigh_r";
	rename -uid "A6FE27C4-4693-5076-8DBF-7AB8CC8A3B1C";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 14.000000810358202 -4.3694239462155338e-06 -3.9360367743768165e-05 ;
	setAttr ".r" -type "double3" 1.8239884774341768e-15 -1.9828770592249113e-14 -5.1684013573782148e-14 ;
	setAttr ".s" -type "double3" 1.0000000000000004 0.99999999999999967 0.99999999999999944 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0.25820470285915004 -1.3073006136477594 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999956 1 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.077006867933143389 -0.99671390879602728 -0.025126207506772358 0
		 -0.14790967986487777 -0.013501832400185805 0.98890870515134377 0 -0.9859983107964212 0.079869171364070499 -0.14638390134239479 0
		 -11.156399999999985 79.593300000000042 2.495560000000002 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "thigh_twist_02_r" -p "thigh_r";
	rename -uid "6FD48D36-41CD-7E93-F52B-5BA223C42D38";
	addAttr -is true -ci true -k true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 
		1 -at "bool";
	addAttr -is true -ci true -h true -k true -sn "filmboxTypeID" -ln "filmboxTypeID" 
		-smn 5 -smx 5 -at "short";
	setAttr ".wfcc" -type "float3" 0.80000001 0.30000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 28.000010100997685 5.8624454144506899e-06 1.9843391196872062e-05 ;
	setAttr ".r" -type "double3" 1.8239884774341768e-15 -1.9828770592249113e-14 -5.1684013573782148e-14 ;
	setAttr ".s" -type "double3" 1.0000000000000004 0.99999999999999967 0.99999999999999944 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0.25820470285915004 -1.3073006136477594 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 0.99999999999999956 1 1.0000000000000002 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" -0.077006867933143389 -0.99671390879602728 -0.025126207506772358 0
		 -0.14790967986487777 -0.013501832400185805 0.98890870515134377 0 -0.9859983107964212 0.079869171364070499 -0.14638390134239479 0
		 -12.3437 65.643799999999985 2.45052 1;
	setAttr -cb on ".ds";
	setAttr -k on ".filmboxTypeID" 5;
createNode joint -n "ezorLeatherStrip_left_a01_jnt" -p "pelvis";
	rename -uid "7F4A0EF6-4D6F-CBA9-C18F-A2A3ADE8EBB0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 1.8781923159138785 -15.042880807299255 -3.7330623276581454 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -10.079780113080666 2.9069977958874809 -170.98128835012875 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.050714917866914656 -0.9744634889619932 0.21874392742604815 0
		 0.17479406050371799 0.22430568352044261 0.95871476297856728 0 -0.98329803900871005 -0.010386001176927027 0.18170607436510819 0
		 3.7330623276581454 98.724424744196355 17.174499195977912 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_a02_jnt" -p "ezorLeatherStrip_left_a01_jnt";
	rename -uid "DBFDB809-4172-8A6F-C909-C496C5BBF071";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560827 -1.4210854715202004e-14 4.4408920985006262e-16 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.050714917866914656 -0.9744634889619932 0.21874392742604815 0
		 0.17479406050371799 0.22430568352044261 0.95871476297856728 0 -0.98329803900871005 -0.010386001176927027 0.18170607436510819 0
		 4.005389769198243 93.491779992219264 18.349103762324468 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_a03_jnt" -p "ezorLeatherStrip_left_a02_jnt";
	rename -uid "8945E997-416E-816B-013C-88894B4FE4F2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560258 -1.4210854715202004e-14 8.8817841970012523e-16 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.050714917866914656 -0.9744634889619932 0.21874392742604815 0
		 0.17479406050371799 0.22430568352044261 0.95871476297856728 0 -0.98329803900871005 -0.010386001176927027 0.18170607436510819 0
		 4.2777172107383379 88.25913524024223 19.523708328671013 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_a04_jnt" -p "ezorLeatherStrip_left_a03_jnt";
	rename -uid "349717E6-4E4B-5F53-744F-148B22F8BA5F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560542 -7.1054273576010019e-15 -8.8817841970012523e-16 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.050714917866914656 -0.9744634889619932 0.21874392742604815 0
		 0.17479406050371799 0.22430568352044261 0.95871476297856728 0 -0.98329803900871005 -0.010386001176927027 0.18170607436510819 0
		 4.5500446522784372 83.026490488265168 20.698312895017569 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_a05_jnt" -p "ezorLeatherStrip_left_a04_jnt";
	rename -uid "003F3AE6-4604-208B-3D9B-89BB5818FB8A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560684 -2.8421709430404007e-14 3.1086244689504383e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.050714917866914656 -0.9744634889619932 0.21874392742604815 0
		 0.17479406050371799 0.22430568352044261 0.95871476297856728 0 -0.98329803900871005 -0.010386001176927027 0.18170607436510819 0
		 4.8223720938185295 77.793845736288091 21.872917461364111 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_a06_jnt" -p "ezorLeatherStrip_left_a05_jnt";
	rename -uid "41EE7CDB-461C-1261-FB6C-F89FEB89BE65";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.8499999999999801 0 1.7763568394002505e-15 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 1.590277340731758e-15 3.975693351829396e-16 0 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.050714917866914656 -0.9744634889619932 0.21874392742604815 0
		 0.17479406050371799 0.22430568352044261 0.95871476297856728 0 -0.98329803900871005 -0.010386001176927027 0.18170607436510819 0
		 5.1190543633399779 72.09323432586045 23.152569436806488 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_b01_jnt" -p "pelvis";
	rename -uid "7363C483-4CF3-6198-3829-CA92C6B75D4B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 2.0416358423152445 -12.782407155679337 -10.53141078388739 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -29.590298521755464 7.1006937110042845 -171.76920859495712 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.12361349143113787 -0.9711329914807485 0.20401082714860264 0
		 0.49000744731068446 0.23851035481989397 0.83845423979115019 0 -0.86290926887840924 -0.0036774313509964976 0.50534549585643695 0
		 10.53141078388739 98.744299922232784 14.908211506100825 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_b02_jnt" -p "ezorLeatherStrip_left_b01_jnt";
	rename -uid "C473C2E8-4C25-510B-40FA-119B5992B417";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560542 -1.4210854715202004e-14 7.1054273576010019e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.12361349143113787 -0.9711329914807485 0.20401082714860264 0
		 0.49000744731068446 0.23851035481989397 0.83845423979115019 0 -0.86290926887840924 -0.0036774313509964976 0.50534549585643695 0
		 11.195186794520374 93.52953917552027 16.003702713434567 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_b03_jnt" -p "ezorLeatherStrip_left_b02_jnt";
	rename -uid "CF073C8B-4296-B4F9-052F-C5A21EF7739B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.36976994135604 -1.4210854715202004e-14 -5.3290705182007514e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.12361349143113787 -0.9711329914807485 0.20401082714860264 0
		 0.49000744731068446 0.23851035481989397 0.83845423979115019 0 -0.86290926887840924 -0.0036774313509964976 0.50534549585643695 0
		 11.858962805153368 88.31477842880777 17.0991939207683 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_b04_jnt" -p "ezorLeatherStrip_left_b03_jnt";
	rename -uid "BDE84119-4AE2-7375-E979-BCBAD9A5D72D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560684 -2.1316282072803006e-14 -3.5527136788005009e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.12361349143113787 -0.9711329914807485 0.20401082714860264 0
		 0.49000744731068446 0.23851035481989397 0.83845423979115019 0 -0.86290926887840924 -0.0036774313509964976 0.50534549585643695 0
		 12.522738815786361 83.100017682095242 18.194685128102037 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_b05_jnt" -p "ezorLeatherStrip_left_b04_jnt";
	rename -uid "AEBE1F9A-4FD9-4D12-6586-F286C8BF4703";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560542 -1.4210854715202004e-14 -1.7763568394002505e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.12361349143113787 -0.9711329914807485 0.20401082714860264 0
		 0.49000744731068446 0.23851035481989397 0.83845423979115019 0 -0.86290926887840924 -0.0036774313509964976 0.50534549585643695 0
		 13.186514826419355 77.885256935382728 19.290176335435778 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_b06_jnt" -p "ezorLeatherStrip_left_b05_jnt";
	rename -uid "BBD49BA3-47E8-CA0D-DA56-A2A51724931F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.8499999999999801 2.8421709430404007e-14 -8.8817841970012523e-16 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 7.9513867036587919e-16 3.1805546814635168e-15 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.12361349143113787 -0.9711329914807485 0.20401082714860264 0
		 0.49000744731068446 0.23851035481989397 0.83845423979115019 0 -0.86290926887840924 -0.0036774313509964976 0.50534549585643695 0
		 13.909653751291524 72.204128935220382 20.483639674255123 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_c01_jnt" -p "pelvis";
	rename -uid "A0EF38AF-4A51-6916-AAD1-AC9B9EB2A224";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 2.4840089663619978 -8.8454444160424188 -16.195142703501105 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -49.759773437041758 13.262142797876795 -174.51744588184795 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.22940667579518498 -0.96103802048736475 0.15420278946352184 0
		 0.74298482967315749 0.27524776129742673 0.61009197075220067 0 -0.62876555247258248 -0.025388837674915066 0.77718034390054247 0
		 16.195142703501105 98.936309718055398 10.951129016124595 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_c02_jnt" -p "ezorLeatherStrip_left_c01_jnt";
	rename -uid "F9B78C41-4833-B9E4-32C4-DBAB9C3B2CF8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560827 -1.4210854715202004e-14 8.8817841970012523e-16 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.22940667579518498 -0.96103802048736475 0.15420278946352184 0
		 0.74298482967315749 0.27524776129742673 0.61009197075220067 0 -0.62876555247258248 -0.025388837674915066 0.77718034390054247 0
		 17.427003775532498 93.775756643141989 11.779162519859067 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_c03_jnt" -p "ezorLeatherStrip_left_c02_jnt";
	rename -uid "C421B84E-4CF4-FEFD-01B5-60AAC0CC3A07";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560684 -7.1054273576010019e-15 -8.8817841970012523e-16 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.22940667579518498 -0.96103802048736475 0.15420278946352184 0
		 0.74298482967315749 0.27524776129742673 0.61009197075220067 0 -0.62876555247258248 -0.025388837674915066 0.77718034390054247 0
		 18.658864847563894 88.615203568228594 12.60719602359354 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_c04_jnt" -p "ezorLeatherStrip_left_c03_jnt";
	rename -uid "303EC163-4B1C-6164-FF77-53B52FC272F6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.36976994135604 -2.1316282072803006e-14 -8.8817841970012523e-16 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.22940667579518498 -0.96103802048736475 0.15420278946352184 0
		 0.74298482967315749 0.27524776129742673 0.61009197075220067 0 -0.62876555247258248 -0.025388837674915066 0.77718034390054247 0
		 19.890725919595273 83.454650493315228 13.435229527328 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_c05_jnt" -p "ezorLeatherStrip_left_c04_jnt";
	rename -uid "A865D127-4600-764C-CB42-43B613C14591";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560684 -2.1316282072803006e-14 -8.8817841970012523e-16 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.22940667579518498 -0.96103802048736475 0.15420278946352184 0
		 0.74298482967315749 0.27524776129742673 0.61009197075220067 0 -0.62876555247258248 -0.025388837674915066 0.77718034390054247 0
		 21.122586991626658 78.294097418401833 14.263263031062463 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_c06_jnt" -p "ezorLeatherStrip_left_c05_jnt";
	rename -uid "B209F4C8-4C99-4CCE-8311-9DA0960E7A62";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.8499999999999659 7.1054273576010019e-15 6.2172489379008766e-15 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 3.1805546814635168e-15 -7.9513867036587919e-16 -2.3854160110976376e-15 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.22940667579518498 -0.96103802048736475 0.15420278946352184 0
		 0.74298482967315749 0.27524776129742673 0.61009197075220067 0 -0.62876555247258248 -0.025388837674915066 0.77718034390054247 0
		 22.464616045028485 72.672024998550782 15.165349349424069 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_d01_jnt" -p "pelvis";
	rename -uid "CED7F9A8-492F-52AF-8FE3-848B5DE62992";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 2.9147113984586781 -3.1309620286316537 -19.173123098056671 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -74.699309108798118 18.250566537759767 179.94392455826764 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.31317319704519792 -0.94784585026060197 0.059251943396376808 0
		 0.91603332876459131 0.3179479207739434 0.24452415068452621 0 -0.25061023371951918 -0.022301655079480578 0.96783115621257265 0
		 19.173123098056671 99.004035844231552 5.2208387343958371 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_d02_jnt" -p "ezorLeatherStrip_left_d01_jnt";
	rename -uid "FB5BFB89-43BE-D741-3DED-EB841870FD8A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560542 -1.4210854715202004e-14 -2.2204460492503131e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.31317319704519792 -0.94784585026060197 0.059251943396376808 0
		 0.91603332876459131 0.3179479207739434 0.24452415068452621 0 -0.25061023371951918 -0.022301655079480578 0.96783115621257265 0
		 20.854791117988338 93.91432168846309 5.539008039012626 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_d03_jnt" -p "ezorLeatherStrip_left_d02_jnt";
	rename -uid "F863DAE2-4FDF-AE23-DEC1-9588768CE838";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560542 -2.1316282072803006e-14 4.4408920985006262e-16 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.31317319704519792 -0.94784585026060197 0.059251943396376808 0
		 0.91603332876459131 0.3179479207739434 0.24452415068452621 0 -0.25061023371951918 -0.022301655079480578 0.96783115621257265 0
		 22.536459137919998 88.824607532694628 5.8571773436294157 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_d04_jnt" -p "ezorLeatherStrip_left_d03_jnt";
	rename -uid "B89A9A21-4FA0-623F-E42F-3FA4AAE7011B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560827 -7.1054273576010019e-15 4.4408920985006262e-16 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.31317319704519792 -0.94784585026060197 0.059251943396376808 0
		 0.91603332876459131 0.3179479207739434 0.24452415068452621 0 -0.25061023371951918 -0.022301655079480578 0.96783115621257265 0
		 24.218127157851679 83.734893376926152 6.1753466482462107 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_d05_jnt" -p "ezorLeatherStrip_left_d04_jnt";
	rename -uid "429F3265-4F85-CEFE-BDE5-59BE969A8D8D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560684 -4.9737991503207013e-14 -2.2204460492503131e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.31317319704519792 -0.94784585026060197 0.059251943396376808 0
		 0.91603332876459131 0.3179479207739434 0.24452415068452621 0 -0.25061023371951918 -0.022301655079480578 0.96783115621257265 0
		 25.899795177783318 78.645179221157676 6.4935159528629915 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_d06_jnt" -p "ezorLeatherStrip_left_d05_jnt";
	rename -uid "F7FDBFCA-4676-092E-76EC-DC9A47D9DC74";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.8500000000000014 7.1054273576010019e-15 -4.4408920985006262e-15 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 3.975693351829396e-16 1.2921003393445538e-15 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.31317319704519792 -0.94784585026060197 0.059251943396376808 0
		 0.91603332876459131 0.3179479207739434 0.24452415068452621 0 -0.25061023371951918 -0.022301655079480578 0.96783115621257265 0
		 27.731858380497734 73.100280997133154 6.8401398217317935 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_e01_jnt" -p "pelvis";
	rename -uid "13B7E03C-4B20-FBCE-F11A-DCABE1354DB3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 3.3080871313596703 3.1713364910162962 -19.30683921320075 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -101.98254897418779 18.841875463790871 173.54277916641209 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32295748164311489 -0.94526404571096967 -0.046629914613557699 0
		 0.92579195853264384 0.32576599061736594 -0.19179616490789839 0 0.19648845911917689 0.018772406431166878 0.98032641614400851 0
		 19.30683921320075 98.997262028489544 -1.0937210454631252 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_e02_jnt" -p "ezorLeatherStrip_left_e01_jnt";
	rename -uid "CD07E798-4F99-1E7A-4CE8-1DB42AA3E387";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.36976994135604 -2.8421709430404007e-14 -1.7763568394002505e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32295748164311489 -0.94526404571096967 -0.046629914613557699 0
		 0.92579195853264384 0.32576599061736594 -0.19179616490789839 0 0.19648845911917689 0.018772406431166878 0.98032641614400851 0
		 21.041046590463967 93.921411569186162 -1.3441129593230023 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_e03_jnt" -p "ezorLeatherStrip_left_e02_jnt";
	rename -uid "8BC9AE58-4BA9-BD9B-CCDB-77823EC4C66C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560827 -2.1316282072803006e-14 -2.6645352591003757e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32295748164311489 -0.94526404571096967 -0.046629914613557699 0
		 0.92579195853264384 0.32576599061736594 -0.19179616490789839 0 0.19648845911917689 0.018772406431166878 0.98032641614400851 0
		 22.775253967727203 88.845561109882752 -1.5945048731828837 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_e04_jnt" -p "ezorLeatherStrip_left_e03_jnt";
	rename -uid "11399217-4E32-F268-052F-AC8568272AA6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560684 -2.8421709430404007e-14 8.8817841970012523e-16 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32295748164311489 -0.94526404571096967 -0.046629914613557699 0
		 0.92579195853264384 0.32576599061736594 -0.19179616490789839 0 0.19648845911917689 0.018772406431166878 0.98032641614400851 0
		 24.509461344990427 83.769710650579356 -1.8448967870427595 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_e05_jnt" -p "ezorLeatherStrip_left_e04_jnt";
	rename -uid "17CDCDA0-46B5-ADE2-AE85-3493D527D9BC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560827 -1.4210854715202004e-14 -8.8817841970012523e-16 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32295748164311489 -0.94526404571096967 -0.046629914613557699 0
		 0.92579195853264384 0.32576599061736594 -0.19179616490789839 0 0.19648845911917689 0.018772406431166878 0.98032641614400851 0
		 26.24366872225367 78.693860191275945 -2.0952887009026404 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_e06_jnt" -p "ezorLeatherStrip_left_e05_jnt";
	rename -uid "A1561A61-47D6-07B7-43AD-BCBDBCAB0861";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.8499999999999943 1.4210854715202004e-14 0 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -1.5902773407317584e-15 7.9513867036587919e-16 8.9453100416161419e-16 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32295748164311489 -0.94526404571096967 -0.046629914613557699 0
		 0.92579195853264384 0.32576599061736594 -0.19179616490789839 0 0.19648845911917689 0.018772406431166878 0.98032641614400851 0
		 28.132969989865902 73.164065523866782 -2.3680737013919555 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_f01_jnt" -p "pelvis";
	rename -uid "BC721150-47B7-9111-B518-E6A52A729D94";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 3.6896786026890567 9.2354159050429772 -16.652322183168295 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -130.1714166310785 15.423580113098016 165.45723961528856 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.26595286903967824 -0.94656375819075211 -0.18244484955559512 0
		 0.73659901730750099 0.32163430346534122 -0.59495652155093581 0 0.62184480310700319 0.023841696964872296 0.78277749989038903 0
		 16.652322183168295 98.993822910545731 -7.1697937378427437 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_f02_jnt" -p "ezorLeatherStrip_left_f01_jnt";
	rename -uid "03A283E4-40EC-990E-201B-CC8A13C64510";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560542 -2.8421709430404007e-14 -5.3290705182007514e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.26595286903967824 -0.94656375819075211 -0.18244484955559512 0
		 0.73659901730750099 0.32163430346534122 -0.59495652155093581 0 0.62184480310700319 0.023841696964872296 0.78277749989038903 0
		 18.080427905154938 93.910993294236008 -8.1494806069415926 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_f03_jnt" -p "ezorLeatherStrip_left_f02_jnt";
	rename -uid "1D5DAC52-4FDC-C565-ADE1-1F9ED03C8996";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560969 -1.4210854715202004e-14 3.5527136788005009e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.26595286903967824 -0.94656375819075211 -0.18244484955559512 0
		 0.73659901730750099 0.32163430346534122 -0.59495652155093581 0 0.62184480310700319 0.023841696964872296 0.78277749989038903 0
		 19.50853362714161 88.828163677926241 -9.1291674760404504 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_f04_jnt" -p "ezorLeatherStrip_left_f03_jnt";
	rename -uid "74658FA6-4B58-BC47-403E-3EBA1766BCF5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560684 -2.1316282072803006e-14 0 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.26595286903967824 -0.94656375819075211 -0.18244484955559512 0
		 0.73659901730750099 0.32163430346534122 -0.59495652155093581 0 0.62184480310700319 0.023841696964872296 0.78277749989038903 0
		 20.936639349128264 83.745334061616504 -10.108854345139303 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_f05_jnt" -p "ezorLeatherStrip_left_f04_jnt";
	rename -uid "1BA09156-4302-D6CE-0B71-A2B5EFBF0714";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560684 -2.1316282072803006e-14 0 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.26595286903967824 -0.94656375819075211 -0.18244484955559512 0
		 0.73659901730750099 0.32163430346534122 -0.59495652155093581 0 0.62184480310700319 0.023841696964872296 0.78277749989038903 0
		 22.364745071114918 78.662504445306766 -11.088541214238155 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_f06_jnt" -p "ezorLeatherStrip_left_f05_jnt";
	rename -uid "568ECC06-4103-1846-BE94-D398B45F7AB7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.8499999999999801 -1.4210854715202004e-14 7.1054273576010019e-15 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 3.1805546814635168e-15 0 7.9513867036587919e-16 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.26595286903967824 -0.94656375819075211 -0.18244484955559512 0
		 0.73659901730750099 0.32163430346534122 -0.59495652155093581 0 0.62184480310700319 0.023841696964872296 0.78277749989038903 0
		 23.920569354997024 73.125106459890887 -12.155843584138369 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_g01_jnt" -p "pelvis";
	rename -uid "22D2EB33-41C4-5D5E-56E5-BFA1EF832CDD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 3.9002087869297242 13.390076778992361 -11.035245219676549 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -161.9478366782692 9.0732232460262985 160.52245344585236 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.15769658954313731 -0.94996952087476649 -0.26961026511509384 0
		 0.30600535603639617 0.30659749634464428 -0.90130943482925718 0 0.93887832423775897 0.059631238828014979 0.33904514099502248 0
		 11.035245219676549 98.940660786055389 -11.329445613243131 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_g02_jnt" -p "ezorLeatherStrip_left_g01_jnt";
	rename -uid "474C3335-4413-4458-1392-3DB925178DCF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560542 -2.1316282072803006e-14 -1.7763568394002505e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.15769658954313731 -0.94996952087476649 -0.26961026511509384 0
		 0.30600535603639617 0.30659749634464428 -0.90130943482925718 0 0.93887832423775897 0.059631238828014979 0.33904514099502248 0
		 11.882039626059642 93.839543007657653 -12.77719071073918 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_g03_jnt" -p "ezorLeatherStrip_left_g02_jnt";
	rename -uid "07B1B22A-42F5-E5DF-FCE6-92B9F2CFC77C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560542 -1.4210854715202004e-14 -3.5527136788005009e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.15769658954313731 -0.94996952087476649 -0.26961026511509384 0
		 0.30600535603639617 0.30659749634464428 -0.90130943482925718 0 0.93887832423775897 0.059631238828014979 0.33904514099502248 0
		 12.728834032442737 88.738425229259917 -14.224935808235237 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_g04_jnt" -p "ezorLeatherStrip_left_g03_jnt";
	rename -uid "CA9CEACC-4D37-0AC8-15FD-8DB1F2D65609";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560684 -3.5527136788005009e-14 7.1054273576010019e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.15769658954313731 -0.94996952087476649 -0.26961026511509384 0
		 0.30600535603639617 0.30659749634464428 -0.90130943482925718 0 0.93887832423775897 0.059631238828014979 0.33904514099502248 0
		 13.575628438825838 83.637307450862153 -15.672680905731275 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_g05_jnt" -p "ezorLeatherStrip_left_g04_jnt";
	rename -uid "988EE91C-404E-BDF0-D4D8-81BFC59890B0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560542 -7.1054273576010019e-15 -3.5527136788005009e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.15769658954313731 -0.94996952087476649 -0.26961026511509384 0
		 0.30600535603639617 0.30659749634464428 -0.90130943482925718 0 0.93887832423775897 0.059631238828014979 0.33904514099502248 0
		 14.422422845208935 78.536189672464417 -17.120426003227337 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_g06_jnt" -p "ezorLeatherStrip_left_g05_jnt";
	rename -uid "B1CFD3FD-499D-689C-1BCC-339E5FA2055F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.8499999999999872 2.1316282072803006e-14 -3.5527136788005009e-15 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0 -1.5902773407317584e-15 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.15769658954313731 -0.94996952087476649 -0.26961026511509384 0
		 0.30600535603639617 0.30659749634464428 -0.90130943482925718 0 0.93887832423775897 0.059631238828014979 0.33904514099502248 0
		 15.34494789403629 72.978867975347057 -18.697646054150653 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_h01_jnt" -p "pelvis";
	rename -uid "23D7C7A2-45D3-F1E2-D674-8B8A94D6606D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 3.923994004535146 14.182220427054787 -3.6379625963476703 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 178.27588689868995 1.7196190699642679 159.78161816366458 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.030008508994760472 -0.9579643451562061 -0.28531351667482202 0
		 -0.030073359380373841 0.28444754341124423 -0.95821980156062736 0 0.99909713363791153 0.037335083457129881 -0.020273359360473225 0
		 3.6379625963476703 98.914202281735498 -12.121504476769916 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_h02_jnt" -p "ezorLeatherStrip_left_h01_jnt";
	rename -uid "E3D420F6-48A2-CA90-65D8-8F8413F9766D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560969 -1.4210854715202004e-14 -8.8817841970012523e-16 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.030008508994760472 -0.9579643451562061 -0.28531351667482202 0
		 -0.030073359380373841 0.28444754341124423 -0.95821980156062736 0 0.99909713363791153 0.037335083457129881 -0.020273359360473225 0
		 3.7991013859326488 93.770154136224818 -13.653572422472964 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_h03_jnt" -p "ezorLeatherStrip_left_h02_jnt";
	rename -uid "965F9787-4E9F-FB50-0CAB-AA968EA909E7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560258 -7.1054273576010019e-15 2.6645352591003757e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.030008508994760472 -0.9579643451562061 -0.28531351667482202 0
		 -0.030073359380373841 0.28444754341124423 -0.95821980156062736 0 0.99909713363791153 0.037335083457129881 -0.020273359360473225 0
		 3.9602401755176282 88.626105990714208 -15.185640368175997 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_h04_jnt" -p "ezorLeatherStrip_left_h03_jnt";
	rename -uid "8EB2B660-40C0-9C0B-E7B0-C4B10EEBED59";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560684 -4.2632564145606011e-14 -1.7763568394002505e-15 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.030008508994760472 -0.9579643451562061 -0.28531351667482202 0
		 -0.030073359380373841 0.28444754341124423 -0.95821980156062736 0 0.99909713363791153 0.037335083457129881 -0.020273359360473225 0
		 4.1213789651026058 83.482057845203556 -16.717708313879008 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_h05_jnt" -p "ezorLeatherStrip_left_h04_jnt";
	rename -uid "FF6B61F9-48A1-4BA9-FC52-249657FDEC25";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.3697699413560684 -1.4210854715202004e-14 -8.8817841970012523e-16 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.030008508994760472 -0.9579643451562061 -0.28531351667482202 0
		 -0.030073359380373841 0.28444754341124423 -0.95821980156062736 0 0.99909713363791153 0.037335083457129881 -0.020273359360473225 0
		 4.282517754687583 78.338009699692904 -18.249776259582049 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_left_h06_jnt" -p "ezorLeatherStrip_left_h05_jnt";
	rename -uid "087569A8-47F7-E16A-2FEE-EEA3E9020CB0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 5.8499999999999801 1.4210854715202004e-14 8.8817841970012523e-16 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -3.975693351829396e-16 -2.4848083448933725e-16 -3.1805546814635168e-15 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.030008508994760472 -0.9579643451562061 -0.28531351667482202 0
		 -0.030073359380373841 0.28444754341124423 -0.95821980156062736 0 0.99909713363791153 0.037335083457129881 -0.020273359360473225 0
		 4.4580675323069316 72.733918280529124 -19.918860332129764 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_h01_jnt" -p "pelvis";
	rename -uid "F4DE8C9E-4851-6ABA-1266-5588B671AA59";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 3.9239914437049208 14.182216103869113 3.6379599999999988 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 178.27588689868992 1.7196190699642484 -20.218381836335418 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.030008508994760132 0.95796434515620588 0.28531351667482169 0
		 -0.030073359380374282 -0.2844475434112439 0.95821980156062769 0 0.99909713363791153 -0.037335083457129672 0.02027335936047376 0
		 -3.6379599999999988 98.914199999999965 -12.121500000000006 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_h02_jnt" -p "ezorLeatherStrip_right_h01_jnt";
	rename -uid "2E8F8A4C-42A3-76F9-C9D5-18926D33AF92";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697330015203733 -4.4373533050645619e-05 -3.6566871219889663e-06 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.030008508994760132 0.95796434515620588 0.28531351667482169 0
		 -0.030073359380374282 -0.2844475434112439 0.95821980156062769 0 0.99909713363791153 -0.037335083457129672 0.02027335936047376 0
		 -3.7990999999999988 93.770200000000017 -13.653599999999996 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_h03_jnt" -p "ezorLeatherStrip_right_h02_jnt";
	rename -uid "738D5C12-4242-6817-E0D2-5186A0EC7694";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.369800266603292 7.9893201458958174e-05 2.1041571631741363e-06 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.030008508994760132 0.95796434515620588 0.28531351667482169 0
		 -0.030073359380374282 -0.2844475434112439 0.95821980156062769 0 0.99909713363791153 -0.037335083457129672 0.02027335936047376 0
		 -3.960239999999998 88.626100000000008 -15.185599999999994 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_h04_jnt" -p "ezorLeatherStrip_right_h03_jnt";
	rename -uid "AF36DE3E-4F65-48D9-9456-71929A7530F5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697330015204017 -4.4373533050645619e-05 -3.6566871202126094e-06 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.030008508994760132 0.95796434515620588 0.28531351667482169 0
		 -0.030073359380374282 -0.2844475434112439 0.95821980156062769 0 0.99909713363791153 -0.037335083457129672 0.02027335936047376 0
		 -4.1213799999999976 83.482100000000031 -16.71769999999999 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_h05_jnt" -p "ezorLeatherStrip_right_h04_jnt";
	rename -uid "C9BA043C-4B1D-FB3F-2E45-36996C60B13F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3698287979549377 -1.5928778701379542e-05 7.6821226713263968e-08 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.030008508994760132 0.95796434515620588 0.28531351667482169 0
		 -0.030073359380374282 -0.2844475434112439 0.95821980156062769 0 0.99909713363791153 -0.037335083457129672 0.02027335936047376 0
		 -4.2825199999999963 78.338000000000036 -18.249799999999986 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_h06_jnt" -p "ezorLeatherStrip_right_h05_jnt";
	rename -uid "0C3D0B43-40DF-31E6-64F1-33AE1FF009FF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.8499999999999872 4.0960729982941757e-05 7.5438379143477619e-06 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.030008508994760132 0.95796434515620588 0.28531351667482169 0
		 -0.030073359380374282 -0.2844475434112439 0.95821980156062769 0 0.99909713363791153 -0.037335083457129672 0.02027335936047376 0
		 -4.4580634724192594 72.733896648007402 -19.918844670226196 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_g01_jnt" -p "pelvis";
	rename -uid "8927157C-4784-5612-C518-0EB2E64F033D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 3.900245031682033 13.390028772541442 11.0352 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -161.94783667826914 9.073223246026302 -19.477546554147658 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.15769658954313734 0.94996952087476616 0.26961026511509406 0
		 0.30600535603639734 -0.30659749634464456 0.90130943482925718 0 0.93887832423775852 -0.059631238828014549 -0.3390451409950237 0
		 -11.0352 98.940699999999978 -11.329399999999996 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_g02_jnt" -p "ezorLeatherStrip_right_g01_jnt";
	rename -uid "1E9DD9B4-4A6B-936D-DA7E-F18D536EF9C6";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3698637337451345 -2.598688411836747e-05 1.8265677530493463e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.15769658954313734 0.94996952087476616 0.26961026511509406 0
		 0.30600535603639734 -0.30659749634464456 0.90130943482925718 0 0.93887832423775852 -0.059631238828014549 -0.3390451409950237 0
		 -11.882000000000001 93.839499999999958 -12.777200000000002 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_g03_jnt" -p "ezorLeatherStrip_right_g02_jnt";
	rename -uid "FEDBB131-4C24-1108-74EC-A3BCF20FE34E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697417757664994 3.3484309724940431e-05 -2.1601960456862912e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.15769658954313734 0.94996952087476616 0.26961026511509406 0
		 0.30600535603639734 -0.30659749634464456 0.90130943482925718 0 0.93887832423775852 -0.059631238828014549 -0.3390451409950237 0
		 -12.728800000000003 88.73839999999997 -14.224900000000002 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_g04_jnt" -p "ezorLeatherStrip_right_g03_jnt";
	rename -uid "4CAD2DE6-4476-57BA-D065-4B9E9D3DCC26";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697687367930484 -5.6646633737500451e-05 1.2302553644261138e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.15769658954313734 0.94996952087476616 0.26961026511509406 0
		 0.30600535603639734 -0.30659749634464456 0.90130943482925718 0 0.93887832423775852 -0.059631238828014549 -0.3390451409950237 0
		 -13.575600000000003 83.637299999999939 -15.672699999999994 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_g05_jnt" -p "ezorLeatherStrip_right_g04_jnt";
	rename -uid "96272289-479E-9A67-FE8F-889D83DAE814";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697417757664994 3.3484309732045858e-05 -2.1601960451533841e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.15769658954313734 0.94996952087476616 0.26961026511509406 0
		 0.30600535603639734 -0.30659749634464456 0.90130943482925718 0 0.93887832423775852 -0.059631238828014549 -0.3390451409950237 0
		 -14.422399999999998 78.536199999999951 -17.120399999999989 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_g06_jnt" -p "ezorLeatherStrip_right_g05_jnt";
	rename -uid "7B5386C4-4C18-82D4-F41E-9EA06FC01B46";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.8499999999999943 -2.5927670094461064e-05 -6.9659031019853046e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.15769658954313734 0.94996952087476616 0.26961026511509406 0
		 0.30600535603639734 -0.30659749634464456 0.90130943482925718 0 0.93887832423775852 -0.059631238828014549 -0.3390451409950237 0
		 -15.344998384187582 72.97889040609563 -18.697619802220974 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_f01_jnt" -p "pelvis";
	rename -uid "B9F7B0E2-4346-35D6-EBD7-D8BF479425BF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 3.6896555013305061 9.2354136264892368 16.652299999999983 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -130.17141663107847 15.423580113098009 -14.542760384711499 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.26595286903967819 0.946563758190752 0.1824448495555962 0
		 0.73659901730750132 -0.32163430346534183 0.59495652155093515 0 0.62184480310700319 -0.023841696964871227 -0.78277749989038947 0
		 -16.652299999999983 98.993800000000007 -7.1697899999999883 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_f02_jnt" -p "ezorLeatherStrip_right_f01_jnt";
	rename -uid "8E76B660-45AD-A5D3-6CA0-A099AB82D7BE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697409570686574 -7.1735614568524397e-06 5.3028835500512628e-06 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.26595286903967819 0.946563758190752 0.1824448495555962 0
		 0.73659901730750132 -0.32163430346534183 0.59495652155093515 0 0.62184480310700319 -0.023841696964871227 -0.78277749989038947 0
		 -18.080400000000001 93.910999999999987 -8.1494800000000023 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_f03_jnt" -p "ezorLeatherStrip_right_f02_jnt";
	rename -uid "CC6C6589-4B15-4DB4-AEE9-30B0FD5EE1FB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697409570686432 -7.1735614355361577e-06 5.3028835447221923e-06 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.26595286903967819 0.946563758190752 0.1824448495555962 0
		 0.73659901730750132 -0.32163430346534183 0.59495652155093515 0 0.62184480310700319 -0.023841696964871227 -0.78277749989038947 0
		 -19.508500000000005 88.828199999999981 -9.1291699999999967 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_f04_jnt" -p "ezorLeatherStrip_right_f03_jnt";
	rename -uid "68ADE593-40DD-1AD9-15B8-2B8AAF0897F2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3698429112384218 1.1916080495666392e-06 3.8998153249814038e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.26595286903967819 0.946563758190752 0.1824448495555962 0
		 0.73659901730750132 -0.32163430346534183 0.59495652155093515 0 0.62184480310700319 -0.023841696964871227 -0.78277749989038947 0
		 -20.936599999999995 83.7453 -10.108899999999997 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_f05_jnt" -p "ezorLeatherStrip_right_f04_jnt";
	rename -uid "1CE96E6D-4C22-7997-AFE7-DF8C6369560B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697245370321838 4.6372525495996797e-05 -6.514709143701225e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.26595286903967819 0.946563758190752 0.1824448495555962 0
		 0.73659901730750132 -0.32163430346534183 0.59495652155093515 0 0.62184480310700319 -0.023841696964871227 -0.78277749989038947 0
		 -22.364699999999999 78.662499999999994 -11.088500000000002 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_f06_jnt" -p "ezorLeatherStrip_right_f05_jnt";
	rename -uid "1CC8B0A9-4522-9A5C-13C2-F8A29AC3FAE2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.8500000000000014 -8.1951819844050533e-05 3.399226761402474e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.26595286903967819 0.946563758190752 0.1824448495555962 0
		 0.73659901730750132 -0.32163430346534183 0.59495652155093515 0 0.62184480310700319 -0.023841696964871227 -0.78277749989038947 0
		 -23.92056351159712 73.125127562667245 -12.155877736052167 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_e01_jnt" -p "pelvis";
	rename -uid "F666340D-4DEB-EFA7-905A-AFB5167E9342";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 3.308124960309911 3.1713330415061911 19.30680000000001 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -101.98254897418772 18.841875463790871 -6.4572208335879333 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32295748164311489 0.94526404571096967 0.046629914613557852 0
		 0.92579195853264418 -0.32576599061736594 0.19179616490789705 0 0.19648845911917578 -0.018772406431166247 -0.98032641614400862 0
		 -19.30680000000001 98.997299999999967 -1.093720000000002 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_e02_jnt" -p "ezorLeatherStrip_right_e01_jnt";
	rename -uid "291B7EF0-4742-DF19-D39A-3E866FFCDD58";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3698142986098105 2.3335556065262608e-05 5.0333778034428178e-07 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32295748164311489 0.94526404571096967 0.046629914613557852 0
		 0.92579195853264418 -0.32576599061736594 0.19179616490789705 0 0.19648845911917578 -0.018772406431166247 -0.98032641614400862 0
		 -21.041000000000004 93.921400000000048 -1.3441100000000026 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_e03_jnt" -p "ezorLeatherStrip_right_e02_jnt";
	rename -uid "5DC656C1-4168-65EF-62DA-9EAD035020CC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697520679535273 -0.00010182023881100122 -2.1022748777355105e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32295748164311489 0.94526404571096967 0.046629914613557852 0
		 0.92579195853264418 -0.32576599061736594 0.19179616490789705 0 0.19648845911917578 -0.018772406431166247 -0.98032641614400862 0
		 -22.775300000000005 88.84559999999999 -1.5944999999999987 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_e04_jnt" -p "ezorLeatherStrip_right_e03_jnt";
	rename -uid "9B8DBDA6-4AA7-AA38-304D-1A99C64A8235";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3698147649090657 2.141759443219371e-05 1.0306601942566829e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32295748164311489 0.94526404571096967 0.046629914613557852 0
		 0.92579195853264418 -0.32576599061736594 0.19179616490789705 0 0.19648845911917578 -0.018772406431166247 -0.98032641614400862 0
		 -24.50950000000002 83.769699999999958 -1.844900000000002 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_e05_jnt" -p "ezorLeatherStrip_right_e04_jnt";
	rename -uid "A86FAEAD-4FCF-C19E-2762-C4A039C23220";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697197722052579 -9.2410429672895589e-06 -1.3739028617010263e-06 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32295748164311489 0.94526404571096967 0.046629914613557852 0
		 0.92579195853264418 -0.32576599061736594 0.19179616490789705 0 0.19648845911917578 -0.018772406431166247 -0.98032641614400862 0
		 -26.243699999999993 78.693900000000014 -2.095289999999999 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_e06_jnt" -p "ezorLeatherStrip_right_e05_jnt";
	rename -uid "630B1F65-4654-B0DA-328D-F29DD22EDFB1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.8499999999999943 -6.008403296675624e-06 -5.5877626845557415e-06 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.32295748164311489 0.94526404571096967 0.046629914613557852 0
		 0.92579195853264418 -0.32576599061736594 0.19179616490789705 0 0.19648845911917578 -0.018772406431166247 -0.98032641614400862 0
		 -28.133007928074548 73.16410739482005 -2.3680706750466549 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_d01_jnt" -p "pelvis";
	rename -uid "258F89FF-485E-5FDD-2A67-8A96A1248060";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 2.9146755460662064 -3.1309610203439266 19.173100000000009 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -74.699309108798147 18.25056653775982 -0.056075441732297199 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.31317319704519875 0.94784585026060131 -0.059251943396377828 0
		 0.91603332876459098 -0.3179479207739444 -0.24452415068452527 0 -0.25061023371951874 0.022301655079479572 -0.96783115621257265 0
		 -19.173100000000009 99.003999999999991 5.220839999999999 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_d02_jnt" -p "ezorLeatherStrip_right_d01_jnt";
	rename -uid "A0AF32CB-40AF-0977-F696-D49667F7FD8F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697665803726977 -3.3965643559952241e-05 7.6572159355414726e-06 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 1.2074182697257331e-06 -2.2202090304166429e-22 3.351258674569408e-23 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.31317319704519875 0.94784585026060131 -0.059251943396377828 0
		 0.91603332876459098 -0.3179479207739444 -0.24452415068452527 0 -0.25061023371951874 0.022301655079479572 -0.96783115621257265 0
		 -20.854800000000001 93.914300000000011 5.5390099999999949 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_d03_jnt" -p "ezorLeatherStrip_right_d02_jnt";
	rename -uid "684CBD86-4262-1267-D14E-61AAB2BC863E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697665803727546 -3.3965643567057668e-05 7.6572159337651158e-06 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 1.2074182697257331e-06 -2.2202090304166429e-22 3.351258674569408e-23 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.31317319704519875 0.94784585026060131 -0.059251943396377828 0
		 0.91603332876459098 -0.3179479207739444 -0.24452415068452527 0 -0.25061023371951874 0.022301655079479572 -0.96783115621257265 0
		 -22.536500000000014 88.824599999999975 5.8571799999999978 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_d04_jnt" -p "ezorLeatherStrip_right_d03_jnt";
	rename -uid "BBFFD009-42C6-3B05-99BD-AB8F42636687";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697352630530304 5.7637689295120254e-05 -1.7403807438309826e-05 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 1.2074182697257331e-06 -2.2202090304166429e-22 3.351258674569408e-23 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.31317319704519875 0.94784585026060131 -0.059251943396377828 0
		 0.91603332876459098 -0.3179479207739444 -0.24452415068452527 0 -0.25061023371951874 0.022301655079479572 -0.96783115621257265 0
		 -24.218100000000035 83.734899999999968 6.1753500000000034 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_d05_jnt" -p "ezorLeatherStrip_right_d04_jnt";
	rename -uid "D836CB57-4D52-2D82-BE3C-7DA31A4F74BF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697665803726835 -3.3965643559952241e-05 7.6572159302124021e-06 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 1.2074182697257331e-06 -2.2202090304166429e-22 3.351258674569408e-23 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.31317319704519875 0.94784585026060131 -0.059251943396377828 0
		 0.91603332876459098 -0.3179479207739444 -0.24452415068452527 0 -0.25061023371951874 0.022301655079479572 -0.96783115621257265 0
		 -25.89980000000002 78.645200000000003 6.4935200000000037 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_d06_jnt" -p "ezorLeatherStrip_right_d05_jnt";
	rename -uid "28C24FC1-40B3-E816-108C-558E2148D962";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.8500000000000085 5.8973491157132685e-05 -8.7115921507674443e-06 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 1.2074182697257331e-06 -2.2202090304166429e-22 3.351258674569408e-23 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.31317319704519875 0.94784585026060131 -0.059251943396377828 0
		 0.91603332876459098 -0.3179479207739444 -0.24452415068452527 0 -0.25061023371951874 0.022301655079479572 -0.96783115621257265 0
		 -27.731806997816879 73.100282831193653 6.8401378797762797 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_c01_jnt" -p "pelvis";
	rename -uid "047043EB-4269-03AE-9176-57BD86FDAB63";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 2.4840011065075629 -8.8454148424262193 16.195100000000007 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -49.759773437041751 13.262142797876802 5.4825541181520601 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.22940667579518514 0.96103802048736464 -0.15420278946352192 0
		 0.74298482967315749 -0.2752477612974269 -0.61009197075220067 0 -0.62876555247258259 0.025388837674915128 -0.77718034390054236 0
		 -16.195100000000007 98.936299999999989 10.951100000000007 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_c02_jnt" -p "ezorLeatherStrip_right_c01_jnt";
	rename -uid "F1A8B60D-4B6E-270F-E963-FE9DD95C3240";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697381185919113 -8.4100478879634011e-05 -2.5855514453887452e-05 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 8.5377364625159377e-07 -4.7393957376387766e-23 -8.2939426843198156e-23 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.22940667579518514 0.96103802048736464 -0.15420278946352192 0
		 0.74298482967315749 -0.2752477612974269 -0.61009197075220067 0 -0.62876555247258259 0.025388837674915128 -0.77718034390054236 0
		 -17.427000000000014 93.775799999999947 11.779199999999999 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_c03_jnt" -p "ezorLeatherStrip_right_c02_jnt";
	rename -uid "A7294C86-4440-299D-69EE-42902482C05E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3698188021149207 4.4334943112289693e-06 4.9323636155840234e-05 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 8.5377364625159377e-07 -4.7393957376387766e-23 -8.2939426843198156e-23 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.22940667579518514 0.96103802048736464 -0.15420278946352192 0
		 0.74298482967315749 -0.2752477612974269 -0.61009197075220067 0 -0.62876555247258259 0.025388837674915128 -0.77718034390054236 0
		 -18.658900000000003 88.615200000000002 12.607199999999997 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_c04_jnt" -p "ezorLeatherStrip_right_c03_jnt";
	rename -uid "226601E0-4ECC-10A9-5AFD-CFBE21FE467A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3696997576453214 5.1207201153147253e-05 -1.1014035318446247e-05 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 8.5377364625159377e-07 -4.7393957376387766e-23 -8.2939426843198156e-23 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.22940667579518514 0.96103802048736464 -0.15420278946352192 0
		 0.74298482967315749 -0.2752477612974269 -0.61009197075220067 0 -0.62876555247258259 0.025388837674915128 -0.77718034390054236 0
		 -19.890699999999999 83.454700000000031 13.435199999999991 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_c05_jnt" -p "ezorLeatherStrip_right_c04_jnt";
	rename -uid "960E55FE-4C56-2CE7-1E92-2882F2A73A2C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3698342223939619 -5.6575702764405378e-05 -2.8394398227327144e-05 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 8.5377364625159377e-07 -4.7393957376387766e-23 -8.2939426843198156e-23 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.22940667579518514 0.96103802048736464 -0.15420278946352192 0
		 0.74298482967315749 -0.2752477612974269 -0.61009197075220067 0 -0.62876555247258259 0.025388837674915128 -0.77718034390054236 0
		 -21.122600000000013 78.294099999999986 14.263299999999997 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_c06_jnt" -p "ezorLeatherStrip_right_c05_jnt";
	rename -uid "65CA4269-450D-18B2-AF50-FFA64A11C37E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.8500000000000014 5.9483046584318799e-05 4.4245868623171702e-05 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 8.5377364625159377e-07 -4.7393957376387766e-23 -8.2939426843198156e-23 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.22940667579518514 0.96103802048736464 -0.15420278946352192 0
		 0.74298482967315749 -0.2752477612974269 -0.61009197075220067 0 -0.62876555247258259 0.025388837674915128 -0.77718034390054236 0
		 -22.464612678678641 72.672012330924673 15.165315641213091 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_b01_jnt" -p "pelvis";
	rename -uid "BB9AA14D-4C64-61DB-2C3E-65A840C23985";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 2.041636649035496 -12.782395677630454 10.531400000000012 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -29.590298521755464 7.100693711004249 8.2307914050428668 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.12361349143113726 0.97113299148074883 -0.20401082714860244 0
		 0.49000744731068457 -0.23851035481989352 -0.8384542397911503 0 -0.86290926887840924 0.0036774313509960466 -0.50534549585643695 0
		 -10.531400000000012 98.74430000000001 14.90820000000001 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_b02_jnt" -p "ezorLeatherStrip_right_b01_jnt";
	rename -uid "235DBFD6-4876-CB93-BA0D-4792826FE7C7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3698128207270202 -9.7649012644751565e-06 1.6112961586767227e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.12361349143113726 0.97113299148074883 -0.20401082714860244 0
		 0.49000744731068457 -0.23851035481989352 -0.8384542397911503 0 -0.86290926887840924 0.0036774313509960466 -0.50534549585643695 0
		 -11.195200000000007 93.52950000000007 16.003700000000002 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_b03_jnt" -p "ezorLeatherStrip_right_b02_jnt";
	rename -uid "EEA709B0-44FA-D91C-01B9-3AB675D92DAE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697157074279573 -3.361593674355845e-05 1.648070472048957e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.12361349143113726 0.97113299148074883 -0.20401082714860244 0
		 0.49000744731068457 -0.23851035481989352 -0.8384542397911503 0 -0.86290926887840924 0.0036774313509960466 -0.50534549585643695 0
		 -11.859000000000009 88.314800000000048 17.09920000000001 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_b04_jnt" -p "ezorLeatherStrip_right_b03_jnt";
	rename -uid "4EA5DBC7-467E-8AD6-1D36-E48F45738447";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3698004593779842 3.9235843495077916e-05 -7.0177965302509193e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.12361349143113726 0.97113299148074883 -0.20401082714860244 0
		 0.49000744731068457 -0.23851035481989352 -0.8384542397911503 0 -0.86290926887840924 0.0036774313509960466 -0.50534549585643695 0
		 -12.522700000000002 83.100000000000009 18.194700000000001 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_b05_jnt" -p "ezorLeatherStrip_right_b04_jnt";
	rename -uid "A5DD98D8-4BE6-2F10-5E2F-97ABF21F800C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697157074279147 -3.3615936750663877e-05 1.6480704728483175e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.12361349143113726 0.97113299148074883 -0.20401082714860244 0
		 0.49000744731068457 -0.23851035481989352 -0.8384542397911503 0 -0.86290926887840924 0.0036774313509960466 -0.50534549585643695 0
		 -13.186500000000009 77.885300000000029 19.290200000000002 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_b06_jnt" -p "ezorLeatherStrip_right_b05_jnt";
	rename -uid "99332A55-4178-D35C-3DE0-7B8A7381E173";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.8500000000000512 3.7937169715007713e-05 1.5377475313105293e-05 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.12361349143113726 0.97113299148074883 -0.20401082714860244 0
		 0.49000744731068457 -0.23851035481989352 -0.8384542397911503 0 -0.86290926887840924 0.0036774313509960466 -0.50534549585643695 0
		 -13.909633604742458 72.204163007979403 20.483623759300656 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_a01_jnt" -p "pelvis";
	rename -uid "FFAFBDA6-4E91-7007-3752-B3ADBC11D3E1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 1.8781675704977943 -15.042880041735181 3.7330600000000005 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -10.079780113080657 2.9069977958874791 9.0187116498712641 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr -av ".is" -type "double3" 1.0000000000000004 1.0000000000000004 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.050714917866914622 0.97446348896199331 -0.21874392742604815 0
		 0.17479406050371782 -0.22430568352044267 -0.95871476297856739 0 -0.98329803900871005 0.010386001176927033 -0.18170607436510802 0
		 -3.7330600000000005 98.724399999999989 17.174499999999995 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_a02_jnt" -p "ezorLeatherStrip_right_a01_jnt";
	rename -uid "77698281-4D89-1F5C-F8FE-8B8FD76B3BBB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697254630798739 -6.107502528607256e-06 3.810255597036516e-06 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.050714917866914622 0.97446348896199331 -0.21874392742604815 0
		 0.17479406050371782 -0.22430568352044267 -0.95871476297856739 0 -0.98329803900871005 0.010386001176927033 -0.18170607436510802 0
		 -4.0053899999999993 93.491799999999969 18.349099999999993 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_a03_jnt" -p "ezorLeatherStrip_right_a02_jnt";
	rename -uid "62A43506-4605-6274-5B6F-659D35D5AC90";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3698229094287058 1.632306580745535e-05 2.7716554831247464e-06 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.050714917866914622 0.97446348896199331 -0.21874392742604815 0
		 0.17479406050371782 -0.22430568352044267 -0.95871476297856739 0 -0.98329803900871005 0.010386001176927033 -0.18170607436510802 0
		 -4.2777200000000013 88.259100000000018 19.523699999999991 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_a04_jnt" -p "ezorLeatherStrip_right_a03_jnt";
	rename -uid "866EFF1C-4840-3C2A-3460-768EE7F14937";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3697249559307068 -4.3595619132474894e-06 -6.022724790666345e-06 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.050714917866914622 0.97446348896199331 -0.21874392742604815 0
		 0.17479406050371782 -0.22430568352044267 -0.95871476297856739 0 -0.98329803900871005 0.010386001176927033 -0.18170607436510802 0
		 -4.5500400000000019 83.026499999999984 20.698299999999982 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_a05_jnt" -p "ezorLeatherStrip_right_a04_jnt";
	rename -uid "F03F1A75-4232-14DB-29C6-A7821EC0254D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.3698229094287342 1.6323065793244496e-05 2.7716554800161219e-06 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.050714917866914622 0.97446348896199331 -0.21874392742604815 0
		 0.17479406050371782 -0.22430568352044267 -0.95871476297856739 0 -0.98329803900871005 0.010386001176927033 -0.18170607436510802 0
		 -4.8223700000000047 77.793800000000005 21.872900000000001 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode joint -n "ezorLeatherStrip_right_a06_jnt" -p "ezorLeatherStrip_right_a05_jnt";
	rename -uid "D30FED1C-4EA9-A473-0901-2A9E05676F5D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc";
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" -5.8499999999999801 -5.8865782726513771e-05 -6.6045716800022802e-06 ;
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
	setAttr -av ".is" -type "double3" 1 1 1 ;
	setAttr -av ".is";
	setAttr ".bps" -type "matrix" 0.050714917866914622 0.97446348896199331 -0.21874392742604815 0
		 0.17479406050371782 -0.22430568352044267 -0.95871476297856739 0 -0.98329803900871005 0.010386001176927033 -0.18170607436510802 0
		 -5.1190560646482606 72.093201724906905 23.152609611028105 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 0.25;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "FD6C5927-4909-2E1A-DADE-41A88C7CEB66";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "88ECA364-4252-CD5E-358E-F9A6609D835F";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "9A9D906E-4732-CFF3-DCF5-2590ACA2D628";
createNode displayLayerManager -n "layerManager";
	rename -uid "15538173-40F6-CC0A-F50E-599E09AAAF1D";
createNode displayLayer -n "defaultLayer";
	rename -uid "9742A93A-4CAA-C2B2-C8C4-E4B27F15F2AC";
	setAttr ".ufem" -type "stringArray" 0  ;
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "B63F0C6F-42BC-9B03-9A8E-56BA460A80A4";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "DF75A2D4-40E7-677B-D39C-19BD8817A48B";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "97595B33-4093-0C52-7F28-2CAA88D15319";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 1\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 1\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n"
		+ "            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n"
		+ "            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n"
		+ "            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n"
		+ "            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n"
		+ "            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n"
		+ "            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n"
		+ "            -camera \"|persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 1\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n"
		+ "            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n"
		+ "            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1842\n            -height 1066\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n"
		+ "            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n"
		+ "            -longNames 0\n            -niceNames 1\n            -selectCommand \"print(\\\"\\\")\" \n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n"
		+ "            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n"
		+ "            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -ufeFilter \"USD\" \"InactivePrims\" -ufeFilterValue 1\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
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
		+ "                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -connectionMinSegment 0.03\n                -connectionOffset 0.03\n                -connectionRoundness 0.8\n                -connectionTension -100\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n"
		+ "                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -connectionMinSegment 0.03\n                -connectionOffset 0.03\n                -connectionRoundness 0.8\n                -connectionTension -100\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n"
		+ "                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"|persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n"
		+ "                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n"
		+ "                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n"
		+ "                -clipGhosts 1\n                -bluePencil 1\n                -greasePencils 0\n                -excludeObjectPreset \"All\" \n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName; };\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n"
		+ "\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1842\\n    -height 1066\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1842\\n    -height 1066\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 50 -size 1200 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines no -displayPerspectiveLabels yes -displayOrthographicLabels yes -displayAxesBold no -perspectiveLabelPosition axis -orthographicLabelPosition axis;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "D2176D4F-463C-D376-255C-EDA56B551DE1";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 24 -ast 0 -aet 24 ";
	setAttr ".st" 6;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "6A4C9E8C-4B97-3C4C-911C-CB9106C97EC3";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -1132.1428121555439 -571.42854872204111 ;
	setAttr ".tgi[0].vh" -type "double2" 1132.1428121555439 570.23807257887017 ;
select -ne :time1;
	setAttr ".o" 0;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".ta" 3;
	setAttr ".tmrm" 1;
	setAttr ".tmr" 512;
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
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".ro" yes;
	setAttr -s 4 ".aovs";
	setAttr ".aovs[0].aov_name" -type "string" "albedo";
	setAttr ".aovs[1].aov_name" -type "string" "diffuse";
	setAttr ".aovs[2].aov_name" -type "string" "direct";
	setAttr ".aovs[3].aov_name" -type "string" "RGBA";
	setAttr ".aal" -type "attributeAlias" 8 "ai_aov_albedo" "aiCustomAOVs[0].aovName" "ai_aov_diffuse" "aiCustomAOVs[1].aovName" "ai_aov_direct" "aiCustomAOVs[2].aovName" "ai_aov_RGBA" "aiCustomAOVs[3].aovName" ;
select -ne :initialParticleSE;
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".ro" yes;
	setAttr -s 4 ".aovs";
	setAttr ".aovs[0].aov_name" -type "string" "albedo";
	setAttr ".aovs[1].aov_name" -type "string" "diffuse";
	setAttr ".aovs[2].aov_name" -type "string" "direct";
	setAttr ".aovs[3].aov_name" -type "string" "RGBA";
	setAttr ".aal" -type "attributeAlias" 8 "ai_aov_albedo" "aiCustomAOVs[0].aovName" "ai_aov_diffuse" "aiCustomAOVs[1].aovName" "ai_aov_direct" "aiCustomAOVs[2].aovName" "ai_aov_RGBA" "aiCustomAOVs[3].aovName" ;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".ren" -type "string" "arnold";
	setAttr ".outf" 51;
	setAttr ".imfkey" -type "string" "exr";
	setAttr ".dss" -type "string" "standardSurface1";
select -ne :defaultResolution;
	setAttr ".w" 1024;
	setAttr ".h" 1024;
	setAttr ".pa" 1;
	setAttr ".dar" 1;
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "C:/Program Files/Autodesk/Maya2025/resources/OCIO-configs/Maya2022-default/config.ocio";
	setAttr ".vtn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".vn" -type "string" "ACES 1.0 SDR-video";
	setAttr ".dn" -type "string" "sRGB";
	setAttr ".wsn" -type "string" "ACEScg";
	setAttr ".otn" -type "string" "ACES 1.0 SDR-video (sRGB)";
	setAttr ".potn" -type "string" "ACES 1.0 SDR-video (sRGB)";
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "root.s" "pelvis.is";
connectAttr "pelvis.s" "spine_01.is";
connectAttr "spine_01.s" "spine_02.is";
connectAttr "spine_02.s" "spine_03.is";
connectAttr "spine_03.s" "spine_04.is";
connectAttr "pelvis.s" "thigh_l.is";
connectAttr "thigh_l.s" "calf_l.is";
connectAttr "calf_l.s" "calf_twist_02_l.is";
connectAttr "calf_l.s" "calf_twist_01_l.is";
connectAttr "calf_l.s" "foot_l.is";
connectAttr "foot_l.s" "ball_l.is";
connectAttr "thigh_l.s" "thigh_twist_01_l.is";
connectAttr "thigh_l.s" "thigh_twist_02_l.is";
connectAttr "pelvis.s" "thigh_r.is";
connectAttr "thigh_r.s" "calf_r.is";
connectAttr "calf_r.s" "calf_twist_02_r.is";
connectAttr "calf_r.s" "calf_twist_01_r.is";
connectAttr "calf_r.s" "foot_r.is";
connectAttr "foot_r.s" "ball_r.is";
connectAttr "thigh_r.s" "thigh_twist_01_r.is";
connectAttr "thigh_r.s" "thigh_twist_02_r.is";
connectAttr "pelvis.s" "ezorLeatherStrip_left_a01_jnt.is";
connectAttr "ezorLeatherStrip_left_a01_jnt.s" "ezorLeatherStrip_left_a02_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_a02_jnt.s" "ezorLeatherStrip_left_a03_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_a03_jnt.s" "ezorLeatherStrip_left_a04_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_a04_jnt.s" "ezorLeatherStrip_left_a05_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_a05_jnt.s" "ezorLeatherStrip_left_a06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_left_b01_jnt.is";
connectAttr "ezorLeatherStrip_left_b01_jnt.s" "ezorLeatherStrip_left_b02_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_b02_jnt.s" "ezorLeatherStrip_left_b03_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_b03_jnt.s" "ezorLeatherStrip_left_b04_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_b04_jnt.s" "ezorLeatherStrip_left_b05_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_b05_jnt.s" "ezorLeatherStrip_left_b06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_left_c01_jnt.is";
connectAttr "ezorLeatherStrip_left_c01_jnt.s" "ezorLeatherStrip_left_c02_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_c02_jnt.s" "ezorLeatherStrip_left_c03_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_c03_jnt.s" "ezorLeatherStrip_left_c04_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_c04_jnt.s" "ezorLeatherStrip_left_c05_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_c05_jnt.s" "ezorLeatherStrip_left_c06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_left_d01_jnt.is";
connectAttr "ezorLeatherStrip_left_d01_jnt.s" "ezorLeatherStrip_left_d02_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_d02_jnt.s" "ezorLeatherStrip_left_d03_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_d03_jnt.s" "ezorLeatherStrip_left_d04_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_d04_jnt.s" "ezorLeatherStrip_left_d05_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_d05_jnt.s" "ezorLeatherStrip_left_d06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_left_e01_jnt.is";
connectAttr "ezorLeatherStrip_left_e01_jnt.s" "ezorLeatherStrip_left_e02_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_e02_jnt.s" "ezorLeatherStrip_left_e03_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_e03_jnt.s" "ezorLeatherStrip_left_e04_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_e04_jnt.s" "ezorLeatherStrip_left_e05_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_e05_jnt.s" "ezorLeatherStrip_left_e06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_left_f01_jnt.is";
connectAttr "ezorLeatherStrip_left_f01_jnt.s" "ezorLeatherStrip_left_f02_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_f02_jnt.s" "ezorLeatherStrip_left_f03_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_f03_jnt.s" "ezorLeatherStrip_left_f04_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_f04_jnt.s" "ezorLeatherStrip_left_f05_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_f05_jnt.s" "ezorLeatherStrip_left_f06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_left_g01_jnt.is";
connectAttr "ezorLeatherStrip_left_g01_jnt.s" "ezorLeatherStrip_left_g02_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_g02_jnt.s" "ezorLeatherStrip_left_g03_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_g03_jnt.s" "ezorLeatherStrip_left_g04_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_g04_jnt.s" "ezorLeatherStrip_left_g05_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_g05_jnt.s" "ezorLeatherStrip_left_g06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_left_h01_jnt.is";
connectAttr "ezorLeatherStrip_left_h01_jnt.s" "ezorLeatherStrip_left_h02_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_h02_jnt.s" "ezorLeatherStrip_left_h03_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_h03_jnt.s" "ezorLeatherStrip_left_h04_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_h04_jnt.s" "ezorLeatherStrip_left_h05_jnt.is"
		;
connectAttr "ezorLeatherStrip_left_h05_jnt.s" "ezorLeatherStrip_left_h06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_right_h01_jnt.is";
connectAttr "ezorLeatherStrip_right_h01_jnt.s" "ezorLeatherStrip_right_h02_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_h02_jnt.s" "ezorLeatherStrip_right_h03_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_h03_jnt.s" "ezorLeatherStrip_right_h04_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_h04_jnt.s" "ezorLeatherStrip_right_h05_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_h05_jnt.s" "ezorLeatherStrip_right_h06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_right_g01_jnt.is";
connectAttr "ezorLeatherStrip_right_g01_jnt.s" "ezorLeatherStrip_right_g02_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_g02_jnt.s" "ezorLeatherStrip_right_g03_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_g03_jnt.s" "ezorLeatherStrip_right_g04_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_g04_jnt.s" "ezorLeatherStrip_right_g05_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_g05_jnt.s" "ezorLeatherStrip_right_g06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_right_f01_jnt.is";
connectAttr "ezorLeatherStrip_right_f01_jnt.s" "ezorLeatherStrip_right_f02_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_f02_jnt.s" "ezorLeatherStrip_right_f03_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_f03_jnt.s" "ezorLeatherStrip_right_f04_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_f04_jnt.s" "ezorLeatherStrip_right_f05_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_f05_jnt.s" "ezorLeatherStrip_right_f06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_right_e01_jnt.is";
connectAttr "ezorLeatherStrip_right_e01_jnt.s" "ezorLeatherStrip_right_e02_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_e02_jnt.s" "ezorLeatherStrip_right_e03_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_e03_jnt.s" "ezorLeatherStrip_right_e04_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_e04_jnt.s" "ezorLeatherStrip_right_e05_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_e05_jnt.s" "ezorLeatherStrip_right_e06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_right_d01_jnt.is";
connectAttr "ezorLeatherStrip_right_d01_jnt.s" "ezorLeatherStrip_right_d02_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_d02_jnt.s" "ezorLeatherStrip_right_d03_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_d03_jnt.s" "ezorLeatherStrip_right_d04_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_d04_jnt.s" "ezorLeatherStrip_right_d05_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_d05_jnt.s" "ezorLeatherStrip_right_d06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_right_c01_jnt.is";
connectAttr "ezorLeatherStrip_right_c01_jnt.s" "ezorLeatherStrip_right_c02_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_c02_jnt.s" "ezorLeatherStrip_right_c03_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_c03_jnt.s" "ezorLeatherStrip_right_c04_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_c04_jnt.s" "ezorLeatherStrip_right_c05_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_c05_jnt.s" "ezorLeatherStrip_right_c06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_right_b01_jnt.is";
connectAttr "ezorLeatherStrip_right_b01_jnt.s" "ezorLeatherStrip_right_b02_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_b02_jnt.s" "ezorLeatherStrip_right_b03_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_b03_jnt.s" "ezorLeatherStrip_right_b04_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_b04_jnt.s" "ezorLeatherStrip_right_b05_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_b05_jnt.s" "ezorLeatherStrip_right_b06_jnt.is"
		;
connectAttr "pelvis.s" "ezorLeatherStrip_right_a01_jnt.is";
connectAttr "ezorLeatherStrip_right_a01_jnt.s" "ezorLeatherStrip_right_a02_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_a02_jnt.s" "ezorLeatherStrip_right_a03_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_a03_jnt.s" "ezorLeatherStrip_right_a04_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_a04_jnt.s" "ezorLeatherStrip_right_a05_jnt.is"
		;
connectAttr "ezorLeatherStrip_right_a05_jnt.s" "ezorLeatherStrip_right_a06_jnt.is"
		;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of skeleton.ma
