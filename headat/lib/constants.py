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
    }
}
EXPORT_FOLDERS = "out"
EXCEL_ROW_LIMIT = 1048576 - 2


"""
        try:
            if formats[format]["method"] == "custom":
                print(f"Not yet supported for {format}")
                return False
            if format in ["json", "pickle"]:
                # Error with the JSON format: 'index=False' is only valid when 'orient' is 'split' or 'table'
                eval(f"df.{formats[format]['method']}(self.folder_name + f'out_{get_current_datetime()}.{formats[format]['extension']}')")
            elif format == "latex":
                eval(f"df.{formats[format]['method']}(self.folder_name + f'out_{get_current_datetime()}.{formats[format]['extension']}')")
            else:
                eval(f"df.{formats[format]['method']}(self.folder_name + f'out_{get_current_datetime()}.{formats[format]['extension']}', index=False)")
            print(f"Export finished for {format} format")
            return True
        except Exception as e:
            print(e)
            return False
"""