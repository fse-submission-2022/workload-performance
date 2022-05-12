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

## Resources

### Included in this repository
* [`resources/performance`](resources/performance`) includes the configurations tested and the respective performance observations in one CSV file per system. The performance metric columns are: execution time: `time`, maximum memory footprint: `max-resident-size`, throughput (transactions per second): `throughput` 
* [`resources/variability_models`](resources/variability_models`) includes the constraints considered when sampling configurations. These constraint were collected from the software system's documentation and are provided as DIMACS files.
* [`resources/code`](resources/code`) includes the code of the software sytems tested.
* [`resources/coverage`](resources/coverage) includesall raw coverage measurements. In order to read these reports, they need to be transformed to XML/HTML reports. If one wants to get a browser-readable version of a particular coverage report, one can convert the Jacoco binary format into HTML/XML using the `jacoco_cli.jar` provided [here](resources/coverage/jacoco_cli.jar). We provide all necessary class and source files in this repository, for further information on how to use this tool see the [Jacoco documentation](https://www.jacoco.org/jacoco/trunk/doc/cli.html).

### Not included in this repository
We provide all workloads used in the empirical study (except for h2) in a separate [MEGA cloud folder](https://mega.nz/folder/VUpClDiA#-pJj8fm8d_Td5udauW61aQ). For h2, please refer to the benchmark specifications of [benchbase](https://github.com/cmu-db/benchbase).

### Software Systems
h2 is an embedded database system which can be easily integrated into other applications; jump3r is a Java implementation of an MP3 codec which processes uncompressed WAV audio files. Kanzi is a command-line file compression tool akin to, e.g., GNU xz or gzip;  Apache batik is a utility to rasterize/render SVG vector graphics; dconvert is a utility to transform image files to formats and sizes frequently used in Android app development; jadx is a decompiler for DEX bytecode (bytecode for the VM used by Android) back to Java source code. 

The resources of the six software systems used in this empirical study stem from their respective repositories and Web sites:
* [jadx](https://github.com/skylot/jadx)
* [batik](https://xmlgraphics.apache.org/batik/tools/rasterizer.html)
* [dconvert](https://github.com/patrickfav/density-converter)
* [kanzi](https://github.com/flanglet/kanzi)
* [jump3r](https://github.com/Sciss/jump3r)
* [h2](https://github.com/h2database/h2database)
