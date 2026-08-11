//Maya ASCII 2025ff03 scene
//Name: rig_helpers.ma
//Last modified: Tue, Nov 18, 2025 02:11:22 PM
//Codeset: 1252
requires maya "2025ff03";
requires -nodeType "ikSpringSolver" "ikSpringSolver" "1.0";
requires "stereoCamera" "10.0";
requires "mtoa" "5.5.4.2";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2025";
fileInfo "version" "2025";
fileInfo "cutIdentifier" "202409190603-cbdc5a7e54";
fileInfo "osv" "Windows 11 Pro v2009 (Build: 22631)";
fileInfo "UUID" "3668D1D1-4688-EC77-122E-FDAB094825AA";
createNode transform -s -n "persp";
	rename -uid "55BC850F-44F7-3FAD-F0C6-2A9C2C8841E4";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 208.68640297478632 278.01157625185868 -220.97714031080818 ;
	setAttr ".r" -type "double3" -33.938352729595657 119.79999999998542 0 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "C0B2E9BE-4456-86BE-61F4-8C8DC006424C";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 308.27480657726716;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 1.5093432664871216 128.34225463867188 -39.737533569335938 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "3A1E4F47-438B-C354-8592-49ACA4ED5E47";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -90 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "3488C7F0-4145-D099-4851-56BFC44D867F";
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
	rename -uid "B4967F65-450D-C518-FC8D-A99DB12088F1";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "03B0DC7B-4265-1D21-E478-D0B10A501FDE";
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
	rename -uid "BF5EEEF6-4928-A0BA-47F0-70B9E3F3E29F";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 90 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "1901109F-458F-14B3-7134-9C903D28F941";
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
createNode transform -n "flexiSurfaceTailStretch_geo";
	rename -uid "363E4D80-4D94-B0BD-0A6E-609540F73686";
createNode mesh -n "flexiSurfaceTailStretch_geoShape" -p "flexiSurfaceTailStretch_geo";
	rename -uid "00A12A08-4666-EA62-B081-7C8C7CD4248C";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr -s 6 ".gtag";
	setAttr ".gtag[0].gtagnm" -type "string" "back";
	setAttr ".gtag[0].gtagcmp" -type "componentList" 0;
	setAttr ".gtag[1].gtagnm" -type "string" "bottom";
	setAttr ".gtag[1].gtagcmp" -type "componentList" 0;
	setAttr ".gtag[2].gtagnm" -type "string" "front";
	setAttr ".gtag[2].gtagcmp" -type "componentList" 0;
	setAttr ".gtag[3].gtagnm" -type "string" "left";
	setAttr ".gtag[3].gtagcmp" -type "componentList" 0;
	setAttr ".gtag[4].gtagnm" -type "string" "right";
	setAttr ".gtag[4].gtagcmp" -type "componentList" 0;
	setAttr ".gtag[5].gtagnm" -type "string" "top";
	setAttr ".gtag[5].gtagcmp" -type "componentList" 1 "f[0:17]";
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 38 ".uvst[0].uvsp[0:37]" -type "float2" 0.046976984 0.51750457
		 0.046942353 0.48341963 0.079578698 0.48338631 0.079613447 0.51747125 0.15129888 0.51739812
		 0.15126407 0.48331323 0.22308457 0.48323992 0.22311932 0.51732486 0.28264934 0.51726413
		 0.28261453 0.4831793 0.34210533 0.48311859 0.34214002 0.51720345 0.40313274 0.51714122
		 0.40309793 0.48305631 0.46412528 0.48299402 0.46416008 0.517079 0.51872951 0.51702332
		 0.51869464 0.48293841 0.57318139 0.48288292 0.57321608 0.51696771 0.6221602 0.51691782
		 0.62212551 0.48283291 0.67112029 0.48278296 0.67115504 0.51686782 0.72508633 0.5168128
		 0.72505158 0.48272786 0.77896392 0.48267296 0.77899873 0.51675779 0.88031173 0.51665443
		 0.88027692 0.48256955 0.98159289 0.48246619 0.9816277 0.51655114 0.014265835 0.48345295
		 0.014300585 0.51753789 0 0.517551 0 0.48346606 1 0.48244897 1 0.51653385;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 38 ".vt[0:37]"  -5 141.42915344 -5.24106884 5 141.42915344 -5.24106884
		 -5 133.90995789 -22.86310768 5 133.90995789 -22.86310768 -5 121.50054169 -63.086921692
		 5 121.50054169 -63.086921692 -5 111.96482849 -96.67427826 5 111.96482849 -96.67427826
		 -5 105.51963806 -131.87168884 5 105.51963806 -131.87168884 -5 102.18252563 -163.68144226
		 5 102.18252563 -163.68144226 -5 102.17100525 -192.41174316 5 102.17100525 -192.41174316
		 -5 102.5200119 -224.048339844 5 102.5200119 -224.048339844 -5 100.49681854 -283.46221924
		 5 100.49681854 -283.46221924 -5 142.9433136 -1.79890656 5 142.9433136 -1.79890656
		 -5 100.49681854 -288.42745972 5 100.49681854 -288.42745972 -5 108.21379089 -114.17103577
		 5 108.21379089 -114.17103577 -5 116.47245789 -79.81270599 5 116.47245789 -79.81270599
		 -5 127.32009888 -42.83544159 5 127.32009888 -42.8354454 -5 137.51982117 -13.99460411
		 5 137.51982117 -13.99460411 -5 103.43108368 -147.7447052 5 103.43108368 -147.7447052
		 -5 101.9526825 -178.0390625 5 101.9526825 -178.0390625 -5 102.48176575 -208.23132324
		 5 102.48176575 -208.23132324 -5 101.52099609 -253.75526428 5 101.52099609 -253.75526428;
	setAttr -s 55 ".ed[0:54]"  0 1 0 2 3 0 0 28 0 1 29 0 2 26 0 3 27 0 4 5 1
		 4 24 0 5 25 0 6 7 1 6 22 0 7 23 0 8 9 1 8 30 0 9 31 0 10 11 1 10 32 0 11 33 0 12 13 1
		 12 34 0 13 35 0 14 15 1 14 36 0 15 37 0 16 17 0 0 18 0 1 19 0 18 19 0 16 20 0 17 21 0
		 20 21 0 22 8 0 23 9 0 22 23 1 24 6 0 25 7 0 24 25 1 26 4 0 27 5 0 26 27 1 28 2 0
		 29 3 0 28 29 1 30 10 0 31 11 0 30 31 1 32 12 0 33 13 0 32 33 1 34 14 0 35 15 0 34 35 1
		 36 16 0 37 17 0 36 37 1;
	setAttr -s 18 -ch 72 ".fc[0:17]" -type "polyFaces" 
		f 4 42 41 -2 -41
		mu 0 4 0 1 2 3
		f 4 39 38 -7 -38
		mu 0 4 4 5 6 7
		f 4 36 35 -10 -35
		mu 0 4 8 9 10 11
		f 4 33 32 -13 -32
		mu 0 4 12 13 14 15
		f 4 45 44 -16 -44
		mu 0 4 16 17 18 19
		f 4 48 47 -19 -47
		mu 0 4 20 21 22 23
		f 4 51 50 -22 -50
		mu 0 4 24 25 26 27
		f 4 54 53 -25 -53
		mu 0 4 28 29 30 31
		f 4 -1 25 27 -27
		mu 0 4 32 33 34 35
		f 4 24 29 -31 -29
		mu 0 4 31 30 36 37
		f 4 9 11 -34 -11
		mu 0 4 11 10 13 12
		f 4 6 8 -37 -8
		mu 0 4 7 6 9 8
		f 4 1 5 -40 -5
		mu 0 4 3 2 5 4
		f 4 0 3 -43 -3
		mu 0 4 33 32 1 0
		f 4 12 14 -46 -14
		mu 0 4 15 14 17 16
		f 4 15 17 -49 -17
		mu 0 4 19 18 21 20
		f 4 18 20 -52 -20
		mu 0 4 23 22 25 24
		f 4 21 23 -55 -23
		mu 0 4 27 26 29 28;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "flexiSurfaceTailMain_geo";
	rename -uid "D48177CE-4E4A-2A53-CB3A-6CA5E5414B78";
createNode mesh -n "flexiSurfaceTailMain_geoShape" -p "flexiSurfaceTailMain_geo";
	rename -uid "A0C3E9E1-4A5F-1082-69D5-5B932F7FB61C";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr -s 6 ".gtag";
	setAttr ".gtag[0].gtagnm" -type "string" "back";
	setAttr ".gtag[0].gtagcmp" -type "componentList" 0;
	setAttr ".gtag[1].gtagnm" -type "string" "bottom";
	setAttr ".gtag[1].gtagcmp" -type "componentList" 0;
	setAttr ".gtag[2].gtagnm" -type "string" "front";
	setAttr ".gtag[2].gtagcmp" -type "componentList" 0;
	setAttr ".gtag[3].gtagnm" -type "string" "left";
	setAttr ".gtag[3].gtagcmp" -type "componentList" 0;
	setAttr ".gtag[4].gtagnm" -type "string" "right";
	setAttr ".gtag[4].gtagcmp" -type "componentList" 0;
	setAttr ".gtag[5].gtagnm" -type "string" "top";
	setAttr ".gtag[5].gtagcmp" -type "componentList" 1 "f[0:17]";
	setAttr ".pv" -type "double2" 0 0.50050853192806244 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 38 ".uvst[0].uvsp[0:37]" -type "float2" 0.046976984 0.51750457
		 0.046942353 0.48341963 0.079578698 0.48338631 0.079613447 0.51747125 0.15129888 0.51739812
		 0.15126407 0.48331323 0.22308457 0.48323992 0.22311932 0.51732486 0.28264934 0.51726413
		 0.28261453 0.4831793 0.34210533 0.48311859 0.34214002 0.51720345 0.40313274 0.51714122
		 0.40309793 0.48305631 0.46412528 0.48299402 0.46416008 0.517079 0.51872951 0.51702332
		 0.51869464 0.48293841 0.57318139 0.48288292 0.57321608 0.51696771 0.6221602 0.51691782
		 0.62212551 0.48283291 0.67112029 0.48278296 0.67115504 0.51686782 0.72508633 0.5168128
		 0.72505158 0.48272786 0.77896392 0.48267296 0.77899873 0.51675779 0.88031173 0.51665443
		 0.88027692 0.48256955 0.98159289 0.48246619 0.9816277 0.51655114 0.014265835 0.48345295
		 0.014300585 0.51753789 0 0.517551 0 0.48346606 1 0.48244897 1 0.51653385;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 38 ".vt[0:37]"  -5 141.42915344 -5.24106884 5 141.42915344 -5.24106884
		 -5 133.90995789 -22.86310768 5 133.90995789 -22.86310768 -5 121.50054169 -63.086921692
		 5 121.50054169 -63.086921692 -5 111.96482849 -96.67427826 5 111.96482849 -96.67427826
		 -5 105.51963806 -131.87168884 5 105.51963806 -131.87168884 -5 102.18252563 -163.68144226
		 5 102.18252563 -163.68144226 -5 102.17100525 -192.41174316 5 102.17100525 -192.41174316
		 -5 102.5200119 -224.048339844 5 102.5200119 -224.048339844 -5 100.49681854 -283.46221924
		 5 100.49681854 -283.46221924 -5 142.9433136 -1.79890656 5 142.9433136 -1.79890656
		 -5 100.49681854 -288.42745972 5 100.49681854 -288.42745972 -5 108.21379089 -114.17103577
		 5 108.21379089 -114.17103577 -5 116.47245789 -79.81270599 5 116.47245789 -79.81270599
		 -5 127.32009888 -42.83544159 5 127.32009888 -42.8354454 -5 137.51982117 -13.99460411
		 5 137.51982117 -13.99460411 -5 103.43108368 -147.7447052 5 103.43108368 -147.7447052
		 -5 101.9526825 -178.0390625 5 101.9526825 -178.0390625 -5 102.48176575 -208.23132324
		 5 102.48176575 -208.23132324 -5 101.52099609 -253.75526428 5 101.52099609 -253.75526428;
	setAttr -s 55 ".ed[0:54]"  0 1 0 2 3 0 0 28 0 1 29 0 2 26 0 3 27 0 4 5 1
		 4 24 0 5 25 0 6 7 1 6 22 0 7 23 0 8 9 1 8 30 0 9 31 0 10 11 1 10 32 0 11 33 0 12 13 1
		 12 34 0 13 35 0 14 15 1 14 36 0 15 37 0 16 17 0 0 18 0 1 19 0 18 19 0 16 20 0 17 21 0
		 20 21 0 22 8 0 23 9 0 22 23 1 24 6 0 25 7 0 24 25 1 26 4 0 27 5 0 26 27 1 28 2 0
		 29 3 0 28 29 1 30 10 0 31 11 0 30 31 1 32 12 0 33 13 0 32 33 1 34 14 0 35 15 0 34 35 1
		 36 16 0 37 17 0 36 37 1;
	setAttr -s 18 -ch 72 ".fc[0:17]" -type "polyFaces" 
		f 4 42 41 -2 -41
		mu 0 4 0 1 2 3
		f 4 39 38 -7 -38
		mu 0 4 4 5 6 7
		f 4 36 35 -10 -35
		mu 0 4 8 9 10 11
		f 4 33 32 -13 -32
		mu 0 4 12 13 14 15
		f 4 45 44 -16 -44
		mu 0 4 16 17 18 19
		f 4 48 47 -19 -47
		mu 0 4 20 21 22 23
		f 4 51 50 -22 -50
		mu 0 4 24 25 26 27
		f 4 54 53 -25 -53
		mu 0 4 28 29 30 31
		f 4 -1 25 27 -27
		mu 0 4 32 33 34 35
		f 4 24 29 -31 -29
		mu 0 4 31 30 36 37
		f 4 9 11 -34 -11
		mu 0 4 11 10 13 12
		f 4 6 8 -37 -8
		mu 0 4 7 6 9 8
		f 4 1 5 -40 -5
		mu 0 4 3 2 5 4
		f 4 0 3 -43 -3
		mu 0 4 33 32 1 0
		f 4 12 14 -46 -14
		mu 0 4 15 14 17 16
		f 4 15 17 -49 -17
		mu 0 4 19 18 21 20
		f 4 18 20 -52 -20
		mu 0 4 23 22 25 24
		f 4 21 23 -55 -23
		mu 0 4 27 26 29 28;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode transform -n "tailClothAttach_geo";
	rename -uid "FEA96CA9-4AD6-E203-A130-068D0827A327";
createNode mesh -n "tailClothAttach_geoShape" -p "tailClothAttach_geo";
	rename -uid "B79F3DCC-454B-7291-A996-EABB5D874577";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr -s 6 ".gtag";
	setAttr ".gtag[0].gtagnm" -type "string" "back";
	setAttr ".gtag[0].gtagcmp" -type "componentList" 1 "f[2]";
	setAttr ".gtag[1].gtagnm" -type "string" "bottom";
	setAttr ".gtag[1].gtagcmp" -type "componentList" 1 "f[3]";
	setAttr ".gtag[2].gtagnm" -type "string" "front";
	setAttr ".gtag[2].gtagcmp" -type "componentList" 1 "f[0]";
	setAttr ".gtag[3].gtagnm" -type "string" "left";
	setAttr ".gtag[3].gtagcmp" -type "componentList" 1 "f[5]";
	setAttr ".gtag[4].gtagnm" -type "string" "right";
	setAttr ".gtag[4].gtagcmp" -type "componentList" 1 "f[4]";
	setAttr ".gtag[5].gtagnm" -type "string" "top";
	setAttr ".gtag[5].gtagcmp" -type "componentList" 1 "f[1]";
	setAttr ".pv" -type "double2" 0.5 0.5 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 14 ".uvst[0].uvsp[0:13]" -type "float2" 0.25665265 0.0051773521
		 0.74366373 0.0057788491 0.25633633 0.26127842 0.74334735 0.26187998 0.25604171 0.49984649
		 0.74305272 0.50044805 0.25572535 0.75594765 0.7427364 0.75654924 0.2554307 0.99451572
		 0.74244177 0.99511719 0.98223174 0.0060736914 0.98191547 0.26217479 0.01808458 0.0048828125
		 0.017768264 0.26098394;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 8 ".vt[0:7]"  -5.19822931 142.69248962 3.98415661 5.19822931 142.69248962 3.98415661
		 -5.19822931 147.67680359 1.73783779 5.19822931 147.67680359 1.73783779 -5.19822931 145.58427429 -2.90524435
		 5.19822931 145.58427429 -2.90524435 -5.19822931 140.59996033 -0.65892553 5.19822931 140.59996033 -0.65892553;
	setAttr -s 12 ".ed[0:11]"  0 1 0 2 3 0 4 5 0 6 7 0 0 2 0 1 3 0 2 4 0
		 3 5 0 4 6 0 5 7 0 6 0 0 7 1 0;
	setAttr -s 6 -ch 24 ".fc[0:5]" -type "polyFaces" 
		f 4 0 5 -2 -5
		mu 0 4 0 1 3 2
		f 4 1 7 -3 -7
		mu 0 4 2 3 5 4
		f 4 2 9 -4 -9
		mu 0 4 4 5 7 6
		f 4 3 11 -1 -11
		mu 0 4 6 7 9 8
		f 4 -12 -10 -8 -6
		mu 0 4 1 10 11 3
		f 4 10 4 6 8
		mu 0 4 12 0 2 13;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
createNode joint -n "tailCloth_01_jnt";
	rename -uid "CBE4814D-4926-526C-419D-13AE02E01B14";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 4;
	setAttr ".t" -type "double3" -9.5588706475736648e-15 141.42915763273101 -5.2410686467904162 ;
	setAttr ".r" -type "double3" -2.0673605429512861e-14 -1.0734372049939367e-14 1.431249606658583e-14 ;
	setAttr -cb on ".ro";
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -89.999999999999929 66.892390787226319 -89.999999999999929 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".is" -type "double3" 1 1 0.99999999999999956 ;
	setAttr ".bps" -type "matrix" 4.4408920985006262e-16 -0.39245927078818299 -0.9197693845591991 0
		 1.3877787807814459e-16 0.91976938455919899 -0.39245927078818299 0 1 1.3877787807814459e-16 4.4408920985006262e-16 0
		 -9.5588706475736648e-15 141.42915763273101 -5.2410686467904162 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "tailCloth_02_jnt" -p "tailCloth_01_jnt";
	rename -uid "C9E5C1B6-4FDE-BFFB-C73E-DDBFE4E7641D";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 4;
	setAttr ".t" -type "double3" 19.159192357087502 2.2737367544323206e-13 6.9310863444613921e-15 ;
	setAttr -cb on ".ro";
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0 5.9621383990728862 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" 4.5610205280893645e-16 -0.29479876462348648 -0.9555593588974296 0
		 9.1899092338278759e-17 0.95555935889742949 -0.29479876462348648 0 1 1.3877787807814459e-16 4.4408920985006262e-16 0
		 5.8806062921121078e-15 133.90995497137811 -22.863107209720187 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "tailCloth_03_jnt" -p "tailCloth_02_jnt";
	rename -uid "FEE101BB-4DB4-1A83-2FC0-AF873145E5F0";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 4;
	setAttr ".t" -type "double3" 42.094524383544936 -8.5265128291212022e-14 1.7338934578038505e-14 ;
	setAttr -cb on ".ro";
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0 1.2958072436080115 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" 4.5806363454375394e-16 -0.27311418829462619 -0.96198162152515576 0
		 8.156121907923851e-17 0.96198162152515565 -0.27311418829462619 0 1 1.3877787807814459e-16 4.4408920985006262e-16 0
		 4.2418939853501278e-14 121.50054118569575 -63.086923942752577 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "tailCloth_04_jnt" -p "tailCloth_03_jnt";
	rename -uid "6CE98276-4A89-65B1-D109-A1B745E92CDC";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 4;
	setAttr ".t" -type "double3" 34.914756774902131 -5.6843418860808015e-14 2.7743366059210742e-14 ;
	setAttr -cb on ".ro";
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0 5.4728879173328764 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" 4.6375440314287183e-16 -0.18012044826752444 -0.98364456187990312 0
		 3.7501724156684584e-17 0.98364456187990301 -0.18012044826752444 0 1 1.3877787807814459e-16 4.4408920985006262e-16 0
		 8.6155486300234832e-14 111.96482572961401 -96.674278280229331 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "tailCloth_05_jnt" -p "tailCloth_04_jnt";
	rename -uid "418EB484-4CF3-259C-AF82-738E733EEDB4";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 4;
	setAttr ".t" -type "double3" 35.782649993896513 9.9475983006414026e-14 2.9488539380657522e-14 ;
	setAttr -cb on ".ro";
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0 4.387871543994657 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" 4.6526430576361213e-16 -0.10433586236208504 -0.99454211968380735 0
		 1.9108980688099754e-18 0.99454211968380724 -0.10433586236208504 0 1 1.3877787807814459e-16 4.4408920985006262e-16 0
		 1.3223838717168213e-13 105.51963877251353 -131.87168735637761 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "tailCloth_06_jnt" -p "tailCloth_05_jnt";
	rename -uid "EE16BC8A-4FF4-8E4C-5568-918FBC512C0D";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 4;
	setAttr ".t" -type "double3" 31.984313964843764 0 -2.5243548967072378e-28 ;
	setAttr -cb on ".ro";
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0 5.9659194883333271 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" 4.6294299811023148e-16 -0.00040115729309880832 -0.9999999195364101 0
		 -4.6457574730451615e-17 0.99999991953640999 -0.00040115729309879444 0 1 1.3877787807814459e-16 4.4408920985006262e-16 0
		 1.4711954680386032e-13 102.18252779293188 -163.68143476360572 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "tailCloth_07_jnt" -p "tailCloth_06_jnt";
	rename -uid "B093FEA0-422E-75E6-6B37-E29A3D1392EB";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 4;
	setAttr ".t" -type "double3" 28.730306625366495 -1.7053025658242404e-13 2.7624283232403906e-14 ;
	setAttr -cb on ".ro";
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0 0.65503679621314925 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" 4.6238162745949577e-16 0.0110311677751928 -0.99993915481768991 0
		 -5.1747041819155211e-17 0.9999391548176898 0.011031167775192816 0 1 1.3877787807814459e-16 4.4408920985006262e-16 0
		 1.8804432432203764e-13 102.17100242089597 -192.41173907722862 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "tailCloth_08_jnt" -p "tailCloth_07_jnt";
	rename -uid "8C6FF23F-4129-7BA8-2BA5-6B8F351EBEF3";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 4;
	setAttr ".t" -type "double3" 31.638521194457468 1.4210854715202004e-13 1.2252317548087136e-13 ;
	setAttr -cb on ".ro";
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0 -2.5823659966058523 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" 4.6424356194386842e-16 -0.034032824536468942 -0.99942071564185142 0
		 -3.0861641932906813e-17 0.99942071564185131 -0.034032824536468928 0 1 1.3877787807814459e-16 4.4408920985006262e-16 0
		 3.2519657072321401e-13 102.52001225635117 -224.04833522009599 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "tailCloth_09_jnt" -p "tailCloth_08_jnt";
	rename -uid "0551FFF6-418C-124D-B9C4-CAB0AED19F9E";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 4;
	setAttr ".t" -type "double3" 59.448326110840185 -2.8421709430404007e-14 -1.2835137694177389e-13 ;
	setAttr -cb on ".ro";
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" 0 0 -0.92276147960322263 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" 4.6468036812364732e-16 -0.050123611655780512 -0.99874302178016794 0
		 -2.3381215314798402e-17 0.99874302178016783 -0.050123611655780498 0 1 1.3877787807814459e-16 4.4408920985006262e-16 0
		 2.2444369644673725e-13 100.49681780483412 -283.46222384550208 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 3;
	setAttr ".fbxID" 5;
createNode joint -n "tailClothFlexi_start_jnt";
	rename -uid "B81A492C-4B1A-11A7-A76E-D9B4597BCDD0";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" -9.5588706475736758e-15 141.42915763273098 -5.2410686467903984 ;
	setAttr ".r" -type "double3" 3.1805546814635168e-15 7.9513867036587899e-16 4.7708320221952752e-15 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 1.0000000000000004 1.0000000000000002 0.99999999999999978 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -89.999999999999929 66.892390787226319 -89.999999999999929 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".is" -type "double3" 1 1 0.99999999999999956 ;
	setAttr ".bps" -type "matrix" 4.4408920985006262e-16 -0.39245927078818299 -0.9197693845591991 0
		 1.9428902930940244e-16 0.91976938455919899 -0.39245927078818305 0 1 5.5511151231257839e-17 4.4408920985006262e-16 0
		 -9.5588706475736648e-15 141.42915763273101 -5.2410686467904162 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 7;
	setAttr ".fbxID" 5;
createNode joint -n "tailClothFlexi_mid_jnt" -p "tailClothFlexi_start_jnt";
	rename -uid "677F3905-4ECC-B1B3-3E50-128BCDC898D0";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 130.56398982310301 16.668884216341837 7.9555309957161321e-14 ;
	setAttr ".r" -type "double3" 0 0 -3.1805546814635168e-15 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 1.0000000000000024 0.99999999999999944 0.99999999999999745 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -3.1491328657786588e-15 2.3735952248353523e-15 17.118705104008455 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" 4.8160414319932107e-16 -0.10433586236208475 -0.99454211968380724 0
		 5.4962737090602302e-17 0.99454211968380712 -0.10433586236208475 0 1 5.5511151231257839e-17 4.4408920985006262e-16 0
		 1.3121707971906496e-13 105.51963877251353 -131.87168735637758 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 7;
	setAttr ".fbxID" 5;
createNode joint -n "tailClothFlexi_end_jnt" -p "tailClothFlexi_mid_jnt";
	rename -uid "66A2F59F-4BEE-91E8-5634-A5A9C0870D7A";
	addAttr -is true -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -h true -sn "fbxID" -ln "filmboxTypeID" -at "short";
	setAttr -cb on ".wfcr";
	setAttr -cb on ".wfcg";
	setAttr -cb on ".wfcb";
	setAttr -cb on ".uoc" 1;
	setAttr -cb on ".oc" 6;
	setAttr ".t" -type "double3" 151.28723384105251 10.820922338535809 3.823672671132713e-14 ;
	setAttr ".r" -type "double3" 0 0 -1.1927080055488188e-15 ;
	setAttr -cb on ".ro";
	setAttr ".s" -type "double3" 1.0000000000000129 0.99999999999999989 0.99999999999998634 ;
	setAttr -cb on ".rax";
	setAttr -cb on ".ray";
	setAttr -cb on ".raz";
	setAttr -cb on ".dla";
	setAttr ".jo" -type "double3" -1.2886680819342925e-13 -4.3193358013375275e-15 3.1158288083373971 ;
	setAttr -cb on ".jox";
	setAttr -cb on ".joy";
	setAttr -cb on ".joz";
	setAttr -cb on ".ssc" no;
	setAttr ".bps" -type "matrix" 4.8387966553044452e-16 -0.050123611655780276 -0.99874302178016783 0
		 2.8704050261033249e-17 0.99874302178016772 -0.050123611655780269 0 1 5.5511151231257839e-17 4.4408920985006262e-16 0
		 2.4290911257097866e-13 100.49681780483417 -283.46222384550197 1;
	setAttr -cb on ".ds";
	setAttr ".radi" 7;
	setAttr ".fbxID" 5;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "2E488107-4C15-CC23-54E1-82B5D7805C58";
	setAttr -s 4 ".lnk";
	setAttr -s 4 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "6D3CF792-4A1B-63EB-96F2-618ADCEA16C5";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "598F39EB-4999-AC2F-2CE4-98B2B6BD8039";
createNode displayLayerManager -n "layerManager";
	rename -uid "407F77AF-4B31-D060-0FCE-AB91E7B34251";
createNode displayLayer -n "defaultLayer";
	rename -uid "6103E445-4A49-4002-52FB-F8ABC602CEA6";
	setAttr ".ufem" -type "stringArray" 0  ;
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "8295A04D-44B2-93DC-F8AF-5BABE51C1884";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "5892954B-4297-14D3-EA95-8EB6A2AB7B1A";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "FB06D4FC-4D19-5671-16F2-08A97265253D";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n"
		+ "            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n"
		+ "            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n"
		+ "            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"|front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n"
		+ "            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n"
		+ "            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n"
		+ "            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n"
		+ "            -camera \"|persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 1\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n"
		+ "            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n"
		+ "            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -bluePencil 1\n            -greasePencils 0\n            -excludeObjectPreset \"All\" \n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1865\n            -height 1114\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n"
		+ "            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n"
		+ "            -longNames 0\n            -niceNames 1\n            -selectCommand \"print(\\\"\\\")\" \n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            -ufeFilter \"USD\" \"InactivePrims\" -ufeFilterValue 1\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n"
		+ "            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n"
		+ "            -showUfeItems 1\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -ufeFilter \"USD\" \"InactivePrims\" -ufeFilterValue 1\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
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
		+ "                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -connectionMinSegment 0.03\n                -connectionOffset 0.03\n                -connectionRoundness 0.8\n                -connectionTension -100\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit 1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n"
		+ "                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -connectionMinSegment 0.03\n                -connectionOffset 0.03\n                -connectionRoundness 0.8\n                -connectionTension -100\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n"
		+ "                -connectedGraphingMode 1\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit 1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -showUnitConversions 0\n                -editorMode \"default\" \n                -hasWatchpoint 0\n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n{ string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"|persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n"
		+ "                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n"
		+ "                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n"
		+ "                -clipGhosts 1\n                -bluePencil 1\n                -greasePencils 0\n                -excludeObjectPreset \"All\" \n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName; };\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n"
		+ "\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1865\\n    -height 1114\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -bluePencil 1\\n    -greasePencils 0\\n    -excludeObjectPreset \\\"All\\\" \\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1865\\n    -height 1114\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 50 -size 500 -divisions 2 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "6120426B-4598-291A-F460-7FAF8E28CFAC";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 24 -ast 0 -aet 24 ";
	setAttr ".st" 6;
createNode materialInfo -n "materialInfo38";
	rename -uid "B2160A1F-4E33-523C-1DDE-DFBC6EC5F40E";
createNode shadingEngine -n "standardSurface2SG";
	rename -uid "9C9798E3-42F9-B22C-D370-DCACF46A8D7E";
	setAttr ".ihi" 0;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
createNode standardSurface -n "flexiSurface_mat";
	rename -uid "456C3FF9-43FC-3D3A-EA95-5EA9810C0692";
	setAttr ".bc" -type "float3" 0.208 0.3515 0.6631 ;
	setAttr ".s" 0.47926267981529236;
	setAttr ".sc" -type "float3" 0.49308756 0.49308756 0.49308756 ;
	setAttr ".sr" 0.48847925662994385;
createNode materialInfo -n "materialInfo39";
	rename -uid "9BB097E8-4146-0233-BA5C-D2B6590DDD6E";
createNode shadingEngine -n "clothAux_matSG";
	rename -uid "546768F1-4CD4-F646-FEBF-F38668D58F72";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode standardSurface -n "clothAux_mat";
	rename -uid "8A88053F-46C8-A144-AD8D-359D1F5DE090";
	setAttr ".bc" -type "float3" 0.6785714 0.386509 0.2661455 ;
	setAttr ".s" 0.50967741012573242;
	setAttr ".sc" -type "float3" 0.4967742 0.4967742 0.4967742 ;
	setAttr ".sr" 0.50322580337524414;
createNode nodeGraphEditorInfo -n "hyperShadePrimaryNodeEditorSavedTabsInfo";
	rename -uid "8788C623-488C-4593-2CD2-2DAB9244906B";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -1013.0951978384521 -695.99098464276267 ;
	setAttr ".tgi[0].vh" -type "double2" 1321.4708055497301 723.37193593569361 ;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "15992DEF-4DC1-64E2-1885-99A27A988408";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -1514.2856541134088 -790.47615906549015 ;
	setAttr ".tgi[0].vh" -type "double2" 1514.2856541134088 790.47615906549015 ;
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
	setAttr -s 4 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 7 ".s";
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
	setAttr ".dss" -type "string" "lambert1";
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
connectAttr "tailCloth_01_jnt.s" "tailCloth_02_jnt.is";
connectAttr "tailCloth_02_jnt.s" "tailCloth_03_jnt.is";
connectAttr "tailCloth_03_jnt.s" "tailCloth_04_jnt.is";
connectAttr "tailCloth_04_jnt.s" "tailCloth_05_jnt.is";
connectAttr "tailCloth_05_jnt.s" "tailCloth_06_jnt.is";
connectAttr "tailCloth_06_jnt.s" "tailCloth_07_jnt.is";
connectAttr "tailCloth_07_jnt.s" "tailCloth_08_jnt.is";
connectAttr "tailCloth_08_jnt.s" "tailCloth_09_jnt.is";
connectAttr "tailClothFlexi_start_jnt.s" "tailClothFlexi_mid_jnt.is";
connectAttr "tailClothFlexi_mid_jnt.s" "tailClothFlexi_end_jnt.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "standardSurface2SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "clothAux_matSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "standardSurface2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "clothAux_matSG.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "standardSurface2SG.msg" "materialInfo38.sg";
connectAttr "flexiSurface_mat.msg" "materialInfo38.m";
connectAttr "flexiSurface_mat.msg" "materialInfo38.t" -na;
connectAttr "flexiSurface_mat.oc" "standardSurface2SG.ss";
connectAttr "flexiSurfaceTailStretch_geoShape.iog" "standardSurface2SG.dsm" -na;
connectAttr "flexiSurfaceTailMain_geoShape.iog" "standardSurface2SG.dsm" -na;
connectAttr "clothAux_matSG.msg" "materialInfo39.sg";
connectAttr "clothAux_mat.msg" "materialInfo39.m";
connectAttr "clothAux_mat.oc" "clothAux_matSG.ss";
connectAttr "tailClothAttach_geoShape.iog" "clothAux_matSG.dsm" -na;
connectAttr "standardSurface2SG.pa" ":renderPartition.st" -na;
connectAttr "clothAux_matSG.pa" ":renderPartition.st" -na;
connectAttr "flexiSurface_mat.msg" ":defaultShaderList1.s" -na;
connectAttr "clothAux_mat.msg" ":defaultShaderList1.s" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of rig_helpers.ma
