# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 11:15:02 2021

@author: khaja
"""
#import os
#os.chdir('D:/analysis/KHAJA/Doc_dash/Doc_dash/datasets')
from app import app
import pandas as pd
import numpy as np
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_daq as daq
#import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import glob
import pathlib
import dash_table
import itertools
from functools import reduce
#import dash_extensions as de
BASE_PATH = pathlib.Path(__file__).parent
DATA_PATH = BASE_PATH.joinpath("datasets").resolve()



### Styling ###

tab_style_cont = {
    'width': '50%',
    'margin-left': '0px',
    'background': 'white',
    'height': '30px',
    'border-bottom': '3px solid #337ab7',
    #'box-shadow': '0 -3px 14px rgba(0,0,0,0.2)',
    'position':'relative',
    'padding': '6px',
    'border-top':'none',
    'transition': 'all .5s',   
}
tab_selected_style_cont = {
    'content': "",
    'display': 'inline-block',
    'z-index': '0',
    'height': '30px',
    'width': '50%',
    'background': '#337ab7',
    'position':'relative',
    'padding': '6px',
    #'box-shadow': '0 -3px 14px rgba(0,0,0,0.2)',
    'border-top':'none',
    'color':'white',
    #'border-radius':'2rem',
    'transition': 'all .5s',  
}

data=DATA_PATH.glob("p*.csv")

dataset={}
for i in data:
    dataset[i]=pd.read_csv(i)
    
new_keys=["Patient1", "Patient2", "Patient3"]

for key,n_key in zip(list(dataset.keys()), new_keys):
    dataset[n_key] = dataset.pop(key)
    df=dataset[n_key]
            #print(df)
    df["Date"]=pd.to_datetime(df["Date"], format= "%d-%m-%Y").dt.date
    #date=pd.to_datetime(df["Date"], format= "%d-%m-%Y").dt.date
    #datestr=pd.DatetimeIndex(df["Date"].strftime("%d-%m-%Y"))
    #df["Date"]= [date.strftime("%d-%m-%Y") for date in df["Date"]]
    df.Age = df.Age.astype(str)    
   
def iterfy(iterable):
    if isinstance(iterable, str):
        yield iterable
    else:
        try:
            yield from iter(iterable)
        except TypeError:
            yield iterable
            
column_set = df.columns[0:26]
column_set1 = column_set[~column_set.isin(["Height", "Year"])]
column_set2 = column_set[~column_set.isin(["Height", "Quarter", "Year", "Month", "Age","Date", "Drugs"])]
column_set3 = column_set[column_set.isin(["HbA1C", "UrineGlucose", "TwoHours"])]
column_table = df.columns[~df.columns.isin(["Month", "Year", "Day", "BMR"])]

drug=df["Drugs"].unique()
Months=df["Month"].unique()
Quarters=df["Quarter"].unique()

#print(drug)

#year=df.index.unique()
#slider_label = [{'label' : i, 'value' : i} for i in df['year'].unique()]
#print(slider_label)


head = html.Div(html.H1(children='DOCTORS DASHBOARD'))

top_btn = html.Div([html.A(id='button_top',children='Reports', n_clicks=0),
                           html.A(id='button_top2',children='Predictions', n_clicks=0),
                           ]
                          )

compare = html.Div(id='compare_div', children=[
    html.Div([html.P(id='compare',
                     children = 'COMPARE', style={'color':'black','font-weight': 'bold'}),
              daq.BooleanSwitch(
                  id='switch',
                  on=False,
                  color="#337ab7",
                  ),
              ],
             ),
    html.Div(id='patient_div', children=[
        html.P(id='patient',
               children = 'PATIENTS', style={'color':'black','font-weight': 'bold'}),
        dcc.Dropdown(id = 'Patientid', options=[{'label': k, 'value': k} for k in new_keys],
                     value="Patient1", placeholder='Select Feature'),
        ],
        ),
    ]
        )

#options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

selectors = html.Div(id = 'selector_div', children=[
    #html.Div(id='doc_img_div', children = de.Lottie(options=options, width="50%", height="50%", url="https://assets8.lottiefiles.com/packages/lf20_l13zwx3i.json")),
    html.Div(id='xaxis_div', children=[
    html.P(id = 'x_axis',
                   children = 'READINGS',style={'color':'black','font-weight': 'bold'}),
    dcc.Dropdown(id = 'x_opt', options=[{'label': k, 'value': k} for k in column_set1],
                 value="Date", placeholder='Select Feature'),
    ],
         ),
    #html.Button('Year Filter', id='submit_val', n_clicks=0),
    html.Div(id='button_div', children=[
        html.P(id = 'button_title',
               children ="Month",style={'color':'black','font-weight': 'bold'}),
        daq.BooleanSwitch(
            id='submit_val',
            on=False,
            color="#337ab7",
            ),
        ],
        ),
   
    html.Div(id='slider_div', children=[

# =============================================================================
#     daq.Slider(
#                 id='slider',
#                 handleLabel={"showCurrentValue": True,"label": "Year"},
#                 step=1,
#                 size=460,
#                 min=2015,
#                 max= 2020,
#                 #value = 2010,
#                 color='#337ab7',
#             ),
# =============================================================================
# =============================================================================
#     dcc.RadioItems(
#           id='Radio-val', options= [{'label': k, 'value': k} for k in Months],
#                                     #value=Months[0],
#           labelStyle={'display': 'inline-block'}
# )  
# =============================================================================
      
    dcc.Checklist(
          id='cklist', options= [{'label': k, 'value': k} for k in Months],
                                    #value=Months[0],
          labelStyle={'display': 'inline-block'}
)  
],
        ),
    
# =============================================================================
#     html.Div(id='Q_cklist_div', children=[
#         dcc.Checklist(
#           id='Q_cklist', options= [{'label': k, 'value': k} for k in Quarters],
#                                     #value=Months[0],
#           labelStyle={'display': 'inline-block'}
# )
# ],
#         ),        
# =============================================================================
        
    html.Div(id='yaxis_div', children=[
    html.P(id = 'y_axis',
                   children = 'OBSERVATIONS',style={'color':'black','font-weight': 'bold'}),
    dcc.Dropdown(id = 'opt', options=[{'label': k, 'value': k} for k in column_set2],
                 value="Fasting",multi=True, placeholder='Select Features'),
    ],
        ),
    ]
    )

graph = html.Div(id = 'graphtable_div', children= [
    html.Div(id = 'graph_div', children= [dcc.Graph(id='example-graph',
                                                        config = {'displayModeBar': False}),
                                          ],
             ),
    html.Div(id= 'table_div', children=[
        #html.P(id = 'table_id', children = 'REPORT',style={'color':'black','font-weight': 'bold'}),
    dash_table.DataTable(id = 'table',
                         #columns=[{"name": i, "id": i} for i in column_table],
                         #data=df.to_dict('records'),
                         fixed_rows={'headers': True},
                         fixed_columns={'data': 1},
                         #fixed_columns={'headers': True, 'data': 1},
                         virtualization=True,
                         style_table={'height': 400, 'overflowY': 'auto'},
                         style_header={ 'border': '1px solid black' },
                         style_cell={
                             # all three widths are needed
                             'minWidth': 95, 'maxWidth': 95, 'width': 95,
                             'overflow': 'hidden',
                             'border': '1px solid black',
                             'textAlign': 'center'
                             #'textOverflow': 'ellipsis',
                             }
                         )
    ],
        ),
    ]
    )

selectors2 = html.Div(id = 'selector_drug', children=[
    html.Div(id='drug_div_yaxis', children=[
    html.P(id = 'drug_y_axis',
                   children = 'FEATURES',style={'color':'black','font-weight': 'bold'}),
    dcc.Dropdown(id = 'y_option', options=[{'label': k, 'value': k} for k in column_set3],
                 value="HbA1C", placeholder='Select Feature', multi=True),
    ],
         ),
    html.Div(id='drug_div', children=[
    html.P(id = 'drug_selection',
                   children = 'DRUGS',style={'color':'black','font-weight': 'bold'}),
    dcc.Dropdown(id = 'drug_id', options=[{'label': k, 'value': k} for k in drug],
                 value=drug[0],
                 placeholder='Select Feature', multi=True),
    ],
        ),
    ], 
    )

graph2 = html.Div(id = 'graph_drug', children= [dcc.Graph(id='drug-graph',
                                                        config = {'displayModeBar': False}),
                                               ],
                 )

tab = html.Div(id = 'tab_div',children=[dbc.Col([
    #html.P(id = 'tab_text', children = 'Type of report',style={'color':'black','font-weight': 'bold'}),
    dcc.Tabs(id="tab_test", value='Consolidate Report',children=[
        dcc.Tab(id='tab1_test',
                label='Consolidate Report',
                value='Consolidate Report',
                style=tab_style_cont,
                selected_style=tab_selected_style_cont,
                ),
        dcc.Tab(id='tab2_test',
                label='Drug Comparison',
                value='Drug Comparison',
                style=tab_style_cont,
                selected_style=tab_selected_style_cont,
                ),
        ]
        )
    ]
    )
    ]
    )

main =  html.Div(id='main', children=[head,
                                      top_btn,
                                      compare,
                                      html.Br(),
                                      html.Hr(),
                                      tab,
                                      html.Br()])                                        
                                                 
content1 = html.Div(id='container1', children=[selectors,
                                               graph])

content2 = html.Div(id='container2', children=[selectors2,
                                               graph2])


app.layout = html.Div([main, content1, content2])

@app.callback(Output('container1', 'style'),
              [Input('tab_test', 'value')])
def hide_tab1(tab_test_value) :
    if tab_test_value == 'Consolidate Report' :
        return {'display':'block'}
    else :
        return {'display':'none'}

@app.callback(Output('container2', 'style'),
              [Input('tab_test', 'value')])
def hide_tab2(tab_test_value) :
    if tab_test_value != 'Consolidate Report' :
        return {'display':'block'}
    else :
        return {'display':'none'}
    
@app.callback([Output('table', 'data'),
              Output('table', 'columns'),
              Output('table', 'style_data_conditional')],
              [Input('Patientid', 'value')],
              [Input('x_opt', 'value')],
              [Input('opt', 'value')],
              [Input('cklist', 'value')])              
def update_table(Patientid_value, x_opt_value, opt_value, cklist_value):
    
    if cklist_value:
        #print(cklist_value)
        data_frames = [dataset[a] for a in iterfy(Patientid_value)]
        full= reduce(lambda  left,right: pd.merge(left,right,on=['Date'], suffixes=["_1", "_2"],
                                          how='outer'), data_frames) 
        
        full=full[full.Month.isin(cklist_value)] if "Month" in full.columns else full[full.Month_1.isin(cklist_value)]
        #print(full)
        data=full.to_dict('records')
        
        #print(x_opt_value, opt_value)
        club=[]
        x_opt_value=[x_opt_value]
        opt_value=[opt_value]
        opt=list(itertools.chain(*opt_value))
        
        for i in x_opt_value+opt :
            cl=full.columns[pd.Series(full.columns).str.startswith(i)]
            club.append(cl)
        #print(club)
        col=list(itertools.chain(*club))
        
        columns = [{'name':i, 'id':i} for i in col]
        
        filtered_df= full[col]
        #print(filtered_df)
        int_columns=filtered_df.select_dtypes("number").columns
        #print(int_columns)
        style_data_conditional=[]
        
        for nm in int_columns:
            for i in full[nm].nlargest(3):
                style_data_conditional.append({
                    'if': { 'filter_query': '{{{}}} = {}'.format(nm, i), 'column_id': nm}, 
                            'color': '#0074D9',
                            'content': '\00A7 ',
                            })
        #print(style_data_conditional)
        
        return [data, columns, style_data_conditional]
                         
    else :
        data_frames = [dataset[a] for a in iterfy(Patientid_value)]
        full= reduce(lambda  left,right: pd.merge(left,right,on=['Date'], suffixes=["_1", "_2"],
                                          how='outer'), data_frames)   
        data=full.to_dict('records')
        
        #print(x_opt_value, opt_value)
        club=[]
        x_opt_value=[x_opt_value]
        opt_value=[opt_value]
        opt=list(itertools.chain(*opt_value))
        
        for i in x_opt_value+opt :
            cl=full.columns[pd.Series(full.columns).str.startswith(i)]
            club.append(cl)
        #print(club)
        col=list(itertools.chain(*club))
        #print(col)
        #col=list(itertools.chain.from_iterable([iterfy(x_opt_value), iterfy(opt_value)]))
        #col=[x_opt_value]+[opt_value]
        #print(col)
        #data.set_index('Date')
        columns = [{'name':i, 'id':i} for i in col]
        
        filtered_df= full[col]
        #print(filtered_df)
        int_columns=filtered_df.select_dtypes("number").columns
        #print(int_columns)
        style_data_conditional=[]
        
        for nm in int_columns:
            for i in full[nm].nlargest(3):
                style_data_conditional.append({
                    'if': { 'filter_query': '{{{}}} = {}'.format(nm, i), 'column_id': nm}, 
                            'color': 'red',
                            })
        #print(style_data_conditional)
        
        return [data, columns, style_data_conditional]  
    

# =============================================================================
# @app.callback([
#     Output('slider','min'),
#     Output('slider','max'),
#     Output('slider','value')],
#     [Input('x_opt', 'value')])
# def update_slider(x_opt_value, slider_value) :
#     df1=df[df.index == slider_value]
#     print(df1.index)
#     for i in x_opt_value:
#         min=df1.index.min()
#         max=df1.index.max()
#         val=df1.index.min()
#         return [min,max,val]
# =============================================================================

#@app.callback([
#    Output('slider', 'min'),
#    Output('slider', 'max'),
#    Output('slider', 'value')],
#    [Input('submit_val', 'n_clicks')])
#def update(n_clicks) :
#    if n_clicks > 0 :
#        df1=df["Year"]
#                print(df1)
#        min1 = df1['Year'].min()
#        max2 = df1['Year'].max()
#        value = df1['Year'].min()
#        return (min1, max2, value)


# =============================================================================
# @app.callback(
#     Output('Q_cklist', 'style'),
#     [Input('submit_val', 'on')],
#     [Input('x_opt', 'value')])
# def update_Q_list(on, x_opt_value):
#     if x_opt_value == "Quarter" and on == True :
#         return {'display':'inline-block'}
#     else :
#         return {'display':'none'}
#     
# =============================================================================
                
# =============================================================================
# @app.callback([
#     Output('button_div', 'style'),
#     Output("cklist", 'style')],
#     [Input('x_opt', 'value')],
#     [Input('submit_value', 'on')])
# def update_Button(x_opt_value, on):
#     if x_opt_value == "Quarter" :
#         if on == True :
#             return [{'display':'none'}, {'display':'none'}]
#         else : 
#             return [{'display':'none'}, {'display':'none'}]
#     else :
#         return [{'display':'inline-block'},{'display':'inline-block'}]
# =============================================================================
    



@app.callback(
    Output('cklist', 'style'),
    [Input('submit_val', 'on')])
def update_cklist(on):
    if on == True :
        return {'display':'inline-block'}
    else :
        return {'display':'none'}
    
@app.callback(
    Output('submit_val', 'disabled'),
    [Input('submit_val', 'on')])
def update_bool(on):
    if on == True :
        disabled = True
        return disabled
    else:
        return None
    
@app.callback(
    Output('Patientid', 'multi'),
    [Input('switch', 'on')])
def update_selection(on):
    if on == True :
        multi = True
        return multi
    else :
        return None

@app.callback(Output('example-graph', 'figure'),
              [Input('opt', 'value')],
              [Input('x_opt', 'value')],
              [Input('cklist', 'value')],
              [Input('Patientid', 'value')])
              #[Input('submit_val', 'value')]
              #[Input('submit_val', 'n_clicks')])
def display_value(opt_value, x_opt_value, cklist_value, Patientid_value):
    #print(Radio_value)
    #df1=df[df.Year == slider_value]
    #print(df.dtypes)
    #print(df1[x_opt_value])
    #print(opt_value)
    #print(df1.index)
    #df1 = df[df[x_opt_value].eq(slider_value)]
    
    if cklist_value:
        if x_opt_value not in ["Quarter", "Year", "Month","Age", "Drugs"]:
            fig = go.Figure()
            for a in iterfy(Patientid_value):
                dff=dataset[a][dataset[a].Month.isin(cklist_value)]
                dff.sort_values(by=x_opt_value, inplace= True)
                for i in iterfy(opt_value):
                    label="-".join([a, i])
                    fig.add_trace(go.Scatter(x=dff[x_opt_value], y=dff[i], mode="lines+markers",name = label,
                                             hoverlabel=dict(namelength=25), hovertemplate=None, showlegend=True))
        else :
            fig = go.Figure()
            for a in iterfy(Patientid_value):
                dff=dataset[a][dataset[a].Month.isin(cklist_value)]
                dff.sort_values(by=x_opt_value, inplace= True)
                for i in iterfy(opt_value):
                    label="-".join([a, i]) 
                    fig.add_trace(go.Bar(x=dff[x_opt_value].astype(str), y=dff[i],name = label,
                                         hoverlabel=dict(namelength=25), hovertemplate=None, showlegend=True))
                              
    else :
        
        #df.Year = df.Year.astype(str)
        if x_opt_value not in ["Quarter", "Year", "Month", "Age", "Drugs"]:
            fig = go.Figure()
            for a in iterfy(Patientid_value):
                dataset[a].sort_values(by=x_opt_value, inplace= True)
                for i in iterfy(opt_value):
                    label="-".join([a, i]) 
                    fig.add_trace(go.Scatter(x=dataset[a][x_opt_value], y=dataset[a][i], mode="lines+markers",
                                             name = label,
                                             hoverlabel=dict(namelength=25), hovertemplate=None, showlegend=True))
            
        else :
            fig = go.Figure()
            for a in iterfy(Patientid_value):
                for i in iterfy(opt_value):
                    label="-".join([a, i]) 
                    fig.add_trace(go.Bar(x=dataset[a][x_opt_value].astype(str), y=dataset[a][i],name = label,
                                         hoverlabel=dict(namelength=25), hovertemplate=None, showlegend=True))
                        
    fig.update_layout(xaxis_title=x_opt_value, yaxis_title="Observations")
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_layout(plot_bgcolor='white')
    return fig

@app.callback(Output('drug-graph', 'figure'),
              [Input('drug_id', 'value')],
              [Input('y_option', 'value')],
              [Input('Patientid', 'value')])
     
def displaydrug_value(drug_id_value, y_option_value, Patientid_value):
    fig = go.Figure()
    for a in iterfy(Patientid_value):
        drugdf=dataset[a]
        #drugdf["Date"]=pd.to_datetime(drugdf["Date"])
        #drugdf["Date"]=np.array(drugdf["Date"], dtype='datetime64')
        #print(drugdf["Date"])
        drugdf.sort_values(by="Date", inplace= True)
        grp=drugdf.groupby("Drugs")
        for b in iterfy(drug_id_value):
            grpdata=grp.get_group(b)
# =============================================================================
#             lv=[]
#             for i in grpdata["Date"]:
#                 da=(i-grpdata["Date"].min())/np.timedelta64(1, "M")
#                 lv.append(da)
# =============================================================================
            
            for i in iterfy(y_option_value):
                #label="-".join([a, i, b])
                label= "-".join([a, i])
                #dfd=dfd[dfd["Drugs"]== b]
                fig.add_trace(go.Scatter(x=grpdata["Date"], y=grpdata[i], mode="lines+markers",
                                         name = label, hovertext=grpdata["Date"],
                                         hoverlabel=dict(namelength=35), hovertemplate= "%{y}<br>%{hovertext}",
                                         showlegend=True))
            
    fig.update_layout(xaxis_title="Month-Year", yaxis_title="Observations")
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_layout(plot_bgcolor='#fcf8ec')
    return fig

@app.callback(
    Output('button_top', 'href'),
    [Input('button_top', 'n_clicks')])
def update_layout(n_clicks):
    if n_clicks >0 :
        return 'http://208.77.20.147:8000/apps/report'
    else :
        return 'http://208.77.20.147:8000/apps/report'
    
@app.callback(
    Output('button_top2', 'href'),
    [Input('button_top2', 'n_clicks')])
def update_layout2(n_clicks):
    if n_clicks >0 :
        return 'http://208.77.20.147:8000/apps/prediction'
    else :
        return 'http://208.77.20.147:8000/apps/prediction'

# =============================================================================
# @app.callback(Output('button_title', 'children'),
#               [Input("x_opt", "value")])
# 
# def update_button_title(x_opt_value):
#     if x_opt_value == "Quarter":
#         return "Quarter"
#     else :
#         return "Month"
# =============================================================================

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=6000)