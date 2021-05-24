# datajoint-retinal-ganglion-pipeline

## Pipeline

```
# build tables
python ./pipeline/run.py -db tutorial-db.datajoint.io -u USERNAME -p PASSWORD -b
# clean up tables
python ./pipeline/run.py -db tutorial-db.datajoint.io -u USERNAME -p PASSWORD -b -cln
# load data
python ./pipeline/run.py -db tutorial-db.datajoint.io -u USERNAME -p PASSWORD -b -l ./pipeline/data_source_manifest.json
# load data with log
python ./pipeline/run.py -db tutorial-db.datajoint.io -u USERNAME -p PASSWORD -b -l ./pipeline/data_source_manifest.json > loading.log
# test
python ./pipeline/run.py -db tutorial-db.datajoint.io -u USERNAME -p PASSWORD -t
```

## Visualization
```
python ./visualization/app.py
# then access http://localhost:8050
# other people under the same network can access http://<YOUR_IP>:8050
```