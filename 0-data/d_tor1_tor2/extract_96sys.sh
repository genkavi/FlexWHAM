start=100000 # 100 ns
stop=4000000 # 4000 nS
skip=10000   # 10 ns

source="/BIOBACKUP/biofys4/common/Hanna_SPC_dimers/92_systems/"

#remove the header |  invert the file | sort the file based on time | convert the time to integer | downsample

for j in `seq 0 96`
do	
	i=$((j+1296))
	file="$source/$j/BIAS.txt"
	#echo $file
	grep -v "#" $file | tac | sort -unk1 | awk '{printf("%.0f ", $1); for (i=2; i<=NF; i++) printf("%s ", $i); print"" }' | awk -v start=$start -v stop=$stop -v skip=$skip '$1>=start && $1<=stop && $1%skip==0 {print $1, $2, $3, $4}' > $i.txt
done

