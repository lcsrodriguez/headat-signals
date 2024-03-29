<p align="center">
<img src="img/logo.png" width="150"/>
</p>

# HEA/DAT signals file processing

Official GitHub repository for **HEADAT** library: `.hea`/`.dat` files processing tool & Wrapper of [wfdb](https://wfdb.readthedocs.io/en/latest/) library.

## Introduction

[PhysioNet](https://physionet.org/about/) is an association which has as main mission to conduct and catalyze for biomedical research & education, in part by offering free access to large collections of physiological and clinical data and related open-source software.


[PhysioBank](https://archive.physionet.org/physiobank/) is an extensive archive of [PhysioNet](https://physionet.org/) of well-characterized digital recordings of physiologic signals, time series, and related data for use by the biomedical research community.



PhysioBank has adopted a unified and well-structured file format in order to store and organize records and signals. The entire format system description is freely available in a highly-documented website (see [Resources](#resources))


**HEADAT** is a light-weight, fully-operational Python library used for extracting, processing, converting and 
exporting ECGs signals and records data (under `.hea` and `.dat` format) within specified in-memory formats (DataFrames, Series, ...) 
or on-disk exports/database files (see [Supported Export format](#list-of-in-memory-conversion-types) for more details).

**HEADAT** has one goal : *make ECG signals processing **easier** and **funnier*** by :
- embedding the core functions and datasets of WFDB/ECG signals within the Python data-science ecosystem : NumPy, SciPy, Bokeh, Scikit-Learn, TensorFlow, ...
- exporting data in high-quality formats for further development in various languages : **Python**, **R**, **Julia**, ...
- supporting main features for High-Performance Computing (HPC) applications
- using streaming solutions for real-time analytics and making medical insights.

As a new module, the community goal is to reach each one of these items in the coming months.

## Install

**HEADAT** core functions are using other modules in order to run.

1. Please make sure a recent version of Python is running
```bash
python -V
python3 -V
```

2. Upgrade `pip` package-management system and underlying modules
```bash
pip install --upgrade pip
```
*On Windows, it's recommended to perform the following command :* `python -m pip install --upgrade pip`


3. Instal **HEADAT**
    - by cloning the current repository: `git clone https://github.com/lcsrodriguez/headat-signals`
    - *by installing it using `pip`: `pip install headat`* (not operational yet)

If you choose the cloning method, please perform a preliminary step: installing the dependencies manually by executing `pip install -r requirements.txt`

## Getting started

Create a HEADAT view corresponding to a simple record :
```python
a = HDView()
```

Add a record reference :
1. directly to the constructor
```python
v = HDView("samples/aami3a")
```
2. by calling the `.add_record()` method
```python
v = HDView()
v.add_record("samples/aami3a")
```

**Remark** : The library supports both remote and local resources; you can specify a URL or a relative/absolute path to 
the file. In addition, you can specify or not the `.hea` extension of the file, depending on your technical choice; HEADAT
will automatically parse the file, gather the signals and perform the needed processing.

For instance, you can set up a HDView using either :
1. `samples/aami3a`
2. `samples/aami3a.hea`
3. `https://physionet.org/files/aami-ec13/1.0.0/aami3a.hea`
4. `https://physionet.org/files/aami-ec13/1.0.0/aami3a`

Then, you can extract and convert the signals' data to **manu supported formats** (see [list](#list-of-in-memory-conversion-types))
```python
v.t_csv()
v.t_xlsx()
v.t_json()
v.t_xml()
v.t_md()
v.t_tex()
v.t_parquet()
v.t_pickle()
v.t_wav()
v.t_edf()
v.t_csv()
v.t_feather()
```
The output will be stored into a timestamped file within the folder `out/view_<simulation_timestamp>`.


Get the supported MIME types with extensions for export formats :
```python
get_export_types()
get_export_extensions()
```

Additionally, for monitoring purposes, you can check the number of HDView instantiated by calling :
```python
HDView.VIEWS_INITIALIZED_COUNTER
```

You may have the need to collect and print the underlying signals files from one HDView :
```python
v.get_record_files()
```

You can also gather the information labels and the raw signals :
```python
v.get_signals()
v.get_infos()
```

If you find any other relevant feature to be implemented, please open a new issue !

## List of in-memory conversion types

| Class     | Type        | Description                                                              | Ok   |
|-----------|-------------|--------------------------------------------------------------------------|:-----|
| Raw array | `list`      | "Pure" Python array (list of lists)                                      | ✅    |
| Raw dict  | `dict`      | "Pure" Python dict (dict of lists)                                       | ✅    |
| Numpy     | `ndarray`   | Numpy n-dimensions array (for fast computations) (underlying C-layers)   | ✅    |
| Numpy     | `record`    | Numpy record array                                                       | ✅    |
| Pandas    | `DataFrame` | Pandas DataFrame conversion (best solution for further data processing)  | ✅    |
| HDFS      | -           | Hadoop Distributed File System (HDFS) *(using PyArrow)*                  | ❌    |
| RDD       | -           | Resilient Distributed Datasets (RDD) *(using PySpark)*                   | ✅    |

## List of export formats

| Name      | Extension      | Description                                                                                     | Ok |
|-----------|----------------|-------------------------------------------------------------------------------------------------|:--:|
| Text file | custom         | Standard text file     (`.out`, `.dat`, `.txt` or other custom extension)                       |  ✅ |
| Excel     | `.xslx`        | MS Excel/OpenOffice Calc file                                                                   | ✅[^1] |
| CSV       | `.csv`         | Better for data-science                                                                         |  ✅ |
| JSON      | `.json`        | JSON file                                                                                       |  ✅ |
| XML       | `.xml`         | Useful for XML parsing                                                                          |  ✅ |
| Markdown  | `.md`          | Useful for quick report in Markdown                                                             |  ✅ |
| HTML      | `.html`        | Useful for web development                                                                      |  ✅ |
| LaTeX     | `.tex`         | Recommended for highly-detailed article in LaTeX                                                |  ✅ |
| Parquet   | `.pqt`         | [Apache Parquet](https://parquet.apache.org/) format : highly recommended for HPC               |  ✅ |
| Pickle    | `.pkl`         | For data serialization and unserialization (could be useful for such applications)              |  ✅ |
| HDF5       | `.h5`         | Hierarchical Data Format (HDF)                                                                  |  ✅ |
| SQLite    | `.db, .sqlite` | Classic and light-weight file-based SQL RDBMS (can be relevant for requesting organized records |  ❌ |
| MATLAB    | `.mat`         | For heavy computations on MATLAB programs (proprietary software)                                |  ✅ |
| WAV       | `.wav`         | WAV files                                                                                       |  ✅ |
| EDF       | `.edf`         | European Data Format ([EDF](https://www.edfplus.info/specs/edf.html)) files                     |  ✅ |
| Feather   | `.fea, .feather`| Apache Arrow's [Feather](https://arrow.apache.org/docs/python/feather.html) file format for fast binary columnar in-memory storage                  |  ✅ |
| STATA   | `.dta`| STATA Statistical Analysis software (proprietary software)                                                 |  ✅ |



*For fast processing steps, please consider the **Pickle**, **Parquet** and **Feather** formats, especially designed for HPC.*

**Remarks**
- If you want to suggest a new supported format, please create a **new issue** with the *NEW EXPORT FORMAT* label.
- If you want to add your own version of a new exporter for WFDB data, please init a **new Pull Request**

[^1]: MS Excel (`.xls`/`.xlsx`) files have a maximum limit of lines to be written on a single spreadsheet (1048576). 
If the studied signals are too long, unexpected behavior can occur ! Please better consider `.csv` export with additional processing steps instead of incomplete `.xlsx` formatting.


## Resources 

See [RESOURCES](docs/RESOURCES.md).

## Acknowledgement

- *Developer & Maintainer*: **Lucas RODRIGUEZ**
- *Development date*: June 2022 - today


*PhysioNet* is a repository of freely-available medical research data, managed by the MIT Laboratory for Computational Physiology ([MIT-LCP](https://github.com/MIT-LCP)).

This wrapper is based on [wfdb](https://github.com/MIT-LCP/wfdb-python) features. Please consider using it for further development.


## License

The [LICENSE](LICENSE.md) file contains the full license details.