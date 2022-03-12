# On the Relation of Software Configurations and Workloads: An Empirical Study of Performance

## Interactive Dashboard
We provide an interactive dashboard using `streamlit` that allows exploring in detail our analysis for each configuration option and workload. We have deployed a version on [Heroku](https://workload-performance.herokuapp.com) and provide a Docker-ized version to run the dashboard locally.

### Build & Run Docker image
```bash
cd ./dashboard
sudo docker build -t streamlitapp:latest .
docker run -p 8501:8501 streamlitapp:latest
```
You can now explore the dashboard **running locally** at [https://127.0.0.1:8501](https://127.0.0.1:8501).

### Usage
some words on how to use the dashboard


## Resources

### Included in this repository
* [`resources/performance`](resources/performance`) includes the configurations tested and the respective performance observations in one CSV file per system. The performance metric columns are: execution time: `time`, maximum memory footprint: `max-resident-size`, throughput (transactions per second): `throughput` 
* [`resources/variability_models`](resources/variability_models`) includes the constraints considered when sampling configurations. These constraint were collected from the software system's documentation and are provided as DIMACS files.
* [`resources/code`](resources/code`) includes the code of the software sytems tested.

### Not included in this repository (raw coverage reports)
The coverage reports provided by Jacoco are in a binary format. We provide all raw measurements [`resources/coverage`](resources/coverage). In order to read these reports, they need to be transformed to XML/HTML reports. Due to the file size limit of GitHub (100 MB per file) and HotCRP (600 MB) we had to move some additional data to another [cloud folder](https://mega.nz/folder/VUpClDiA#-pJj8fm8d_Td5udauW61aQ). There, we provide the workload files for all software systems, except for h2. In addition, there we provide a machine-readable representation of all coverage reports in the Hierarchical Data Format (HDF). These report files can be easily used, for instance with Python's `pandas` package. Note, that the raw file size ranges from 500 MB to over 70 GB. For the latter file (jadx), we provide a `lrzip`-compressed version. In the HDF data frames, the references to classes and workloads have been replaced by foreign keys, which can be found here.

##### Converting Raw Coverage Reports
If one wants to get a browser-readable version of a particular coverage report, one can convert the Jacoco binary format into HTML/XML using the `jacoco_cli.jar` provided [here](resources/coverage/jacoco_cli.jar). We provide all necessary class and source files in this repository, for further information on how to use this tool see the [Jacoco documentation](https://www.jacoco.org/jacoco/trunk/doc/cli.html).

### Software Systems
The resources of the six software systems used in this empirical study stem from their respective repositories and Web sites:
* [jadx](https://github.com/skylot/jadx)
* [batik](https://xmlgraphics.apache.org/batik/tools/rasterizer.html)
* [dconvert](https://github.com/patrickfav/density-converter)
* [kanzi](https://github.com/flanglet/kanzi)
* [jump3r](https://github.com/Sciss/jump3r)
* [h2](https://github.com/h2database/h2database)
