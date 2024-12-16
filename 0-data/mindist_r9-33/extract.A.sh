start=100000 # 100 ns
stop=4000000 # 4000 nS
skip=10000   # 10 ns

#source="/BIOBACKUP/biofys4/common/Hanna_SPC_dimers/renamed"
source="../traj/"

xtcs=`ls $source/*.protein.xtc | awk -F'[./]' '{print $6}'`

for i in $xtcs
do
xtc=${source}/$i.protein.xtc
tpr=${source}/topol.pdb
#ls $xtc
#ls $tpr

echo "
echo 21 22 | gmx mindist -f $xtc \
-s $tpr \
-n index.ndx \
-od $i.A.mindist.xvg \
-on $i.A.numcont.xvg \
-or $i.A.mindistres.xvg \
-b $start \
-e $stop \
-dt $skip \
-respertime
"
done | parallel -j 5
