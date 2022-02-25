#! /bin/bash

./corenlp-server.sh -quiet true -port 9000 -timeout 15000  &
sleep 1

export PYTHONPATH=../../../util

python3 baseline-DDI.py ../../../data/devel devel.out > devel.stats
python3 baseline-DDI.py ../../../data/test test.out > test.stats

kill `cat /tmp/corenlp-server.running`
sleep 1
