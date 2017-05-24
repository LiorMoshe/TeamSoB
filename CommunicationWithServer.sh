i="0"
botNum="0"
botNumTwo="1"
while [ $i -lt 50 ]
do
python SimpleIRCClient.py bla$[$botNum] \#testit$[$i] &
python SimpleIRCClien2.py bla$[$botNumTwo] \#testit$[$i] &
i=$[$i+1]
botNum=$[$botNum+2]
botNumTwo=$[$botNumTwo+2]
done


