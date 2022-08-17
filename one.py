import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
from collections import Counter
import time


#####################################################################    EXTRACT DATA    ################################################################################

df=pd.read_excel('AP SCOPE.xlsx')




##############################################################  FRAME CONTAINERS (layout of the dashboard    #####################################################

font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css" ##css design
meta_tags = [{"name": "viewport", "content": "width=device-width"}] ##css design

external_stylesheets = [meta_tags, font_awesome]


app = JupyterDash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Div([
## title head layout
        html.Div([
            html.Img(src=app.get_asset_url('saint-gobain.png'),
                     id='sg-image',
                     style={
                         "height": "100px",
                         "width": "auto",
                         "margin-bottom": "25px",},),



        ],className="one-third column",),

        html.Div([
            html.Div([
                html.H4("AP SOLUTIONS AROUND SAINT-GOBAIN", style={"margin-bottom": "0px", 'color': 'white'}),
                html.H6("Track AP tool Implementation", style={"margin-top": "0px", 'color': 'white'}),])], className="one-half column", id="title"),

        html.Div([
            html.H6('Data Last Updated: August 10, 2022' ,
                    style={'color': 'orange'}),], className="one-third column", id='title1'),

    ], id="header", className="row flex-display1", style={"margin-bottom": "25px"}),
## filter container
    html.Div([
        html.Div([
            html.P('Select Tool', className = 'fix_label', style = {'color': 'white', 'margin-top': '2px'}),
            dcc.Dropdown(id='tools',
                         multi=False,
                         clearable=True,
                         value='Medius',
                         placeholder='Please select your tool',
                         options=['Medius', 'APIA','Readsoft', 'Scanvisio'], className='dcc_compon'),



            ], className = "create_container1 four columns", style = {'margin-bottom': '0px'}),
        ], className = "row flex-display"),

##################### TEXT AREA
    html.Div([
         html.Div([html.Div(id= "info",),
                   ],className="div1",),], className="row flex-display"),



## cards to filter on countries etc....

    html.Div([html.Div([
        dbc.Button(id= "text1",className = 'card_size'
                ),
        dbc.Modal([

                   dbc.ModalBody(id='data1'),
                   dbc.ModalFooter(dbc.Button("Close", id="close1",style={'background-color':'#ced4da'}),),],
                 id="modal1",
                 centered=True,
                 is_open=False,
                 size="xl",        # "sm", "lg", "xl"
                 backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                 scrollable=True,  # False or True if modal has a lot of text
                 #fullscreen=True,    # True, False
                 fade=True,
                 ),

        ], className="card_container big three columns",),

          html.Div([
              dbc.Button(id="text2",className = 'card_size'
                      ),
              dbc.Modal([

                         dbc.ModalBody(id='data2'),
                         dbc.ModalFooter(dbc.Button("Close", id="close2",style={'background-color':'#ced4da'}),),],
                       id="modal2",
                       centered=True,
                       is_open=False,
                       size="xl",        # "sm", "lg", "xl"
                       backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                       scrollable=True,  # False or True if modal has a lot of text
                       #fullscreen=True,    # True, False
                       fade=True,
                       ),  ]       # True, False


            , className="card_container big three columns",),

           html.Div([
              dbc.Button(id="text3",className = 'card_size'
                      ),
             dbc.Modal([

                        dbc.ModalBody(id='data3'),
                        dbc.ModalFooter(dbc.Button("Close", id="close3",style={'background-color':'#ced4da'}),),],
                      id="modal3",
                      centered=True,
                      is_open=False,
                      size="xl",        # "sm", "lg", "xl"
                      backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                      scrollable=True,  # False or True if modal has a lot of text
                      #fullscreen=True,    # True, False
                      fade=True,
                      ),

            ], className="card_container big three columns",
          ),

          html.Div([
              dbc.Button(id="text4",className = 'card_size'
                      ),
              dbc.Modal([

                         dbc.ModalBody(id='data4'),
                         dbc.ModalFooter(dbc.Button("Close", id="close4",style={'background-color':'#ced4da'}),),],
                       id="modal4",
                       centered=True,
                       is_open=False,
                       size="xl",        # "sm", "lg", "xl"
                       backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                       scrollable=True,  # False or True if modal has a lot of text
                       #fullscreen=True,    # True, False
                       fade=True,
                       ),

              ], className="card_container big three columns")

      ], className="row flex-display"),




    html.Div([
        html.Div([
## Pie chart container
                    dcc.Graph(id='pie_chart',
                            config={'displayModeBar': 'hover'}),

        ], className="create_container four columns", id="cross-filter-options"),
## map container
        html.Div([
                        dcc.Graph(id="map")], className="create_container nine columns"),

                        ], className="row flex-display"),

### download button
     html.Div([html.Div([
                         html.Button("Download Excel", id="btn_xlsx",style={'background-color':'#1f2c56','color':'white'}),
                         dcc.Download(id="download-dataframe-xlsx"),], className = "create_container2 two columns",),], className="row flex-display"),


                ], id="mainContainer",style={"display": "flex", "flex-direction": "column"}
                )

############################################################################# Assignment #################################################################################
###########INFO

@app.callback(Output('info', 'children'),
              [Input('tools', 'value')],)


def update_info(tools):

    info=df[df['ACCOUNTING TOOL']==tools][["ACCOUNTING TOOL","ERP","FINTECH"]]
    info.ERP = info.ERP.str.lstrip("SAP")


    def join_and(items):
        if len(items)==0:
            return ''
        if len(items)==1:
            return items[0]
        return ', '.join(items[:-1]) + ' and '+items[-1]

    ### ERP UNIQUE
    ERP=list(info["ERP"].unique())
    ERP=join_and(ERP)


    ### Respo UNIQUE
    RESPO=list(info["FINTECH"].unique())
    RESPO=join_and(RESPO)


    def text(x,y):
       text = ["FinTech team is accountable to ",x," for ",tools," in ",y,"."]
       return text

    return [html.H6(children=text(RESPO,ERP),
                    style = {'color': ' #1f2c56','fontSize': 15,},),]








#########   TEXT 1

@app.callback(Output('text1', 'children'),
              [Input('tools', 'value')])

def update_text1(tools):
    scn=df[df['ACCOUNTING TOOL']==tools]['SCANNING SOLUTION'].unique()
    if len(scn)==1:
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
       return [html.H6(children='Used for ',
                    style = {'textAlign':'center',
                             'color': 'white',},),
               html.P(len(scn),
                      style = {'textAlign':'center',
                               'color': 'orange',
                               'fontSize': 40,},),
               html.P('Scanning Solution',
                       style = {'textAlign':'center',
                                'color': 'orange',
                                'fontSize': 20,},),]


@app.callback(
    Output("data1", "children"),
    [Input("tools", "value"),],)


def data1(tools):
    dff1=df[df['ACCOUNTING TOOL']==tools][['ACCOUNTING TOOL','SCANNING SOLUTION','ERP','COMPANY CODE','COUNTRY','ENTITY NAME']]

    return [dbc.Table.from_dataframe(dff1, striped=True, bordered=True, hover=True)]


@app.callback(
    Output("modal1", "is_open"),
    [Input("text1", "n_clicks"),
    Input("close1", "n_clicks"),],
    [State("modal1", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


########## TEXT 2

@app.callback(Output('text2', 'children'),
              [Input('tools', 'value')])

def update_text2(tools):
    Countries=df[df['ACCOUNTING TOOL']==tools]['COUNTRY'].unique()

    return [html.H6(children='Implemented in ',
                    style = {'textAlign':'center',
                             'color': 'white',},),
            html.P(len(Countries) ,
                   style = {'textAlign':'center',
                            'color': '#dd1e35',
                            'fontSize': 40,},),
            html.P(' Countries',
                   style = {'textAlign':'center',
                             'color': '#dd1e35',
                             'fontSize': 20,},),]

@app.callback(
    Output("data2", "children"),
    [Input("tools", "value"),],)


def data2(tools):
    names=df[df['ACCOUNTING TOOL']==tools]['SCANNING SOLUTION'].unique()
    int=len(names)
    tabs = []
    for num in range(int):
        tabs.append(dbc.Tab(
                            label=names[num],
                            tab_id=f"tab_{num + 1}"))

    return[dbc.Container([
                          html.H1("Scanning Tools implemented for " + tools),
                          html.Hr(),
                          dbc.Tabs(children=tabs,
                                   id="tabs2",
                                   active_tab="tab_1",),
                          html.Div(id="tab-content2", className="p-4"),])]


@app.callback(
    Output("tab-content2", "children"),
    [Input("tabs2", "active_tab"), ],
    [Input("tools", "value"),])

def render_tab_content(active_tab,tools):
    dff1=df[df['ACCOUNTING TOOL']==tools][['SCANNING SOLUTION','COUNTRY']]
    names=dff1['SCANNING SOLUTION'].unique()


    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab  is not None:
        if active_tab == "tab_1":
            dff1_cn_tab1=dff1[dff1['SCANNING SOLUTION']==names[0]][['SCANNING SOLUTION','COUNTRY']]
            scn_data_tab1=pd.pivot_table(dff1_cn_tab1,values=('COUNTRY'),index=['SCANNING SOLUTION','COUNTRY'],aggfunc='count')
            scn_data_tab1=scn_data_tab1.reset_index()
            scn_cn_tab1=dff1_cn_tab1['COUNTRY'].unique()
            return [ dbc.Container([dbc.Card(dbc.CardBody([html.H6(children='Implemented in ',
                                                    style = {'textAlign':'center','color': 'black',},),
                                            html.P(len(scn_cn_tab1) ,
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 40,},),
                                            html.P('Countries',
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 20,})]),style={"width":"35rem","float":'center'}),
                                    html.Hr(),
                                    dbc.Table.from_dataframe(scn_data_tab1, striped=True, bordered=True, hover=True)])]

        elif active_tab == "tab_2":
            dff1_cn_tab2=dff1[dff1['SCANNING SOLUTION']==names[0]][['SCANNING SOLUTION','COUNTRY']]
            scn_data_tab2=pd.pivot_table(dff1_cn_tab2,values=('COUNTRY'),index=['SCANNING SOLUTION','COUNTRY'],aggfunc='count')
            scn_data_tab2=scn_data_tab2.reset_index()
            scn_cn_tab2=dff1_cn_tab2['COUNTRY'].unique()
            return [ dbc.Container([dbc.Card(dbc.CardBody([html.H6(children='Implemented in ',
                                                    style = {'textAlign':'center','color': 'black',},),
                                            html.P(len(scn_cn_tab2) ,
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 40,},),
                                            html.P('Countries',
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 20,})]),style={"width":"35rem","float":'center'}),
                                    html.Hr(),
                                    dbc.Table.from_dataframe(scn_data_tab2, striped=True, bordered=True, hover=True)])]
        elif active_tab == "tab_3":
            dff1_cn_tab3=dff1[dff1['SCANNING SOLUTION']==names[0]][['SCANNING SOLUTION','COUNTRY']]
            scn_data_tab3=pd.pivot_table(dff1_cn_tab3,values=('COUNTRY'),index=['SCANNING SOLUTION','COUNTRY'],aggfunc='count')
            scn_data_tab3=scn_data_tab3.reset_index()
            scn_cn_tab3=dff1_cn_tab3['COUNTRY'].unique()
            return [ dbc.Container([dbc.Card(dbc.CardBody([html.H6(children='Implemented in ',
                                                    style = {'textAlign':'center','color': 'black',},),
                                            html.P(len(scn_cn_tab3) ,
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 40,},),
                                            html.P('Countries',
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 20,})]),style={"width":"35rem","float":'center'}),
                                    html.Hr(),
                                    dbc.Table.from_dataframe(scn_data_tab3, striped=True, bordered=True, hover=True)])]
    return "No Scanning Solution"



@app.callback(
    Output("modal2", "is_open"),
    [Input("text2", "n_clicks"),
    Input("close2", "n_clicks"),],
    [State("modal2", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open




###########@ TEXT 3

@app.callback(Output('text3', 'children'),
              [Input('tools', 'value')],)

def update_text3(tools):

    BUs=df[df['ACCOUNTING TOOL']==tools]['ERP'].unique()

    return [html.H6(children='Implemented in ',
                    style = {'textAlign':'center',
                            'color': 'white',},),
            html.P(len(BUs) ,
                    style = {'textAlign':'center',
                             'color': '#09F3F0',
                             'fontSize': 40,},),
            html.P('BU / ERP',
                   style = {'textAlign':'center',
                            'color': '#09F3F0',
                            'fontSize': 20,},),]

@app.callback(
    Output("data3", "children"),
    [Input("tools", "value"),],)


def scn_data_tab3(tools):
    names=df[df['ACCOUNTING TOOL']==tools]['SCANNING SOLUTION'].unique()
    int=len(names)
    tabs = []
    for num in range(int):
        tabs.append(dbc.Tab(
                            label=names[num],
                            tab_id=f"tab_{num + 1}"))

    return[dbc.Container([
                          html.H1("Scanning Tools implemented for " + tools),
                          html.Hr(),
                          dbc.Tabs(children=tabs,
                                   id="tabs3",
                                   active_tab="tab_1",),
                          html.Div(id="tab-content3", className="p-4"),])]


@app.callback(
    Output("tab-content3", "children"),
    [Input("tabs3", "active_tab"), ],
    [Input("tools", "value"),])

def render_tab_content(active_tab,tools):
    dff1=df[df['ACCOUNTING TOOL']==tools][['SCANNING SOLUTION','ERP']]
    names=dff1['SCANNING SOLUTION'].unique()


    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab  is not None:
        if active_tab == "tab_1":
            scn_data_tab1=dff1[dff1['SCANNING SOLUTION']==names[0]][['SCANNING SOLUTION','ERP']]
            scn_erp_tab1=scn_data_tab1['ERP'].unique()
            return [ dbc.Container([dbc.Card(dbc.CardBody([html.H6(children='Implemented in ',
                                                    style = {'textAlign':'center','color': 'black',},),
                                            html.P(len(scn_erp_tab1) ,
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 40,},),
                                            html.P('BU / ERP',
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 20,})]),style={"width":"35rem","float":'center'}),
                                    html.Hr(),
                                    dbc.Table.from_dataframe(scn_data_tab1, striped=True, bordered=True, hover=True)])]

        elif active_tab == "tab_2":
            scn_data_tab2=dff1[dff1['SCANNING SOLUTION']==names[1]][['SCANNING SOLUTION','ERP']]
            scn_erp_tab2=scn_data_tab2['ERP'].unique()
            return [ dbc.Container([dbc.Card(dbc.CardBody([html.H6(children='Implemented in ',
                                                    style = {'textAlign':'center','color': 'black',},),
                                            html.P(len(scn_erp_tab2) ,
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 40,},),
                                            html.P('BU / ERP',
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 20,})]),style={"width":"35rem","float":'center'}),
                                    html.Hr(),
                                    dbc.Table.from_dataframe(scn_data_tab2, striped=True, bordered=True, hover=True)])]
        elif active_tab == "tab_3":
            scn_data_tab3=dff1[dff1['SCANNING SOLUTION']==names[2]][['SCANNING SOLUTION','ERP']]
            scn_erp_tab3=scn_data_tab3['ERP'].unique()
            return [ dbc.Container([dbc.Card(dbc.CardBody([html.H6(children='Implemented in ',
                                                    style = {'textAlign':'center','color': 'black',},),
                                            html.P(len(scn_erp_tab3) ,
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 40,},),
                                            html.P('BU / ERP',
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 20,})]),style={"width":"35rem","float":'center'}),
                                    html.Hr(),
                                    dbc.Table.from_dataframe(scn_data_tab3, striped=True, bordered=True, hover=True)])]
    return "No Scanning Solution"



@app.callback(
    Output("modal3", "is_open"),
    [Input("text3", "n_clicks"), Input("close3", "n_clicks")],
    [State("modal3", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


############### TEXT 4

@app.callback(Output('text4', 'children'),
              [Input('tools', 'value')],)


def update_text4(tools):

    Entities=df[df['ACCOUNTING TOOL']==tools]['COMPANY CODE'].unique()

    return [html.H6(children='Implemented in ',
                    style = {'textAlign':'center',
                             'color': 'white',},),
            html.P(len(Entities) ,
                    style = {'textAlign':'center',
                             'color': '#e55467',
                             'fontSize': 40,},),
            html.P(' Entities',
                   style = {'textAlign':'center',
                            'color': '#e55467',
                            'fontSize': 20,},),]


@app.callback(
    Output("data4", "children"),
    [Input("tools", "value"),],)


def data4(tools):
    names=df[df['ACCOUNTING TOOL']==tools]['SCANNING SOLUTION'].unique()
    int=len(names)
    tabs = []
    for num in range(int):
        tabs.append(dbc.Tab(
                            label=names[num],
                            tab_id=f"tab_{num + 1}"))

    return[dbc.Container([
                          html.H1("Scanning Tools implemented for " + tools),
                          html.Hr(),
                          dbc.Button("Regenerate graphs",color="blue",id="button4",className="mb-3",),
                          html.Hr(),
                          dbc.Tabs(children=tabs,
                                   id="tabs4",
                                   active_tab="tab_1",),
                          html.Div(id="tab-content4", className="p-4"),])]


@app.callback(
    Output("tab-content4", "children"),
    [Input("tabs4", "active_tab"), ],
    [Input("tools", "value"),])

def render_tab_content(active_tab,tools):
    dff1=df[df['ACCOUNTING TOOL']==tools][['SCANNING SOLUTION','COMPANY CODE','ENTITY NAME']]
    names=dff1['SCANNING SOLUTION'].unique()


    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab  is not None:
        if active_tab == "tab_1":
            scn_data_tab1=dff1[dff1['SCANNING SOLUTION']==names[0]][['SCANNING SOLUTION','COMPANY CODE','ENTITY NAME']]
            scn_en_tab1=scn_data_tab1['COMPANY CODE'].unique()
            return [ dbc.Container([dbc.Card(dbc.CardBody([html.H6(children='Implemented in ',
                                                    style = {'textAlign':'center','color': 'black',},),
                                            html.P(len(scn_en_tab1) ,
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 40,},),
                                            html.P('BU / ERP',
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 20,})]),style={"width":"35rem","float":'center'}),
                                    html.Hr(),
                                    dbc.Table.from_dataframe(scn_data_tab1, striped=True, bordered=True, hover=True)])]

        elif active_tab == "tab_2":
            scn_data_tab2=dff1[dff1['SCANNING SOLUTION']==names[1]][['SCANNING SOLUTION','COMPANY CODE','ENTITY NAME']]
            scn_en_tab2=scn_data_tab2['COMPANY CODE'].unique()
            return [ dbc.Container([dbc.Card(dbc.CardBody([html.H6(children='Implemented in ',
                                                    style = {'textAlign':'center','color': 'black',},),
                                            html.P(len(scn_en_tab2) ,
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 40,},),
                                            html.P('BU / ERP',
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 20,})]),style={"width":"35rem","float":'center'}),
                                    html.Hr(),
                                    dbc.Table.from_dataframe(scn_data_tab2, striped=True, bordered=True, hover=True)])]
        elif active_tab == "tab_3":
            scn_data_tab3=dff1[dff1['SCANNING SOLUTION']==names[2]][['SCANNING SOLUTION','COMPANY CODE','ENTITY NAME']]
            scn_en_tab3=scn_data_tab3['COMPANY CODE'].unique()
            return [ dbc.Container([dbc.Card(dbc.CardBody([html.H6(children='Implemented in ',
                                                    style = {'textAlign':'center','color': 'black',},),
                                            html.P(len(scn_en_tab3) ,
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 40,},),
                                            html.P('BU / ERP',
                                                    style = {'textAlign':'center','color': '#09F3F0','fontSize': 20,})]),style={"width":"35rem","float":'center'}),
                                    html.Hr(),
                                    dbc.Table.from_dataframe(scn_data_tab3, striped=True, bordered=True, hover=True)])]
    return "No Scanning Solution"




@app.callback(
    Output("modal4", "is_open"),
    [Input("text4", "n_clicks"), Input("close4", "n_clicks")],
    [State("modal4", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

########### Create pie chart :

@app.callback(Output('pie_chart', 'figure'),
              [Input('tools', 'value')])

def update_graph(tools):

    labels=list(Counter(df["ACCOUNTING TOOL"]).keys()) # equals to list(set(words))
    values=list(Counter(df["ACCOUNTING TOOL"]).values()) # counts the elements' frequency
    colors = ['#09F3F0',  '#e55467','orange','#dd1e35']
    pull=[]
    for tool in labels:
        if tool==tools:
            pull.append(0.2)
        else:
            pull.append(0)

    return {
        'data': [go.Pie(labels=labels,
                        values=values,
                        pull=pull,
                        marker=dict(colors=colors),
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
                'text': 'Scanning Solution for  ' + '<br>' + (tools),


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
                family="AmstelvarAlpha",
                size=12,
                color='white')
            ),


        }



################@ CREATE MAP

@app.callback(
    Output("map", "figure"),
    Input("tools", "value"),)

def updateGraphCB(tools):
    map_data=df[df['ACCOUNTING TOOL']==tools][["ACCOUNTING TOOL","SCANNING SOLUTION","ERP","LAT","LNG","COMPANY CODE","ENTITY NAME","COUNTRY","FINTECH"]]

    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(lon=map_data ['LNG'],
                                   lat=map_data ['LAT'],
                                   name=  tools ,
                                   mode='markers',
                                   marker=dict(size=15),
                                   meta=tools,
                                   hoverinfo='text',
                                   hovertext=
                                    '<b>Country</b>: ' + map_data['COUNTRY'].astype(str) + '<br>' +
                                    '<b>Tool</b>: ' +tools+'<br>' +
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


############################# download excel

@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,)
def func(n_clicks):
    df=df[["ACCOUNTING TOOL","SCANNING SOLUTION","ERP","COMPANY CODE","ENTITY NAME","COUNTRY","FINTECH"]]
    return dcc.send_data_frame(df.to_excel, "MDM_DATA.xlsx", sheet_name="Customer - Vendor",index=False)




if __name__ == '__main__':
    app.run_server(debug=True)

