# HEA/DAT signals file processing

Official GitHub repository for **HEADAT** library: `.hea`/`.dat` files processing tool & Wrapper of [wfdb](https://wfdb.readthedocs.io/en/latest/) library.

## Introduction

[PhysioNet](https://physionet.org/about/) is an association which has as main mission to conduct and catalyze for biomedical research & education, in part by offering free access to large collections of physiological and clinical data and related open-source software.


[PhysioBank](https://archive.physionet.org/physiobank/) is an extensive archive of [PhysioNet](https://physionet.org/) of well-characterized digital recordings of physiologic signals, time series, and related data for use by the biomedical research community.



PhysioBank has adopted an unified and well-structured file format in order to store and organize records and signals. The entire format system description is freely available in an highly-documentated website (check Section **Resources**)


**HEADAT** is a light-weight, fully-operational Python library used for extracting, processing, converting and exporting signals and records data (under `.hea` and `.dat` format) within specified in-program format (DataFrames, Series, ...) or out-of-file on-disk or database files (see Section **Supported Export format** for more details) 

**HEADAT** has one goal : *make ECG-related signals processing **easier** and **funnier*** by :
- embedding the core functions and datasets of WFDB/ECG signals within the Python data-science ecosystem : NumPy, SciPy, Bokeh, Scikit-Learn, TensorFlow, ...
- exporting data in high-quality format for further development in various languages and platforms : **R**, **Julia**, ...
- supporting main features for High-Performance Computing (HPC) application
- using streaming solutions for real-time analytics and making insights

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
    - by installing it using `pip`: `pip install headat`

If you choose the cloning method, please perform a prelinimary step: installing the dependencies manually by executing `pip install -r requirements.txt`

**Remark**: If you want to clearly uninstall the module, please use: `pip uninstall headat`.

## Supported export format

- Excel
- CSV
- XML
- JSON
- Markdown
- LaTeX
- Parquet (Apache Parquet)
- Pickle
- SQLite

**Remarks**
- If you want to suggest a new supported format, please create a **new issue**
- If you want to add your own version of a new exporter for WFDB data, please init a **new Pull Request**

## Resources 

Here are some useful online resources in order to get a clear understanding of the .hea/.dat files format:
- https://www.physionet.org/physiotools/wag/header-5.htm
- https://archive.physionet.org/tutorials/creating-records.shtml
- https://archive.physionet.org/faq.shtml#wfdbdigitalorphysical
- https://www.physionet.org/physiotools/wag/wag.pdf


## Acknowledgement

- *Developer & Maintener*: **Lucas RODRIGUEZ**
- *Development date*: June 2022 - today


*PhysioNet* is a repository of freely-available medical research data, managed by the MIT Laboratory for Computational Physiology.


This wrapper is based on [wfdb](https://github.com/MIT-LCP/wfdb-python) features. Please consider using it for further development.


## License

Pleas check the [LICENSE](LICENSE.md) file for further details.

TODO : Add license details