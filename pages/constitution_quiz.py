import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler



# ファイルの読み込むためのパス
csvfile_path = os.path.join(os.getcwd(), 'csv_data')
# クイズ数の変数
n_quiz = 39

# セッション情報の初期化
if "page_select" not in st.session_state:
    st.session_state.page_select = "page_1"
if "answers" not in st.session_state:
    st.session_state.answers = np.zeros(n_quiz, dtype=int).tolist()

# ページ遷移作成
pages = {
    "page_1": "体質　チェック",
    "page_2": "分析結果"
}

page_id = st.sidebar.selectbox( # st.sidebar.*でサイドバーに表示する
    "ページ名",
    pages.keys(),
    format_func=lambda page_id: pages[page_id], # 描画する項目を日本語に変換
    key="page_select"
)


def page_1():
    # 変数
    text_dict = {
        0: "ない",
        1: "あるが、気にならない",
        2: "たまに気に病む",
        3: "常に気に病む"
    }

    st.title(f"体質チェック　全{n_quiz}問")
    st.write("あくまでも自覚症状なのでその時々の感覚で気兼ねなくチェックを付けてみてください")

    def change_page():

        for i in range(n_quiz):
            exec(f'st.session_state.answers[{i}] = st.session_state.answers_{i + 1}')
        st.session_state.page_select = "page_2"
        
    # diagnosis_CSV読込
    df_dia = pd.read_csv(os.path.join(csvfile_path, 'diagnosis.csv'), header=0)
    with st.form(key="name-form"):
        for num in range(n_quiz):
            question = df_dia['質問内容'][num]
            st.markdown(
                f"<h5>第{num + 1}問</h5>",
                unsafe_allow_html=True,
            )
            select_num = st.radio(
                f'**{question}**',
                text_dict.keys(),
                format_func=lambda text: text_dict[text],
                horizontal=True,
                # key=f'answers[{num}]' # 直接代入するパターン･･･×
                key=f'answers_{num + 1}' # session_stateに別の変数で登録したパターン･･･〇
            )
        st.form_submit_button(label="結果を確認", on_click=change_page)



def page_2():
    answer_lists = st.session_state.answers
    # ページ遷移　回答をやり直す
    def back_page():
        st.session_state.page_select = "page_1"
        st.session_state.answers = np.zeros(n_quiz, dtype=int).tolist()

    # アンケート結果をグラフ用の数値とレコメンドのベクトルを作成
    def mk_vector_arr(answer_lists):
        graph_list = [sum(answer_lists[x*3:x*3+3])+1 for x in range(int(len(answer_lists)/3))]
        # 正規化で使用する最小値と最大値を定義
        # ベクトル化
        arr = np.array(graph_list).reshape(-1, 1)

        # [0, 1]でスケーリングする場合（デフォルト）
        minmax_scaler = MinMaxScaler()
        minmax_scaler.fit(arr)
        arr_scaled = minmax_scaler.transform(arr)
        
        # 0.5が切り上げるように調整
        vector_arr = np.floor(arr_scaled+0.5).astype(int).reshape(1, -1)

        return graph_list, vector_arr
    
    # ベクトルからレコメンドデータを作成
    def mk_results(csvfile_path, vector_arr):
        # categoryのCSV読込
        df_cat = pd.read_csv(os.path.join(csvfile_path, 'category.csv'), header=0)
        # symptomのCSV読込
        df_sym = pd.read_csv(os.path.join(csvfile_path, 'symptom.csv'), header=0)
        # vectorのCSV読込
        df_vec = pd.read_csv(os.path.join(csvfile_path, 'vector.csv'), header=0)
        # relationのCSV読込
        df_rel = pd.read_csv(os.path.join(csvfile_path, 'relation.csv'), header=0)
        df = df_vec.set_index('ID').drop('証', axis=1)
        nodes = len(df_vec)
        # knnのインスタンスを呼び出し
        knn = NearestNeighbors(n_neighbors=nodes, algorithm= 'brute', metric= 'cosine')
        # 前処理したデータセットでモデルを訓練
        model_knn = knn.fit(df)
        # 未知のベクトルからレコメンド
        distance, indice = model_knn.kneighbors(vector_arr, n_neighbors=nodes)

        # 類似スコアが上位の高い証だけ抽出
        distance_lists = distance.flatten()
        top_score = np.unique(distance_lists)[0:2]
        num_highscore = np.count_nonzero(distance <= top_score[-1]) if np.count_nonzero(distance <= top_score[-1]) <= 3 else 3

        # subjective_IDのリスト取得
        subjective_ID_lists = (indice.flatten()[0:num_highscore] + 1).tolist()

        # IDから証を取得
        inner_lists = df_vec[df_vec['ID'].isin(subjective_ID_lists)]['証'].tolist()
        # 体質に関連する症状取得
        symptom_ID_lists = df_rel[df_rel['subjective_ID'].isin(subjective_ID_lists)]['symptom_ID'].tolist()
        df_pred = df_sym[df_sym['ID'].isin(symptom_ID_lists)]

        # カテゴリから気になるカテゴリーを選ぶ
        select_dict = {}

        # カテゴリーの選択肢となる辞書を作成する
        for category_ID, frequency in df_pred['category_ID'].value_counts().items():
            category_name =  df_cat[df_cat['ID'] == category_ID]['分類'].values[0]
            exec(f'select_dict[{category_ID}] = category_name + "　　･･･　　" + str(frequency) + "件"')
        
        # select_dictのキーでsort
        sort_select_dict = dict(sorted(select_dict.items(), key=lambda x: x[0]))

        return df_pred, sort_select_dict, inner_lists

    # 五臓弁証をチェックする関数
    def judge_five_results(csvfile_path, five_elems_list):
        # five_resultのCSV読込
        df_fiv = pd.read_csv(os.path.join(csvfile_path, 'five_result.csv'), header=0)
        # リスト内で点数が高い
        max_ID = [i+1 for i, x in enumerate(five_elems_list) if x == max(five_elems_list)]
        # 点数が高い臓系統を抽出
        df_five_result = df_fiv[df_fiv['ID'].isin(max_ID)].set_index('ID')
        five_header_elem = []
        five_str_elem = []
        five_food_elem = []
        for index, row in df_five_result.iterrows():
            five_header_elem.append(row[0])
            five_str_elem.append(f'・{row[0]}タイプ： {row[1]}')
            five_food_elem.append(f'・{row[0]}の食材テーマ...{row[2]}')
            five_food_elem.append(f'例えば...{row[3]}など')

        return five_header_elem, five_str_elem, five_food_elem
    
    # 熱証をチェックする関数
    def judge_BT_results(csvfile_path, BT_elems_list):
        # type_resultのCSV読込
        df_typ = pd.read_csv(os.path.join(csvfile_path, 'type_result.csv'), header=0)
        if BT_elems_list[0] > BT_elems_list[1]:
            BT_type_id = 1
        else:
            BT_type_id = 2

        BT_img_path = os.path.join(os.getcwd(), 'images/results', f'0{str(BT_type_id)}.png')
        BT_category =  df_typ[df_typ['ID'] == BT_type_id]['分類'].values[0]
        BT_type_comment = df_typ[df_typ['ID'] == BT_type_id]['解説'].values[0].split('、')

        return BT_img_path, BT_category, BT_type_comment
    
    # 実証か虚証をチェックする関数
    def judge_physical_results(csvfile_path, physical_elems_list):
        # type_resultのCSV読込
        df_typ = pd.read_csv(os.path.join(csvfile_path, 'type_result.csv'), header=0)
        if sum(physical_elems_list[0::2]) > sum(physical_elems_list[1::2]):
            physical_type_id = 3
        else:
            physical_type_id = 4

        physical_img_path = os.path.join(os.getcwd(), 'images/results', f'0{str(physical_type_id)}.png')
        physical_category =  df_typ[df_typ['ID'] == physical_type_id]['分類'].values[0]
        physical_type_comment = df_typ[df_typ['ID'] == physical_type_id]['解説'].values[0].split('、')

        return physical_img_path, physical_category, physical_type_comment

    # 気血水をチェックする関数
    def judge_kiketusui_results(csvfile_path, kiketusui_list):
        # upset_resultのCSV読込
        df_ups = pd.read_csv(os.path.join(csvfile_path, 'upset_result.csv'), header=0)
        # 最も点数が高いID
        max_ID = [i+1 for i, x in enumerate(kiketusui_list) if x == max(kiketusui_list)]

        df_kiketusui = df_ups[df_ups['ID'].isin(max_ID)].set_index('ID')
        kiketusui_type = []
        kiketusui_comment = []
        for index, row in df_kiketusui.iterrows():
            kiketusui_type.append(f'{row[0]}･･･{row[1]}')
            kiketusui_comment.append(f'{row[0]}の主な要因：{row[2]}')
        return kiketusui_type, kiketusui_comment




    graph_list, vector_arr = mk_vector_arr(answer_lists)
    df_pred, sort_select_dict, inner_lists = mk_results(csvfile_path, vector_arr)

    st.title("回答結果　グラフver")
    st.write("数値が:blue[高い]体質系統に支障をきたしやすい傾向にあります")
    st.caption("詳細は回答結果　要約をご覧ください。")
    tab1_1, tab1_2, tab1_3 = st.tabs(["五臓スコア", "気血水＋寒熱スコア", "数値の目安"])
    with tab1_1:
        radar_data_1 = {
            'r': graph_list[:5],
            'theta': ['肝', '心', '脾', '肺', '腎']
        }
        df_radar_1 = pd.DataFrame(radar_data_1)

        fig_1 = px.line_polar(df_radar_1, r='r', theta='theta', line_close=True)
        fig_1.update_traces(fill='toself')
        fig_1.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True, # 目盛を表示
            range=[0, 10] # 表示範囲の出力
            )),
        )

        st.plotly_chart(fig_1, theme="streamlit", use_container_width=True)

    with tab1_2:
        # レーダーチャートの元になるデータフレーム作成
        radar_data_2 = {
            'r': graph_list[5:],
            'theta': ['気虚', '気滞', '血虚', '瘀血', '津虚', '水滞', '冷え性', '暑がり',]
        }
        df_radar_2 = pd.DataFrame(radar_data_2)

        # レーダーチャート表示
        fig_2 = px.line_polar(df_radar_2, r='r', theta='theta', line_close=True)
        fig_2.update_traces(fill='toself')
        fig_2.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True, # 目盛を表示
            range=[0, 10] # 表示範囲の出力
            )),
        )

        st.plotly_chart(fig_2, theme="streamlit", use_container_width=True)

    with tab1_3:
        st.header('１～４点： 良好')
        st.write('**備えあれば、尚、より盤石なものに**')

        st.header('５～７点： :blue[要警戒]')
        st.write('**早めの対策が鍵**')

        st.header('８～１０点： :red[要対策]')
        st.write('**体質改善に向け、精進されたし**')
    
    if sum(graph_list) == 13:
        st.title("回答結果　健康的な体質")
        st.caption("回答結果が未反映の可能性があります。")
    else:
        st.title("回答結果　要約")
        st.caption('用語が難しく感じた方は「main app > ページ選択"結果をより知る"」に解説があります')
        tab2_1, tab2_2, tab2_3= st.tabs(["五臓", "熱証・実虚", "気血水"])
        with tab2_1:
            st.header("五臓弁証")
            if sum(graph_list[:5]) == 5:
                st.markdown(f"<h5>五臓のバランスは良好です</h5>", unsafe_allow_html=True,)
                five_header_elem = ['肝']
            else:
                five_header_elem, five_str_elem, five_food_elem = judge_five_results(csvfile_path, graph_list[:5])

                st.markdown(f"<h5>五臓タイプ：　{'、 '.join(five_header_elem)}</h5>", unsafe_allow_html=True,)

                st.markdown(f"<h5>Q.  あなたが影響を受けやすい部分は？</h5>", unsafe_allow_html=True,)
                # 改行に半角2回スペース
                st.write('  \n  \n'.join(five_str_elem))
                st.markdown(f"<h5>Q.  このタイプと相性の良い食材は？</h5>", unsafe_allow_html=True,)
                st.write('  \n  \n'.join(five_food_elem))
            st.image(os.path.join(os.getcwd(), 'images/results', '07.png'))

        with tab2_2:
            col1, col2 = st.columns(2)
            with col1:
                st.header("寒熱タイプ")
                BT_img_path, BT_category, BT_type_comment = judge_BT_results(csvfile_path, graph_list[-2:])
                st.markdown(f"<h4>どちらかいえば...  \n{BT_category}タイプ</h4>", unsafe_allow_html=True,)
                st.image(BT_img_path)
                st.write('  \n'.join(BT_type_comment))

            with col2:
                st.header("実虚タイプ")
                physical_img_path, physical_category, physical_type_comment = judge_physical_results(csvfile_path, graph_list[5:])
                st.markdown(f"<h4>どちらかいえば...{physical_category}タイプ</h4>", unsafe_allow_html=True,)
                st.image(physical_img_path)
                st.write('  \n'.join(physical_type_comment))

        with tab2_3:
            st.header("気血水タイプ")

            if sum(graph_list[5:11]) == 6:
                st.markdown(f"<h5>気血水のバランスは良好です</h5>", unsafe_allow_html=True,)
                kiketusui_type = ['気虚･･･気力不足タイプ']
            else:
                kiketusui_type, kiketusui_comment = judge_kiketusui_results(csvfile_path, graph_list[5:11])

                st.write('  \n  \n'.join(kiketusui_type))
                st.markdown(f"<h5><b>この体質になりやすい要因は？</b></h5>", unsafe_allow_html=True,)
                st.write('  \n  \n'.join(kiketusui_comment))
            st.image(os.path.join(os.getcwd(), 'images/results', '06.png'))
        
        st.header("レコメンド結果")
        st.subheader("回答をもとにレコメンドした証はこちらです")
        st.write('、　'.join(inner_lists))
        st.caption('左の証ほど類似度が高いです  \n  \n  \n  \n')
        st.subheader("上記の証に関連した症状を知る")
        # df_predのcategory_IDでfilterをかける
        option_filter = st.selectbox(
            '気になるカテゴリーを選択してください',
            sort_select_dict.keys(),
            format_func=lambda select_id: sort_select_dict[select_id]
            )
        st.caption('左：カテゴリー名、　右：各カテゴリーのうち体質にヒットした症状の数')
        st.caption('ヒットした症状の数とそのカテゴリーへの罹患リスクは一切関係はありません  \n  \n  \n  \n')
        st.subheader('**選択したカテゴリーで表れやすい症状はこちらです**')
        # 症状を一覧表示
        select_list = df_pred[df_pred['category_ID'] == option_filter]['症状'].tolist()
        st.write('、　'.join(select_list))

        st.markdown("<br>", unsafe_allow_html=True,)
        st.markdown("<h5>症状や体質をもとに健康のヒントに役立ててみてください！</h5>", unsafe_allow_html=True,)
        st.write(f'**(1)証、または、証に効く漢方薬を知りたい**  \n･･･「具体的な証(ex."{inner_lists[0]}"など)　漢方」  \n')
        st.write(f'**(2)一から証の候補を探りたい　その１**  \n･･･「気血水の不調(ex."{kiketusui_type[0][:2]}"など)　悩み症状(ex."{select_list[0]}"など)　証」  \n')
        st.write(f'**(3)一から証の候補を探りたい　その２**  \n･･･「五臓の不調(ex."{five_header_elem[0]}"など)　悩み症状(ex."{select_list[-1]}"など)　証」  \n')
        st.write(f'**(4)生活改善方法を調べたい**  \n･･･「{kiketusui_type[-1][:2]}　対策　食べ物/漢方茶/薬膳」')

    st.button('回答をやり直す', on_click=back_page)



if st.session_state.page_select == "page_1":
    page_1()

if st.session_state.page_select == "page_2":
    page_2()