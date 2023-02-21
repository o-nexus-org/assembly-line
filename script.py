
import streamlit as st
import os
import streamlit as st
import pandas as pd
import numpy as np
from time import sleep
from typing import Union, Tuple
from pathlib import Path
from src.checks import (raise_err_if_file_is_filled_in,
                        check_binary_has_bin_ending,
                        read_prov
)

from src.process import (extract_mac_from_stream,)
from src.config import TEMP_FOLDER, prov_local_fp, bin_dest
from src.excel import to_excel
from src.utils import (delete_files_in_folder, 
                       save_binary_locally,
                       save_prov_locally
)


if __name__ == "__main__":

    # if st.button("Run"):
        
    #     with st.form("my_form"):
    #         command = """testing/data/file.sh"""
    #         # command = """sleep 5"""
    #         mac = extract_mac_from_stream(command)
    #         st.write(f"Inside the form {mac}")
    #         slider_val = st.text_input("Sim number")
    #         # checkbox_val = st.checkbox("Form checkbox")
    #         submit_button = st.form_submit_button(label="Submit")

    import streamlit as st

    form = st.form("my_form")
    sli = form.slider("Inside the form")
    print(sli)
    sim = form.text_input("Sim number")
    print(sim)
    st.slider("Outside the form")

    # Now add a submit button to the form:
    sent = form.form_submit_button("Submit")
    if sent:
        print("Form submitted!")
        print(form)