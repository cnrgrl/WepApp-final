from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)



schifa = pd.read_csv(r'static/asset/SCHIFA.csv')
schifa.reset_index(drop=True, inplace=True)

klinikList = pd.read_csv(r'static/asset/KlinikList.csv')
k_name = klinikList['Klinikname']

merged_all_google_updated = pd.read_csv(r'static/asset/merged_all_google_updated.csv')
merged_all_kb_updated = pd.read_csv(r'static/asset/merged_all_kb_updated.csv')


kList = klinikList[['Klinik_ID', 'Klinikname', 'Bild', 'Link Google Maps', 'Link Klinikbewertungen', 'IframeLink']]

schifa_list = schifa[['Klinik_ID', 'KB_Sentiment', 'Prediction', 'Klinikumbew_Gesamt', 'Negative_x','Neutral_x','Positive_x', 'Total_Comments_x', 'GesamtsterneWithNull', 'Negative_y', 'Neutral_y','Positive_y', 'Total_Comments_y', 'SCHIFA', 'Shifa_Score']]

def get_description(select):
    # k_selected=kList[kList['Klinikname']==select]
    iframe = ""
    bild = ""
    k_id = kList.loc[kList['Klinikname'] == select]['Klinik_ID']
    # description[0].loc[description[0]['Klinik_ID']==description[1]]['IframeLink']
    eleman = kList.loc[kList['Klinikname'] == select, 'IframeLink'].tolist()
    for i in eleman:
        iframe = i

    bild_path = kList.loc[kList['Klinikname'] == select, 'Bild'].tolist()
    for i in bild_path:
        bild = i


    return kList, k_id, select, iframe, bild


def get_google_infos(select):
    klinik_selected = merged_all_google_updated.loc[merged_all_google_updated['Name_Klinik'] == select]
    df = klinik_selected[['Sternebewertung', 'Textuelle_Bewertung', 'Likes', 'Bewertung_Datum']]

    g_infos = []
    for i in range(len(df)):
        g_infos.append(list(df.iloc[i]))

    return (g_infos)

def get_schifa(select):
    id = 0
    schifa_point = "" #DONE       0
    schifa_scr = "" #             1
    google_sterne="" #            2

    google_positive="" #          3
    google_negative="" #          4
    google_neutral="" #           5
    google_total=""   #           6

    kb_sterne="" #              7
    kb_sentiment="" #           8
    kb_predicted="" #           9
    kb_positive="" #            10
    kb_negative="" #            11
    kb_neutral="" #             12
    kb_total="" #               13

    k_id = kList.loc[kList['Klinikname'] == select, 'Klinik_ID'].tolist()
    for i in k_id:
        id = int(i)

    # schifa_sterne = schifa_list.loc[schifa_list['Klinik_ID'] == k_id]['Klinik_ID']
    # description[0].loc[description[0]['Klinik_ID']==description[1]]['IframeLink']
    schifa_sterne = schifa_list.loc[schifa_list['Klinik_ID'] == id, 'SCHIFA'].tolist()
    for i in schifa_sterne:
        schifa_point = i

    schifa_score = schifa_list.loc[schifa_list['Klinik_ID'] == id, 'Shifa_Score'].tolist()
    for i in schifa_score:
        schifa_scr = i
    ######
    g_sterne = schifa_list.loc[schifa_list['Klinik_ID'] == id, 'GesamtsterneWithNull'].tolist()
    for i in g_sterne:
        google_sterne = i

    # g_sentiment = schifa_list.loc[schifa_list['Klinik_ID'] == id, 'Sentiment'].tolist()
    # for i in g_sentiment:
    #     google_sentiment = i

    g_positive = schifa_list.loc[schifa_list['Klinik_ID'] == id, 'Positive_y'].tolist()
    for i in g_positive:
        google_positive = int(i)

    g_negative = schifa_list.loc[schifa_list['Klinik_ID'] == id, 'Negative_y'].tolist()
    for i in g_negative:
        google_negative = int(i)

    g_neutral = schifa_list.loc[schifa_list['Klinik_ID'] == id, 'Neutral_y'].tolist()
    for i in g_neutral:
        google_neutral = int(i)
    
    g_total = schifa_list.loc[schifa_list['Klinik_ID'] == id, 'Total_Comments_y'].tolist()
    for i in g_total:
        google_total = int(i)

    #############

    k_sterne=schifa_list.loc[schifa_list['Klinik_ID'] == id, 'Klinikumbew_Gesamt'].tolist()
    for i in k_sterne:
        kb_sterne = i

    k_sentiment=schifa_list.loc[schifa_list['Klinik_ID'] == id, 'KB_Sentiment'].tolist()
    for i in k_sentiment:
        kb_sentiment = i
        

    k_predicted=schifa_list.loc[schifa_list['Klinik_ID'] == id, 'Prediction'].tolist()
    for i in k_predicted:
        kb_predicted = i

    k_positive=schifa_list.loc[schifa_list['Klinik_ID'] == id, 'Positive_x'].tolist()
    for i in k_positive:
        kb_positive = int(i)

    k_negative=schifa_list.loc[schifa_list['Klinik_ID'] == id, 'Negative_x'].tolist()
    for i in k_negative:
        kb_negative = int(i)

    k_neutral=schifa_list.loc[schifa_list['Klinik_ID'] == id, 'Neutral_x'].tolist()
    for i in k_neutral:
        kb_neutral = int(i)

    k_total=schifa_list.loc[schifa_list['Klinik_ID'] == id, 'Total_Comments_x'].tolist()
    for i in k_total:
        kb_total = int(i)

    
    return schifa_point, schifa_scr, google_sterne,google_positive,google_negative,google_neutral,google_total,kb_sterne,kb_sentiment,kb_predicted,kb_positive,kb_negative,kb_neutral,kb_total
            #0              1           2               3                   4               5            6           7           8          9            10           11          12      13          14 




def get_klinik_infos(select):
    k_selected = merged_all_kb_updated.loc[merged_all_kb_updated['Name_Klinik'] == select]
    k_df = k_selected[['Titel', 'Fach_Bereich', 'Textuelle_Bewertung', 'Gesamte_Sterne', 'Bewertung_Datum']]

    k_infos = []
    for i in range(len(k_df)):
        k_infos.append(list(k_df.iloc[i]))

    return k_infos


@app.route('/', methods=['GET', 'POST'])
def index():
    select = str(request.form.get("klinik-list"))
    # kInfo=getKlinikInfos(select)
    g_infos = get_google_infos(select)
    k_infos = get_klinik_infos(select)
    description = get_description(select)
    g_schifa = get_schifa(select)


    return render_template("index.html", kliniks=k_name, description=description, g_infos=g_infos, k_infos=k_infos, g_schifa = g_schifa)


if __name__ == "__main__":
    app.run(debug=True)
