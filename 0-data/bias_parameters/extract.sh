source="/BIOBACKUP/biofys4/common/Hanna_SPC_dimers/PLUMED_files/"

for i in `seq 0 1295`
do
	file="$source/plumed.$i"
	echo $file	
	awk '$1=="UPPER_WALLS"  && $2=="ARG=d" {print $3, $4}' $file | awk -F'[/= ]' '{print $2, $4 }' > $i.txt
	awk '$1=="RESTRAINT" && $3=="ARG=tor1" {print $4, $5}' $file | awk -F'[/= ]' '{print $2, $4 }' >>  $i.txt
 	awk '$1=="RESTRAINT" && $3=="ARG=tor2" {print $4, $5}' $file | awk -F'[/= ]' '{print $2, $4 }' >> $i.txt
done
