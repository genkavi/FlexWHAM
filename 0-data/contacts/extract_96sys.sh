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
gmx select -s $tpr \
-f $xtc \
-om $i.A.mask.xvg \
-select \"( (group 19) and within 0.6 of (group 20) )\" \
-seltype res_com \
-n index.ndx \
-b $start \
-e $stop \
-dt $skip
"
done | parallel -j 5

for j in `seq 0 96`
do
i=$((j+1296))	
xtc=$source/$j/all_traj.xtc
tpr=$source/$j/2a_eq_npt.tpr
#ls $xtc
#ls $tpr

echo "
gmx select -s $tpr \
-f $xtc \
-om $i.B.mask.xvg \
-select \"( (group 20) and within 0.6 of (group 19) )\" \
-seltype res_com \
-n index.ndx \
-b $start \
-e $stop \
-dt $skip
"
done | parallel -j 5
