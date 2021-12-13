import streamlit as st
import pandas as pd
import time as t
from examples import excel_example
import re


def write_results():
    st.write("Resultado do algoritmo")
    xls = pd.ExcelFile('saida.xlsx')

    for name in xls.sheet_names:

        df = pd.read_excel(xls, name)

        index_list = df.index.tolist()
        df.index = [re.sub(r'(\d+)', r'Horário \1', str(item)) for item in index_list]

        st.write(name)
        st.dataframe(df)



if __name__ == '__main__':
    st.write(""" # METASCHEDULE """)
    example_file = open('excel_example.xlsx', 'rb')

    st.download_button("Modelo de arquivo para ser utilizado", example_file, "excel_example.xlsx")
    file = st.file_uploader("Selecione o arquivo a ser utilizado")
    if file is not None:
        with open('./testfile.xlsx', 'wb') as f:

            # Recebendo arquivo e salvando localmente
            f.write(file.getbuffer())
            f.close()

            # Calculando horários
            with st.spinner("Em progresso..."):
                excel_example('testfile.xlsx')


            # Exibindo resultado
            st.success("Execução finalizada!")
            write_results()