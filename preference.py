import numpy as np
import dash
from dash import callback_context
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
from itertools import combinations
import pandas as pd
import plotly.express as px
import pathlib
import string
from reader import read_txt
from style import button_style,matrix_table_style,\
                    pref_name_stlye,pie_style,histo_style,plots_style, \
                    left_col_style,title_style,radio_style,style_background



dummy_letters=list(string.ascii_lowercase)

cur_dir = pathlib.Path.cwd()
working_dir = cur_dir / "preferences"


path='/home/djamel/PycharmProjects/SVA/preferences/Eissorten.txt'

path='/home/djamel/PycharmProjects/SVA/preferences/Küche.txt'


prefs_list,title=read_txt(path)

# TODO title Eis einbauen


prefs_let=dict(zip(dummy_letters[0:len(prefs_list)], [0]*len(prefs_list)))





combis=[]
for it in combinations(prefs_let.keys(), 2):
    combis+=[list(it)]

r=len(prefs_let)-1
combs = []
for k in range(len(prefs_let)-1):
    f = len(prefs_let)
    j=1
    for _ in range(r):
        combs+=[combis[k]]
        k+=f-j
        j+=1
    f-=1
    r-=1

app = dash.Dash(__name__)


k=0
l=1
font_size=45
new_list=[]

b_list=[]
for ii in range(len(combs)):
    b_list+=[html.Div(html.Td(id='val_per_'+str(ii+1)))]
new_list+=[html.Div(children=b_list,style={'fontSize': font_size,"margin-left": "80px","type":"numeric"})]

b_list=[]
for ii in range(len(combs)):
    b_list+=[html.Div(html.Td(id='val_'+str(ii+1)))]
new_list+=[html.Div(children=b_list,style={'fontSize': font_size,"margin-left": "50px"})]

b_list=[]
for ii in range(len(prefs_list)):
    b_list+=[html.Div(html.Label(prefs_list[ii]),style={'color': 'white'})]
new_list+=[html.Div(children=b_list,style={'fontSize': font_size,"margin-left": "50px"})]



n_list=[]
for lets in prefs_let.keys():
    n_list+=[html.Div(html.Label(lets),style={'color': 'white'})]
new_list+=[html.Div(children=n_list,style={'fontSize': font_size,"margin-left": "50px"})]




for j in range(len(prefs_let)-1):
    button_list=[]
    for i in range(len(prefs_let)-l):
        button_list+=[html.Div(children=dcc.RadioItems(
                id="button_{}".format(k+1),
                options=[
                            {'label': combs[k][0], 'value': combs[k][0]},
                            {'label': combs[k][1], 'value': combs[k][1]},
                        ]
                ),style = radio_style,className="button"
        )
        ]
        k+=1
    new_list+=[html.Div(children=button_list)]
    l+=1

#######################################
# hier werden buchstaben zurück gegeben
Inpts_let=[Input(component_id="button_"+str(ii+1), component_property='value') for ii in range(len(combs))]
Outpts_val=[Output(component_id='val_'+str(ii+1), component_property='children') for ii in range(len(prefs_let))]
@app.callback(output=Outpts_val,inputs=Inpts_let)
def preference_core(*ch):

    for k in prefs_let.keys():
        prefs_let[k]=0.0

    for v in ch:
        if v is not None:
            prefs_let[v]+=1

    return list(prefs_let.values())


Inpts_let=[Input(component_id="val_per_"+str(ii+1), component_property='children') for ii in range(len(prefs_let))]
@app.callback(output=Output('histogram', 'figure'),inputs=Inpts_let)
def update_figure(*ch):
    df=pd.DataFrame(prefs_let.items(), columns=["prefenrence", "fraction"])
    df["prefenrence"]=prefs_list
    df["fraction"]=list(ch)
    fig = px.bar(df, x="prefenrence", y="fraction", color="prefenrence")

    # fig.update_layout(transition_duration=500)

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="#ffe4b5",
        yaxis=dict(tickfont=dict(size=15),titlefont=dict(size=15)),
        xaxis=dict(tickfont=dict(size=15),titlefont=dict(size=15)),
        # legend=dict(font=dict(family="Courier", size=30))
        showlegend=False
        # yaxis=list(titlefont=list(size=25), title="test"))
    )

    # fig.update_layout(
    #     yaxis=dict(tickfont=dict(size=30)))

    return fig


Inpts_let=[Input(component_id="val_per_"+str(ii+1), component_property='children') for ii in range(len(prefs_let))]
@app.callback(output=Output('pie-graph', 'figure'),inputs=Inpts_let)
def update_figure(*ch):
    df=pd.DataFrame(prefs_let.items(), columns=["prefenrence", "fraction"])
    df["prefenrence"]=prefs_list
    df["fraction"]=list(ch)
    fig_p = px.pie(df, names="prefenrence", values="fraction", color="prefenrence")


    fig_p.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="#ffe4b5",
        yaxis=dict(tickfont=dict(size=20),titlefont=dict(size=20)),
        xaxis=dict(tickfont=dict(size=20),titlefont=dict(size=20)),
        legend=dict(font=dict(family="Courier", size=20)))

    return fig_p












#######################################
# hier werden buchstaben zurück gegeben
Inpts_let=[Input(component_id="val_"+str(ii+1), component_property='children') for ii in range(len(prefs_let))]
Outpts_val=[Output(component_id='val_per_'+str(ii+1),
                   component_property='children') for ii in range(len(prefs_let))]
@app.callback(output=Outpts_val,inputs=Inpts_let)
def preference_core(*ch):

    if not any(ch):
        return [format(0,".3f")]*len(ch)
    ch=list(np.round(ch / np.sum(ch), 3))
    return [format(ii,".3f") for ii in ch]





app.layout = html.Div([html.Div(children=[
                                html.Div(children=[
                                    html.Div(children=[
                                    html.Div(children=[html.P('Präferenzmatrix am Beispiel: {}'.format(title))],style=title_style),
                                    html.Div(children=[html.P(" ")],style=pref_name_stlye),
                                    html.Div(children=new_list,style = matrix_table_style)])],style=left_col_style),
                                    html.Div(children=[
                                    html.Div(children=[dcc.Graph(id='histogram')],style=histo_style),
                                    html.Div(children=[dcc.Graph(id='pie-graph')],style=pie_style),
                                    html.Div(children=[html.Button(id='save_figure histo',
                                                                   n_clicks=0,
                                                                   children='print pie (d)',
                                                                   style=button_style)],
                                                                    style={"padding-left": "5em"}),
                                    html.Div(children=[html.Button('save data (d)',id='save_data',
                                                                   n_clicks=0,
                                                                   style=button_style)],
                                                                    style={"padding-left": "1em"}
                                             )
                                ],

                                    style=plots_style)
                            ],
                            style=style_background)
                            ]
                        )

@app.callback(inputs=Input(component_id="save_data",component_property='n_clicks'))
def save_data(save):
    aaa=0
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'save_data' in changed_id:
        df = pd.DataFrame(prefs_let.items(), columns=["prefenrence", "fraction"])




if __name__ == '__main__':
    app.run_server()