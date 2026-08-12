//Maya ASCII 2026 scene
//Name: propExample_rig.ma
//Last modified: Tue, Aug 11, 2026 06:13:10 PM
//Codeset: 1252
requires maya "2026";
requires "stereoCamera" "10.0";
requires -nodeType "aiOptions" -nodeType "aiImagerDenoiserOidn" "mtoa" "5.6.3";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2026";
fileInfo "version" "2026";
fileInfo "cutIdentifier" "202510291147-60ec9eda33";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 26200)";
fileInfo "UUID" "EA3E2317-4A3C-5A1C-859C-28A31644F2F4";
createNode transform -s -n "persp";
	rename -uid "912ED059-4B31-9202-F02B-F689C1C4F289";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 2880 2160 2880 ;
	setAttr ".r" -type "double3" -27.938352729602379 44.999999999999972 -5.172681101354183e-14 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "91A80F57-44FA-9F6D-79CB-E5BCE36AE157";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 4610.2494509516509;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "F65A966B-4AC2-B75A-2105-7DB2B74C7DA2";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "8F2007B0-42E2-EDC6-20EE-318B7228AFA2";
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
	rename -uid "A9698CEB-4C7C-6780-29C0-9E8041B58286";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "3452CE92-4F6C-D1B9-57A8-B692C880A105";
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
	rename -uid "820FA92E-4348-4701-B8F3-65A14E437CC6";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "168FA684-48AE-683B-6E42-84ABB4D0430D";
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
createNode transform -n "main_skeletalMeshGrp";
	rename -uid "683DFFE1-42F5-5AFF-3379-5A97EEAA3465";
createNode joint -n "propMain_jnt" -p "main_skeletalMeshGrp";
	rename -uid "9465D106-4D2B-FA0D-BD5D-6C889C0D9EA2";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc";
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 90.000000000000014 0 90.000000000000057 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" -1.1102230246251565e-15 1 0 0 2.2204460492503123e-16 0 0.99999999999999967 0
		 0.99999999999999989 1.1102230246251563e-15 -2.2204460492503128e-16 0 0 0 0 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 4;
	setAttr ".fbxID" 5;
createNode joint -n "propTop_jnt" -p "propMain_jnt";
	rename -uid "7CE8FFBE-43C9-18A5-54E6-97A0269CAD8E";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc";
	setAttr ".t" -type "double3" 99.780136108398438 2.4868995751603516e-14 3.3892045337015419e-08 ;
	setAttr ".r" -type "double3" 4.9696166897867451e-15 0 0 ;
	setAttr ".s" -type "double3" 1 0.99999999999999967 0.99999999999999989 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" -1.1102230246251565e-15 1 0 0 2.2204460492503116e-16 0 0.99999999999999933 0
		 0.99999999999999978 1.1102230246251561e-15 -2.2204460492503126e-16 0 3.3891934558810904e-08 99.780136108398438 2.486899574407796e-14 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 2;
	setAttr ".fbxID" 5;
createNode parentConstraint -n "propMain_jntParentConstraint" -p "propMain_jnt";
	rename -uid "EA832F5E-457D-DEB6-7665-D48E6D52E5BD";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "prop_ctrlW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode scaleConstraint -n "propMain_jntScaleConstraint" -p "propMain_jnt";
	rename -uid "DF2F624E-442F-ED3A-D60A-09ADD00E2240";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "prop_ctrlW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "prop_geo" -p "main_skeletalMeshGrp";
	rename -uid "90907B63-48D3-861A-F3ED-0C93451BF431";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode mesh -n "prop_geoShape" -p "prop_geo";
	rename -uid "93D41EDB-4F32-733F-499F-C2BBD860A73C";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.10174348577857018 0.50070997048169374 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcol" yes;
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".vcs" 2;
createNode mesh -n "prop_geoShapeOrig" -p "prop_geo";
	rename -uid "70CAA9FF-4DD1-5EC2-7667-43BED0D92A0F";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 138 ".uvst[0].uvsp[0:137]" -type "float2" 0.781138 0.15441893
		 0.78261977 0.16903791 0.67148882 0.027530469 0.66830963 0.17088234 0.66651839 0.15031385
		 0.78010845 0.13956858 0.78140146 0.065064102 0.6687755 0.047820702 0.78024793 0.079886146
		 0.66686618 0.068342753 0.77956295 0.094808854 0.66569251 0.088891342 0.77931893 0.10970885
		 0.66524458 0.10930056 0.77949238 0.12462701 0.66551572 0.12972367 0.94520485 0.14794771
		 0.94452965 0.13535954 0.94356114 0.097595088 0.94464368 0.084939882 0.94291657 0.11017738
		 0.94537342 0.072340272 0.94586563 0.060111832 0.94350642 0.12273271 0.95127082 0.1483359
		 0.94992065 0.13525501 0.95747316 0.13482089 0.95909691 0.14820023 0.94909424 0.097747162
		 0.95003355 0.085077599 0.95758474 0.085552938 0.95670795 0.098151393 0.94848102 0.11018018
		 0.95594919 0.11019166 0.95144558 0.071995795 0.95270205 0.057585198 0.96162397 0.16307324
		 0.95927298 0.072176538 0.94904166 0.12260088 0.9566558 0.12222781 0.96507812 0.1339279
		 0.96664357 0.14674331 0.96518713 0.086483143 0.96447378 0.098671161 0.96332937 0.11020567
		 0.97025657 0.16056514 0.96681339 0.073671222 0.96442157 0.12174258 0.98181325 0.125065
		 0.99256539 0.12077911 0.98188919 0.095436521 0.97129107 0.099633202 0.96968442 0.11021969
		 0.99707031 0.11029079 0.99262005 0.099778906 0.9712407 0.12081292 0.9826616 0.11025273
		 0.52171504 0.08387693 0.52250051 0.058822136 0.52374113 0.033779908 0.52543819 0.0089532137
		 0.52137721 0.10874057 0.52148587 0.13361076 0.52204227 0.1586847 0.52305722 0.18375701
		 0.36605725 0.081811264 0.36603862 0.055416949 0.36592862 0.029050531 0.36463591 0.21312688
		 0.36597145 0.10801047 0.36577657 0.13421215 0.36547643 0.16061379 0.36508733 0.18699154
		 0.21127176 0.058214497 0.21234047 0.082687877 0.066693321 0.087927118 0.064048082
		 0.07011956 0.20945928 0.033872306 0.059805579 0.052519199 0.20550999 0.20433186 0.052926611
		 0.17542835 0.21259312 0.10704357 0.067459151 0.10568243 0.21199898 0.13140954 0.066279143
		 0.1233862 0.21057194 0.15591238 0.063230149 0.14103626 0.20837064 0.1802959 0.058586188
		 0.15840037 0.03846975 0.077092364 0.041647054 0.091339514 0.027539833 0.094302662
		 0.02492639 0.083202615 0.032876946 0.063329756 0.020074477 0.072691493 0.023770561
		 0.15894517 0.011912557 0.064082921 0.042675782 0.10549867 0.028690292 0.10525084
		 0.041280851 0.11956318 0.027301176 0.116138 0.037735511 0.1335576 0.024430208 0.12704924
		 0.031853687 0.14683671 0.019379977 0.13724062 0.020461109 0.096755728 0.013250615
		 0.094568923 0.0059781899 0.097807333 0.0029296875 0.10508393 0.021785518 0.10517256
		 0.020298384 0.11355164 0.01312625 0.11568122 0.0059053674 0.11238473 0.012771975
		 0.10512367 0.78294486 0.050404068 0.94561154 0.16022956 0.95244414 0.16277714 0.054663368
		 0.035206068 0.024767656 0.050414182 0.36574978 0.0029296875 0.20702082 0.0098679624
		 0.014090915 0.13171765 0.008839462 0.07252647 0.0081773838 0.13712181 0.018409919
		 0.12359693 0.014667559 0.078160539 0.01110144 0.14549026 0.018828785 0.086549684
		 0.52453405 0.20862351 0.67088115 0.19127266 0.97651392 0.15588614 0.97672802 0.064575486
		 0.97314876 0.14489673 0.97331053 0.075547725 0.97135293 0.087420262 0.97124702 0.13301896
		 0.97049373 0.059869934 0.96187639 0.057325169;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcol" yes;
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 41 ".pt";
	setAttr ".pt[5]" -type "float3" 7.5709288e-08 -0.43664482 -0.12263913 ;
	setAttr ".pt[6]" -type "float3" 0.085882425 -0.43664584 -0.086718544 ;
	setAttr ".pt[7]" -type "float3" 0.12180237 -0.43664584 -4.7404119e-11 ;
	setAttr ".pt[8]" -type "float3" 0.085881755 -0.43664584 0.086718537 ;
	setAttr ".pt[9]" -type "float3" 7.5709288e-08 -0.43664584 0.12263913 ;
	setAttr ".pt[13]" -type "float3" -0.085882291 -0.43664584 -0.086718544 ;
	setAttr ".pt[14]" -type "float3" -0.12180243 -0.43664584 -4.7404119e-11 ;
	setAttr ".pt[15]" -type "float3" -0.08588139 -0.43664584 0.086718537 ;
	setAttr ".pt[16]" -type "float3" -0.41784522 -0.52158862 0.42191568 ;
	setAttr ".pt[17]" -type "float3" -0.59261239 -0.52158862 1.9355542e-10 ;
	setAttr ".pt[18]" -type "float3" 0.59261256 -0.52158862 1.9355542e-10 ;
	setAttr ".pt[19]" -type "float3" 0.41784304 -0.52158862 -0.42191568 ;
	setAttr ".pt[20]" -type "float3" 7.1864939e-08 -0.52158862 -0.59668154 ;
	setAttr ".pt[21]" -type "float3" 7.1864939e-08 -0.5215857 0.59668154 ;
	setAttr ".pt[22]" -type "float3" 0.41784525 -0.52158862 0.42191568 ;
	setAttr ".pt[23]" -type "float3" -0.41784281 -0.52158862 -0.42191568 ;
	setAttr ".pt[24]" -type "float3" -0.46900988 -0.75129366 0.47357589 ;
	setAttr ".pt[25]" -type "float3" -0.66517246 -0.75138283 2.1803552e-10 ;
	setAttr ".pt[26]" -type "float3" 0.66517252 -0.75138283 2.1803552e-10 ;
	setAttr ".pt[27]" -type "float3" 0.46900696 -0.75129366 -0.47357589 ;
	setAttr ".pt[28]" -type "float3" 7.1462019e-08 -0.75108218 -0.66973996 ;
	setAttr ".pt[29]" -type "float3" 7.1462019e-08 -0.75108039 0.66973996 ;
	setAttr ".pt[30]" -type "float3" 0.46900988 -0.75129366 0.47357589 ;
	setAttr ".pt[31]" -type "float3" -0.46900672 -0.75129366 -0.47357589 ;
	setAttr ".pt[32]" -type "float3" -0.49941909 -0.11343309 0.50428164 ;
	setAttr ".pt[33]" -type "float3" -0.70830059 -0.11331768 2.3277223e-10 ;
	setAttr ".pt[34]" -type "float3" 0.70830065 -0.11331768 2.3277223e-10 ;
	setAttr ".pt[35]" -type "float3" 0.4994154 -0.11343309 -0.50428164 ;
	setAttr ".pt[36]" -type "float3" 6.7497673e-08 -0.11370827 -0.71316499 ;
	setAttr ".pt[37]" -type "float3" 6.7497673e-08 -0.11370514 0.71316499 ;
	setAttr ".pt[38]" -type "float3" 0.49941924 -0.11343309 0.50428164 ;
	setAttr ".pt[39]" -type "float3" -0.49941534 -0.11343309 -0.50428164 ;
	setAttr ".pt[40]" -type "float3" -0.58890051 -0.018649984 0.59463418 ;
	setAttr ".pt[41]" -type "float3" -0.83520722 -0.01848593 2.759083e-10 ;
	setAttr ".pt[42]" -type "float3" 0.83520728 -0.01848593 2.759083e-10 ;
	setAttr ".pt[43]" -type "float3" 0.58889616 -0.018649984 -0.59463418 ;
	setAttr ".pt[44]" -type "float3" 8.0329634e-08 -0.019041117 -0.84094459 ;
	setAttr ".pt[45]" -type "float3" 8.0329634e-08 -0.019037649 0.84094459 ;
	setAttr ".pt[46]" -type "float3" 0.58890057 -0.018649984 0.59463418 ;
	setAttr ".pt[47]" -type "float3" -0.5888961 -0.018649984 -0.59463418 ;
	setAttr ".pt[48]" -type "float3" 7.1864939e-08 0.014992325 1.9203112e-18 ;
	setAttr -s 114 ".vt[0:113]"  2.2147646 23.22196198 -2.23575234 0 23.22192574 -3.16184139
		 0 23.22196198 3.16184115 2.21475363 23.22196198 2.23575211 3.14084935 23.22196198 1.9814607e-08
		 0 -8.78012753 -1.74060774 1.21892238 -8.78012085 -1.23079145 1.72873557 -8.78012085 -5.7958216e-10
		 1.21891439 -8.78012085 1.23079121 0 -8.78012085 1.74060774 -2.2147646 23.22196198 -2.23575234
		 -2.21475363 23.22196198 2.23575211 -3.14084935 23.22196198 1.9814607e-08 -1.21892238 -8.78012085 -1.23079145
		 -1.72873557 -8.78012085 -5.7958216e-10 -1.21891439 -8.78012085 1.23079121 2.086740494 -9.18594933 -2.107059
		 2.95951724 -9.18594933 -9.922192e-10 -2.95951724 -9.18594933 -9.922192e-10 -2.08672595 -9.18594933 2.107059
		 0 -9.18594933 2.97984457 0 -9.18596268 -2.97984457 -2.086740494 -9.18594933 -2.107059
		 2.08672595 -9.18594933 2.107059 2.30428267 -9.84975052 -2.32671928 3.26804638 -9.84975052 -1.0956573e-09
		 -3.26804638 -9.84975052 -1.0956573e-09 -2.30426693 -9.84975052 2.32671905 0 -9.84975052 3.29049039
		 0 -9.84976387 -3.29049039 -2.30428267 -9.84975052 -2.32671928 2.30426693 -9.84975052 2.32671905
		 2.14616251 -11.37074852 -2.16705918 3.043792963 -11.37118721 -1.0204734e-09 -3.043792963 -11.37118721 -1.0204734e-09
		 -2.14614749 -11.37074852 2.16705918 0 -11.3697052 3.064697504 0 -11.36971855 -3.064697504
		 -2.14616251 -11.37074852 -2.16705918 2.14614749 -11.37074852 2.16705918 1.78039205 -11.96928596 -1.79772747
		 2.52503896 -11.96978188 -8.4655422e-10 -2.52503896 -11.96978188 -8.4655422e-10 -1.78037918 -11.96928596 1.79772747
		 0 -11.96810341 2.54238153 0 -11.9681139 -2.54238153 -1.78039205 -11.96928596 -1.79772747
		 1.78037918 -11.96928596 1.79772747 0 -12.23491859 -2.7019342e-11 -2.68571377 40.14924622 2.71117711
		 -3.80874109 40.14924622 -5.9145036e-09 -2.68572688 40.14924622 -2.71117759 0 40.14920425 -3.83419728
		 0 40.14924622 3.83419633 2.68571377 40.14924622 2.71117711 3.80874109 40.14924622 -5.9145036e-09
		 2.68572688 40.14924622 -2.71117759 -2.60247612 76.65042877 2.6271503 -3.69069815 76.65042877 2.9169081e-08
		 -2.60248947 76.65042877 -2.62715077 0 76.65042114 -3.71536469 0 76.65042877 3.71536469
		 2.60247612 76.65042877 2.6271503 3.69069815 76.65042877 2.9169081e-08 2.60248947 76.65042877 -2.62715077
		 -1.67782772 97.2746048 1.69373441 -2.37942791 97.27456665 -1.039797e-07 -1.67783582 97.2746048 -1.69373488
		 0 97.27468872 -2.39525938 0 97.27471161 2.3952589 1.67782772 97.2746048 1.69373441
		 2.37942791 97.27456665 -1.039797e-07 1.67783582 97.2746048 -1.69373488 -1.28721905 98.96088409 1.29942346
		 -1.82546711 98.96143341 -1.3278833e-07 -1.28722525 98.96088409 -1.29942393 0 98.95954895 -1.83766997
		 0 98.95955658 1.83766949 1.28721905 98.96088409 1.29942346 1.82546711 98.96143341 -1.3278833e-07
		 1.28722525 98.96088409 -1.29942393 -0.80152673 99.48959351 0.8091234 -1.13668251 99.48993683 -1.7834606e-07
		 -0.80152988 99.48959351 -0.80912399 0 99.48880005 -1.14427876 0 99.48881531 1.14427829
		 0.80152673 99.48959351 0.8091234 1.13668251 99.48993683 -1.7834606e-07 0.80152988 99.48959351 -0.80912399
		 0 99.78013611 -2.5205094e-07 -2.81578445 58.48843384 2.8424809 -3.99320173 58.48843384 5.1397159e-08
		 -2.81579852 58.48843384 -2.84248161 0 58.48841858 -4.019886971 2.81579852 58.48843384 -2.84248161
		 3.99320173 58.48843384 5.1397159e-08 2.81578445 58.48843384 2.8424809 0 58.4884491 4.019886971
		 -1.95716238 94.075622559 1.97571838 -2.77570128 94.075317383 -1.2563645e-07 -1.9571718 94.075622559 -1.97571886
		 0 94.076339722 -2.79372454 1.9571718 94.075622559 -1.97571886 2.77570128 94.075317383 -1.2563645e-07
		 1.95716238 94.075622559 1.97571838 0 94.076370239 2.79372334 0 9.9578476 -2.26315832
		 -1.58101153 9.95942688 -1.59578288 -2.23938251 9.9601326 1.358484e-06 -1.58101141 9.95945168 1.59578812
		 0 9.95786285 2.26315022 1.58101141 9.95945168 1.59578812 2.23938251 9.9601326 1.358484e-06
		 1.58101153 9.95942688 -1.59578288;
	setAttr -s 232 ".ed";
	setAttr ".ed[0:165]"  1 106 0 6 113 0 7 112 0 8 111 0 9 110 0 6 7 0 11 12 0
		 12 10 0 10 1 0 13 107 0 14 108 0 15 109 0 14 15 0 15 9 0 2 11 0 5 13 0 2 3 0 8 9 0
		 3 4 0 7 8 0 4 0 0 13 14 0 0 1 0 5 6 0 6 16 0 16 17 0 18 19 0 19 20 0 21 22 0 23 20 0
		 17 23 0 22 18 0 21 16 0 16 24 0 17 25 0 24 25 0 18 26 0 19 27 0 26 27 0 20 28 0 27 28 0
		 21 29 0 22 30 0 29 30 0 23 31 0 31 28 0 25 31 0 30 26 0 29 24 0 24 32 0 25 33 0 32 33 0
		 26 34 0 27 35 0 34 35 0 28 36 0 35 36 0 29 37 0 30 38 0 37 38 0 31 39 0 39 36 0 33 39 0
		 38 34 0 37 32 0 32 40 0 33 41 0 40 41 0 34 42 0 35 43 0 42 43 0 36 44 0 43 44 0 37 45 0
		 38 46 0 45 46 0 39 47 0 47 44 0 41 47 0 46 42 0 45 40 0 40 48 0 41 48 0 42 48 0 43 48 0
		 44 48 0 45 48 0 46 48 0 47 48 0 11 49 0 12 50 0 49 50 0 10 51 0 50 51 0 1 52 0 51 52 0
		 2 53 0 53 49 0 3 54 0 53 54 0 4 55 0 54 55 0 0 56 0 55 56 0 56 52 0 49 90 0 50 91 0
		 57 58 0 51 92 0 58 59 0 52 93 0 59 60 0 53 97 0 61 57 0 54 96 0 61 62 0 55 95 0 62 63 0
		 56 94 0 63 64 0 64 60 0 57 98 0 58 99 0 65 66 0 59 100 0 66 67 0 60 101 0 67 68 0
		 61 105 0 69 65 0 62 104 0 69 70 0 63 103 0 70 71 0 64 102 0 71 72 0 72 68 0 65 73 0
		 66 74 0 73 74 0 67 75 0 74 75 0 68 76 0 75 76 0 69 77 0 77 73 0 70 78 0 77 78 0 71 79 0
		 78 79 0 72 80 0 79 80 0 80 76 0 73 81 0 74 82 0 81 82 0 75 83 0 82 83 0 76 84 0 83 84 0
		 77 85 0 85 81 0 78 86 0 85 86 0 79 87 0 86 87 0;
	setAttr ".ed[166:231]" 80 88 0 87 88 0 88 84 0 81 89 0 82 89 0 83 89 0 84 89 0
		 85 89 0 86 89 0 87 89 0 88 89 0 90 57 0 91 58 0 92 59 0 93 60 0 94 64 0 95 63 0 96 62 0
		 97 61 0 90 91 0 91 92 0 92 93 0 93 94 0 94 95 0 95 96 0 96 97 0 97 90 0 98 65 0 99 66 0
		 100 67 0 101 68 0 102 72 0 103 71 0 104 70 0 105 69 0 98 99 0 99 100 0 100 101 0
		 101 102 0 102 103 0 103 104 0 104 105 0 105 98 0 5 21 0 13 22 0 14 18 0 15 19 0 9 20 0
		 8 23 0 7 17 0 106 5 0 107 10 0 108 12 0 109 11 0 110 2 0 111 3 0 112 4 0 113 0 0
		 106 107 0 107 108 0 108 109 0 109 110 0 110 111 0 111 112 0 112 113 0 113 106 0;
	setAttr -s 120 -ch 464 ".fc[0:119]" -type "polyFaces" 
		f 4 231 -1 -23 -224
		mu 0 4 0 1 129 3
		f 4 -223 230 223 -21
		mu 0 4 4 5 0 3
		f 4 224 217 8 0
		mu 0 4 114 6 7 2
		f 4 -218 225 218 7
		mu 0 4 7 6 8 9
		f 4 226 219 6 -219
		mu 0 4 8 10 11 9
		f 4 227 220 14 -220
		mu 0 4 10 12 13 11
		f 4 228 221 -17 -221
		mu 0 4 12 14 15 13
		f 4 229 222 -19 -222
		mu 0 4 14 5 4 15
		f 4 -25 5 215 -26
		mu 0 4 24 16 17 25
		f 4 -13 211 26 -213
		mu 0 4 18 19 29 28
		f 4 -14 212 27 -214
		mu 0 4 20 18 28 32
		f 4 -16 209 28 -211
		mu 0 4 21 22 35 34
		f 4 17 213 -30 -215
		mu 0 4 23 20 32 38
		f 4 19 214 -31 -216
		mu 0 4 17 23 38 25
		f 4 -22 210 31 -212
		mu 0 4 19 21 34 29
		f 4 23 24 -33 -210
		mu 0 4 115 16 24 116
		f 4 25 34 -36 -34
		mu 0 4 24 25 26 27
		f 4 -27 36 38 -38
		mu 0 4 28 29 30 31
		f 4 -28 37 40 -40
		mu 0 4 32 28 31 33
		f 4 -29 41 43 -43
		mu 0 4 34 35 137 37
		f 4 29 39 -46 -45
		mu 0 4 38 32 33 39
		f 4 30 44 -47 -35
		mu 0 4 25 38 39 26
		f 4 -32 42 47 -37
		mu 0 4 29 34 37 30
		f 4 32 33 -49 -42
		mu 0 4 116 24 27 36
		f 4 35 50 -52 -50
		mu 0 4 27 26 40 41
		f 4 -39 52 54 -54
		mu 0 4 31 30 42 43
		f 4 -41 53 56 -56
		mu 0 4 33 31 43 44
		f 4 -44 57 59 -59
		mu 0 4 37 137 136 46
		f 4 45 55 -62 -61
		mu 0 4 39 33 44 47
		f 4 46 60 -63 -51
		mu 0 4 26 39 47 40
		f 4 -48 58 63 -53
		mu 0 4 30 37 46 42
		f 4 48 49 -65 -58
		mu 0 4 36 27 41 45
		f 4 51 66 -68 -66
		mu 0 4 41 40 135 132
		f 4 -55 68 70 -70
		mu 0 4 43 42 134 51
		f 4 -57 69 72 -72
		mu 0 4 44 43 51 52
		f 4 -60 73 75 -75
		mu 0 4 46 136 131 133
		f 4 61 71 -78 -77
		mu 0 4 47 44 52 55
		f 4 62 76 -79 -67
		mu 0 4 40 47 55 135
		f 4 -64 74 79 -69
		mu 0 4 42 46 133 134
		f 4 64 65 -81 -74
		mu 0 4 45 41 132 130
		f 3 67 82 -82
		mu 0 3 49 48 56
		f 3 -71 83 -85
		mu 0 3 51 50 56
		f 3 -73 84 -86
		mu 0 3 52 51 56
		f 3 -76 86 -88
		mu 0 3 54 53 56
		f 3 77 85 -89
		mu 0 3 55 52 56
		f 3 78 88 -83
		mu 0 3 48 55 56
		f 3 -80 87 -84
		mu 0 3 50 54 56
		f 3 80 81 -87
		mu 0 3 53 49 56
		f 4 -7 89 91 -91
		mu 0 4 9 11 57 58
		f 4 -8 90 93 -93
		mu 0 4 7 9 58 59
		f 4 -9 92 95 -95
		mu 0 4 2 7 59 60
		f 4 -15 96 97 -90
		mu 0 4 11 13 61 57
		f 4 16 98 -100 -97
		mu 0 4 13 15 62 61
		f 4 18 100 -102 -99
		mu 0 4 15 4 63 62
		f 4 20 102 -104 -101
		mu 0 4 4 3 64 63
		f 4 22 94 -105 -103
		mu 0 4 3 129 128 64
		f 4 -92 105 185 -107
		mu 0 4 58 57 65 66
		f 4 -94 106 186 -109
		mu 0 4 59 58 66 67
		f 4 -96 108 187 -111
		mu 0 4 60 59 67 119
		f 4 -98 112 192 -106
		mu 0 4 57 61 69 65
		f 4 99 114 191 -113
		mu 0 4 61 62 70 69
		f 4 101 116 190 -115
		mu 0 4 62 63 71 70
		f 4 103 118 189 -117
		mu 0 4 63 64 72 71
		f 4 104 110 188 -119
		mu 0 4 64 128 68 72
		f 4 -108 121 201 -123
		mu 0 4 73 74 75 76
		f 4 -110 122 202 -125
		mu 0 4 77 73 76 78
		f 4 -112 124 203 -127
		mu 0 4 120 77 78 117
		f 4 -114 128 208 -122
		mu 0 4 74 81 82 75
		f 4 115 130 207 -129
		mu 0 4 81 83 84 82
		f 4 117 132 206 -131
		mu 0 4 83 85 86 84
		f 4 119 134 205 -133
		mu 0 4 85 87 88 86
		f 4 120 126 204 -135
		mu 0 4 87 79 80 88
		f 4 -124 137 139 -139
		mu 0 4 89 90 91 92
		f 4 -126 138 141 -141
		mu 0 4 93 89 92 94
		f 4 -128 140 143 -143
		mu 0 4 118 93 94 96
		f 4 -130 144 145 -138
		mu 0 4 90 97 98 91
		f 4 131 146 -148 -145
		mu 0 4 97 99 100 98
		f 4 133 148 -150 -147
		mu 0 4 99 101 102 100
		f 4 135 150 -152 -149
		mu 0 4 101 103 104 102
		f 4 136 142 -153 -151
		mu 0 4 103 95 126 104
		f 4 -140 153 155 -155
		mu 0 4 92 91 105 127
		f 4 -142 154 157 -157
		mu 0 4 94 92 127 125
		f 4 -144 156 159 -159
		mu 0 4 96 94 125 122
		f 4 -146 160 161 -154
		mu 0 4 91 98 109 105
		f 4 147 162 -164 -161
		mu 0 4 98 100 110 109
		f 4 149 164 -166 -163
		mu 0 4 100 102 124 110
		f 4 151 166 -168 -165
		mu 0 4 102 104 121 124
		f 4 152 158 -169 -167
		mu 0 4 104 126 123 121
		f 3 -156 169 -171
		mu 0 3 106 105 113
		f 3 -158 170 -172
		mu 0 3 107 106 113
		f 3 -160 171 -173
		mu 0 3 108 107 113
		f 3 -162 173 -170
		mu 0 3 105 109 113
		f 3 163 174 -174
		mu 0 3 109 110 113
		f 3 165 175 -175
		mu 0 3 110 111 113
		f 3 167 176 -176
		mu 0 3 111 112 113
		f 3 168 172 -177
		mu 0 3 112 108 113
		f 4 -186 177 107 -179
		mu 0 4 66 65 74 73
		f 4 -187 178 109 -180
		mu 0 4 67 66 73 77
		f 4 -188 179 111 -181
		mu 0 4 119 67 77 120
		f 4 -189 180 -121 -182
		mu 0 4 72 68 79 87
		f 4 -190 181 -120 -183
		mu 0 4 71 72 87 85
		f 4 -191 182 -118 -184
		mu 0 4 70 71 85 83
		f 4 -192 183 -116 -185
		mu 0 4 69 70 83 81
		f 4 -193 184 113 -178
		mu 0 4 65 69 81 74
		f 4 -202 193 123 -195
		mu 0 4 76 75 90 89
		f 4 -203 194 125 -196
		mu 0 4 78 76 89 93
		f 4 -204 195 127 -197
		mu 0 4 117 78 93 118
		f 4 -205 196 -137 -198
		mu 0 4 88 80 95 103
		f 4 -206 197 -136 -199
		mu 0 4 86 88 103 101
		f 4 -207 198 -134 -200
		mu 0 4 84 86 101 99
		f 4 -208 199 -132 -201
		mu 0 4 82 84 99 97
		f 4 -209 200 129 -194
		mu 0 4 75 82 97 90
		f 4 9 -225 216 15
		mu 0 4 21 6 114 22
		f 4 -226 -10 21 10
		mu 0 4 8 6 21 19
		f 4 11 -227 -11 12
		mu 0 4 18 10 8 19
		f 4 4 -228 -12 13
		mu 0 4 20 12 10 18
		f 4 3 -229 -5 -18
		mu 0 4 23 14 12 20
		f 4 2 -230 -4 -20
		mu 0 4 17 5 14 23
		f 4 -231 -3 -6 1
		mu 0 4 0 5 17 16
		f 4 -217 -232 -2 -24
		mu 0 4 115 1 0 16;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "main_rigGrp";
	rename -uid "5A6CF381-4A7D-D7C5-CD66-5992A8C48B52";
createNode transform -n "prop_ctrlGrp" -p "main_rigGrp";
	rename -uid "CD3F1E11-4D16-E7FD-D621-61AC3A59C3AA";
	setAttr ".r" -type "double3" 90.000000000000014 0 90.000000000000057 ;
	setAttr ".s" -type "double3" 1 0.99999999999999967 0.99999999999999989 ;
createNode transform -n "prop_ctrlPrntGrp" -p "prop_ctrlGrp";
	rename -uid "22656790-4ACC-6670-E9ED-06AB01DC5226";
createNode transform -n "prop_ctrlPrntSwchGrp" -p "prop_ctrlPrntGrp";
	rename -uid "AA4D0B6A-4FA2-6A0E-4070-E2806082F42A";
createNode transform -n "prop_ctrlOffsetGrp" -p "prop_ctrlPrntSwchGrp";
	rename -uid "C8FCC3DC-4F0D-3683-870F-B88FFCE00C24";
createNode transform -n "prop_ctrl" -p "prop_ctrlOffsetGrp";
	rename -uid "49E18E52-4479-9817-D3BB-48BE16811045";
	addAttr -ci true -sn "mirrorTranslateX" -ln "mirrorTranslateX" -min -1 -max 1 -at "long";
	addAttr -ci true -sn "mirrorTranslateY" -ln "mirrorTranslateY" -min -1 -max 1 -at "long";
	addAttr -ci true -sn "mirrorTranslateZ" -ln "mirrorTranslateZ" -min -1 -max 1 -at "long";
	addAttr -ci true -sn "mirrorRotateX" -ln "mirrorRotateX" -min -1 -max 1 -at "long";
	addAttr -ci true -sn "mirrorRotateY" -ln "mirrorRotateY" -min -1 -max 1 -at "long";
	addAttr -ci true -sn "mirrorRotateZ" -ln "mirrorRotateZ" -min -1 -max 1 -at "long";
	setAttr -l on -k off ".v";
createNode nurbsCurve -n "sword_ctrlShape" -p "prop_ctrl";
	rename -uid "351B4E0F-4EE9-4306-920E-9588D3F170E3";
	setAttr -k off ".v";
	setAttr ".wfcc" -type "float3" 1 0.40000001 0 ;
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		-12.170227125346992 3.3400668265094566 3.3400668265094566
		-12.170227125346992 3.3400668265094566 -3.3400668265094566
		12.170227125346992 3.3400668265094566 -3.3400668265094566
		12.170227125346992 3.3400668265094566 3.3400668265094566
		-12.170227125346992 3.3400668265094566 3.3400668265094566
		-12.170227125346992 -3.3400668265094566 3.3400668265094566
		-12.170227125346992 -3.3400668265094566 -3.3400668265094566
		12.170227125346992 -3.3400668265094566 -3.3400668265094566
		12.170227125346992 -3.3400668265094566 3.3400668265094566
		-12.170227125346992 -3.3400668265094566 3.3400668265094566
		-12.170227125346992 3.3400668265094566 3.3400668265094566
		12.170227125346992 3.3400668265094566 3.3400668265094566
		12.170227125346992 -3.3400668265094566 3.3400668265094566
		12.170227125346992 -3.3400668265094566 -3.3400668265094566
		12.170227125346992 3.3400668265094566 -3.3400668265094566
		-12.170227125346992 3.3400668265094566 -3.3400668265094566
		-12.170227125346992 -3.3400668265094566 -3.3400668265094566
		;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "1813FDB4-4109-0372-29E1-B782DFB24B18";
	setAttr -s 3 ".lnk";
	setAttr -s 3 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "887A353C-43A9-EEEF-B7EB-F48BA390B9B2";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "2A3EDE2A-4B88-4934-CA19-EB83487FEEA4";
createNode displayLayerManager -n "layerManager";
	rename -uid "E211560F-4170-7F11-6288-36AF4A91DA1D";
	setAttr -s 3 ".dli[1:2]"  1 2;
	setAttr -s 3 ".dli";
createNode displayLayer -n "defaultLayer";
	rename -uid "2429054E-4486-ABDE-AB67-4F86BD28C743";
	setAttr ".ufem" -type "stringArray" 0  ;
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "13487629-4E52-3764-3A5A-5A844F850169";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "F6C9BA1F-40CE-BE59-5CFD-07B8EA82D42B";
	setAttr ".g" yes;
createNode materialInfo -n "materialInfo2";
	rename -uid "8015F6EC-4236-A5EC-E10F-FF830D4097D9";
createNode shadingEngine -n "prop_matSG";
	rename -uid "9AEA53B3-489D-9C19-94E7-7E9FF9BF7344";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode standardSurface -n "prop_mat";
	rename -uid "66C8BCBF-4647-4D2C-993D-E3B430267815";
	setAttr ".bc" -type "float3" 0.70490003 0.53149998 0.0407 ;
	setAttr ".sr" 0.44999998807907104;
createNode aiOptions -s -n "defaultArnoldRenderOptions";
	rename -uid "040D3182-4751-2741-7C37-BD815FF4633C";
	setAttr ".version" -type "string" "5.6.3";
createNode aiImagerDenoiserOidn -s -n "defaultArnoldDenoiser";
	rename -uid "2C63FC1B-48F5-4D9A-EEF9-29B993C2CD29";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "41FA0C10-4B5E-3C1A-DC58-77954F08788B";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n"
		+ "            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n"
		+ "            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n"
		+ "            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n"
		+ "            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n"
		+ "            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n"
		+ "            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n"
		+ "            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n"
		+ "            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n"
		+ "            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1810\n            -height 1114\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n"
		+ "            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n"
		+ "            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -selectCommand \"print(\\\"\\\")\" \n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n"
		+ "            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n"
		+ "            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n"
		+ "                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -showUfeItems 1\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n"
		+ "                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayValues 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showPlayRangeShades \"on\" \n                -lockPlayRangeShades \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n"
		+ "                -showUpstreamCurves 1\n                -tangentScale 1\n                -tangentLineThickness 1\n                -keyMinScale 1\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -preSelectionHighlight 0\n                -limitToSelectedCurves 0\n                -constrainDrag 0\n                -valueLinesToggle 0\n                -outliner \"graphEditor1OutlineEd\" \n                -highlightAffectedCurves 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n"
		+ "                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n"
		+ "                -setFilter \"0\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -showUfeItems 1\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n"
		+ "                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -hierarchyBelow 0\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n"
		+ "                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayValues 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n"
		+ "                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n"
		+ "                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n"
		+ "                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"motionMakerEditorPanel\" (localizedPanelLabel(\"MotionMaker Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"MotionMaker Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"|persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n"
		+ "                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n"
		+ "                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n"
		+ "                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -bluePencil 1\n                -greasePencils 0\n                -excludeObjectPreset \"All\" \n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName; };\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1810\\n    -height 1114\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1810\\n    -height 1114\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 500 -size 1200 -divisions 20 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "07E6B72E-4A24-3EC5-2BF7-79B4A55F7D95";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 240 -ast -10 -aet 240 ";
	setAttr ".st" 6;
createNode nodeGraphEditorInfo -n "hyperShadePrimaryNodeEditorSavedTabsInfo";
	rename -uid "2F14E505-40BF-741C-6111-89A35468272B";
	setAttr ".def" no;
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -1201.3561132835068 -723.80949504791874 ;
	setAttr ".tgi[0].vh" -type "double2" 1146.7437175422415 720.23806661840592 ;
createNode nodeGraphEditorInfo -n "skeleton_hyperShadePrimaryNodeEditorSavedTabsInfo";
	rename -uid "6428A033-417C-9EDA-2CB0-0C982B68621D";
	setAttr ".def" no;
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -1201.3561132835068 -723.80949504791874 ;
	setAttr ".tgi[0].vh" -type "double2" 1146.7437175422415 720.23806661840592 ;
createNode nodeGraphEditorInfo -n "hyperShadePrimaryNodeEditorSavedTabsInfo1";
	rename -uid "07EDE9FA-4A78-915B-0D19-DB9AC48C6263";
	setAttr ".def" no;
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -1032.1428161291867 -635.71426045327053 ;
	setAttr ".tgi[0].vh" -type "double2" 1033.3332922723573 634.5237843100997 ;
createNode displayLayer -n "joints_lyr";
	rename -uid "0355D71C-42E6-2307-D69E-DD9301764B46";
	setAttr ".dt" 2;
	setAttr ".v" no;
	setAttr ".ufem" -type "stringArray" 0  ;
	setAttr ".do" 1;
createNode displayLayer -n "geo_lyr";
	rename -uid "449703B9-4945-869B-C03D-81BBCA3BE320";
	setAttr ".dt" 2;
	setAttr ".ufem" -type "stringArray" 0  ;
	setAttr ".do" 2;
createNode skinCluster -n "prop_skinCluster";
	rename -uid "391EF295-4AB2-4F6F-47FD-7796584FE402";
	setAttr -s 114 ".wl";
	setAttr ".wl[0:113].w"
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1
		1 0 1;
	setAttr -s 2 ".pm";
	setAttr ".pm[0]" -type "matrix" -1.1102230246251563e-15 2.2204460492503136e-16 1 -0
		 1 2.4651903288156623e-31 1.1102230246251565e-15 -0 2.4651903288156615e-31 1.0000000000000002 -2.2204460492503131e-16 -0
		 -0 0 -0 1;
	setAttr ".pm[1]" -type "matrix" -1.1102230246251563e-15 2.2204460492503146e-16 1.0000000000000002 -0
		 1 2.4651903288156636e-31 1.1102230246251567e-15 -0 2.4651903288156615e-31 1.0000000000000007 -2.2204460492503136e-16 -0
		 -99.780136108398423 -2.4868995751603522e-14 -3.3892045337015425e-08 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 2 ".ma";
	setAttr -s 2 ".dpf[0:1]"  4 4;
	setAttr -s 2 ".lw";
	setAttr -s 2 ".lw";
	setAttr ".bm" 1;
	setAttr ".ucm" yes;
	setAttr -s 2 ".ifcl";
	setAttr -s 2 ".ifcl";
createNode dagPose -n "bindPose1";
	rename -uid "A8BD88CD-428A-C2B8-5916-41AACAF15B1A";
	setAttr -s 3 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 3 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 0.99999999999999967 0.99999999999999989 8.6736173798840355e-17
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.49999999999999978 0.50000000000000033 0.50000000000000022 0.49999999999999967 1
		 1 1 no;
	setAttr ".xm[2]" -type "matrix" "xform" 1 0.99999999999999967 0.99999999999999989 8.6736173798840355e-17
		 0 0 0 99.780136108398438 2.4868995751603516e-14 3.3892045337015419e-08 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1.0000000000000004 1.0000000000000002 no;
	setAttr -s 3 ".m";
	setAttr -s 3 ".p";
	setAttr -s 3 ".g[0:2]" yes no no;
	setAttr ".bp" yes;
createNode controller -n "prop_ctrl_tag";
	rename -uid "3175E874-4CAC-CFAC-8725-5E9B4275C6E7";
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
	setAttr -s 3 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 7 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :standardSurface1;
	setAttr ".bc" -type "float3" 0.40000001 0.40000001 0.40000001 ;
	setAttr ".sr" 0.5;
select -ne :openPBR_shader1;
	setAttr ".bc" -type "float3" 0.40000001 0.40000001 0.40000001 ;
	setAttr ".sr" 0.5;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".ren" -type "string" "arnold";
	setAttr ".dss" -type "string" "openPBR_shader1";
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
connectAttr "propMain_jntScaleConstraint.csx" "propMain_jnt.sx";
connectAttr "propMain_jntScaleConstraint.csy" "propMain_jnt.sy";
connectAttr "propMain_jntScaleConstraint.csz" "propMain_jnt.sz";
connectAttr "joints_lyr.di" "propMain_jnt.do";
connectAttr "propMain_jntParentConstraint.ctx" "propMain_jnt.tx";
connectAttr "propMain_jntParentConstraint.cty" "propMain_jnt.ty";
connectAttr "propMain_jntParentConstraint.ctz" "propMain_jnt.tz";
connectAttr "propMain_jntParentConstraint.crx" "propMain_jnt.rx";
connectAttr "propMain_jntParentConstraint.cry" "propMain_jnt.ry";
connectAttr "propMain_jntParentConstraint.crz" "propMain_jnt.rz";
connectAttr "propMain_jnt.s" "propTop_jnt.is";
connectAttr "propMain_jnt.ro" "propMain_jntParentConstraint.cro";
connectAttr "propMain_jnt.pim" "propMain_jntParentConstraint.cpim";
connectAttr "propMain_jnt.rp" "propMain_jntParentConstraint.crp";
connectAttr "propMain_jnt.rpt" "propMain_jntParentConstraint.crt";
connectAttr "propMain_jnt.jo" "propMain_jntParentConstraint.cjo";
connectAttr "prop_ctrl.t" "propMain_jntParentConstraint.tg[0].tt";
connectAttr "prop_ctrl.rp" "propMain_jntParentConstraint.tg[0].trp";
connectAttr "prop_ctrl.rpt" "propMain_jntParentConstraint.tg[0].trt";
connectAttr "prop_ctrl.r" "propMain_jntParentConstraint.tg[0].tr";
connectAttr "prop_ctrl.ro" "propMain_jntParentConstraint.tg[0].tro";
connectAttr "prop_ctrl.s" "propMain_jntParentConstraint.tg[0].ts";
connectAttr "prop_ctrl.pm" "propMain_jntParentConstraint.tg[0].tpm";
connectAttr "propMain_jntParentConstraint.w0" "propMain_jntParentConstraint.tg[0].tw"
		;
connectAttr "propMain_jnt.pim" "propMain_jntScaleConstraint.cpim";
connectAttr "prop_ctrl.s" "propMain_jntScaleConstraint.tg[0].ts";
connectAttr "prop_ctrl.pm" "propMain_jntScaleConstraint.tg[0].tpm";
connectAttr "propMain_jntScaleConstraint.w0" "propMain_jntScaleConstraint.tg[0].tw"
		;
connectAttr "geo_lyr.di" "prop_geo.do";
connectAttr "prop_skinCluster.og[0]" "prop_geoShape.i";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "prop_matSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "prop_matSG.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "prop_matSG.msg" "materialInfo2.sg";
connectAttr "prop_mat.msg" "materialInfo2.m";
connectAttr "prop_mat.msg" "materialInfo2.t" -na;
connectAttr "prop_mat.oc" "prop_matSG.ss";
connectAttr "prop_geoShape.iog" "prop_matSG.dsm" -na;
connectAttr ":defaultArnoldDenoiser.msg" ":defaultArnoldRenderOptions.imagers" -na
		;
connectAttr "layerManager.dli[1]" "joints_lyr.id";
connectAttr "layerManager.dli[2]" "geo_lyr.id";
connectAttr "prop_geoShapeOrig.w" "prop_skinCluster.ip[0].ig";
connectAttr "prop_geoShapeOrig.o" "prop_skinCluster.orggeom[0]";
connectAttr "bindPose1.msg" "prop_skinCluster.bp";
connectAttr "propMain_jnt.wm" "prop_skinCluster.ma[0]";
connectAttr "propTop_jnt.wm" "prop_skinCluster.ma[1]";
connectAttr "propMain_jnt.liw" "prop_skinCluster.lw[0]";
connectAttr "propTop_jnt.liw" "prop_skinCluster.lw[1]";
connectAttr "propMain_jnt.obcc" "prop_skinCluster.ifcl[0]";
connectAttr "propTop_jnt.obcc" "prop_skinCluster.ifcl[1]";
connectAttr "main_skeletalMeshGrp.msg" "bindPose1.m[0]";
connectAttr "propMain_jnt.msg" "bindPose1.m[1]";
connectAttr "propTop_jnt.msg" "bindPose1.m[2]";
connectAttr "bindPose1.w" "bindPose1.p[0]";
connectAttr "bindPose1.m[0]" "bindPose1.p[1]";
connectAttr "bindPose1.m[1]" "bindPose1.p[2]";
connectAttr "propMain_jnt.bps" "bindPose1.wm[1]";
connectAttr "propTop_jnt.bps" "bindPose1.wm[2]";
connectAttr "prop_ctrl.msg" "prop_ctrl_tag.act";
connectAttr "prop_matSG.pa" ":renderPartition.st" -na;
connectAttr "prop_mat.msg" ":defaultShaderList1.s" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of propExample_rig.ma
