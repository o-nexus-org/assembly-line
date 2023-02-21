import pandas as pd

from typing import Union

import streamlit as st 


def read_prov(file: str) -> pd.DataFrame:
    return pd.read_excel(file, sheet_name='site', engine='openpyxl')


def raise_err_if_file_is_filled_in(file: Union[str, None]) -> Union[str, None]:
    if file is None or file == "":
        return None
    if file.name.endswith('.xlsx'):
        df = read_prov(file)
        for col in ['macaddress', 'iccid']:
            if df[col].any():
                err_msg = f"Column='{col}' is filled in, choose another file"
                st.error(err_msg)
                return err_msg
        return None
    err_msg = "Provisioning file should be an excel file!!"
    st.error(err_msg)
    return err_msg


def check_binary_has_bin_ending(file: str) -> Union[str, None]:
    if file is None or file == "":
        return None
    if file.name.endswith('.bin'):
        return None
    err_msg = f"Firmware binary '{file}' does not end with '.bin'"
    st.error(err_msg)
    return err_msg
