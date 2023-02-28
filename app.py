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
from src import qr
from src import label
from src.print import print_img
from src.listener_esp import flash_esp

def update_excel_file(mac: str, sim_number: str) -> Tuple[bool, str]:
    try:
        print('about to update excel file')
        # get latest site overview
        n_updated_files = len(list(Path(TEMP_FOLDER).rglob("updated*.pkl")))
        # n_updated_files = current_row - 1  # -1 because we start at 1
        if n_updated_files == 0:
            df = pd.read_pickle(prov_local_fp)
        else:
            fp = Path(TEMP_FOLDER) / f'updated_{n_updated_files}.pkl'
            print(f'UPDATING FROM fp={fp}')
            df = pd.read_pickle(fp)
        # first idx where mac is Nan
        first_row_with_nan = df['macaddress'].isna().idxmax()
        print(f'{first_row_with_nan=}')
        df.loc[first_row_with_nan, 'macaddress'] = mac
        df.loc[first_row_with_nan, 'iccid'] = sim_number
        df.to_pickle(f'{TEMP_FOLDER}/updated_{first_row_with_nan}.pkl')
        print(df.columns)
        # df.loc[first_row_with_nan, 'iccid']
        return True, 'some address'
    except Exception as e:
        print(e)
        return False, ""


if __name__ == "__main__":
    finished_step = True

    with st.sidebar:
        st.info("Used to start a new provisioning process")
        delete = st.button('Delete all temporary files / start over')
        if delete:
            delete_files_in_folder(TEMP_FOLDER)

        selected_prov = st.file_uploader("Select provisioning file",
                                         type=['xlsx'])

        error_for_file_upload = raise_err_if_file_is_filled_in(selected_prov)
        selected_bin = st.file_uploader("Select firmware version", type=['bin'])
        error_bin_file = check_binary_has_bin_ending(selected_bin)
    st.title('Assembly Line Gateway')

    if error_for_file_upload:
        st.error('Please select a valid provisioning file')
    if error_bin_file:
        st.error('Please select a valid firmware binary')
    if selected_prov is None:
        st.error('Please select a provisioning file')
    print('here')
    if 'CURRENT_ROW' not in st.session_state:
        numerator = '1'
    else:
        numerator = str(st.session_state['CURRENT_ROW'])

    col1, col2 = st.columns(2)
    
    

    ready = selected_prov is not None and selected_bin is not None

    # this is done to avoid the error if file is not selected
    if selected_prov is not None:
        df = read_prov(selected_prov)
        total_rows = len(df)
        # check if done
        n_updated_files = len(list(Path(TEMP_FOLDER).rglob("updated*.pkl")))
        city_prov = df['city'].unique()[0].capitalize()
            
    else:
        city_prov = 'No file selected'
        total_rows=0
        n_updated_files=None
    # end of check if done
    print(f'city_prov={city_prov}')

    done = total_rows == n_updated_files
    if done:
        idx_last_row = n_updated_files - 1
        fp = Path(TEMP_FOLDER) / f'updated_{idx_last_row}.pkl'
        df = pd.read_pickle(fp)
        st.success ("""Each address has a MAc and an ICCID now.
                    You can download the complete provisioning file or start over (ON THE TOP LEFT).

This file contains only the 'site' tab,
DO NOT OVERWRITE THE ORIGINAL PROVISIONING!!!
        """)
        st.download_button(
        label='Download latest version',
        data=to_excel(df),
        file_name="MAC_SIM" + selected_prov.name,
        )
        st.stop()

    elif ready or st.session_state.get('ready'):
        # ready to run
        st.session_state['ready'] = True


        st.session_state['TOTAL_ROWS'] = total_rows
        message_start = f'Assemble GW {numerator}/{total_rows}'
        # start_burn = col2.button(f'Start {message_start}')
        # print(st.session_state)
        # print('hjere')
        # if start_burn:
        # if 'CURRENT_ROW' not in st.session_state:
        #     st.session_state['CURRENT_ROW'] = 1
        # else:
        #     st.session_state['CURRENT_ROW'] += 1
        # if st.session_state['CURRENT_ROW'] > total_rows:
        #     st.info("Somethign went wrong, please delete temporary files and start over")  # noqa: E501
        #     delete = st.button("Start over")
        #     st.session_state['CURRENT_ROW'] = 0
        #     st.stop()

        mac, err = flash_esp()
        if err:
            # error
            st.error("Please try flashing again:" + err)
        else:
            # save original provisioning file
            form = st.form("my_form")

            # command = """testing/data/file.sh"""
            # print(command)
            form.info("MAC FOUND: " + mac)
            sim_number = form.text_input('Enter sim card number', max_chars=20)
            sent = form.form_submit_button("Submit & print")
            if sent or st.session_state.get('sent'):
                st.session_state['sent'] = True
                save_prov_locally(df, prov_local_fp,
                                temp_folder=TEMP_FOLDER)
                save_binary_locally(selected_bin, bin_dest,
                                    temp_folder=TEMP_FOLDER)
                updated, address = update_excel_file(mac=mac,
                                                        sim_number=sim_number)
                print('updated')
                print("Form submitted!")
                print('heyy must print nowww')
                # TODO extract city
                label_img = label.create_label_png(mac=mac, address=address, city='city')
                print_img(img=label_img, n_copy=4)
                print(form)
            # if updated:
            #     if st.button('Print label'):
            #         print('heyy must print nowww')
            #         qr.create_and_print_qr(mac=mac, address=address, n_copy=2)
        # form.info(f'Processing row {st.session_state["CURRENT_ROW"]} of {total_rows}')  # noqa: E501

    #     submit_button = form.form_submit_button('Confirm SIM and update record')
    #     if submit_button and st.button('Confirm SIM and update record'):
    #         print('updated2')
    #         save_prov_locally(df, prov_local_fp,
    #                         temp_folder=TEMP_FOLDER)
    #         save_binary_locally(selected_bin, bin_dest,
    #                             temp_folder=TEMP_FOLDER)
    #         updated, address = update_excel_file(mac=mac,
    #                                                 sim_number=sim_number)
    #         print('updated')
    #         st.success(f'Updated record for {address}')




    #             # if st.session_state['MAC']:

    #             #     st.info(f'Found MAC: {mac}')
    #             #     sim_number = st.text_input('Enter sim card number', max_chars=20)
    #             #     print('sim entereddddd')
    #             #     # sim_number = "21321321312321"
    #             #     confirm = col2.button('Confirm SIM and update record')
    #             #     good_sim = len(sim_number) == 20
    #             #     print('before confirm')
    #             #     if good_sim and st.button('Confirm SIM and update record'):
    #             #         print('where ti should be')
    #             #         pass
    #             #     else:
    #             #         print(sim_number)
    #             #         print('not good sim')


    #             #     if st.button('Confirm SIM and update record') and len(sim_number) > 15 :
    #             #         # st.success('ICCID entered')
    #             #         print('yooooo')
    #             #         print(st.session_state)
    #             #         updated, address = update_excel_file(mac=mac,
    #             #                                     sim_number=sim_number)
    #             #         if not updated:
    #             #             st.session_state['CURRENT_ROW'] -= 1
    #             #         if st.session_state['CURRENT_ROW'] == total_rows and updated:
    #             #             # st.success('All rows processed')
    #             #             # read final excel file
    #             #             curren_count = st.session_state['CURRENT_ROW']
    #             #             fp = Path(TEMP_FOLDER) / f'updated_{curren_count}.pkl'
    #             #             df = pd.read_pickle(fp)
    #             #             st.warning("""This version only contains the site tab!!!
    #             #                         DO NOT OVERWRITE THE ORIGINAL FILE!!!
    #             #                     """)
    #             #             st.download_button(
    #             #                 label='Download latest version',
    #             #                 data=to_excel(df),
    #             #                 file_name=selected_prov.name,
    #             #             )
    #             #     else:
    #             #         print('yooooo', sim_number)
    #             # else:
    #             #     print('2222>>>>>')
    #             #         # elif confirm:
    #             #         #     print(f'{len(sim_number)=}')
    #             #         #     print(f'{sim_number=}')
    #             #         #     st.error('Please enter a valid sim number')
    #             #         # else:
    #             #         #     print("life is hard")