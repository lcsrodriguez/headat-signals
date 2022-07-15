formats = {
    "txt": {
        "extension": "txt",
        "method": "custom",
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
    },
    "csv": {
        "extension": "csv",
        "method": "to_csv",
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
        "extension": "pqt",
        "method": "to_parquet"
    },
    "pickle": {
        "extension": "pkl",
        "method": "to_pickle"
    },
    "sqlite": {
        "extension": "db",
        "method": "to_sql"
    },
    "matlab": {
        "extension": "mat",
        "method": "custom"
    }
}
EXPORT_FOLDERS = "out"
EXCEL_ROW_LIMIT = 1048576 - 2