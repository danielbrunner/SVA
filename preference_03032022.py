from dash.dependencies import Input, Output,State
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash
import pathlib
from itertools import combinations
import os
import plotly.express as px
import pymysql
import pandas as pd
import json
from collections import Counter

from style_03032022 import project_inupt,project_name,project_button,\
    atribute_input,atribute_button,iterator_choicer,number_counter,\
    next_button,save_button,reset_button,pair_iterator,atribute_title




project={"working_dir":"","project name":""}

project["working_dir"]=pathlib.Path.cwd()
project_atribute={}
title=[{"name": "Attribute", "id": "Attribute"},{"name": "Summe", "id": "Summe"}]

n_clicks_list={"radio buttons":0}

dict_tot={}


# creataing app
app = dash.Dash(__name__)



@app.callback(
            Output("project-name","children"),
            Input('button', 'n_clicks'),
            State('project-input', 'value')
            )
def update_project_name(n_clicks,project_name):
    if n_clicks==0:
        return "1. Bitte Projektname eingeben"

    if n_clicks==1:
        project["working_dir"] = pathlib.Path.cwd()/project_name
        project["project name"] = project_name

        if not os.path.exists(project["working_dir"]):
            pathlib.Path(project["working_dir"]).mkdir(parents=True, exist_ok=True)
        project["project name exist"]=project_name
        return "Projektname: {}".format(project["project name"])

    if n_clicks > 1:
        if os.path.exists(project["project name exist"]):
            project["project name"] = project_name
            project["working_dir"] = pathlib.Path.cwd() / project_name
            pathlib.Path(project["working_dir"]).mkdir(parents=True, exist_ok=True)
        return "Projektname: {}".format(project["project name"])



@app.callback(
            Output("val_3","value"),
            Input('button', 'n_clicks'),
            State('project-input', 'value')
            )
def save_project_to_mysql(n_clicks,project_name):

    if n_clicks==1:
        conn = pymysql.connect(
            host='localhost',
            user='test_user',
            password="Zbastards+03",
            db='preference',
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO preference.project (id,date,project_name) VALUES (default,CURRENT_DATE(),'{}');".format(project_name))
        conn.commit()
        conn.close()


    return ""




@app.callback(
            Output("atribute-list","children"),
            Input('button-atribute', 'n_clicks'),
            Input('button', 'n_clicks'),
            State('input-atribute', 'value')
            )
def update_output(n_clicks,n_click_2,atribute_name):
    if n_click_2==0:
        return ""
    if n_clicks==0:
        return ""
    if n_clicks>=1:
        project_atribute[atribute_name] = 0
    return ""



@app.callback(
            Output("val_4","value"),
            Input('button-atribute', 'n_clicks'),
            # Input('button', 'n_clicks'),
            State('input-atribute', 'value')
            )
def save_atr_to_mysql(n_clicks,atribute_name):

    if n_clicks==1:
        conn = pymysql.connect(
                host='localhost',
                user='test_user',
                password="Zbastards+03",
                db='preference',
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO preference.atributes(project_id, atr) VALUES(LAST_INSERT_ID(), '{}');".format(atribute_name))
        # cur.execute("INSERT INTO preference.project (id,date,project_name) VALUES (default,CURRENT_DATE(),'{}');".format(atribute_name))
        conn.commit()
        conn.close()


    return ""



@app.callback(
            Output('container', 'children'),
            Output('num-left', 'children'),
            Input('iter-pairs', 'n_clicks'),
            )
def iterator_pairs(n_clicks):

    if not project_atribute:
        if n_clicks>0:
            n_clicks_list["radio buttons"] += 1
        return [dcc.RadioItems(
                                options=[
                                        {'label':"",'value':"val"},
                                        {'label': "",'value': "val"},
                                        ],
                            ),"----"]

    pairs = []
    for i_1, i_2 in combinations(project_atribute.keys(), 2):
        pairs.append([i_1, i_2])

    if len(project_atribute)==1:
        return ["Du hast nur ein Attribut gewählt. Bitte drücke Reset und starte nochmal neu!",""]

    if n_clicks > n_clicks_list["radio buttons"]+len(pairs):
        return ["","Fertig!"]




    return [dcc.RadioItems(
                options=[
                            {'label':pairs[n_clicks-n_clicks_list["radio buttons"]-1][0],
                             'value':pairs[n_clicks-n_clicks_list["radio buttons"]-1][0]},
                            {'label':pairs[n_clicks-n_clicks_list["radio buttons"]-1][1],
                             'value': pairs[n_clicks-n_clicks_list["radio buttons"]-1][1]},
                        ],
                id="switch",style={"align-item": "center"},
                ),"noch {} mal".format(n_clicks_list["radio buttons"]+len(pairs)-n_clicks+1)]




#######################################

@app.callback(
            Output("val","value"),
            Input('switch', 'value')
            )
def preference_core(swi):
    project_atribute[swi]+=1
    return ""




@app.callback(
            Output("val_5","value"),
            Input('summarize', 'n_clicks')
            )
def summarize(n_clicks):
    path=project["working_dir"]
    # prefs={}
    if n_clicks==1:
        files=os.listdir(path)
        for file in files:
            if file=="file_summary.txt" or file=="file_summary.xlsx":
                continue
            with open(path/file) as f:
                data = f.read()
            project_atribute.update(dict(Counter(project_atribute) + Counter(json.loads(data))))
            # project_atribute.update(json.loads(data))
        with open(project["working_dir"]/"file_summary.txt",'w') as file:
            file.write(json.dumps(project_atribute))
    return ""


@app.callback(
            Output("val_6","value"),
            Input('excel', 'n_clicks')
            )
def save_excel(n_clicks):
    if n_clicks==1:

        if os.path.exists(project["working_dir"]/"file_summary.txt"):
            with open(project["working_dir"]/"file_summary.txt") as f:
                data = f.read()
            df = pd.DataFrame(data=json.loads(data), index=[0])
            df.to_excel(project["working_dir"]/"file_summary.xlsx")

    return ""








@app.callback(
            Output("table",'columns'),
            Output("table", 'data'),
            Input('iter-pairs', 'n_clicks'),
            Input('button-atribute', 'n_clicks'),
            )
def table_update(swi,tt):

    return [title,[{"Attribute": i, "Summe": j} for i, j in project_atribute.items()]]




@app.callback(Output('histogram', 'figure'),Input('iter-pairs', 'n_clicks'),Input('summarize', 'n_clicks'))
def update_figure(ch,aa):

    df = pd.DataFrame([[0,0]], columns=["Präferenz", "Summe"])
    if project_atribute:
        df=pd.DataFrame(project_atribute.items(), columns=["Präferenz", "Summe"])
    fig = px.bar(df, x="Präferenz", y="Summe")
    return     fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="#fffacd",
        plot_bgcolor="#ffffb3",
        yaxis=dict(tickfont=dict(size=25),titlefont=dict(size=25)),
        xaxis=dict(tickfont=dict(size=25),titlefont=dict(size=25)),

    )





@app.callback(
            Output("val_2","children"),
            Input('save-dict', 'n_clicks')
            )
def save_dict(n_clicks):
    if n_clicks==0:
        return ""

    if n_clicks >= 1:
        path, dirs, files = next(os.walk(project["working_dir"]))
        n_files = len(files)

        with open(project["working_dir"]/"file_{}.txt".format(n_files+1), 'w') as file:
            file.write(json.dumps(project_atribute))

        project_atribute.clear()
        return ""






############## reset knpf
@app.callback(Output('button','n_clicks'),
              Output("project-name","children"),
              Output('button', 'n_clicks'),
              Output('button-atribute', 'n_clicks'),
              Output('iter-pairs', 'n_clicks'),
              Input('reset','n_clicks'))
def set_reset(reset):
    if reset>0:
        if not os.listdir(project["working_dir"]):
            os.rmdir(project["working_dir"])
        project_atribute.clear()
    return [0,"Bitte Projektname eingeben",0,0,0]




bc="#fffacd"


app.layout = html.Div([
    #########################
    # project name definition
    # TODO hier noch titel
    html.H1("Präferenzmatrix",style={"font-size":"60px",'backgroundColor':"#ffffcc"}),

html.Div(children=[
        html.Div(children=[html.H1(id='project-name',style=project_name),
                            html.Div(dcc.Input(id='project-input', type='text',style=project_inupt)),
                            html.Button('Projektname', id='button', n_clicks=0, style=project_button)]
             ,style={'backgroundColor':bc,"height": "190px","width":"1050px"}),


    ###########################
    # atribute input ##########
    html.Div(children=[html.H1('2. Bitte Attribute eingeben ',style=atribute_title),
                        html.Div(dcc.Input(id='input-atribute', type='text',style=atribute_input)),
                        html.Button('Attribute', id='button-atribute', n_clicks=0,style=atribute_button),
                       ],style={'backgroundColor':bc,"height": "190px","width":"1050px"})
                    ],
            style={'display': 'flex','flex-direction': 'row'}
    ),

    html.Div(id='atribute-list'),
    ##########################
    # iterator ###############

    html.Div(children=[
                    html.Button('nächster', id='iter-pairs', n_clicks=0,style=next_button),
                    html.Div(id='val'),
                    html.Div(id='val_3'),
                    html.Div(id='val_4'),
                    html.Div(id='val_5'),
                    html.Div(id='val_6'),
                    html.Div(id='num-left',style=number_counter)],
                    style=pair_iterator
                ),
    html.Div(id='container', style=iterator_choicer),

    html.Div(children=[
                    html.Button('Projekt speichern', id='save-dict', n_clicks=0,style=save_button),
                    html.Div(id='val_2',style={"font-size": "50px",})
                    ],style={'backgroundColor':bc,"height": "80px"}),

    html.Div(children=[html.Button('reset', id='reset', n_clicks=0,style=reset_button),
                       html.Button('summarize', id='summarize', n_clicks=0,style=reset_button),
                        html.Button('save ecxel', id='excel', n_clicks=0,style=reset_button)
                       ],
             style={"height": "80px",'backgroundColor':bc}),

    ################################
    # Table #######################


    html.Div(children=[
    dash_table.DataTable(id='table',
                         # columns=title,
                         data=[],
                         style_header={"font-size": "30px",'backgroundColor':"#fff599",
                                       "width": "500px","text-align": "center"},
                         style_cell={"font-size": "30px",'backgroundColor':"#fffce6",
                                     "text-align": "center"}),


    ###################################
    ## Plots

    dcc.Graph(id='histogram',style={"font-size": "30px",'backgroundColor':bc,"width": "1000px","margin-left":"30px"})
    ],
        style={'display': 'flex','flex-direction': 'row','backgroundColor':bc})

    ],style={"text-align": "center",'backgroundColor':"#ffffb3","height": "1500px"})








if __name__ == '__main__':
    app.run_server(debug=True)








