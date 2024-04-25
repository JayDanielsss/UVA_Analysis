try:
    from pandas import read_csv
except ImportError as ERROR:
    print(f"> [{__name__}]: Error importing pandas' `read_csv` file:\n> {ERROR}")

_TAB_SEPARATOR_DELIMITER = '\t'

def read_tsv_file_with_python(file_path_as_string: str):
    """
    """
    try:
        
        # (1): Attempt to read the `.tsv` file:
        tsv_file_data = read_csv(
            file_path_as_string,
            sep = _TAB_SEPARATOR_DELIMITER
        )

        # (2): Return the file:
        return tsv_file_data
    
    except Exception as ERROR:
        print(f"> [{__name__}]: Error reading the `.tsv` file:\n> {ERROR}")
        return None