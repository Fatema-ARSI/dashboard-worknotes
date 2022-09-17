from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from collections import Counter
import pathlib
from app import app

##################################################    LOAD THE DATA    #####################################################################

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

df= pd.read_excel(DATA_PATH.joinpath('AP SCOPE.xlsx'))
df['COMPANY CODE']=df['COMPANY CODE'].map(str)


layout = html.Div([


#################################################### FILTER CONTAINER   ##################################################

    html.Div([
        html.Div([
            html.P('Select SSC', className = 'fix_label', style = {'color': 'white', 'margin-top': '2px'}),
            dcc.Dropdown(id='ssc',
                         multi=False,
                         clearable=False,
                         value='SSC Breda',
                         placeholder='Please select your SSC',
                         options=[{'label': i, 'value': i} for i in (df['SSC'].unique())],
                         className='dcc_compon'),],
                    className = "create_container1 four columns", style = {'margin-bottom': '0px'}),], className = "row flex-display"),

########################################################## TEXT AREA  ##################################################

    html.Div([html.Div([html.Div(id= "info_1",),],className="div1",),], className="row flex-display"),


############################################## CARDS FOR COUNTRIES, ERP , ETC....  ########################################

    html.Div([html.Div([
        dbc.Button(id= "text1_1",className = 'card_size'),
        dbc.Modal([dbc.ModalHeader(
                                   html.Div(className="row",
                                            children=[html.Div(className='six columns',
                                                               children=[dbc.Label("Select Column",style={'font-weight': 'bold','color':'#1f2c56','fontSize': 20}),
                                                                         dcc.Dropdown(id='select_1',
                                                                                      options=['ACCOUNTING TOOL','SCANNING SOLUTION','ERP','COMPANY CODE','COUNTRY','ENTITY NAME'],
                                                                                      clearable=True, )] ,
                                                                         style={'width': '500px'}),
                                                    html.Div(className='six columns',
                                                             children=[dbc.Label("Select Value",style={'font-weight': 'bold','color':'#1f2c56','fontSize': 20}),
                                                                       dcc.Dropdown(id='dropdown1_1',
                                                                                    multi=True,
                                                                                    clearable=False, )],
                                                                        style={'width': '500px'})],
                                          style=dict(display='flex')),close_button=False),

                   dbc.ModalBody(dbc.Container([html.Div(id='table_1')])),

                   dbc.ModalFooter(dbc.Button("Close", id="close1_1",style={'background-color':'#1f2c56','color':'white'}),),],
                 id="modal1_1",
                 centered=True,
                 is_open=False,
                 size="xl",        # "sm", "lg", "xl"
                 backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                 scrollable=True,  # False or True if modal has a lot of text
                 #fullscreen=True,    # True, False
                 fade=True,),], className="card_container big three columns",),

          html.Div([
              dbc.Button(id="text2_1",className = 'card_size'),
              dbc.Modal([dbc.ModalHeader(
                                   html.Div(className="row",
                                            children=[html.Div(className='six columns',
                                                               children=[dbc.Label("Select Tool",style={'font-weight': 'bold','color':'#1f2c56','fontSize': 20}),
                                                                         dcc.Dropdown(id='dropdown2_1',
                                                                                     clearable=True,)],
                                                                         style={'width': '500px'})],
                                                      style=dict(display='flex')),close_button=False),

                         dbc.ModalBody(id='data2_1'),
                         dbc.ModalFooter(dbc.Button("Close", id="close2_1",style={'background-color':'#1f2c56','color':'white'}),),],
                       id="modal2_1",
                       centered=True,
                       is_open=False,
                       size="xl",        # "sm", "lg", "xl"
                       backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                       scrollable=True,  # False or True if modal has a lot of text
                       #fullscreen=True,    # True, False
                       fade=True,),  ]  , className="card_container big three columns",),

           html.Div([
              dbc.Button(id="text3_1",className = 'card_size' ),
             dbc.Modal([dbc.ModalHeader(
                                  html.Div(className="row",
                                           children=[html.Div(className='six columns',
                                                              children=[dbc.Label("Select Tool",style={'font-weight': 'bold','color':'#1f2c56','fontSize': 20}),
                                                                        dcc.Dropdown(id='dropdown3_1',
                                                                                    clearable=True, )],
                                                                        style={'width': '500px'})],
                                                     style=dict(display='flex')),close_button=False),

                        dbc.ModalBody(id='data3_1'),
                        dbc.ModalFooter(dbc.Button("Close", id="close3_1",style={'background-color':'#1f2c56','color':'white'}),),],
                      id="modal3_1",
                      centered=True,
                      is_open=False,
                      size="xl",        # "sm", "lg", "xl"
                      backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                      scrollable=True,  # False or True if modal has a lot of text
                      #fullscreen=True,    # True, False
                      fade=True,),], className="card_container big three columns",),

          html.Div([
              dbc.Button(id="text4_1",className = 'card_size'),
              dbc.Modal([dbc.ModalHeader(
                                   html.Div(className="row",
                                            children=[html.Div(className='six columns',
                                                               children=[dbc.Label("Select Tool",style={'font-weight': 'bold','color':'#1f2c56','fontSize': 20}),
                                                                         dcc.Dropdown(id='dropdown4_1',
                                                                                     clearable=True,)],
                                                                         style={'width': '500px'})],
                                                      style=dict(display='flex')),close_button=False),dbc.ModalBody(id='data4_1'),
                         dbc.ModalFooter(dbc.Button("Close", id="close4_1",style={'background-color':'#1f2c56','color':'white'}),),],
                       id="modal4_1",
                       centered=True,
                       is_open=False,
                       size="xl",        # "sm", "lg", "xl"
                       backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                       scrollable=True,  # False or True if modal has a lot of text
                       #fullscreen=True,    # True, False
                       fade=True,),], className="card_container big three columns")], className="row flex-display"),


################################################## GRAPHS ##########################################

    html.Div([

############################################## PIE CHART CONTAINER ############################

        html.Div([dcc.Graph(id='pie_chart_1',
                            config={'displayModeBar': 'hover'}),
                            ], className="create_container four columns", id="cross-filter-options"),

############################################### MAP CONTAINER  ####################################################

        html.Div([dcc.Graph(id="map_1")], className="create_container nine columns"),], className="row flex-display"),

#################################################### DOWNLOAD DATA ######################################################

     html.Div([html.Div([html.Button("Download Excel", id="btn_xlsx_1",style={'background-color':'#1f2c56','color':'white'}),
                         dcc.Download(id="download-dataframe-xlsx_1"),], className = "create_container2 ",),], className="row flex-display"),],
                        id="mainContainer",style={"display": "flex", "flex-direction": "column"})

##################################################### CALLBACK ASIIGNMENT FUNCTION ####################################################


############################################   INFO CONTAINER #################################################

@app.callback(Output('info_1', 'children'),
              [Input('ssc', 'value')],)


def update_info(ssc):

    info=df[df['SSC']==ssc][["ACCOUNTING TOOL","ERP","FINTECH"]]
    info.ERP = info.ERP.str.lstrip("SAP")

    def join_and(items):
        if len(items)==0:
            return ''
        if len(items)==1:
            return items[0]
        return ', '.join(items[:-1]) + ' and '+items[-1]

    ERP=list(info["ERP"].unique())
    ERP=join_and(ERP)

    RESPO=list(info["FINTECH"].unique())
    RESPO=join_and(RESPO)

    def text(x,y):
       text = ["FinTech team is accountable to ",x," for ",ssc," in ",y,"."]
       return text

    return [html.H6(children=text(RESPO,ERP),
                    style = {'color': ' #1f2c56','fontSize': 15,},),]



############################################   TEXT1 #################################################

@app.callback(Output('text1_1', 'children'),
              [Input('ssc', 'value')])

def update_text1(ssc):
    ac=df[df['SSC']==ssc]['ACCOUNTING TOOL'].unique()

    return [html.H6(children='Implemented ',
                    style = {'textAlign':'center',
                             'color': 'white',},),
            html.P(len(ac),
                   style = {'textAlign':'center',
                            'color': 'orange',
                            'fontSize': 40,},),
            html.P('Accounting Tool',
                    style = {'textAlign':'center',
                             'color': 'orange',
                             'fontSize': 20,},),]

############################################   MODAL1 #################################################

@app.callback(Output('dropdown1_1', 'options'),
             [Input("ssc", "value"),],
             [Input("select_1", "value")],)

def output(ssc,select):
    dff1=df[df['SSC']==ssc][['ACCOUNTING TOOL','SCANNING SOLUTION','SSC','ERP','COMPANY CODE','COUNTRY','ENTITY NAME']]
    if select is None:
        options=list(set(dff1['SSC']))
        return [{'label': i, 'value': i} for i in options]

    options=list(set(dff1[select]))
    return [{'label': i, 'value': i} for i in options]

@app.callback(Output('table_1', 'children'),
             [Input("ssc", "value"),],
             [Input("select_1", "value")],
             [Input("dropdown1_1", "value")],)

def output_table(ssc,select,dropdown):
    dff1=df[df['SSC']==ssc][['ACCOUNTING TOOL','SCANNING SOLUTION','SSC','ERP','COMPANY CODE','COUNTRY','ENTITY NAME']]

    if select is not None:
        if dropdown is not None:
           dff = dff1[dff1[select].str.contains('|'.join(dropdown),na=False)]

           return [dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True)]
    return [dbc.Table.from_dataframe(dff1, striped=True, bordered=True, hover=True)]


@app.callback(
    Output("modal1_1", "is_open"),
    [Input("text1_1", "n_clicks"),
    Input("close1_1", "n_clicks"),],
    [State("modal1_1", "is_open")],)

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


############################################   TEXT2 #################################################

@app.callback(Output('text2_1', 'children'),
              [Input('ssc', 'value')])

def update_text2(ssc):
    scn=df[df['SSC']==ssc]['SCANNING SOLUTION'].unique()

    if np.any(scn == 'None')==True:
       return[html.P(children='NO ',
                    style = {'textAlign':'center',
                             'color': 'orange',
                             'fontSize': 20,},),
               html.P('Scanning Solution',
                      style = {'textAlign':'center',
                               'color': 'orange',
                               'fontSize': 20,},),
               html.P('Used',
                       style = {'textAlign':'center',
                                'color': 'orange',
                                'fontSize': 20,},),]
    else:
       return [html.H6(children='Implemented',
                    style = {'textAlign':'center',
                             'color': 'white',},),
               html.P(len(scn),
                      style = {'textAlign':'center',
                               'color': 'orange',
                               'fontSize': 40,},),
               html.P('Scanning Solutions',
                       style = {'textAlign':'center',
                                'color': 'orange',
                                'fontSize': 20,},),]

############################################   MODAL2 #################################################
@app.callback(Output('dropdown2_1', 'options'),
             [Input("ssc", "value"),], )

def output(ssc):
    options=df[df['SSC']==ssc]['ACCOUNTING TOOL'].unique()

    return [{'label': i, 'value': i} for i in options]



@app.callback(Output("data2_1", "children"),
              [Input("ssc", "value"),],
              [Input("dropdown2_1", "value")])

def data2(ssc,dropdown):

    dff=df[df['SSC']==ssc][['SSC','ACCOUNTING TOOL','SCANNING SOLUTION']]

    if dropdown is not None:
        dff1=dff[dff['ACCOUNTING TOOL']==dropdown][['SSC','ACCOUNTING TOOL','SCANNING SOLUTION']]
    else :
        dff1=dff

    names=dff1['SCANNING SOLUTION'].unique()
    def tabdata(number):
        dff1_tab=dff1[dff1['SCANNING SOLUTION']==names[number]][['SSC','ACCOUNTING TOOL','SCANNING SOLUTION']]

        scn_data_tab=pd.pivot_table(dff1_tab,values=('SCANNING SOLUTION'),index=['SSC','ACCOUNTING TOOL','SCANNING SOLUTION'],aggfunc='count')
        scn_data_tab=scn_data_tab.reset_index()



        return [dbc.Container([

                               html.Hr(),
                               dbc.Row([dbc.Table.from_dataframe(scn_data_tab, striped=True, bordered=True, hover=True)])])]



    tabs = []
    for num in range(len(names)):
        tabs.append(dbc.Tab(
                            label=names[num],
                            tab_id=f"tab_{num + 1}",
                            children=tabdata(num)))

    if np.any(names == 'None')==True:
        return html.P(' No Scanning Solution Used',
                       style = {'textAlign':'center',
                                'color': 'orange',
                                'fontSize': 20,},),
    else:

        return[dbc.Container([html.H3("Scanning Tools implemented for " + ssc,style={'color':'black'}),
                              html.Hr(),
                              dbc.Tabs(children=tabs,
                                       active_tab="tab_1", ),])]


@app.callback(
    Output("modal2_1", "is_open"),
    [Input("text2_1", "n_clicks"),
    Input("close2_1", "n_clicks"),],
    [State("modal2_1", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


############################################   TEXT3 #################################################

@app.callback(Output('text3_1', 'children'),
              [Input('ssc', 'value')],)

def update_text3(ssc):

    BUs=df[df['SSC']==ssc]['ERP'].unique()

    return [html.H6(children='Implemented in ',
                    style = {'textAlign':'center',
                            'color': 'white',},),
            html.P(len(BUs) ,
                    style = {'textAlign':'center',
                             'color': 'orange',
                             'fontSize': 40,},),
            html.P('BU / ERP',
                   style = {'textAlign':'center',
                            'color': 'orange',
                            'fontSize': 20,},),]

############################################   MODAL3 #################################################

@app.callback(Output('dropdown3_1', 'options'),
             [Input("ssc", "value"),], )

def output(ssc):
    options=df[df['SSC']==ssc]['ACCOUNTING TOOL'].unique()

    return [{'label': i, 'value': i} for i in options]



@app.callback(Output("data3_1", "children"),
              [Input("ssc", "value"),],
              [Input("dropdown3_1", "value")])

def data2(ssc,dropdown):

    dff=df[df['SSC']==ssc][['SSC','ACCOUNTING TOOL','SCANNING SOLUTION','ERP']]

    if dropdown is not None:
        dff1=dff[dff['ACCOUNTING TOOL']==dropdown][['SSC','ACCOUNTING TOOL','SCANNING SOLUTION','ERP']]
    else :
        dff1=dff

    names=dff1['SCANNING SOLUTION'].unique()
    def tabdata(number):
        dff1_tab=dff1[dff1['SCANNING SOLUTION']==names[number]][['SSC','ACCOUNTING TOOL','SCANNING SOLUTION','ERP']]

        scn_data_tab=pd.pivot_table(dff1_tab,values=('SCANNING SOLUTION'),index=['SSC','ACCOUNTING TOOL','SCANNING SOLUTION','ERP'],aggfunc='count')
        scn_data_tab=scn_data_tab.reset_index()



        return [dbc.Container([

                               html.Hr(),
                               dbc.Row([dbc.Table.from_dataframe(scn_data_tab, striped=True, bordered=True, hover=True)])])]

    dff1_notab=pd.pivot_table(dff1[['SSC','ACCOUNTING TOOL','ERP']],values=('ERP'),index=['SSC','ACCOUNTING TOOL','ERP'],aggfunc='count')
    dff1_notab=dff1_notab.reset_index()


    tabs = []
    for num in range(len(names)):
        tabs.append(dbc.Tab(
                            label=names[num],
                            tab_id=f"tab_{num + 1}",
                            children=tabdata(num)))

    if np.any(names == 'None')==True:
        return [dbc.Table.from_dataframe(dff1_notab, striped=True, bordered=True, hover=True)]
    else:

        return[dbc.Container([html.H3("Scanning Tools implemented for " + ssc,style={'color':'black'}),
                              html.Hr(),
                              dbc.Tabs(children=tabs,
                                       active_tab="tab_1", ),])]



@app.callback(
    Output("modal3_1", "is_open"),
    [Input("text3_1", "n_clicks"),
    Input("close3_1", "n_clicks")],
    [State("modal3_1", "is_open")],)

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


############################################   TEXT4 #################################################

@app.callback(Output('text4_1', 'children'),
              [Input('ssc', 'value')],)

def update_text4(ssc):

    Entities=df[df['SSC']==ssc]['COMPANY CODE'].unique()

    return [html.H6(children='Implemented in ',
                    style = {'textAlign':'center',
                             'color': 'white',},),
            html.P(len(Entities) ,
                    style = {'textAlign':'center',
                             'color': 'orange',
                             'fontSize': 40,},),
            html.P(' Entities',
                   style = {'textAlign':'center',
                            'color': 'orange',
                            'fontSize': 20,},),]


############################################   MODAL4 #################################################

@app.callback(Output('dropdown4_1', 'options'),
             [Input("ssc", "value"),], )

def output(ssc):
    options=df[df['SSC']==ssc]['ACCOUNTING TOOL'].unique()

    return [{'label': i, 'value': i} for i in options]



@app.callback(Output("data4_1", "children"),
              [Input("ssc", "value"),],
              [Input("dropdown4_1", "value")])

def data2(ssc,dropdown):

    dff=df[df['SSC']==ssc][['SSC','ACCOUNTING TOOL','SCANNING SOLUTION','COMPANY CODE']]

    if dropdown is not None:
        dff1=dff[dff['ACCOUNTING TOOL']==dropdown][['SSC','ACCOUNTING TOOL','SCANNING SOLUTION','COMPANY CODE']]
    else :
        dff1=dff

    names=dff1['SCANNING SOLUTION'].unique()
    def tabdata(number):
        dff1_tab=dff1[dff1['SCANNING SOLUTION']==names[number]][['SSC','ACCOUNTING TOOL','SCANNING SOLUTION','COMPANY CODE']]

        scn_data_tab=pd.pivot_table(dff1_tab,values=('SCANNING SOLUTION'),index=['SSC','ACCOUNTING TOOL','SCANNING SOLUTION','COMPANY CODE'],aggfunc='count')
        scn_data_tab=scn_data_tab.reset_index()



        return [dbc.Container([

                               html.Hr(),
                               dbc.Row([dbc.Table.from_dataframe(scn_data_tab, striped=True, bordered=True, hover=True)])])]

    dff1_notab=pd.pivot_table(dff1[['SSC','ACCOUNTING TOOL','COMPANY CODE']],values=('COMPANY CODE'),index=['SSC','ACCOUNTING TOOL','COMPANY CODE'],aggfunc='count')
    dff1_notab=dff1_notab.reset_index()


    tabs = []
    for num in range(len(names)):
        tabs.append(dbc.Tab(
                            label=names[num],
                            tab_id=f"tab_{num + 1}",
                            children=tabdata(num)))

    if np.any(names == 'None')==True:
        return [dbc.Table.from_dataframe(dff1_notab, striped=True, bordered=True, hover=True)]
    else:

        return[dbc.Container([html.H3("Scanning Tools implemented for " + ssc,style={'color':'black'}),
                              html.Hr(),
                              dbc.Tabs(children=tabs,
                                       active_tab="tab_1", ),])]


@app.callback(Output("modal4_1", "is_open"),
              [Input("text4_1", "n_clicks"),
              Input("close4_1", "n_clicks")],
              [State("modal4_1", "is_open")],)

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

############################################   PIE CHART #################################################

@app.callback(Output('pie_chart_1', 'figure'),
              [Input('ssc', 'value')])

def update_graph(ssc):
    dff1=df[df['SSC']==ssc][['SSC','ACCOUNTING TOOL']]
    labels=list(Counter(dff1["ACCOUNTING TOOL"]).keys()) # equals to list(set(words))
    values=list(Counter(dff1["ACCOUNTING TOOL"]).values()) # counts the elements' frequency
    colors = ['#09F3F0',  '#e55467','orange','#dd1e35']



    return {
        'data': [go.Pie(labels=labels,
                        values=values,

                        marker=dict(colors=colors,),
                        hoverinfo='label+value+percent',
                        textinfo='label+value',
                        textfont=dict(size=13),
                        textposition='outside',
                        hole=.3,
                        rotation=45
                        # insidetextorientation='radial',


                        )],

        'layout': go.Layout(
            # width=800,
            # height=520,
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            hovermode='closest',
            title={
                'text': 'Accounting Tool Implementation  ' ,
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                       'color': 'white',
                       'size': 20},
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family="Computer Modern",
                size=17,
                color='white')),}


############################################   MAP #################################################

@app.callback(Output("map_1", "figure"),
              Input("ssc", "value"),)

def updateGraphCB(ssc):
    map_data=df[df['SSC']==ssc][["ACCOUNTING TOOL","SCANNING SOLUTION","ERP","LAT","LNG","COMPANY CODE","ENTITY NAME","COUNTRY","FINTECH"]]

    if np.any(map_data["SCANNING SOLUTION"] == 'None')==True:
        name=' '
    else:
        name= map_data['SCANNING SOLUTION'].astype(str)

    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(lon=map_data ['LNG'],
                                   lat=map_data ['LAT'],
                                   name= ssc ,
                                   mode='markers',
                                   marker=dict(size=15),
                                   meta=map_data ['ACCOUNTING TOOL'].astype(str),
                                   hoverinfo='text',
                                   hovertext=
                                    '<b>Country</b>: ' + map_data['COUNTRY'].astype(str) + '<br>' +
                                    '<b>Tool</b>: ' + map_data ['ACCOUNTING TOOL'].astype(str) + ' ' + name+'<br>' +
                                    '<b>BU</b>: ' +  map_data['ERP'].astype(str) + '<br>' +
                                    '<b>Company Code</b>: ' + map_data['COMPANY CODE'].astype(str) ))



    fig.layout.plot_bgcolor = '#1f2c56'
    fig.layout.paper_bgcolor = '#1f2c56'

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      width=900,
                      height=550,
                      hovermode='closest',
                      mapbox=dict(accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',),)


    return fig


############################################  DOWNLOAD EXCEL #################################################

@app.callback(Output("download-dataframe-xlsx_1", "data"),
              Input("btn_xlsx_1", "n_clicks"),
              prevent_initial_call=True,)

def func(n_clicks):
    df=df[["ACCOUNTING TOOL","SCANNING SOLUTION","ERP","COMPANY CODE","ENTITY NAME","COUNTRY","FINTECH"]]
    return dcc.send_data_frame(df.to_excel, "MDM_DATA.xlsx", sheet_name="Customer - Vendor",index=False)
