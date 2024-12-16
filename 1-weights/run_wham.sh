for i in `seq 0 89`
do
echo "	
python run_wham.py weights.$i.npy 
"
done

