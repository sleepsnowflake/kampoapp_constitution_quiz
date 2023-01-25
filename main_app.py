import streamlit as st
import pandas as pd
import os

def main():
    # セッション情報の初期化
    if "main_page_select" not in st.session_state:
        st.session_state.main_page_select = "main_page_1"

    # ページ遷移作成
    main_pages = {
        "main_page_1": "ようこそ",
        "main_page_2": "操作マニュアル",
        "main_page_3": "結果をより知る"
    }

    page_id = st.sidebar.selectbox( # st.sidebar.*でサイドバーに表示する
        "ページ名",
        main_pages.keys(),
        format_func=lambda page_id: main_pages[page_id], # 描画する項目を日本語に変換
        key="main_page_select"
    )

    def main_page_1():
        st.title("漢方　体質チェッカー")
        
        st.subheader("どんなアプリ？")
        st.markdown("<h5>１.　回答をもとに体質の分析</h5>", unsafe_allow_html=True,)
        st.markdown("<h5>２.　体質から証をレコメンド</h5>", unsafe_allow_html=True,)
        st.caption("証を簡単に言うと、**体質を中医学的**に表現した言葉です")
        st.markdown('<h5>詳しくは下記の<span style="color:#0000ff;">結果のサンプル</span>をご覧ください</h5><br>', unsafe_allow_html=True,)

        st.subheader("早速、試してみたい！")
        st.markdown('<h5>左サイドメニュー「<span style="color:#ff0000;">constitution quiz</span>」をクリック</h5>', unsafe_allow_html=True,)
        st.markdown("<h5>問診を回答してみましょう</h5>", unsafe_allow_html=True,)
        st.write("回答したら:red[ボタンを押して]結果を確認しよう")
        st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_1', '01.png'))
        st.markdown("<br>", unsafe_allow_html=True,)

        st.subheader("どんな人が対象？")
        tutorial_col1_1, tutorial_col1_2 = st.columns(2)
        with tutorial_col1_1:
            st.subheader("(1)どんな人が楽しめる？")
            st.markdown("<h5>・予防医学や健康への興味がある</h5>", unsafe_allow_html=True,)
            st.markdown("<h5>・漢方、中医学に興味がある</h5>", unsafe_allow_html=True,)
            st.markdown("<h5>・体質を把握するヒントにしたい</h5>", unsafe_allow_html=True,)
            st.markdown("<br>", unsafe_allow_html=True,)
            st.write("体質に関する特色、傾向を掲載してます。  \n  \n健康に過ごすためのヒントにどうぞ！")
        with tutorial_col1_2:
            st.subheader("(2)どんな人には不向き？")
            st.markdown("<h5>・治療薬を探している</h5>", unsafe_allow_html=True,)
            st.markdown("<h5>・実際の診断を受けたい</h5>", unsafe_allow_html=True,)
            st.markdown("<h5>・疾患の直接的な助言を求める</h5>", unsafe_allow_html=True,)
            st.write("簡易的な問診と体質に関する情報であり  \n  \n100%オーダーメイドな結果ではないです。  \n  \n病院、漢方専門医にご相談を推奨します")

        st.markdown("<br>", unsafe_allow_html=True,)

        st.subheader("使ってみて困ったら")
        tutorial_col2_1, tutorial_col2_2 = st.columns(2)
        with tutorial_col2_1:
            st.subheader("(1)使い方について")
            st.markdown("<h5>「ページ名」下のセレクトボックス</h5>", unsafe_allow_html=True,)
            st.markdown('<h5>「<span style="color:#0000ff;">操作マニュアル</span>」をクリック</h5>', unsafe_allow_html=True,)
            st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_1', '02.png'))

        with tutorial_col2_2:
            st.subheader("(2)漢方用語について")
            st.markdown("<h5>「ページ名」下のセレクトボックス</h5>", unsafe_allow_html=True,)
            st.markdown('<h5>「<span style="color:#0000ff;">結果をより知る</span>」をクリック</h5>', unsafe_allow_html=True,)
            st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_1', '03.png'))
        
        st.markdown("<br>", unsafe_allow_html=True,)
        
        st.subheader("結果のサンプル")
        st.write('項目をクリックすると表示が変わります。')
        tutorial_tab1_1, tutorial_tab1_2, tutorial_tab1_3, tutorial_tab1_4, tutorial_tab1_5 = st.tabs(['五臓スコア', '気血水＋寒熱スコア', '証レコメンド', 'カテゴリー選択', '症状'])
        with tutorial_tab1_1:
            st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_1', 'tutorial_sample_1.png'))

        with tutorial_tab1_2:
            st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_1', 'tutorial_sample_2.png'))

        with tutorial_tab1_3:
            st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_1', 'tutorial_sample_3.png'))

        with tutorial_tab1_4:
            st.write('カテゴリーから気になる症状群を選択します')
            st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_1', 'tutorial_sample_4.png'))

        with tutorial_tab1_5:
            st.write('選択すると  \n証の持ち主が抱えやすい症状が表示されます')
            st.write('')
            st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_1', 'tutorial_sample_5.png'))

        st.markdown("<br><br>", unsafe_allow_html=True,)
        st.markdown("<h5>体質や証を調べるきっかけになれば幸いです！</h5>", unsafe_allow_html=True,)
        st.write('※上記のようなタイプの検索例')
        st.write('**(1)証、または、証に効く漢方薬を知りたい**  \n･･･「具体的な証(ex."心肝火旺")　漢方」  \n')
        st.write('**(2)一から証の候補を探りたい　その１**  \n･･･「気血水の不調(ex."気滞")　悩み症状(ex."腹部膨満"など)　証」  \n')
        st.write('**(3)一から証の候補を探りたい　その２**  \n･･･「五臓の不調(ex."肝"や"心"など)　悩み症状(ex."便秘"など)　証」  \n')
        st.write('**(4)生活改善方法を調べたい**  \n･･･「気虚　対策　食べ物/漢方茶/薬膳」')
        st.markdown("<br><br>", unsafe_allow_html=True,)

        st.subheader("参考")
        st.markdown("<h5>五臓(肝・心・脾・肺・腎)の基本的理解</h5>", unsafe_allow_html=True,)
        st.write('小金井 信宏：中医学ってなんだろう１人間のしくみ、東洋学術出版社')
        st.markdown("<h5>気血水弁証の基本的内容</h5>", unsafe_allow_html=True,)
        st.write('谿 忠人：わかった気になる漢方薬学４～１０、漢方情報誌phil漢方')
        st.markdown("<h5>症状ごとの代表的な証を把握するのに便利</h5>", unsafe_allow_html=True,)
        st.write('幸井 俊高：症状・疾患別にみる漢方治療指針、日経BP社')
        st.markdown("<h5>代表的な漢方薬と適応する証の解説</h5>", unsafe_allow_html=True,)
        st.write('杉山 卓也：現場で使える薬剤師・登録販売者のための漢方相談便利帖  \nわかる！選べる！漢方薬１６３、翔泳社')
        st.markdown("<h5>マイナーな自覚症状や漢方薬まで網羅</h5>", unsafe_allow_html=True,)
        st.write('桑木 崇秀：健保漢方エキス剤による漢方診療ハンドブック[第４版]、創元社')
    
    def main_page_2():
        st.title('操作マニュアル')
        st.header('パソコンで操作することを推奨します')
        st.write('スマホだと表記やページの表示が見にくい可能性があります。')
        st.markdown("<br>", unsafe_allow_html=True,)

        st.header('結果を閲覧するまでの流れ')
        st.markdown("<br>", unsafe_allow_html=True,)
        st.subheader("１．問診ページに進む")
        st.write('**左サイドメニュー「:red[constitution quiz]」をクリック**')
        st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_2', 'usage01.png'))
        st.caption('サイドメニュー')
        st.write("**左サイドメニューが閉じられていた時は？**")
        st.write('左上のサイドメニューを開く「:red[＞]」アイコンをクリック')
        st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_2', 'usage02.png'))
        st.caption('左上画像')
        st.markdown("<br>", unsafe_allow_html=True,)

        st.subheader("２．回答を進める")
        st.write('**回答を進める際の注意点**')
        st.write('**（１）一時保存できないので回答は一気に進めましょう**')
        st.write('・:blue[途中でページを移動する]と回答箇所が:blue[デフォルト]の左に戻ります')
        st.write('・:red[結果を確認]ボタンまで押すと:red[結果は保持]されるためページ移動しても問題ありません。  \n※ただし回答の各位置は保持されませんのでご注意を！')
        st.markdown("<br>", unsafe_allow_html=True,)

        st.write('**（２）Webブラウザの更新ボタンを押すと一から回答しなおす必要があります**')
        st.write('・結果を確認:red[押した後]でも更新を押すと:red[初期化]されます！')
        st.write('・:blue[ページを移動したい]際は左の:blue[サイドメニュー]からご利用ください。  \n※ただし回答の各位置は保持されませんのでご注意を！')
        st.markdown("<br>", unsafe_allow_html=True,)

        st.subheader("３．結果を見る")
        st.write('**[注意]結果そのものの意味を知りたい方は「結果をより知る」をご覧ください**')
        st.write('・「結果をより知る」への移動の方法  \n※「constitution quiz」表示中は選択ボックスに「結果をより知る」は出てきません。')
        st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_2', 'usage04.png'))
        st.caption('問診回答中や結果表示中の選択ボックスは上記のようになってます')
        st.write('**:blue[main app]をクリック後、:blue[選択ボックス]をクリックします**')
        usage_col1_1, usage_col1_2 = st.columns(2)
        with usage_col1_1:
            st.write('**[1] main appをクリック**')
            st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_2', 'usage03.png'))
            st.caption('サイドメニュー')
        with usage_col1_2:
            st.write('**[2] 選択BOXを開きクリック**')
            st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_2', 'usage05.png'))
            st.caption('サイドメニュー 選択BOX')
        st.markdown("<br>", unsafe_allow_html=True,)

        st.write('**（１）タブをクリックすると表示が変わります**')
        st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_2', 'usage06.png'))
        st.caption('タブをクリックできる箇所一例')
        st.markdown("<br>", unsafe_allow_html=True,)
        st.write('・回答結果をご覧になる際にご活用ください')
        st.write('・グラフで表示された画像はダウンロードできます。')
        usage_col2_1, usage_col2_2 = st.columns(2)
        with usage_col2_1:
            st.write('**[1] カメラマークをクリック**')
            st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_2', 'usage07.png'))
            st.caption('グラフにカーソルを当てるとアイコンが表示')
        with usage_col2_2:
            st.write('**[2] ダウンロードされる**')
            st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_2', 'usage08.png'))
            st.caption('newplot.pngとしてダウンロードされます')
        st.markdown("<br>", unsafe_allow_html=True,)

        st.write('**（２）カテゴリーを選択すると表示される症状が変わります**')
        st.write('下の画像はレコメンド結果の一部サンプルです。  \n表示されるカテゴリーや症状は証によって変わります')
        st.write('**「気になるカテゴリーを選択してください」の:blue[下のセレクト]から変更できます**')
        usage_tab1_1, usage_tab1_2 = st.tabs(['before', 'after'])
        with usage_tab1_1:
            st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_2', 'usage09.png'))
            st.caption('カテゴリー選択前の表示　一例')
        with usage_tab1_2:
            st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_2', 'usage10.png'))
            st.caption('カテゴリー選択後の表示　一例')
        
        st.markdown("<br>", unsafe_allow_html=True,)

        st.subheader("４．結果をやり直したい")
        st.write('**どちらの手法でも実行後に前の回答結果は再現できません。**')
        st.write('**（１）「constitution quiz > :blue[分析結果]」のページ一番下の「:blue[回答をやり直す]」ボタンを押す**')
        st.write('入力が初期化された状態の問診のページに移動します')
        st.write('**（２）Webブラウザの更新ボタンを押す**')
        st.write('「main app > ようこそ」のページに遷移します')

    def main_page_3():
        csvfile_path = os.path.join(os.getcwd(), 'csv_data')

        def make_five_explain(csvfile_path=csvfile_path):
            # CSVの読み込み
            df_fiv = pd.read_csv(os.path.join(csvfile_path, 'five_result.csv'), header=0).set_index('ID')
            five_explains = {}
            # 説明該当箇所をリストに格納
            for index, row in df_fiv.iterrows():
                datum = []
                datum.append(row[4])
                datum.append(row[5])
                five_explains[row[0]] = datum
            return five_explains
        
        def make_type_explain(csvfile_path=csvfile_path):
            # CSVの読み込み
            df_ups = pd.read_csv(os.path.join(csvfile_path, 'upset_result.csv'), header=0).set_index('ID')
            type_explains = {}
            # 説明該当箇所をリストに格納
            for index, row in df_ups.iterrows():
                datum = []
                datum.append(row[3])
                datum.append(row[4])
                datum.append(row[5])
                type_explains[row[0]] = datum
            return type_explains

            
        st.title('結果をより知る')
        st.header('五臓と気血水についてまとめています。')
        st.write('質問意図や結果の解釈の一助になるかと思います。')
        
        st.subheader("五臓とは？")
        st.write('''
        人体の働きを「:blue[五行説]（木・火・土・金・水）」:blue[にあてはめ]、  \n
        ５つに分けたものが五臓「:red[肝]・:red[心]・:red[脾]・:red[肺]・:red[腎]」です。 \n
        五臓がお互いに協力し合い:green[バランスが整った状態]が、  \n
        心身ともに:green[健康的]で整っている状態だとされます。''')
        st.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_3', 'help_01.png'), width=600)

        st.subheader("五臓は臓器と勘違いされがち？？")
        st.write('''
        例えば、五臓の「肝」は、肝臓を、:blue[そのまま表した言葉ではない]ということありません。  \n
        「肝」は肝臓といった働きも含まれますが、自律神経系まで含めた概念です。  \n
        五臓はその内臓だけではなく、:red[その概念よりも広い機能]をさします。  \n
        ''')
        st.write('**下のタブからそれぞれの特性を見ることができます**')

        five_explains = make_five_explain()
        # 肝、心、脾、肺、腎のタブを作る
        help_tab1_1, help_tab1_2, help_tab1_3, help_tab1_4, help_tab1_5 = st.tabs(list(five_explains.keys()))
        for i, five_explain in enumerate(list(five_explains.keys())):
            exec(f"help_tab1_{i+1}.subheader('{five_explain}とは？')")
            exec(f"help_tab1_{i+1}.write('**{five_explain}の働きとは**')")
            exec(f"help_tab1_{i+1}.write('  \\n'.join(five_explains[five_explain][0].split('。')))") # execの中では\\にしないとSyntaxError: unterminated string literal
            exec(f"help_tab1_{i+1}.write(f'**{five_explain}が疲弊すると...**')")
            exec(f"help_tab1_{i+1}.write('  \\n'.join(five_explains[five_explain][1].split('。')))")
            exec(f"help_tab1_{i+1}.image(os.path.join(os.getcwd(), 'images/tutorial/main_page_3', f'5_0{i+1}.png'))")
        st.markdown("<br>", unsafe_allow_html=True,)

        st.subheader("気・血・水とは？")
        st.write('''
        :blue[五臓の働きのもと生みだされ、人体を循環]しています。  \n
        :red[心身が健康的な状態を保つための３要素]  \n
        中医学では:green[五臓の働きにアンバランス]が生じると、  \n
        :green[気血水のいずれかに不調]をきたし、身体的・精神的な:green[症状が表れます]。
        ''')
        st.image(os.path.join(os.getcwd(), 'images/results', '06.png'))
        st.markdown("<br>", unsafe_allow_html=True,)
        st.subheader("気・血・水それぞれの特色")

        # 気血水の特徴をタブで
        help_tab2_1, help_tab2_2, help_tab2_3 = st.tabs(['気', '血', '水'])
        with help_tab2_1:
            st.write('**「気」とは**')
            st.write('''
            簡単に言えば体力のこと。「元気」の「気」であり、  \n
            各組織が正常に機能するための:red[生体のエネルギー源]。  \n
            「気」が不足した状態を:blue[気虚]、「気」の流れが悪い状態を:blue[気滞]という
            ''')

        with help_tab2_2:
            st.write('**「血」とは**')
            st.write('''
            「血液」の「血」であり、  \n
            役割としては、各組織に:red[必要な栄養などを運ぶ]  \n
            「血」が不足することを:blue[血虚]、「血」の流れが悪くなることを:blue[瘀血]という
            ''')

        with help_tab2_3:
            st.write('**「水」とは**')
            st.write('''
            「血」以外の水分であり、体内の様々な水液。  \n
            :red[体を潤し、物質の運搬、関節など特定の部位を満たす]役割がある。  \n
            体が正常に機能するのに:green[必要な水分とそれ以外]で区別して呼称する。  \n
            必要な水分を「:blue[津液]」、うまく代謝されず停滞した水分を「:blue[湿]・:blue[痰]・:blue[飲]」等と呼ぶ  \n
            「水(津液)」が不足することを:blue[津虚]、「水(津液)」の流れが悪くなることを:blue[水滞]という
            ''')
            st.caption('血＋津液を陰液と呼び、津虚の時は血も消耗していることが多い。  \nそのため津虚の際にネット上では**陰虚**と呼ぶ方もいる')

        # 気虚～水滞の特徴をタブで
        st.subheader("気・血・水の不調時について")
        type_explains = make_type_explain()
        help_tab3_1, help_tab3_2, help_tab3_3, help_tab3_4, help_tab3_5, help_tab3_6 = st.tabs(list(type_explains.keys()))
        for i, type_explain in enumerate(list(type_explains.keys())):
            exec(f"help_tab3_{i+1}.subheader('{type_explain}とは？')")
            exec(f"help_tab3_{i+1}.write('**この状態のサインを一言で...**')")
            exec(f"help_tab3_{i+1}.write(type_explains[type_explain][0])") # execの中ではを\\にしないとSyntaxError: unterminated string literal
            exec(f"help_tab3_{i+1}.write(f'**特徴は？**')")
            exec(f"help_tab3_{i+1}.write('  \\n'.join(type_explains[type_explain][1].split('。')))")
            exec(f"help_tab3_{i+1}.write(f'**この体質の症状傾向は？**')")
            exec(f"help_tab3_{i+1}.write('  \\n'.join(type_explains[type_explain][2].split('、')))")


    if st.session_state.main_page_select == "main_page_1":
        main_page_1()

    if st.session_state.main_page_select == "main_page_2":
        main_page_2()
    
    if st.session_state.main_page_select == "main_page_3":
        main_page_3()

if __name__ == '__main__':
    main()