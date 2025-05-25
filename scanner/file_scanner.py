import os


def find_excel_files(folder):
    excel_extensions = [".xls", ".xlsx", ".xlsm", ".csv"]
    file_paths = []

    for root, _, files in os.walk(folder):
        for f in files:
            if any(f.lower().endswith(ext) for ext in excel_extensions):
                file_paths.append(os.path.join(root, f))

    return file_paths
