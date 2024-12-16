start=100000 # 100 ns
stop=4000000 # 4000 nS
skip=10000   # 10 ns

source="/BIOBACKUP/biofys4/common/Hanna_SPC_dimers/92_systems/"


for j in `seq 0 96`
do
i=$((j+1296))	
xtc=$source/$j/all_traj.xtc
tpr=$source/$j/2a_eq_npt.tpr
#ls $xtc
#ls $tpr

echo "
gmx pairdist \
-f $xtc \
-s $tpr \
-n index.ndx \
-o $i.dist.xvg \
-b $start \
-e $stop \
-dt $skip \
-selrpos res_com \
-type min \
-refgrouping res \
-selgrouping res \
-ref "chA" \
-sel "chB" 
"
done | parallel -j 5
