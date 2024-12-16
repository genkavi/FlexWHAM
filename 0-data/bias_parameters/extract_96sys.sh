source="/BIOBACKUP/biofys4/common/Hanna_SPC_dimers/92_systems/"

for j in `seq 0 96`
do	
	i=$((j+1296))
	file="$source/$j/plumed.dat"
	echo $file
	awk '$1=="UPPER_WALLS"  && $2=="ARG=d" {print $3, $4}' $file | awk -F'[/= ]' '{print $2, $4 }' >  $i.txt
	awk '$1=="RESTRAINT" && $3=="ARG=tor1" {print $4, $5}' $file | awk -F'[/= ]' '{print $2, $4 }' >> $i.txt
 	awk '$1=="RESTRAINT" && $3=="ARG=tor2" {print $4, $5}' $file | awk -F'[/= ]' '{print $2, $4 }' >> $i.txt
done

