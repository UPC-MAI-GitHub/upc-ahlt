#! /bin/bash

BASEDIR=../../..

# convert datasets to feature vectors
echo "Extracting features..."
python3 extract-features.py $BASEDIR/data/train/ > train.feat
python3 extract-features.py $BASEDIR/data/devel/ > devel.feat
python3 extract-features.py $BASEDIR/data/test/ > test.feat

# train CRF model
echo "Training model..."
python3 train-crf.py model.crf < train.feat
# run CRF model
echo "Running model..."
python3 predict.py model.crf < devel.feat > devel-CRF.out
python3 predict.py model.crf < test.feat > test-CRF.out
# evaluate CRF results
echo "Evaluating results..."
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel devel-CRF.out > devel-CRF.stats
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/test test-CRF.out > test-CRF.stats


# train MEM model
cat train.feat | cut -f5- | grep -v ^$ > train.mem.feat
./megam-64.opt -nobias -nc -maxi 50 multiclass train.mem.feat > model.mem
rm train.mem.feat
# run MEM model
python3 predict.py model.mem < devel.feat > devel-MEM.out
python3 predict.py model.mem < test.feat > test-MEM.out
# evaluate MEM results
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel devel-MEM.out > devel-MEM.stats
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/test test-MEM.out > test-MEM.stats
