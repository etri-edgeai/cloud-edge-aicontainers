# Edge Device Performance


## Apple M1 chip vs Nvidia GPU

https://appleinsider.com/articles/21/10/19/m1-pro-and-m1-max-gpu-performance-versus-nvidia-and-amd

```csv
. Apple Silicon processor,	M1,	M1 Pro,	M1 Pro,	M1 Max,	M1 Max
. GPU core count,	8,	14,	16,	24,	32
. Teraflops,	2.6,	4.5,	5.2,	7.8,	10.4
. AMD equivalent GPU,	Radeon RX 560 (2.6TF),	Radeon RX 5500M (4.6TF),	Radeon RX 5500 (5.2TF),	Radeon RX 5700M (7.9TF),	Radeon RX Vega 56 (10.5TF)
. Nvidia equivalent GPU	GeForce GTX 1650 (2.9TF),	GeForce GTX 1650 Super (4.4TF),	GeForce GTX 1660 Ti (5.4TF), GeForce RTX 2070 (7.4TF),	GeForce RTX 2080 (10TF)

```


- Markdown Table

|. Apple Silicon processor,|M1,                          |M1 Pro,                        |M1 Pro,                                               |M1 Max,                 |M1 Max                    |
|--------------------------|-----------------------------|-------------------------------|------------------------------------------------------|------------------------|--------------------------|
|. GPU core count,         |8,                           |14,                            |16,                                                   |24,                     |32                        |
|. Teraflops,              |2.6,                         |4.5,                           |5.2,                                                  |7.8,                    |10.4                      |
|. AMD equivalent GPU,     |Radeon RX 560 (2.6TF),       |Radeon RX 5500M (4.6TF),       |Radeon RX 5500 (5.2TF),                               |Radeon RX 5700M (7.9TF),|Radeon RX Vega 56 (10.5TF)|
|. Nvidia equivalent GPU   |GeForce GTX 1650 (2.9TF),    |GeForce GTX 1650 Super (4.4TF),|GeForce GTX 1660 Ti (5.4TF), GeForce RTX 2070 (7.4TF),|GeForce RTX 2080 (10TF) |                          |


## Nvidia GPU benchmarks

```csv

Device,Score
NVIDIA GeForce RTX 3090 Ti,260346
NVIDIA A100 80GB PCIe,259828
NVIDIA A100-PCIE-80GB,256292
GeForce RTX 3090,238123
NVIDIA A100-SXM4-40GB,237220
GeForce RTX 3080 Ti,235513
NVIDIA GeForce RTX 3090,235225
GRID A100-7-40C MIG 7g.40gb,233910
NVIDIA GeForce RTX 3080 Ti,233178
A100-SXM4-40GB,230855
RTX A6000,224604
NVIDIA RTX A6000,221395
GRID A100-4C,219037
Tesla V100S-PCIE-32GB,216224
A100-PCIE-40GB,215434
NVIDIA GeForce RTX 3080,206390
NVIDIA A40,205120
A40,204193
Tesla V100-SXM2-32GB,203550
GeForce RTX 3080,202162
Tesla V100-SXM2-16GB,201257
NVIDIA A100-PCIE-40GB,200242
RTX A5000,193384
Tesla V100-PCIE-16GB,192531
Tesla V100-PCIE-32GB,191375
NVIDIA RTX A5000,190987
NVIDIA A10G,187763
NVIDIA A10,186108
NVIDIA A40-8Q,183852
Quadro GV100,180942
NVIDIA TITAN V,179522
GRID V100D-32Q,178886
TITAN V,176773
NVIDIA GeForce RTX 2080 Ti,176681
Tesla V100-FHHL-16GB,174445
NVIDIA RTX A4500,171509
TITAN RTX,167076
NVIDIA TITAN RTX,166517
NVIDIA GeForce RTX 3070 Ti,165866
GeForce RTX 2080 Ti,165093
GRID V100D-16Q,163420
Quadro RTX 6000,159550
GRID RTX6000-3Q,152526
GeForce RTX 3070,149734
GRID RTX6000-6Q,149498
NVIDIA GeForce RTX 3080 Ti Laptop GPU,148511
NVIDIA GeForce RTX 3070,148340
Quadro RTX 8000,144049
NVIDIA GeForce RTX 3070 Ti Laptop GPU,141168
NVIDIA A30,139688
RTX A5000 Laptop GPU,139395
GeForce RTX 3080 Laptop GPU,138398
NVIDIA GeForce RTX 3080 Laptop GPU,137987
GRID RTX6000-2Q,137891
GRID RTX6000-8Q,134624
GRID RTX6000-4Q,132933
GeForce RTX 3060 Ti,128321
NVIDIA RTX A5000 Laptop GPU,127880
NVIDIA GeForce RTX 3060 Ti,126847
NVIDIA GeForce RTX 2080 SUPER,126130
GeForce RTX 2080 SUPER,126056
GRID RTX8000P-6Q,125055
NVIDIA RTX A4000,124547
RTX A4000,123839
NVIDIA GeForce RTX 3070 Laptop GPU,122041
NVIDIA GeForce RTX 2080,120612
NVIDIA Quadro RTX 8000,119714
GeForce RTX 3070 Laptop GPU,119627
GeForce RTX 2080,119410
Graphics Device,118931
NVIDIA RTX A4000 Laptop GPU,118896
NVIDIA Quadro RTX 5000,117173
RTX A4000 Laptop GPU,113500
NVIDIA GeForce RTX 2070 SUPER,108083
GeForce RTX 2070 SUPER,107983
NVIDIA GeForce RTX 2080 Super with Max-Q Design,104422
NVIDIA GeForce RTX 2080 with Max-Q Design,104025
GeForce RTX 2080 with Max-Q Design,102896
GeForce RTX 2080 Super with Max-Q Design,102038
NVIDIA GeForce RTX 3060,99213
NVIDIA Quadro RTX 5000 with Max-Q Design,99084
GeForce RTX 3060,98715
NVIDIA GeForce RTX 3060 Laptop GPU,98709
Quadro RTX 5000 with Max-Q Design,97310
Quadro RTX 5000,96650
GeForce RTX 3060 Laptop GPU,96424
NVIDIA GeForce RTX 2070,96024
GeForce RTX 2070,95666
A40-12Q,95329
GeForce RTX 2060 SUPER,95114
NVIDIA GeForce RTX 2060 SUPER,94330
Quadro RTX 4000,94250
Quadro GP100,92763
NVIDIA RTX A3000 Laptop GPU,90882
RTX A3000 Laptop GPU,90533
NVIDIA GeForce RTX 2070 Super with Max-Q Design,89663
NVIDIA Quadro RTX 4000,87161
NVIDIA GeForce RTX 2070 with Max-Q Design,86778
GeForce RTX 2070 with Max-Q Design,84449
GRID A100-2-10C MIG 2g.10gb,84208
Tesla P100-PCIE-16GB,84011
NVIDIA RTX A2000,84002
NVIDIA RTX A2000 12GB,83470
GeForce RTX 2070 Super with Max-Q Design,80580
Tesla P100-PCIE-12GB,80217
Tesla T4,78434
NVIDIA GeForce RTX 2060,78091
GeForce RTX 2060,77840
GRID T4-2Q,77714
NVIDIA GeForce RTX 3050,72998
NVIDIA Tesla T4,70627
GRID T4-16Q,70576
Quadro RTX 3000,70456
Tesla P100-SXM2-16GB,69446
GeForce RTX 2060 with Max-Q Design,67657
NVIDIA GeForce RTX 2060 with Max-Q Design,67588
Quadro RTX 4000 with Max-Q Design,67141
NVIDIA GeForce RTX 3050 Ti Laptop GPU,66487
NVIDIA GeForce GTX 1660 Ti,66368
GeForce GTX 1660 Ti,65308
NVIDIA GeForce GTX 1660 SUPER,65154
GeForce GTX 1660 SUPER,65044
Quadro RTX 3000 with Max-Q Design,64172
GeForce RTX 3050 Ti Laptop GPU,62628
NVIDIA GeForce GTX 1660 Ti with Max-Q Design,61528
NVIDIA RTX A2000 Laptop GPU,61347
GeForce GTX 1660 Ti with Max-Q Design,60838
NVIDIA GeForce GTX 1660,60503
GeForce GTX 1660,60172
GRID T4-4Q,59903
NVIDIA TITAN Xp COLLECTORS EDITION,59596
GeForce RTX 3050 Laptop GPU,58544
NVIDIA GeForce RTX 3050 Laptop GPU,58518
NVIDIA TITAN Xp,58384
RTX A2000 Laptop GPU,58328
TITAN Xp,57897
NVIDIA GeForce GTX 1650 SUPER,57126
GeForce GTX 1650 SUPER,56481
NVIDIA TITAN X (Pascal),56205
NVIDIA GeForce GTX 1080 Ti,55628
GeForce GTX 1080 Ti,55161
TITAN X (Pascal),54087
GRID T4-8Q,52866
GeForce GTX 1080,51531
NVIDIA GeForce GTX 1080,51030
NVIDIA GeForce GTX 1070 Ti,50088
GeForce GTX 1070 Ti,49727
NVIDIA GeForce GTX 1650 Ti,48337
Tesla P40,47664
Quadro P6000,47462
GeForce GTX 1080 with Max-Q Design,46955
Quadro P5200 with Max-Q Design,46329
Quadro P5200,45689
NVIDIA GeForce GTX 1070,45558
GeForce GTX 1070,45301
Quadro P5000,45153
GeForce GTX 1650 Ti,44348
NVIDIA GeForce GTX 1080 with Max-Q Design,44255
T1200 Laptop GPU,43441
NVIDIA T1200 Laptop GPU,43342
Quadro T2000 with Max-Q Design,41307
GRID A100-1-5C MIG 1g.5gb,41284
GRID P40-2Q,41169
GeForce GTX 1650 Ti with Max-Q Design,41158
Quadro T2000,41149
NVIDIA GeForce GTX 1650 Ti with Max-Q Design,40355
NVIDIA GeForce GTX 1650,40258
GeForce GTX 1650,39941
NVIDIA Quadro P4000,39254
Quadro P4000,38590
NVIDIA T1000 8GB,38577
NVIDIA GeForce GTX 1070 with Max-Q Design,38193
NVIDIA A2,38140
GeForce GTX 1650 with Max-Q Design,37945
GeForce GTX 1070 with Max-Q Design,37934
NVIDIA T1000,37817
Quadro P4200,37676
NVIDIA GeForce GTX 1650 with Max-Q Design,37506
NVIDIA GeForce GTX 980 Ti,36268
NVIDIA T600 Laptop GPU,36000
GeForce GTX 980 Ti,35714
P106-100,34239
Quadro T1000,34236
NVIDIA GeForce GTX 1060 6GB,34034
Quadro T1000 with Max-Q Design,33978
NVIDIA GeForce GTX TITAN X,33701
GeForce GTX 1060 6GB,33538
GeForce GTX TITAN X,33524
Quadro M6000,32385
Quadro M6000 24GB,32156
NVIDIA GeForce GTX 1060 3GB,31922
GeForce GTX 1060 3GB,31768
Quadro P3200 with Max-Q Design,31592
Tesla P4,31513
NVIDIA Tesla M40,31401
GeForce GTX 1060,31129
Tesla M40 24GB,31126
T500,30990
Tesla M40,30703
NVIDIA GeForce GTX 1060,30585
NVIDIA Quadro P2200,30389
GeForce GTX 1060 5GB,30206
Quadro P2200,29989
GeForce MX450,29969
NVIDIA GeForce GTX 980,29848
GeForce GTX 980,29546
NVIDIA GeForce GTX 1060 5GB,28858
NVIDIA GeForce MX450,28725
NVIDIA GeForce GTX 1060 with Max-Q Design,28312
T600,28084
Quadro P3200,27741
GeForce GTX 1060 with Max-Q Design,27623
NVIDIA T500,27144
NVIDIA T600,26600
NVIDIA GeForce GTX 970,25908
GeForce GTX 970,25897
Tesla M60,25404
Quadro M5000,24565
Quadro P3000,22837
Quadro P2000,21668
NVIDIA GeForce GTX 980M,21520
GeForce GTX 980M,21471
NVIDIA Quadro P2000,21174
GeForce GTX 780 Ti,20877
P106-090,20839
NVIDIA GeForce GTX 780 Ti,20818
GeForce GTX 1050 Ti,20616
NVIDIA GeForce GTX 1050 Ti,20406
GeForce GTX TITAN Black,20282
Quadro M5000M,20269
GeForce GTX 1050 Ti with Max-Q Design,18936
NVIDIA GeForce GTX 1050 Ti with Max-Q Design,18674
GeForce GTX TITAN Z,18422
NVIDIA GeForce GTX 970M,18285
Quadro P2000 with Max-Q Design,18218
GeForce GTX 780,18049
NVIDIA GeForce GTX TITAN,17933
GeForce GTX 960,17784
GeForce GTX TITAN,17711
NVIDIA GeForce GTX 960,17693
Quadro K6000,17571
NVIDIA GeForce GTX 1050,17206
GeForce GTX 970M,17191
NVIDIA GeForce GTX 780,17078
GeForce GTX 1050,16976
NVIDIA T400,16856
Quadro M4000,16648
NVIDIA T400 4GB,16323
T400,16307
NVIDIA Tesla K80,16063
NVIDIA GeForce GTX 950,15998
GeForce GTX 950,15806
Quadro M3000M,15678
GeForce GTX 1050 with Max-Q Design,15058
Tesla K80,14679
NVIDIA GeForce GTX 1050 with Max-Q Design,14577
Tesla K40c,14510
Quadro P1000,14286
NVIDIA Tesla K40m,14135
Tesla K40m,14115
GeForce GTX 965M,13861
NVIDIA GeForce GTX 770,13824
GeForce GTX 770,13785
Quadro K5200,13735
NVIDIA GeForce GTX 965M,13714
NVIDIA GeForce GTX 680,13627
GeForce GTX 680,13248
Quadro M2000,13100
Quadro M2200,12812
Tesla K20Xm,12681
GeForce MX350,12572
NVIDIA GeForce GTX 690,12549
NVIDIA GeForce GTX 750 Ti,12510
GeForce GTX 750 Ti,12499
GeForce GTX 690,12263
NVIDIA GeForce MX350,12232
Tesla M10,12054
Tesla K20m,12019
NVIDIA GeForce GTX 670,11969
Tesla K20c,11850
GeForce GTX 960M,11818
Quadro P620,11727
NVIDIA Tesla M10,11721
GeForce GTX 670,11611
NVIDIA Quadro K2200,11549
NVIDIA GeForce GTX 960M,11507
Quadro K2200,11410
GeForce GTX 680MX,11307
NVIDIA GeForce GTX 660 Ti,11298
GeForce GTX 660 Ti,11274
GeForce GTX 860M,11144
NVIDIA Quadro M2000M,11041
NVIDIA GeForce GTX 860M,10778
GeForce GTX 760,10683
Quadro P600,10634
NVIDIA GeForce GTX 760,10624
NVIDIA GeForce GTX 750,10510
GeForce GTX 750,10448
Quadro M2000M,10438
GeForce GT 1030,10307
Quadro M1200,10296
NVIDIA GeForce GT 1030,10287
GeForce GTX 880M,10249
GRID M10-8Q,10107
NVIDIA Quadro P620,9995
GeForce MX330,9906
GeForce MX150,9799
GeForce GTX 950M,9777
GeForce MX250,9734
NVIDIA GeForce MX250,9707
NVIDIA GeForce MX150,9551
NVIDIA GeForce GTX 850M,9545
GeForce GTX 780M,9535
GeForce GTX 870M,9499
NVIDIA GeForce GTX 950M,9463
NVIDIA GeForce MX330,9322
GeForce GTX 850M,9302
Quadro K1200,9073
NVIDIA GeForce GTX 760 (192-bit),9058
GeForce GTX 760 (192-bit),9027
NVIDIA Quadro K4200,8973
Quadro K4200,8946
NVIDIA GeForce GPU,8890
Quadro M620,8602
GeForce GTX 660,8583
Quadro K5000,8558
Quadro M1000M,8471
NVIDIA GeForce GTX 660,8458
Quadro P520,7481
Quadro M520,7173
NVIDIA GeForce MX130,7156
NVIDIA GeForce GTX 650 Ti BOOST,7132
GeForce GTX 675MX,7085
NVIDIA GeForce MX230,6914
GeForce MX130,6872
Quadro K4100M,6821
GeForce GTX 650 Ti BOOST,6809
Quadro K620,6653
NVIDIA Quadro K620,6621
GeForce MX230,6604
GeForce GTX 770M,6572
GeForce GPU,6529
NVIDIA GeForce GTX 745,6443
Quadro P500,6438
NVIDIA GeForce 940MX,6363
GeForce GTX 745,6310
GeForce 940MX,6290
GeForce GTX 650 Ti,6223
NVIDIA GeForce GTX 650 Ti,5920
GeForce 940M,5882
Quadro M500M,5713
NVIDIA GeForce 940M,5703
Quadro P400,5691
NVIDIA GeForce 840M,5629
NVIDIA GeForce 930MX,5599
GeForce 930MX,5566
GeForce 840M,5561
GeForce GTX 765M,5514
Quadro K4000,5210
GeForce 930M,5123
NVIDIA GeForce 930M,4932
Quadro K4000M,4650
GeForce MX110,4625
NVIDIA GeForce MX110,4483
GeForce 830M,4342
GeForce GTX 760M,4287
GeForce 920MX,4274
NVIDIA GeForce 920MX,4240
Quadro K3100M,4121
NVIDIA GeForce GTX 645,3630
NVIDIA GeForce GTX 650,3469
GeForce GTX 650,3424
NVIDIA GeForce GT 740,3302
GeForce GT 740,3273
GeForce GT 750M,3118
Quadro K2000,3055
Quadro K2100M,3028
GeForce GTX 660M,2901
GeForce GT 640,2853
GeForce GT 745M,2836
NVIDIA GeForce GT 640,2825
GeForce GT 635,2794
GeForce GT 740M,2783
GeForce 920M,2766
NVIDIA GeForce GT 730,2743
GeForce GT 730,2682
GeForce GT 650M,2651
GeForce GT 730M,2459
Quadro K2000M,2385
NVIDIA GeForce GT 630,2317
Quadro K1100M,2205
GeForce GT 640M,2200
GeForce GT 630,1715
NVIDIA GeForce GT 710,1534
GeForce GT 710,1519
GeForce GT 720,1514
Quadro K610M,1504
Quadro K600,1356
Quadro K420,1350
Quadro K1000M,1335
NVS 510,1282

```


- Markdown table
|Device|Score                        |
|------|-----------------------------|
|NVIDIA GeForce RTX 3090 Ti|260346                       |
|NVIDIA A100 80GB PCIe|259828                       |
|NVIDIA A100-PCIE-80GB|256292                       |
|GeForce RTX 3090|238123                       |
|NVIDIA A100-SXM4-40GB|237220                       |
|GeForce RTX 3080 Ti|235513                       |
|NVIDIA GeForce RTX 3090|235225                       |
|GRID A100-7-40C MIG 7g.40gb|233910                       |
|NVIDIA GeForce RTX 3080 Ti|233178                       |
|A100-SXM4-40GB|230855                       |
|RTX A6000|224604                       |
|NVIDIA RTX A6000|221395                       |
|GRID A100-4C|219037                       |
|Tesla V100S-PCIE-32GB|216224                       |
|A100-PCIE-40GB|215434                       |
|NVIDIA GeForce RTX 3080|206390                       |
|NVIDIA A40|205120                       |
|A40   |204193                       |
|Tesla V100-SXM2-32GB|203550                       |
|GeForce RTX 3080|202162                       |
|Tesla V100-SXM2-16GB|201257                       |
|NVIDIA A100-PCIE-40GB|200242                       |
|RTX A5000|193384                       |
|Tesla V100-PCIE-16GB|192531                       |
|Tesla V100-PCIE-32GB|191375                       |
|NVIDIA RTX A5000|190987                       |
|NVIDIA A10G|187763                       |
|NVIDIA A10|186108                       |
|NVIDIA A40-8Q|183852                       |
|Quadro GV100|180942                       |
|NVIDIA TITAN V|179522                       |
|GRID V100D-32Q|178886                       |
|TITAN V|176773                       |
|NVIDIA GeForce RTX 2080 Ti|176681                       |
|Tesla V100-FHHL-16GB|174445                       |
|NVIDIA RTX A4500|171509                       |
|TITAN RTX|167076                       |
|NVIDIA TITAN RTX|166517                       |
|NVIDIA GeForce RTX 3070 Ti|165866                       |
|GeForce RTX 2080 Ti|165093                       |
|GRID V100D-16Q|163420                       |
|Quadro RTX 6000|159550                       |
|GRID RTX6000-3Q|152526                       |
|GeForce RTX 3070|149734                       |
|GRID RTX6000-6Q|149498                       |
|NVIDIA GeForce RTX 3080 Ti Laptop GPU|148511                       |
|NVIDIA GeForce RTX 3070|148340                       |
|Quadro RTX 8000|144049                       |
|NVIDIA GeForce RTX 3070 Ti Laptop GPU|141168                       |
|NVIDIA A30|139688                       |
|RTX A5000 Laptop GPU|139395                       |
|GeForce RTX 3080 Laptop GPU|138398                       |
|NVIDIA GeForce RTX 3080 Laptop GPU|137987                       |
|GRID RTX6000-2Q|137891                       |
|GRID RTX6000-8Q|134624                       |
|GRID RTX6000-4Q|132933                       |
|GeForce RTX 3060 Ti|128321                       |
|NVIDIA RTX A5000 Laptop GPU|127880                       |
|NVIDIA GeForce RTX 3060 Ti|126847                       |
|NVIDIA GeForce RTX 2080 SUPER|126130                       |
|GeForce RTX 2080 SUPER|126056                       |
|GRID RTX8000P-6Q|125055                       |
|NVIDIA RTX A4000|124547                       |
|RTX A4000|123839                       |
|NVIDIA GeForce RTX 3070 Laptop GPU|122041                       |
|NVIDIA GeForce RTX 2080|120612                       |
|NVIDIA Quadro RTX 8000|119714                       |
|GeForce RTX 3070 Laptop GPU|119627                       |
|GeForce RTX 2080|119410                       |
|Graphics Device|118931                       |
|NVIDIA RTX A4000 Laptop GPU|118896                       |
|NVIDIA Quadro RTX 5000|117173                       |
|RTX A4000 Laptop GPU|113500                       |
|NVIDIA GeForce RTX 2070 SUPER|108083                       |
|GeForce RTX 2070 SUPER|107983                       |
|NVIDIA GeForce RTX 2080 Super with Max-Q Design|104422                       |
|NVIDIA GeForce RTX 2080 with Max-Q Design|104025                       |
|GeForce RTX 2080 with Max-Q Design|102896                       |
|GeForce RTX 2080 Super with Max-Q Design|102038                       |
|NVIDIA GeForce RTX 3060|99213                        |
|NVIDIA Quadro RTX 5000 with Max-Q Design|99084                        |
|GeForce RTX 3060|98715                        |
|NVIDIA GeForce RTX 3060 Laptop GPU|98709                        |
|Quadro RTX 5000 with Max-Q Design|97310                        |
|Quadro RTX 5000|96650                        |
|GeForce RTX 3060 Laptop GPU|96424                        |
|NVIDIA GeForce RTX 2070|96024                        |
|GeForce RTX 2070|95666                        |
|A40-12Q|95329                        |
|GeForce RTX 2060 SUPER|95114                        |
|NVIDIA GeForce RTX 2060 SUPER|94330                        |
|Quadro RTX 4000|94250                        |
|Quadro GP100|92763                        |
|NVIDIA RTX A3000 Laptop GPU|90882                        |
|RTX A3000 Laptop GPU|90533                        |
|NVIDIA GeForce RTX 2070 Super with Max-Q Design|89663                        |
|NVIDIA Quadro RTX 4000|87161                        |
|NVIDIA GeForce RTX 2070 with Max-Q Design|86778                        |
|GeForce RTX 2070 with Max-Q Design|84449                        |
|GRID A100-2-10C MIG 2g.10gb|84208                        |
|Tesla P100-PCIE-16GB|84011                        |
|NVIDIA RTX A2000|84002                        |
|NVIDIA RTX A2000 12GB|83470                        |
|GeForce RTX 2070 Super with Max-Q Design|80580                        |
|Tesla P100-PCIE-12GB|80217                        |
|Tesla T4|78434                        |
|NVIDIA GeForce RTX 2060|78091                        |
|GeForce RTX 2060|77840                        |
|GRID T4-2Q|77714                        |
|NVIDIA GeForce RTX 3050|72998                        |
|NVIDIA Tesla T4|70627                        |
|GRID T4-16Q|70576                        |
|Quadro RTX 3000|70456                        |
|Tesla P100-SXM2-16GB|69446                        |
|GeForce RTX 2060 with Max-Q Design|67657                        |
|NVIDIA GeForce RTX 2060 with Max-Q Design|67588                        |
|Quadro RTX 4000 with Max-Q Design|67141                        |
|NVIDIA GeForce RTX 3050 Ti Laptop GPU|66487                        |
|NVIDIA GeForce GTX 1660 Ti|66368                        |
|GeForce GTX 1660 Ti|65308                        |
|NVIDIA GeForce GTX 1660 SUPER|65154                        |
|GeForce GTX 1660 SUPER|65044                        |
|Quadro RTX 3000 with Max-Q Design|64172                        |
|GeForce RTX 3050 Ti Laptop GPU|62628                        |
|NVIDIA GeForce GTX 1660 Ti with Max-Q Design|61528                        |
|NVIDIA RTX A2000 Laptop GPU|61347                        |
|GeForce GTX 1660 Ti with Max-Q Design|60838                        |
|NVIDIA GeForce GTX 1660|60503                        |
|GeForce GTX 1660|60172                        |
|GRID T4-4Q|59903                        |
|NVIDIA TITAN Xp COLLECTORS EDITION|59596                        |
|GeForce RTX 3050 Laptop GPU|58544                        |
|NVIDIA GeForce RTX 3050 Laptop GPU|58518                        |
|NVIDIA TITAN Xp|58384                        |
|RTX A2000 Laptop GPU|58328                        |
|TITAN Xp|57897                        |
|NVIDIA GeForce GTX 1650 SUPER|57126                        |
|GeForce GTX 1650 SUPER|56481                        |
|NVIDIA TITAN X (Pascal)|56205                        |
|NVIDIA GeForce GTX 1080 Ti|55628                        |
|GeForce GTX 1080 Ti|55161                        |
|TITAN X (Pascal)|54087                        |
|GRID T4-8Q|52866                        |
|GeForce GTX 1080|51531                        |
|NVIDIA GeForce GTX 1080|51030                        |
|NVIDIA GeForce GTX 1070 Ti|50088                        |
|GeForce GTX 1070 Ti|49727                        |
|NVIDIA GeForce GTX 1650 Ti|48337                        |
|Tesla P40|47664                        |
|Quadro P6000|47462                        |
|GeForce GTX 1080 with Max-Q Design|46955                        |
|Quadro P5200 with Max-Q Design|46329                        |
|Quadro P5200|45689                        |
|NVIDIA GeForce GTX 1070|45558                        |
|GeForce GTX 1070|45301                        |
|Quadro P5000|45153                        |
|GeForce GTX 1650 Ti|44348                        |
|NVIDIA GeForce GTX 1080 with Max-Q Design|44255                        |
|T1200 Laptop GPU|43441                        |
|NVIDIA T1200 Laptop GPU|43342                        |
|Quadro T2000 with Max-Q Design|41307                        |
|GRID A100-1-5C MIG 1g.5gb|41284                        |
|GRID P40-2Q|41169                        |
|GeForce GTX 1650 Ti with Max-Q Design|41158                        |
|Quadro T2000|41149                        |
|NVIDIA GeForce GTX 1650 Ti with Max-Q Design|40355                        |
|NVIDIA GeForce GTX 1650|40258                        |
|GeForce GTX 1650|39941                        |
|NVIDIA Quadro P4000|39254                        |
|Quadro P4000|38590                        |
|NVIDIA T1000 8GB|38577                        |
|NVIDIA GeForce GTX 1070 with Max-Q Design|38193                        |
|NVIDIA A2|38140                        |
|GeForce GTX 1650 with Max-Q Design|37945                        |
|GeForce GTX 1070 with Max-Q Design|37934                        |
|NVIDIA T1000|37817                        |
|Quadro P4200|37676                        |
|NVIDIA GeForce GTX 1650 with Max-Q Design|37506                        |
|NVIDIA GeForce GTX 980 Ti|36268                        |
|NVIDIA T600 Laptop GPU|36000                        |
|GeForce GTX 980 Ti|35714                        |
|P106-100|34239                        |
|Quadro T1000|34236                        |
|NVIDIA GeForce GTX 1060 6GB|34034                        |
|Quadro T1000 with Max-Q Design|33978                        |
|NVIDIA GeForce GTX TITAN X|33701                        |
|GeForce GTX 1060 6GB|33538                        |
|GeForce GTX TITAN X|33524                        |
|Quadro M6000|32385                        |
|Quadro M6000 24GB|32156                        |
|NVIDIA GeForce GTX 1060 3GB|31922                        |
|GeForce GTX 1060 3GB|31768                        |
|Quadro P3200 with Max-Q Design|31592                        |
|Tesla P4|31513                        |
|NVIDIA Tesla M40|31401                        |
|GeForce GTX 1060|31129                        |
|Tesla M40 24GB|31126                        |
|T500  |30990                        |
|Tesla M40|30703                        |
|NVIDIA GeForce GTX 1060|30585                        |
|NVIDIA Quadro P2200|30389                        |
|GeForce GTX 1060 5GB|30206                        |
|Quadro P2200|29989                        |
|GeForce MX450|29969                        |
|NVIDIA GeForce GTX 980|29848                        |
|GeForce GTX 980|29546                        |
|NVIDIA GeForce GTX 1060 5GB|28858                        |
|NVIDIA GeForce MX450|28725                        |
|NVIDIA GeForce GTX 1060 with Max-Q Design|28312                        |
|T600  |28084                        |
|Quadro P3200|27741                        |
|GeForce GTX 1060 with Max-Q Design|27623                        |
|NVIDIA T500|27144                        |
|NVIDIA T600|26600                        |
|NVIDIA GeForce GTX 970|25908                        |
|GeForce GTX 970|25897                        |
|Tesla M60|25404                        |
|Quadro M5000|24565                        |
|Quadro P3000|22837                        |
|Quadro P2000|21668                        |
|NVIDIA GeForce GTX 980M|21520                        |
|GeForce GTX 980M|21471                        |
|NVIDIA Quadro P2000|21174                        |
|GeForce GTX 780 Ti|20877                        |
|P106-090|20839                        |
|NVIDIA GeForce GTX 780 Ti|20818                        |
|GeForce GTX 1050 Ti|20616                        |
|NVIDIA GeForce GTX 1050 Ti|20406                        |
|GeForce GTX TITAN Black|20282                        |
|Quadro M5000M|20269                        |
|GeForce GTX 1050 Ti with Max-Q Design|18936                        |
|NVIDIA GeForce GTX 1050 Ti with Max-Q Design|18674                        |
|GeForce GTX TITAN Z|18422                        |
|NVIDIA GeForce GTX 970M|18285                        |
|Quadro P2000 with Max-Q Design|18218                        |
|GeForce GTX 780|18049                        |
|NVIDIA GeForce GTX TITAN|17933                        |
|GeForce GTX 960|17784                        |
|GeForce GTX TITAN|17711                        |
|NVIDIA GeForce GTX 960|17693                        |
|Quadro K6000|17571                        |
|NVIDIA GeForce GTX 1050|17206                        |
|GeForce GTX 970M|17191                        |
|NVIDIA GeForce GTX 780|17078                        |
|GeForce GTX 1050|16976                        |
|NVIDIA T400|16856                        |
|Quadro M4000|16648                        |
|NVIDIA T400 4GB|16323                        |
|T400  |16307                        |
|NVIDIA Tesla K80|16063                        |
|NVIDIA GeForce GTX 950|15998                        |
|GeForce GTX 950|15806                        |
|Quadro M3000M|15678                        |
|GeForce GTX 1050 with Max-Q Design|15058                        |
|Tesla K80|14679                        |
|NVIDIA GeForce GTX 1050 with Max-Q Design|14577                        |
|Tesla K40c|14510                        |
|Quadro P1000|14286                        |
|NVIDIA Tesla K40m|14135                        |
|Tesla K40m|14115                        |
|GeForce GTX 965M|13861                        |
|NVIDIA GeForce GTX 770|13824                        |
|GeForce GTX 770|13785                        |
|Quadro K5200|13735                        |
|NVIDIA GeForce GTX 965M|13714                        |
|NVIDIA GeForce GTX 680|13627                        |
|GeForce GTX 680|13248                        |
|Quadro M2000|13100                        |
|Quadro M2200|12812                        |
|Tesla K20Xm|12681                        |
|GeForce MX350|12572                        |
|NVIDIA GeForce GTX 690|12549                        |
|NVIDIA GeForce GTX 750 Ti|12510                        |
|GeForce GTX 750 Ti|12499                        |
|GeForce GTX 690|12263                        |
|NVIDIA GeForce MX350|12232                        |
|Tesla M10|12054                        |
|Tesla K20m|12019                        |
|NVIDIA GeForce GTX 670|11969                        |
|Tesla K20c|11850                        |
|GeForce GTX 960M|11818                        |
|Quadro P620|11727                        |
|NVIDIA Tesla M10|11721                        |
|GeForce GTX 670|11611                        |
|NVIDIA Quadro K2200|11549                        |
|NVIDIA GeForce GTX 960M|11507                        |
|Quadro K2200|11410                        |
|GeForce GTX 680MX|11307                        |
|NVIDIA GeForce GTX 660 Ti|11298                        |
|GeForce GTX 660 Ti|11274                        |
|GeForce GTX 860M|11144                        |
|NVIDIA Quadro M2000M|11041                        |
|NVIDIA GeForce GTX 860M|10778                        |
|GeForce GTX 760|10683                        |
|Quadro P600|10634                        |
|NVIDIA GeForce GTX 760|10624                        |
|NVIDIA GeForce GTX 750|10510                        |
|GeForce GTX 750|10448                        |
|Quadro M2000M|10438                        |
|GeForce GT 1030|10307                        |
|Quadro M1200|10296                        |
|NVIDIA GeForce GT 1030|10287                        |
|GeForce GTX 880M|10249                        |
|GRID M10-8Q|10107                        |
|NVIDIA Quadro P620|9995                         |
|GeForce MX330|9906                         |
|GeForce MX150|9799                         |
|GeForce GTX 950M|9777                         |
|GeForce MX250|9734                         |
|NVIDIA GeForce MX250|9707                         |
|NVIDIA GeForce MX150|9551                         |
|NVIDIA GeForce GTX 850M|9545                         |
|GeForce GTX 780M|9535                         |
|GeForce GTX 870M|9499                         |
|NVIDIA GeForce GTX 950M|9463                         |
|NVIDIA GeForce MX330|9322                         |
|GeForce GTX 850M|9302                         |
|Quadro K1200|9073                         |
|NVIDIA GeForce GTX 760 (192-bit)|9058                         |
|GeForce GTX 760 (192-bit)|9027                         |
|NVIDIA Quadro K4200|8973                         |
|Quadro K4200|8946                         |
|NVIDIA GeForce GPU|8890                         |
|Quadro M620|8602                         |
|GeForce GTX 660|8583                         |
|Quadro K5000|8558                         |
|Quadro M1000M|8471                         |
|NVIDIA GeForce GTX 660|8458                         |
|Quadro P520|7481                         |
|Quadro M520|7173                         |
|NVIDIA GeForce MX130|7156                         |
|NVIDIA GeForce GTX 650 Ti BOOST|7132                         |
|GeForce GTX 675MX|7085                         |
|NVIDIA GeForce MX230|6914                         |
|GeForce MX130|6872                         |
|Quadro K4100M|6821                         |
|GeForce GTX 650 Ti BOOST|6809                         |
|Quadro K620|6653                         |
|NVIDIA Quadro K620|6621                         |
|GeForce MX230|6604                         |
|GeForce GTX 770M|6572                         |
|GeForce GPU|6529                         |
|NVIDIA GeForce GTX 745|6443                         |
|Quadro P500|6438                         |
|NVIDIA GeForce 940MX|6363                         |
|GeForce GTX 745|6310                         |
|GeForce 940MX|6290                         |
|GeForce GTX 650 Ti|6223                         |
|NVIDIA GeForce GTX 650 Ti|5920                         |
|GeForce 940M|5882                         |
|Quadro M500M|5713                         |
|NVIDIA GeForce 940M|5703                         |
|Quadro P400|5691                         |
|NVIDIA GeForce 840M|5629                         |
|NVIDIA GeForce 930MX|5599                         |
|GeForce 930MX|5566                         |
|GeForce 840M|5561                         |
|GeForce GTX 765M|5514                         |
|Quadro K4000|5210                         |
|GeForce 930M|5123                         |
|NVIDIA GeForce 930M|4932                         |
|Quadro K4000M|4650                         |
|GeForce MX110|4625                         |
|NVIDIA GeForce MX110|4483                         |
|GeForce 830M|4342                         |
|GeForce GTX 760M|4287                         |
|GeForce 920MX|4274                         |
|NVIDIA GeForce 920MX|4240                         |
|Quadro K3100M|4121                         |
|NVIDIA GeForce GTX 645|3630                         |
|NVIDIA GeForce GTX 650|3469                         |
|GeForce GTX 650|3424                         |
|NVIDIA GeForce GT 740|3302                         |
|GeForce GT 740|3273                         |
|GeForce GT 750M|3118                         |
|Quadro K2000|3055                         |
|Quadro K2100M|3028                         |
|GeForce GTX 660M|2901                         |
|GeForce GT 640|2853                         |
|GeForce GT 745M|2836                         |
|NVIDIA GeForce GT 640|2825                         |
|GeForce GT 635|2794                         |
|GeForce GT 740M|2783                         |
|GeForce 920M|2766                         |
|NVIDIA GeForce GT 730|2743                         |
|GeForce GT 730|2682                         |
|GeForce GT 650M|2651                         |
|GeForce GT 730M|2459                         |
|Quadro K2000M|2385                         |
|NVIDIA GeForce GT 630|2317                         |
|Quadro K1100M|2205                         |
|GeForce GT 640M|2200                         |
|GeForce GT 630|1715                         |
|NVIDIA GeForce GT 710|1534                         |
|GeForce GT 710|1519                         |
|GeForce GT 720|1514                         |
|Quadro K610M|1504                         |
|Quadro K600|1356                         |
|Quadro K420|1350                         |
|Quadro K1000M|1335                         |
|NVS 510|1282                         |


