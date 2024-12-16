start=100000 # 100 ns
stop=4000000 # 4000 nS
skip=10000   # 10 ns

source="/BIOBACKUP/biofys4/common/Hanna_SPC_dimers/500_systems/NEW_RUN_22-35/renamed"

dirs=`find $source -maxdepth 1 -type l | awk -F/ '{print $NF}'`

for i in $dirs
do	
xtc=$source/$i/all_traj.xtc
tpr=$source/$i/npt.tpr
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

for i in $dirs
do	
xtc=$source/$i/all_traj.xtc
tpr=$source/$i/npt.tpr
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


