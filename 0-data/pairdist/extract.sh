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
