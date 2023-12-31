from datetime import datetime, date, timedelta
import pandas as pd
from random import seed, randint
import streamlit as st

current_week_number = date.today().isocalendar().week
dt = date.today()
week_start = dt - timedelta(days=dt.weekday())


def read_data(sheet_id, sheet_names):
    dict_dfs = {}
    for s in sheet_names:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={s}"
        df = pd.read_csv(url)
        df['done'] = df['done'].astype(bool)
        dict_dfs[s] = df.loc[~df['done']].iloc[:, 1:].sample(frac=1) #random_state=current_week_number)
   
    return dict_dfs

sheet_id = "1Y-WG1bAbzlxtFMaW1uceZNDcSz09ENcHm5p9lpGhzx8"
sheet_names = ['diretores', 'albums_all', 'albums_br', 'books_br', 'books_all']
dict_dfs = read_data(sheet_id, sheet_names)

    
st.title('Qual é a boa da semana?')
st.subheader(f'Para a semana de {week_start.strftime('%d/%m/%Y')}, os conteúdos escolhidos serão:')


if st.button('Escolher', type='primary'):

    row_dict = {}
    for s in sheet_names:
        row_dict[s] = randint(0, dict_dfs[s].shape[0])

    # Cinema
    st.write('---')
    col1, col2 = st.columns(2)

    with col1:
        st.title(f'Cinema')

    with col2:
        df = dict_dfs['diretores'].iloc[row_dict['diretores']]
        director_week = df['director']
        director_week_suggestion = df['movie']
        st.markdown(f'#### Diretor: *{director_week}*')
        st.markdown(f'Sugestão de filme: *{director_week_suggestion}*')

    st.write('---')
    
    # Música
    col1, col2 = st.columns(2)

    with col1:
        st.title(f'Música')

    with col2:
        df = dict_dfs['albums_all'].iloc[row_dict['albums_all']]
        album_week = df['album']
        artist_week = df['artist']
                
        df = dict_dfs['albums_br'].iloc[row_dict['albums_br']]
        album_br_week = df['album']
        artist_br_week = df['artist']

        st.markdown(f'#### Álbum internacional')
        st.markdown(f'{album_week} - {artist_week}')
        st.markdown(f'#### Álbum nacional')
        st.markdown(f'{album_br_week} - {artist_br_week}')

    st.write('---')

    # Literatura
    col1, col2 = st.columns(2)

    with col1:
        st.title(f'Literatura')

    with col2:
        df = dict_dfs['books_all'].iloc[row_dict['books_all']]
        book_week = df['book']
        author_week = df['author']
                
        df = dict_dfs['books_br'].iloc[row_dict['books_br']]
        book_week_br = df['book']
        author_week_br = df['author']

        st.markdown(f'#### Livro Luso-Brasileiro')
        st.markdown(f'{book_week_br} - {author_week_br}')
        st.markdown(f'#### Livro Estrangeiro')
        st.markdown(f'{book_week} - {author_week}')

    st.write('---')


    # st.write(directors)
# st.write(director_week)