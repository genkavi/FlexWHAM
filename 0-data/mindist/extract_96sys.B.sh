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
echo chB chA | gmx mindist -f $xtc \
-s $tpr \
-n index.ndx \
-od $i.B.mindist.xvg \
-on $i.B.numcont.xvg \
-or $i.B.mindistres.xvg \
-b $start \
-e $stop \
-dt $skip \
-respertime
"
done | parallel -j 5
