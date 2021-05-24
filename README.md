# Datajoint Retinal Ganglion Pipeline

## Table of Content
- [Pipeline](#pipeline)
- [Visualization](#visualization)
- [Exploration](#exploration)

---

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

### Data Model
Definition: ~/pipeline/ingest/experiment.py
Data Source Manifest: ~/pipeline/data_source_manifest.json
Data Loader: ~/pipeline/load_utils.py

### STRF Calculation
Data Loader: ~/pipeline/compute_utils.py

[Back To Top](#datajoint-retinal-ganglion-pipeline)

---

## Visualization
```
# setup database configuration ~/visualization/config.ini
python ./visualization/app.py
# then access http://localhost:8050
# other people under the same network can access http://<YOUR_IP>:8050
```

### Server
~/visualization/app.py

### Plot
./visualization/plot_utils.py

[Back To Top](#datajoint-retinal-ganglion-pipeline)

---

## Exploration
```
# STRF
~/notebooks/visualization_explore.ipynb
# data set
~/notebooks/data_discovery.ipynb
# database config
~/notebooks/db_conn_test.ipynb
```

[Back To Top](#datajoint-retinal-ganglion-pipeline)

---

- setup.py is not ready
- documation is not ready
- ERD is not ready
- STRF calculation has problem

[Back To Top](#datajoint-retinal-ganglion-pipeline)