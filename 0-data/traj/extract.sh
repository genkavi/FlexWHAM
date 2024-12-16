start=100000 # 100 ns
stop=4000000 # 4000 nS
skip=10000   # 10 ns

source="/BIOBACKUP/biofys4/common/Hanna_SPC_dimers/renamed"

dirs=`find $source -maxdepth 1 -type l | awk -F/ '{print $NF}'`

for i in $dirs
do	
xtc=$source/$i/all_traj.xtc
tpr=topol.tpr
#ls $xtc
#ls $tpr

echo "
echo \"Protein chA Protein\" | \
gmx trjconv -s $tpr \
-f $xtc \
-pbc cluster \
-o $i.protein.xtc \
-center \
-n index.ndx \
-b $start \
-e $stop \
-dt $skip
"
done | parallel -j 5
