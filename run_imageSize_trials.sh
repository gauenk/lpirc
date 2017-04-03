#! /bin/bash


## changes size of input from 100%, 75%, 50%, 25%

for i in {1000,875,750,500};do

    if [[ $i -eq 1000 ]]
    then
	sed -i 's/im_scale = im_scale * float(1.0)/im_scale = im_scale * float(2.0)/g' test_stream_lib.py
	echo "IT HAPPEnd"
	prev="2.0"
	cat test_stream_lib.py | grep im_scale\ \=\ im_scale
    else
	#sed -ie '/^\s*/[\t]im_scale = im_scale * float($prev)/im_scale = im_scale * float("."$i)/g' test_stream_lib.py
	echo "IT HAPPEnd"
	prev="."$i
	cat test_stream_lib.py | grep im_scale\ \=\ im_scale
    fi

done


cat test_stream_lib.py | grep im_scale\ \=\ im_scale
exit 0
