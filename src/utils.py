from pathlib import Path
import shutil
import pandas as pd

def delete_files_in_folder(folder: str) -> None:
    delete_files = Path(folder).iterdir()
    for delete_file in delete_files:
        not_gitkeep = delete_file.name != '.gitkeep'
        if delete_file.is_file() and not_gitkeep:
            delete_file.unlink()


def save_binary_locally(selected_bin, bin_dest: str, temp_folder: str):
    bin_already_exists = bin_dest in Path(temp_folder).iterdir()
    if bin_already_exists:
        pass
    else:
        print(dir(selected_bin))
        print(f'writing binary file to {bin_dest}')
        with open(bin_dest, "wb") as buffer:
            shutil.copyfileobj(selected_bin, buffer)
            

def save_prov_locally(df: pd.DataFrame,
                      prov_local_fp:str, temp_folder: str):
    already_exists = prov_local_fp in Path(temp_folder).iterdir()
    if already_exists:
        pass
    else:
        df.to_pickle(prov_local_fp)