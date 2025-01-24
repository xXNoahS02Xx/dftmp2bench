![alt text](https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.watson.ch%2Fleben%2Ffilm%2F188824316-die-ersten-bilder-vom-set-so-sieht-will-smith-als-genie-in-aladdin-aus&psig=AOvVaw3-ay3yhGB-SVYoOtCkgyC5&ust=1737808891385000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCPjvxN-wjosDFQAAAAAdAAAAABAI)
# Notes about job status

Here's a sentence with a footnote. [^1]

[^1]: This is the footnote. 

## Correct basis sets for Orca
- ! RI-B2PLYP D3BJ def2-TZVP def2-TZVP/C TIGHTSCF
- ! RI-MP2 cc-pVTZ cc-pVTZ/C TIGHTSCF
- ! DLPNO-CCSD(T) cc-pVTZ cc-pVTZ/C TIGHTSCF

errors come from AuxC basis set. See 
and https://sites.google.com/site/orcainputlibrary/coupled-cluster
and https://sites.google.com/site/orcainputlibrary/mp2-mp3


[orca hybrid dft]([https://www.example.com](https://sites.google.com/site/orcainputlibrary/dft-calculations/double-hybrid-dft))

(files without errors and without normal term prolly have some memory problem eg:
gaussian/ala0.xyz/b2plyp/def2tzvpp/ala0.xyz.000b24b8-d9a2-11ef-abea-d85ed34e2189.out (Erroneous write. Write -1 instead of 1995008.)) (didnt check later ones)


## tl;dr

### gaussian:
problem with:
- **(bs)**	...-f12, def2svp, ...-PP, 
- **(met)**	b973c, dlpnoccsd, PBEh-3c, r2scan3c, rimp2, wb97xd3, wb97xd3bj, wb97xv


orca:
urecognized or double keyword: 6-311++G(2D,2P)/C, 6-31+G(D)/C, 6-31+G(D,P)/C, CC-PVTZ-F12/C, sto-g3/c (basis sets)
needs AuxC basis set: b2plyp (9 times) (method)
unassigned or incompatible basis set: dlpnoccsdt (9x), rimp2 (5x) (methods)
error termination in MP2: 	mp2/6311++g2d2p
				mp2/ccpvtzf12
				mp2/def2tzvpp





git add dftmp2bench/dftmp2bench.py directories.json uv.lock


cp ../dftmp2bench_old/dftmp2bench/dftmp2bench.py ../dftmp2bench_old/directories.json ../dftmp2bench_old/uv.lock
git add dftmp2bench/dftmp2bench.py directories.json uv.lock
git commit -m "Noah's first commit :) added uuid to prevent overwrites of gaussian output files"
git push


Files:

Gaussian: 

gaussian/ala0.xyz/b2plyp/ccpvdzpp/ala0.xyz.001d4ec2-d9a2-11ef-abea-d85ed34e2189.out (problem: PP) 

gaussian/ala0.xyz/b2plyp/ccpvtzf12/ala0.xyz.00220e62-d9a2-11ef-abea-d85ed34e2189.out (F12)

gaussian/ala0.xyz/b2plyp/def2svpd/ala0.xyz.00141c08-d9a2-11ef-abea-d85ed34e2189.out (def2...)

gaussian/ala0.xyz/b973c/6311++g2d2p/ala0.xyz.002cc870-d9a2-11ef-abea-d85ed34e2189.out (b973c)

gaussian/ala0.xyz/b973c/631+gd/ala0.xyz.0023c8f6-d9a2-11ef-abea-d85ed34e2189.out (b973c)

gaussian/ala0.xyz/b973c/631+gdp/ala0.xyz.00282a04-d9a2-11ef-abea-d85ed34e2189.out (b973c)

gaussian/ala0.xyz/b973c/ccpvdz/ala0.xyz.0015cd46-d9a2-11ef-abea-d85ed34e2189.out (b973c)

gaussian/ala0.xyz/b973c/ccpvdzpp/ala0.xyz.001a67ac-d9a2-11ef-abea-d85ed34e2189.out (b973c)

gaussian/ala0.xyz/b973c/ccpvtzf12/ala0.xyz.001f0fe6-d9a2-11ef-abea-d85ed34e2189.out (b973c)

gaussian/ala0.xyz/b973c/def2svp/ala0.xyz.000cdd6c-d9a2-11ef-abea-d85ed34e2189.out (b973c)

gaussian/ala0.xyz/b973c/def2svpd/ala0.xyz.001154e6-d9a2-11ef-abea-d85ed34e2189.out (b973c)

gaussian/ala0.xyz/b973c/def2tzvpp/ala0.xyz.000815d4-d9a2-11ef-abea-d85ed34e2189.out (b973c)

gaussian/ala0.xyz/b973c/sto3g/ala0.xyz.003142c4-d9a2-11ef-abea-d85ed34e2189.out (b973c)

gaussian/ala0.xyz/camb3lyp/ccpvdzpp/ala0.xyz.001d03e0-d9a2-11ef-abea-d85ed34e2189.out (PP)

gaussian/ala0.xyz/camb3lyp/ccpvtzf12/ala0.xyz.0021c13c-d9a2-11ef-abea-d85ed34e2189.out (f12)

gaussian/ala0.xyz/camb3lyp/def2svpd/ala0.xyz.0013d6bc-d9a2-11ef-abea-d85ed34e2189.out (def2-SVP)

gaussian/ala0.xyz/ccsd/ccpvdzpp/ala0.xyz.0019d49a-d9a2-11ef-abea-d85ed34e2189.out (PP)

gaussian/ala0.xyz/ccsd/ccpvtzf12/ala0.xyz.001e7c16-d9a2-11ef-abea-d85ed34e2189.out (f12)

gaussian/ala0.xyz/ccsd/def2svpd/ala0.xyz.0010c210-d9a2-11ef-abea-d85ed34e2189.out (def2-svp)

gaussian/ala0.xyz/dlpnoccsd/6311++g2d2p/ala0.xyz.002fd3da-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsd/631+gd/ala0.xyz.0026c7ea-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsd/631+gdp/ala0.xyz.002b2a9c-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsd/ccpvdz/ala0.xyz.0018f34a-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsd/ccpvdzpp/ala0.xyz.001d9990-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd) 

gaussian/ala0.xyz/dlpnoccsd/ccpvtzf12/ala0.xyz.00225c96-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsd/def2svp/ala0.xyz.000fedcc-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsd/def2svpd/ala0.xyz.00146460-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsd/def2tzvpp/ala0.xyz.000b708a-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsd/sto3g/ala0.xyz.00346170-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsdt/6311++g2d2p/ala0.xyz.00301aac-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsdt/631+gd/ala0.xyz.00270ed0-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsdt/631+gdp/ala0.xyz.002b70ba-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsdt/ccpvdz/ala0.xyz.00193d82-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsdt/ccpvdzpp/ala0.xyz.001de472-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsdt/ccpvtzf12/ala0.xyz.0022a980-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsdt/def2svp/ala0.xyz.00103534-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsdt/def2svpd/ala0.xyz.0014ab50-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsdt/def2tzvpp/ala0.xyz.000bbcb6-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/dlpnoccsdt/sto3g/ala0.xyz.0034aac2-d9a2-11ef-abea-d85ed34e2189.out (dlpnoccsd)

gaussian/ala0.xyz/hf/ccpvdzpp/ala0.xyz.001987d8-d9a2-11ef-abea-d85ed34e2189.out (PP)

gaussian/ala0.xyz/hf/ccpvtzf12/ala0.xyz.001e2f18-d9a2-11ef-abea-d85ed34e2189.out (f12)

gaussian/ala0.xyz/hf/def2svpd/ala0.xyz.00107b20-d9a2-11ef-abea-d85ed34e2189.out (def2svp)

gaussian/ala0.xyz/m062x/ccpvdzpp/ala0.xyz.001cba48-d9a2-11ef-abea-d85ed34e2189.out (pp)

gaussian/ala0.xyz/m062x/ccpvtzf12/ala0.xyz.00217538-d9a2-11ef-abea-d85ed34e2189.out (f12)

gaussian/ala0.xyz/m062x/def2svpd/ala0.xyz.00138f0e-d9a2-11ef-abea-d85ed34e2189.out (def2svp)

gaussian/ala0.xyz/mp2/ccpvdzpp/ala0.xyz.001ab27a-d9a2-11ef-abea-d85ed34e2189.out (pp)

gaussian/ala0.xyz/mp2/ccpvtzf12/ala0.xyz.001f5d5c-d9a2-11ef-abea-d85ed34e2189.out (f12)

gaussian/ala0.xyz/mp2/def2svpd/ala0.xyz.00119d84-d9a2-11ef-abea-d85ed34e2189.out (def2)

gaussian/ala0.xyz/pbe0/ccpvdzpp/ala0.xyz.001b488e-d9a2-11ef-abea-d85ed34e2189.out (pp)

gaussian/ala0.xyz/pbe0/ccpvtzf12/ala0.xyz.001ff762-d9a2-11ef-abea-d85ed34e2189.out (f12)

gaussian/ala0.xyz/pbe0/def2svpd/ala0.xyz.00122b82-d9a2-11ef-abea-d85ed34e2189.out (def2svp)

gaussian/ala0.xyz/PBEh-3c/6311++g2d2p/ala0.xyz.002de69c-d9a2-11ef-abea-d85ed34e2189.out (PBEh-3c)

gaussian/ala0.xyz/PBEh-3c/631+gd/ala0.xyz.0024e380-d9a2-11ef-abea-d85ed34e2189.out (PBEh-3c)

gaussian/ala0.xyz/PBEh-3c/631+gdp/ala0.xyz.00294538-d9a2-11ef-abea-d85ed34e2189.out (PBEh-3c)

gaussian/ala0.xyz/PBEh-3c/ccpvdz/ala0.xyz.0016f216-d9a2-11ef-abea-d85ed34e2189.out (PBEh-3c) 

gaussian/ala0.xyz/PBEh-3c/ccpvdzpp/ala0.xyz.001b90aa-d9a2-11ef-abea-d85ed34e2189.out (PBEh-3c)

gaussian/ala0.xyz/PBEh-3c/ccpvtzf12/ala0.xyz.00204032-d9a2-11ef-abea-d85ed34e2189.out (PBEh-3c)

gaussian/ala0.xyz/PBEh-3c/def2svp/ala0.xyz.000dfc6a-d9a2-11ef-abea-d85ed34e2189.out (PBEh-3c)

gaussian/ala0.xyz/PBEh-3c/def2svpd/ala0.xyz.001272ea-d9a2-11ef-abea-d85ed34e2189.out (PBEh-3c)
 
gaussian/ala0.xyz/PBEh-3c/def2tzvpp/ala0.xyz.00095df4-d9a2-11ef-abea-d85ed34e2189.out (PBEh-3c)

gaussian/ala0.xyz/PBEh-3c/sto3g/ala0.xyz.00326a00-d9a2-11ef-abea-d85ed34e2189.out (PBEh-3c)

gaussian/ala0.xyz/r2scan-3c/6311++g2d2p/ala0.xyz.002c7db6-d9a2-11ef-abea-d85ed34e2189.out (r2scan3c)

gaussian/ala0.xyz/r2scan-3c/631+gd/ala0.xyz.00237efa-d9a2-11ef-abea-d85ed34e2189.out (r2scan3c) 

gaussian/ala0.xyz/r2scan-3c/631+gdp/ala0.xyz.0027e12a-d9a2-11ef-abea-d85ed34e2189.out (r2scan3c)

gaussian/ala0.xyz/r2scan-3c/ccpvdz/ala0.xyz.001584f8-d9a2-11ef-abea-d85ed34e2189.out (r2scan3c) 

gaussian/ala0.xyz/r2scan-3c/ccpvdzpp/ala0.xyz.001a1d1a-d9a2-11ef-abea-d85ed34e2189.out (r2scan3c)

gaussian/ala0.xyz/r2scan-3c/ccpvtzf12/ala0.xyz.001ec658-d9a2-11ef-abea-d85ed34e2189.out (r2scan3c)

gaussian/ala0.xyz/r2scan-3c/def2svp/ala0.xyz.000c9348-d9a2-11ef-abea-d85ed34e2189.out (r2scan3c)

gaussian/ala0.xyz/r2scan-3c/def2svpd/ala0.xyz.00110a5e-d9a2-11ef-abea-d85ed34e2189.out (r2scan3c)

gaussian/ala0.xyz/r2scan-3c/def2tzvpp/ala0.xyz.0007c7be-d9a2-11ef-abea-d85ed34e2189.out (r2scan3c)

gaussian/ala0.xyz/r2scan-3c/sto3g/ala0.xyz.0030f72e-d9a2-11ef-abea-d85ed34e2189.out (r2scan3c)

gaussian/ala0.xyz/rimp2/6311++g2d2p/ala0.xyz.002d5998-d9a2-11ef-abea-d85ed34e2189.out (rimp2)

gaussian/ala0.xyz/rimp2/631+gd/ala0.xyz.00245668-d9a2-11ef-abea-d85ed34e2189.out (rimp2)

gaussian/ala0.xyz/rimp2/631+gdp/ala0.xyz.0028b8de-d9a2-11ef-abea-d85ed34e2189.out (rimp2)

gaussian/ala0.xyz/rimp2/ccpvdz/ala0.xyz.00166346-d9a2-11ef-abea-d85ed34e2189.out (rimp2)

gaussian/ala0.xyz/rimp2/ccpvdzpp/ala0.xyz.001afd98-d9a2-11ef-abea-d85ed34e2189.out (rimp2)

gaussian/ala0.xyz/rimp2/ccpvtzf12/ala0.xyz.001faa50-d9a2-11ef-abea-d85ed34e2189.out (rimp2)

gaussian/ala0.xyz/rimp2/def2svp/ala0.xyz.000d6e6c-d9a2-11ef-abea-d85ed34e2189.out (rimp2)

gaussian/ala0.xyz/rimp2/def2svpd/ala0.xyz.0011e53c-d9a2-11ef-abea-d85ed34e2189.out (rimp2)

gaussian/ala0.xyz/rimp2/def2tzvpp/ala0.xyz.0008c89e-d9a2-11ef-abea-d85ed34e2189.out (rimp2)

gaussian/ala0.xyz/rimp2/sto3g/ala0.xyz.0031d766-d9a2-11ef-abea-d85ed34e2189.out (rimp2)

gaussian/ala0.xyz/wb97xd3/6311++g2d2p/ala0.xyz.002e749a-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3)

gaussian/ala0.xyz/wb97xd3/631+gd/ala0.xyz.00256f44-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3)

gaussian/ala0.xyz/wb97xd3/631+gdp/ala0.xyz.0029d2aa-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3)

gaussian/ala0.xyz/wb97xd3bj/6311++g2d2p/ala0.xyz.002ebb44-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3bj)

gaussian/ala0.xyz/wb97xd3bj/631+gd/ala0.xyz.0025b3e6-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3bj)

gaussian/ala0.xyz/wb97xd3bj/631+gdp/ala0.xyz.002a16c0-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3bj)

gaussian/ala0.xyz/wb97xd3bj/ccpvdz/ala0.xyz.0017ce84-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3bj)

gaussian/ala0.xyz/wb97xd3bj/ccpvdzpp/ala0.xyz.001c70b0-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3bj)

gaussian/ala0.xyz/wb97xd3bj/ccpvtzf12/ala0.xyz.00212952-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3bj)

gaussian/ala0.xyz/wb97xd3bj/def2svp/ala0.xyz.000ed3ce-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3bj)

gaussian/ala0.xyz/wb97xd3bj/def2svpd/ala0.xyz.001348b4-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3bj)

gaussian/ala0.xyz/wb97xd3bj/def2tzvpp/ala0.xyz.000a430e-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3bj)

gaussian/ala0.xyz/wb97xd3bj/sto3g/ala0.xyz.003344fc-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3bj)

gaussian/ala0.xyz/wb97xd3/ccpvdz/ala0.xyz.00178596-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3)

gaussian/ala0.xyz/wb97xd3/ccpvdzpp/ala0.xyz.001c2678-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3)

gaussian/ala0.xyz/wb97xd3/ccpvtzf12/ala0.xyz.0020da6a-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3)

gaussian/ala0.xyz/wb97xd3/def2svp/ala0.xyz.000e8b6c-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3)

gaussian/ala0.xyz/wb97xd3/def2svpd/ala0.xyz.00130278-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3)

gaussian/ala0.xyz/wb97xd3/def2tzvpp/ala0.xyz.0009f5ca-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3)

gaussian/ala0.xyz/wb97xd3/sto3g/ala0.xyz.0032fd4e-d9a2-11ef-abea-d85ed34e2189.out (wb97xd3)

gaussian/ala0.xyz/wb97xv/6311++g2d2p/ala0.xyz.002e2d50-d9a2-11ef-abea-d85ed34e2189.out (wb97xv)

gaussian/ala0.xyz/wb97xv/631+gd/ala0.xyz.002529da-d9a2-11ef-abea-d85ed34e2189.out (wb97xv)

gaussian/ala0.xyz/wb97xv/631+gdp/ala0.xyz.00298c78-d9a2-11ef-abea-d85ed34e2189.out (wb97xv)

gaussian/ala0.xyz/wb97xv/ccpvdz/ala0.xyz.00173c1c-d9a2-11ef-abea-d85ed34e2189.out (wb97xv)

gaussian/ala0.xyz/wb97xv/ccpvdzpp/ala0.xyz.001bdb8c-d9a2-11ef-abea-d85ed34e2189.out (wb97xv)

gaussian/ala0.xyz/wb97xv/ccpvtzf12/ala0.xyz.00208ce0-d9a2-11ef-abea-d85ed34e2189.out (wb97xv)

gaussian/ala0.xyz/wb97xv/def2svp/ala0.xyz.000e4594-d9a2-11ef-abea-d85ed34e2189.out (wb97xv)

gaussian/ala0.xyz/wb97xv/def2svpd/ala0.xyz.0012bc0a-d9a2-11ef-abea-d85ed34e2189.out (wb97xv)

gaussian/ala0.xyz/wb97xv/def2tzvpp/ala0.xyz.0009aab6-d9a2-11ef-abea-d85ed34e2189.out (wb97xv)

gaussian/ala0.xyz/wb97xv/sto3g/ala0.xyz.0032b5fa-d9a2-11ef-abea-d85ed34e2189.out (wb97xv)





ORCA: (look for "aborting the run")

ERROR: RI-MP2 needs an AuxC basis but none was defined!: (excluding slurms)

orca/ala0.xyz/b2plyp/6311++g2d2p/ala0.xyz.002f749e-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/b2plyp/631+gd/ala0.xyz.00266a70-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/b2plyp/631+gdp/ala0.xyz.002acda4-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/b2plyp/ccpvdz/ala0.xyz.00189198-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/b2plyp/ccpvtzf12/ala0.xyz.0021f512-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/b2plyp/def2svp/ala0.xyz.000f8e9a-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/b2plyp/def2svpd/ala0.xyz.0014051a-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/b2plyp/def2tzvpp/ala0.xyz.000b0b2c-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/b2plyp/sto3g/ala0.xyz.00340126-d9a2-11ef-abea-d85ed34e2189.out


INPUT ERROR:

orca/ala0.xyz/dlpnoccsd/6311++g2d2p/ala0.xyz.002fbc7e-d9a2-11ef-abea-d85ed34e2189.out (UNRECOGNIZED OR DUPLICATED KEYWORD(S) IN SIMPLE INPUT LINE: "6-311++G(2D,2P)/C")

orca/ala0.xyz/dlpnoccsd/631+gd/ala0.xyz.0026b16a-d9a2-11ef-abea-d85ed34e2189.out (unrec or doub keyw: "6-31+G(D)/C")

orca/ala0.xyz/dlpnoccsd/631+gdp/ala0.xyz.002b1372-d9a2-11ef-abea-d85ed34e2189.out (6-31+G(D,P)/C)

orca/ala0.xyz/dlpnoccsd/ccpvtzf12/ala0.xyz.00224260-d9a2-11ef-abea-d85ed34e2189.out (CC-PVTZ-F12/C)

orca/ala0.xyz/dlpnoccsd/sto3g/ala0.xyz.00344974-d9a2-11ef-abea-d85ed34e2189.out (sto-g3/c)

orca/ala0.xyz/dlpnoccsdt/6311++g2d2p/ala0.xyz.003002d8-d9a2-11ef-abea-d85ed34e2189.out (-311++G(2D,2P)/C)

orca/ala0.xyz/dlpnoccsdt/631+gd/ala0.xyz.0026f774-d9a2-11ef-abea-d85ed34e2189.out (6-31+G(D)/C)

orca/ala0.xyz/dlpnoccsdt/631+gdp/ala0.xyz.002b5968-d9a2-11ef-abea-d85ed34e2189.out (6-31+G(D,P)/C)

orca/ala0.xyz/dlpnoccsdt/ccpvtzf12/ala0.xyz.0022904e-d9a2-11ef-abea-d85ed34e2189.out (CC-PVTZ-F12/C)

orca/ala0.xyz/dlpnoccsdt/sto3g/ala0.xyz.0034928a-d9a2-11ef-abea-d85ed34e2189.out (sto-g3/C)

orca/ala0.xyz/rimp2/6311++g2d2p/ala0.xyz.002d42a0-d9a2-11ef-abea-d85ed34e2189.out (6-311++G(2D,2P)/C)

orca/ala0.xyz/rimp2/631+gd/ala0.xyz.00243fd4-d9a2-11ef-abea-d85ed34e2189.out (6-31+G(D)/C)

orca/ala0.xyz/rimp2/631+gdp/ala0.xyz.0028a236-d9a2-11ef-abea-d85ed34e2189.out (6-31+G(D,P)/C)

orca/ala0.xyz/rimp2/ccpvtzf12/ala0.xyz.001f913c-d9a2-11ef-abea-d85ed34e2189.out (CC-PVTZ-F12/C)

orca/ala0.xyz/rimp2/sto3g/ala0.xyz.0031befc-d9a2-11ef-abea-d85ed34e2189.out (sto-g3/C)


no main basis fcts on atom number X (The basis set was either not assigned or not available for this element - Aborting the run):

orca/ala0.xyz/b2plyp/ccpvdzpp/ala0.xyz.001d3568-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/camb3lyp/ccpvdzpp/ala0.xyz.001cec02-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/ccsd/ccpvdzpp/ala0.xyz.0019bb7c-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/dlpnoccsd/ccpvdzpp/ala0.xyz.001d8176-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/dlpnoccsdt/ccpvdzpp/ala0.xyz.001dcbea-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/hf/ccpvdzpp/ala0.xyz.00196fa0-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/m062x/ccpvdzpp/ala0.xyz.001ca274-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/mp2/ccpvdzpp/ala0.xyz.001a997a-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/pbe0/ccpvdzpp/ala0.xyz.001b304c-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/rimp2/ccpvdzpp/ala0.xyz.001ae560-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/wb97xd3bj/ccpvdzpp/ala0.xyz.001c57f6-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/wb97xd3/ccpvdzpp/ala0.xyz.001c0d28-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/wb97xv/ccpvdzpp/ala0.xyz.001bc304-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/mp2/ccpvdzpp/ala0.xyz.001a997a-d9a2-11ef-abea-d85ed34e2189.out



ORCA finished by error termination in MP2
... aborting the run: (excluding slurms)

orca/ala0.xyz/mp2/6311++g2d2p/ala0.xyz.002cf962-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/mp2/ccpvtzf12/ala0.xyz.001f4358-d9a2-11ef-abea-d85ed34e2189.out

orca/ala0.xyz/mp2/def2tzvpp/ala0.xyz.00084b3a-d9a2-11ef-abea-d85ed34e2189.out




































































