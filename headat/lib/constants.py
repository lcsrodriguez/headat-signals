formats = {
    "txt": {
        "extension": "txt",
        "method": "custom",
        "callback": "t_txt"
    },
    "out": {
        "extension": "out",
        "method": "custom",
    },
    "dat": {
        "extension": "dat",
        "method": "custom",
    },
    "xlsx": {
        "extension": "xlsx",
        "method": "to_excel",
        "callback": "t_xlsx"
    },
    "csv": {
        "extension": "csv",
        "method": "to_csv",
        "callback": "t_csv"
    },
    "json": {
        "extension": "json",
        "method": "to_json",
    },
    "xml": {
        "extension": "xml",
        "method": "to_xml"
    },
    "markdown": {
        "extension": "md",
        "method": "to_markdown"
    },
    "latex": {
        "extension": "tex",
        "method": "to_latex"
    },
    "parquet": {
        "extension": "parquet",
        "method": "to_parquet"
    },
    "pickle": {
        "extension": "pickle",
        "method": "to_pickle"
    },
    "sql": {
        "extension": "db",
        "method": "to_sql"
    },
    "matlab": {
        "extension": "mat",
        "method": "custom"
    },
    "wav": {
        "extension": "wav",
        "method": "custom"
    },
    "edf": {
        "extension": "edf",
        "method": "custom"
    },
    "feather": {
        "extension": "fea",
        "method": "to_feather",
    },
    "stata": {
        "extension": "dta",
        "method": "to_stata",
    },
    "html": {
        "extension": "html",
        "method": "to_html",
    },
    "hdf5": {
        "extension": "h5",
        "method": "to_hdf",
    }

}

EXPORT_FOLDERS = "out"
EXCEL_ROW_LIMIT = 1048576 - 2