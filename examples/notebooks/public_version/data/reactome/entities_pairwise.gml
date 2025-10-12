graph [
  multigraph 1
  node [
    id 0
    label "TP53 binds the PMAIP1 (NOXA) promoter"
    schemaClass "Reaction"
    stId "R-HSA-4331331"
    oldStId "REACT_169265"
    releaseDate "2016-03-23"
    name "['TP53 binds the PMAIP1 (NOXA) promoter']"
    stIdVersion "R-HSA-4331331.6"
    speciesName "Homo sapiens"
    category "binding"
    displayName "TP53 binds the PMAIP1 (NOXA) promoter"
  ]
  node [
    id 1
    label "p-S15,S20-TP53 Tetramer [nucleoplasm]"
    schemaClass "Complex"
    stId "R-HSA-3222171"
    name "['p-S15,S20-TP53 Tetramer']"
    stIdVersion "R-HSA-3222171.1"
    speciesName "Homo sapiens"
    displayName "p-S15,S20-TP53 Tetramer [nucleoplasm]"
  ]
  node [
    id 2
    label "TP53 binds the APAF1 gene promoter"
    schemaClass "Reaction"
    stId "R-HSA-6791349"
    releaseDate "2016-03-23"
    name "['TP53 binds the APAF1 gene promoter']"
    stIdVersion "R-HSA-6791349.3"
    speciesName "Homo sapiens"
    category "binding"
    displayName "TP53 binds the APAF1 gene promoter"
  ]
  node [
    id 3
    label "TP53 stimulates APAF1 gene expression"
    schemaClass "BlackBoxEvent"
    stId "R-HSA-6791348"
    releaseDate "2016-03-23"
    name "['TP53 stimulates APAF1 gene expression']"
    stIdVersion "R-HSA-6791348.4"
    speciesName "Homo sapiens"
    category "omitted"
    displayName "TP53 stimulates APAF1 gene expression"
  ]
  node [
    id 4
    label "CYCS binds to APAF1"
    schemaClass "Reaction"
    stId "R-HSA-114254"
    oldStId "REACT_1640"
    releaseDate "2004-10-27"
    name "['CYCS binds to APAF1']"
    stIdVersion "R-HSA-114254.6"
    speciesName "Homo sapiens"
    category "binding"
    displayName "CYCS binds to APAF1"
  ]
  node [
    id 5
    label "CYCS [cytosol]"
    schemaClass "EntityWithAccessionedSequence"
    stId "R-HSA-53259"
    oldStId "REACT_4972"
    name "['CYCS','Cytochrome c']"
    stIdVersion "R-HSA-53259.1"
    speciesName "Homo sapiens"
    referenceType "ReferenceGeneProduct"
    searchSeed "1"
    displayName "CYCS [cytosol]"
  ]
  node [
    id 6
    label "PMAIP1 Gene [nucleoplasm]"
    schemaClass "EntityWithAccessionedSequence"
    stId "R-HSA-4331342"
    oldStId "REACT_170122"
    name "['PMAIP1 Gene','NOXA Gene']"
    stIdVersion "R-HSA-4331342.1"
    speciesName "Homo sapiens"
    referenceType "ReferenceDNASequence"
    searchSeed "1"
    displayName "PMAIP1 Gene [nucleoplasm]"
  ]
  node [
    id 7
    label "p-S15,S20-TP53 Tetramer:PMAIP1 Gene [nucleoplasm]"
    schemaClass "Complex"
    stId "R-HSA-4331332"
    oldStId "REACT_170069"
    name "['p-S15,S20-TP53 Tetramer:PMAIP1 Gene']"
    stIdVersion "R-HSA-4331332.4"
    speciesName "Homo sapiens"
    displayName "p-S15,S20-TP53 Tetramer:PMAIP1 Gene [nucleoplasm]"
  ]
  node [
    id 8
    label "TP53 stimulates PMAIP1 (NOXA) expression"
    schemaClass "BlackBoxEvent"
    stId "R-HSA-140214"
    oldStId "REACT_2201"
    releaseDate "2004-10-27"
    name "['TP53 stimulates PMAIP1 (NOXA) expression']"
    stIdVersion "R-HSA-140214.6"
    speciesName "Homo sapiens"
    category "omitted"
    displayName "TP53 stimulates PMAIP1 (NOXA) expression"
  ]
  node [
    id 9
    label "Positive gene expression regulation by 'p-S15,S20-TP53 Tetramer:PMAIP1 Gene [nucleoplasm]'"
    schemaClass "PositiveGeneExpressionRegulation"
    stId "R-HSA-159038"
    oldStId "REACT_6033"
    stIdVersion "R-HSA-159038.4"
    displayName "Positive gene expression regulation by 'p-S15,S20-TP53 Tetramer:PMAIP1 Gene [nucleoplasm]'"
  ]
  node [
    id 10
    label "Translocation of PMAIP1 (NOXA) to mitochondria"
    schemaClass "Reaction"
    stId "R-HSA-140216"
    oldStId "REACT_1585"
    releaseDate "2004-10-27"
    name "['Translocation of PMAIP1 (NOXA) to mitochondria']"
    stIdVersion "R-HSA-140216.4"
    speciesName "Homo sapiens"
    category "transition"
    displayName "Translocation of PMAIP1 (NOXA) to mitochondria"
  ]
  node [
    id 11
    label "BH3-only proteins associate with and inactivate anti-apoptotic BCL-2"
    schemaClass "Reaction"
    stId "R-HSA-508163"
    oldStId "REACT_21389"
    releaseDate "2008-06-30"
    name "['BH3-only proteins associate with and inactivate anti-apoptotic BCL-2']"
    stIdVersion "R-HSA-508163.4"
    speciesName "Homo sapiens"
    category "binding"
    displayName "BH3-only proteins associate with and inactivate anti-apoptotic BCL-2"
  ]
  node [
    id 12
    label "Translocation of tBID to mitochondria"
    schemaClass "Reaction"
    stId "R-HSA-139920"
    oldStId "REACT_1370"
    releaseDate "2004-10-27"
    name "['Translocation of tBID to mitochondria']"
    stIdVersion "R-HSA-139920.3"
    speciesName "Homo sapiens"
    category "transition"
    displayName "Translocation of tBID to mitochondria"
  ]
  node [
    id 13
    label "Release of Cytochrome c from mitochondria"
    schemaClass "Reaction"
    stId "R-HSA-114284"
    oldStId "REACT_535"
    releaseDate "2004-07-06"
    name "['Release of Cytochrome c from mitochondria']"
    stIdVersion "R-HSA-114284.7"
    speciesName "Homo sapiens"
    category "transition"
    displayName "Release of Cytochrome c from mitochondria"
  ]
  node [
    id 14
    label "Transactivation of PMAIP1 (NOXA) by E2F1"
    schemaClass "BlackBoxEvent"
    stId "R-HSA-140217"
    oldStId "REACT_1872"
    releaseDate "2004-10-27"
    name "['Transactivation of PMAIP1 (NOXA) by E2F1']"
    stIdVersion "R-HSA-140217.4"
    speciesName "Homo sapiens"
    category "omitted"
    displayName "Transactivation of PMAIP1 (NOXA) by E2F1"
  ]
  node [
    id 15
    label "Positive gene expression regulation by 'E2F1:TFDP1:PMAIP1 Gene [nucleoplasm]'"
    schemaClass "PositiveGeneExpressionRegulation"
    stId "R-HSA-159039"
    oldStId "REACT_6130"
    stIdVersion "R-HSA-159039.1"
    displayName "Positive gene expression regulation by 'E2F1:TFDP1:PMAIP1 Gene [nucleoplasm]'"
  ]
  node [
    id 16
    label "E2F1:TFDP1,TFDP2 [nucleoplasm]"
    schemaClass "Complex"
    stId "R-HSA-68653"
    oldStId "REACT_5400"
    name "['E2F1:TFDP1,TFDP2','DP1/2:E2F1']"
    stIdVersion "R-HSA-68653.2"
    speciesName "Homo sapiens"
    displayName "E2F1:TFDP1,TFDP2 [nucleoplasm]"
  ]
  node [
    id 17
    label "E2F1 [nucleoplasm]"
    schemaClass "EntityWithAccessionedSequence"
    stId "R-HSA-68639"
    oldStId "REACT_2601"
    name "['E2F1','Transcription factor E2F1','E2F-1','Retinoblastoma binding protein 3','RBBP-3','PRB-binding protein E2F-1','PBR3','Retinoblastoma-associated protein 1','RBAP-1']"
    stIdVersion "R-HSA-68639.2"
    speciesName "Homo sapiens"
    referenceType "ReferenceGeneProduct"
    displayName "E2F1 [nucleoplasm]"
  ]
  node [
    id 18
    label "E2F1:(TFDP1,TFDP2) [nucleoplasm]"
    schemaClass "Complex"
    stId "R-HSA-9007512"
    name "['E2F1:(TFDP1,TFDP2)']"
    stIdVersion "R-HSA-9007512.1"
    speciesName "Homo sapiens"
    displayName "E2F1:(TFDP1,TFDP2) [nucleoplasm]"
  ]
  node [
    id 19
    label "E2F1 binds APAF1 gene promoter"
    schemaClass "Reaction"
    stId "R-HSA-9007514"
    releaseDate "2017-09-12"
    name "['E2F1 binds APAF1 gene promoter']"
    stIdVersion "R-HSA-9007514.2"
    speciesName "Homo sapiens"
    category "binding"
    displayName "E2F1 binds APAF1 gene promoter"
  ]
  node [
    id 20
    label "APAF1 gene expression is stimulated by E2F1 and inhibited by E2F6"
    schemaClass "BlackBoxEvent"
    stId "R-HSA-9007496"
    releaseDate "2017-09-12"
    name "['APAF1 gene expression is stimulated by E2F1 and inhibited by E2F6']"
    stIdVersion "R-HSA-9007496.4"
    speciesName "Homo sapiens"
    category "omitted"
    displayName "APAF1 gene expression is stimulated by E2F1 and inhibited by E2F6"
  ]
  node [
    id 21
    label "APAF1 [cytosol]"
    schemaClass "EntityWithAccessionedSequence"
    stId "R-HSA-50099"
    oldStId "REACT_3886"
    name "['APAF1','Apaf-1','Apoptotic protease activating factor 1']"
    stIdVersion "R-HSA-50099.1"
    speciesName "Homo sapiens"
    referenceType "ReferenceGeneProduct"
    displayName "APAF1 [cytosol]"
  ]
  node [
    id 22
    label "APAF1:CYCS [cytosol]"
    schemaClass "Complex"
    stId "R-HSA-114253"
    oldStId "REACT_4880"
    name "['APAF1:CYCS','APAF1:Cytochrome C']"
    stIdVersion "R-HSA-114253.2"
    speciesName "Homo sapiens"
    displayName "APAF1:CYCS [cytosol]"
  ]
  node [
    id 23
    label "E2F1 binds PMAIP1 (NOXA) promoter"
    schemaClass "Reaction"
    stId "R-HSA-4331327"
    oldStId "REACT_169402"
    releaseDate "2013-09-18"
    name "['E2F1 binds PMAIP1 (NOXA) promoter']"
    stIdVersion "R-HSA-4331327.3"
    speciesName "Homo sapiens"
    category "binding"
    displayName "E2F1 binds PMAIP1 (NOXA) promoter"
  ]
  node [
    id 24
    label "PMAIP1 [cytosol]"
    schemaClass "EntityWithAccessionedSequence"
    stId "R-HSA-140215"
    oldStId "REACT_4210"
    name "['PMAIP1','NOXA protein']"
    stIdVersion "R-HSA-140215.1"
    speciesName "Homo sapiens"
    referenceType "ReferenceGeneProduct"
    searchSeed "1"
    displayName "PMAIP1 [cytosol]"
  ]
  node [
    id 25
    label "CYCS [mitochondrial intermembrane space]"
    schemaClass "EntityWithAccessionedSequence"
    stId "R-HSA-114244"
    oldStId "REACT_3942"
    name "['CYCS','Cytochrome c']"
    stIdVersion "R-HSA-114244.1"
    speciesName "Homo sapiens"
    referenceType "ReferenceGeneProduct"
    displayName "CYCS [mitochondrial intermembrane space]"
  ]
  node [
    id 26
    label "CYCS gene:NRF1:PPARGC1B [nucleoplasm]"
    schemaClass "Complex"
    stId "R-HSA-2466382"
    oldStId "REACT_265699"
    name "['CYCS gene:NRF1:PPARGC1B','NRF1:PGC-1beta:CYCS']"
    stIdVersion "R-HSA-2466382.1"
    speciesName "Homo sapiens"
    displayName "CYCS gene:NRF1:PPARGC1B [nucleoplasm]"
  ]
  node [
    id 27
    label "NRF1 [nucleoplasm]"
    schemaClass "EntityWithAccessionedSequence"
    stId "R-HSA-1592205"
    oldStId "REACT_117514"
    name "['NRF1','Nuclear respiratory factor 1','NRF1_HUMAN']"
    stIdVersion "R-HSA-1592205.1"
    speciesName "Homo sapiens"
    referenceType "ReferenceGeneProduct"
    displayName "NRF1 [nucleoplasm]"
  ]
  node [
    id 28
    label "NRF1:p-PPARGC1A, NRF2 bind the TFB2M promoter"
    schemaClass "Reaction"
    stId "R-HSA-2466392"
    oldStId "REACT_264641"
    releaseDate "2014-03-12"
    name "['NRF1:p-PPARGC1A, NRF2 bind the TFB2M promoter']"
    stIdVersion "R-HSA-2466392.2"
    speciesName "Homo sapiens"
    category "binding"
    displayName "NRF1:p-PPARGC1A, NRF2 bind the TFB2M promoter"
  ]
  node [
    id 29
    label "p38 MAPK phosphorylates PPARGC1A"
    schemaClass "Reaction"
    stId "R-HSA-1592233"
    oldStId "REACT_263998"
    releaseDate "2014-03-12"
    name "['p38 MAPK phosphorylates PPARGC1A']"
    stIdVersion "R-HSA-1592233.2"
    speciesName "Homo sapiens"
    category "transition"
    displayName "p38 MAPK phosphorylates PPARGC1A"
  ]
  node [
    id 30
    label "PPARGC1A [nucleoplasm]"
    schemaClass "EntityWithAccessionedSequence"
    stId "R-HSA-442481"
    oldStId "REACT_27383"
    name "['PPARGC1A','Peroxisome proliferator-activated receptor gamma coactivator 1-alpha','PRGC1_HUMAN','PGC1A','PGC-1alpha']"
    stIdVersion "R-HSA-442481.2"
    speciesName "Homo sapiens"
    referenceType "ReferenceGeneProduct"
    displayName "PPARGC1A [nucleoplasm]"
  ]
  node [
    id 31
    label "RORA:Coactivator [nucleoplasm]"
    schemaClass "Complex"
    stId "R-HSA-1368124"
    oldStId "REACT_111748"
    name "['RORA:Coactivator']"
    stIdVersion "R-HSA-1368124.1"
    speciesName "Homo sapiens"
    displayName "RORA:Coactivator [nucleoplasm]"
  ]
  node [
    id 32
    label "EP300 [nucleoplasm]"
    schemaClass "EntityWithAccessionedSequence"
    stId "R-HSA-381325"
    oldStId "REACT_26137"
    name "['EP300','p300','Histone acetyltransferase p300','EP300_HUMAN','KAT3B']"
    stIdVersion "R-HSA-381325.1"
    speciesName "Homo sapiens"
    referenceType "ReferenceGeneProduct"
    displayName "EP300 [nucleoplasm]"
  ]
  node [
    id 33
    label "p-S15,S20-TP53:EP300:PRMT1:CARM1:GADD45A Gene [nucleoplasm]"
    schemaClass "Complex"
    stId "R-HSA-3215149"
    name "['p-S15,S20-TP53:EP300:PRMT1:CARM1:GADD45A Gene']"
    stIdVersion "R-HSA-3215149.1"
    speciesName "Homo sapiens"
    displayName "p-S15,S20-TP53:EP300:PRMT1:CARM1:GADD45A Gene [nucleoplasm]"
  ]
  node [
    id 34
    label "NRF1:PPARGC1B binds the CYCS promoter"
    schemaClass "Reaction"
    stId "R-HSA-2466370"
    oldStId "REACT_264393"
    releaseDate "2014-03-12"
    name "['NRF1:PPARGC1B binds the CYCS promoter']"
    stIdVersion "R-HSA-2466370.2"
    speciesName "Homo sapiens"
    category "binding"
    displayName "NRF1:PPARGC1B binds the CYCS promoter"
  ]
  node [
    id 35
    label "Expression of NRF1"
    schemaClass "BlackBoxEvent"
    stId "R-HSA-1592242"
    oldStId "REACT_264032"
    releaseDate "2014-03-12"
    name "['Expression of NRF1']"
    stIdVersion "R-HSA-1592242.4"
    speciesName "Homo sapiens"
    category "omitted"
    displayName "Expression of NRF1"
  ]
  node [
    id 36
    label "Expression of CYCS"
    schemaClass "BlackBoxEvent"
    stId "R-HSA-1592231"
    oldStId "REACT_263920"
    releaseDate "2014-03-12"
    name "['Expression of CYCS','Expression of Cytochrome c']"
    stIdVersion "R-HSA-1592231.7"
    speciesName "Homo sapiens"
    category "omitted"
    displayName "Expression of CYCS"
  ]
  node [
    id 37
    label "Positive regulation by 'ESRRA [nucleoplasm]'"
    stId "R-HSA-1605565"
    oldStId "REACT_267555"
    schemaClass "PositiveRegulation"
    stIdVersion "R-HSA-1605565.1"
    displayName "Positive regulation by 'ESRRA [nucleoplasm]'"
  ]
  node [
    id 38
    label "ESRRA [nucleoplasm]"
    schemaClass "EntityWithAccessionedSequence"
    stId "R-HSA-446159"
    oldStId "REACT_21133"
    name "['ESRRA','Steroid hormone receptor ERR1','ERR1_HUMAN']"
    stIdVersion "R-HSA-446159.1"
    speciesName "Homo sapiens"
    referenceType "ReferenceGeneProduct"
    displayName "ESRRA [nucleoplasm]"
  ]
  node [
    id 39
    label "ESRRA:PPARGC1A [nucleoplasm]"
    schemaClass "Complex"
    stId "R-HSA-8939924"
    name "['ESRRA:PPARGC1A']"
    stIdVersion "R-HSA-8939924.1"
    speciesName "Homo sapiens"
    displayName "ESRRA:PPARGC1A [nucleoplasm]"
  ]
  edge [
    source 0
    target 1
    key 0
  ]
  edge [
    source 0
    target 6
    key 0
  ]
  edge [
    source 0
    target 7
    key 0
  ]
  edge [
    source 0
    target 8
    key 0
  ]
  edge [
    source 1
    target 2
    key 0
  ]
  edge [
    source 1
    target 7
    key 0
  ]
  edge [
    source 1
    target 9
    key 0
  ]
  edge [
    source 1
    target 33
    key 0
  ]
  edge [
    source 2
    target 3
    key 0
  ]
  edge [
    source 3
    target 21
    key 0
  ]
  edge [
    source 3
    target 4
    key 0
  ]
  edge [
    source 4
    target 5
    key 0
  ]
  edge [
    source 4
    target 13
    key 0
  ]
  edge [
    source 5
    target 13
    key 0
  ]
  edge [
    source 5
    target 22
    key 0
  ]
  edge [
    source 5
    target 36
    key 0
  ]
  edge [
    source 6
    target 7
    key 0
  ]
  edge [
    source 6
    target 8
    key 0
  ]
  edge [
    source 6
    target 14
    key 0
  ]
  edge [
    source 6
    target 23
    key 0
  ]
  edge [
    source 7
    target 9
    key 0
  ]
  edge [
    source 8
    target 9
    key 0
  ]
  edge [
    source 8
    target 10
    key 0
  ]
  edge [
    source 10
    target 14
    key 0
  ]
  edge [
    source 10
    target 11
    key 0
  ]
  edge [
    source 10
    target 24
    key 0
  ]
  edge [
    source 11
    target 12
    key 0
  ]
  edge [
    source 12
    target 13
    key 0
  ]
  edge [
    source 13
    target 25
    key 0
  ]
  edge [
    source 14
    target 15
    key 0
  ]
  edge [
    source 14
    target 23
    key 0
  ]
  edge [
    source 15
    target 16
    key 0
  ]
  edge [
    source 16
    target 17
    key 0
  ]
  edge [
    source 16
    target 23
    key 0
  ]
  edge [
    source 17
    target 18
    key 0
  ]
  edge [
    source 18
    target 19
    key 0
  ]
  edge [
    source 19
    target 20
    key 0
  ]
  edge [
    source 20
    target 21
    key 0
  ]
  edge [
    source 21
    target 22
    key 0
  ]
  edge [
    source 26
    target 27
    key 0
  ]
  edge [
    source 26
    target 34
    key 0
  ]
  edge [
    source 27
    target 28
    key 0
  ]
  edge [
    source 27
    target 34
    key 0
  ]
  edge [
    source 27
    target 35
    key 0
  ]
  edge [
    source 28
    target 29
    key 0
  ]
  edge [
    source 28
    target 35
    key 0
  ]
  edge [
    source 29
    target 30
    key 0
  ]
  edge [
    source 29
    target 35
    key 0
  ]
  edge [
    source 30
    target 31
    key 0
  ]
  edge [
    source 30
    target 39
    key 0
  ]
  edge [
    source 31
    target 32
    key 0
  ]
  edge [
    source 32
    target 33
    key 0
  ]
  edge [
    source 34
    target 35
    key 0
  ]
  edge [
    source 34
    target 36
    key 0
  ]
  edge [
    source 36
    target 37
    key 0
  ]
  edge [
    source 37
    target 38
    key 0
  ]
  edge [
    source 38
    target 39
    key 0
  ]
]
