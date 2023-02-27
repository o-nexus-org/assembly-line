# readme https://github.com/pklaus/brother_ql

# info https://support.brother.com/g/b/manuallist.aspx?c=nl&lang=nl&prod=lpql700euk&type2=70

# drivers
# https://www.brother.nl/ondersteuning/ql-700/downloadshttps://www.brother.nl/ondersteuning/ql-700/downloads

# lsusb | grep Brother | cut -d ' ' -f6 | cut -d ':' -f1 
# --rotate 90 --threshold 0.5 
run_print:# 
	python src/qr.py

run:
	streamlit run app.py