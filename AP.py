import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
import time


###############################    EXTRACT DATA    #####################################

df1=pd.read_excel('Vendor_ALL.xlsx')
df2=pd.read_excel('Customer_ALL.xlsx')

#####################################

def interactive_multi_plot(vendor,customer, addAll = True):
    fig = go.Figure()

    gd_ven = vendor.groupby(['MDM SOLUTION'])
    group_name_d_ven = list(set(vendor['MDM SOLUTION']))

    for grx in group_name_d_ven:
      df_ven = gd_ven.get_group(grx)

      fig.add_trace(go.Scattermapbox(lon=df_ven ['LNG'],
                                    lat=df_ven ['LAT'],
                                    name=  grx +" "+ "Vendor",
                                    mode='markers',
                                    marker=dict(size=8,color="orange"),
                                    meta=grx,
                                    hoverinfo='text',
                                    hovertext=
                                    '<b>Country</b>: ' + df_ven['COUNTRY'].astype(str) + '<br>' +
                                    '<b>Tool</b>: ' +grx+' '+ df_ven['DATA'].astype(str) + '<br>' +
                                    '<b>BU</b>: ' +  df_ven['BU'].astype(str) + '<br>' +
                                    '<b>Company Code</b>: ' + df_ven['COMPANY CODE'].astype(str) ))

    gd_cus = customer.groupby(['MDM SOLUTION'])
    group_name_d_cus = list(set(customer['MDM SOLUTION']))

    for grx in group_name_d_cus:
      df_cus = gd_cus.get_group(grx)
      fig.add_trace(go.Scattermapbox(lon=df_cus ['LNG'],
                                     lat=df_cus ['LAT'],
                                     name=  grx +" "+ "Customer",
                                     mode='markers',
                                     marker=dict(size=8,color="blue"),
                                     meta=grx,
                                     hoverinfo='text',
                                     hovertext=
                                     '<b>Country</b>: ' + df_cus['COUNTRY'].astype(str) + '<br>' +
                                     '<b>Tool</b>: ' +grx+' '+ df_cus['DATA'].astype(str) + '<br>' +
                                     '<b>BU</b>: ' +  df_cus['BU'].astype(str) + '<br>' +
                                     '<b>Company Code</b>: ' + df_cus['COMPANY CODE'].astype(str) ))


    fig.layout.plot_bgcolor = '#1f2c56'
    fig.layout.paper_bgcolor = '#1f2c56'

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      width=900,
                      height=550,
                      hovermode='closest',
                      mapbox=dict(accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
                                  style='open-street-map',),
                      legend=dict(itemclick= 'toggleothers',
                                  # when you are clicking an item in legend all that are not in the same group are hidden
                                  orientation="v",
                                  x=1.05,
                                  y=0.8,
                                  font=dict(color='#fff', size=12),
                                  title='Master Data'))


    return fig

fig = interactive_multi_plot(df1, df2)
################################  FRAME CONTAINERS (layout of the dashboard    #######################################

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
                         "margin-bottom": "25px",
                     },
                     )
        ],
            className="one-third column",
        ),
        html.Div([
            html.Div([
                html.H4("AP SOLUTIONS AROUND SAINT-GOBAIN", style={"margin-bottom": "0px", 'color': 'white'}),
                html.H6("Track AP Tool Implementation", style={"margin-top": "0px", 'color': 'white'}),
            ])
        ], className="one-half column", id="title"),

        html.Div([
            html.H6('Data Last Updated: July 11, 2022' ,
                    style={'color': 'orange'}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display1", style={"margin-bottom": "25px"}),
## filter container
    html.Div([
        html.Div([
            html.P('Select Tool', className = 'fix_label', style = {'color': 'white', 'margin-top': '2px'}),
            dcc.Dropdown(id='tools',
                         multi=False,
                         clearable=True,
                         value='MDM_V2',
                         placeholder='Please select your tool',
                         options=['MDM_V2','Jagger','Promenta'], className='dcc_compon'),
            dcc.RadioItems(id='data',
                          value='Both',
                          options=['Both','Vendor','Customer'],
                          style={'color': 'white','font-size':20,},
                          inputStyle={"margin-left": "20px"},
                          inline=True,
                          className='fix_label'),


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
              dbc.Modal([dbc.ModalBody(id='data2'),
                         dbc.ModalFooter(dbc.Button("Close", id="close2",style={'background-color':'#ced4da'}),),],
                       id="modal2",
                       centered=True,
                       is_open=False,
                       size="xl",        # "sm", "lg", "xl"
                       backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                       scrollable=False,  # False or True if modal has a lot of text
                       #fullscreen=True,    # True, False
                       fade=True,
                       ),  ]       # True, False


            , className="card_container big three columns",),

          html.Div([
              dbc.Button(id="text3",className = 'card_size'
                      ),
             dbc.Modal([

                        dbc.ModalBody(dbc.Container([
                   dcc.Store(id="store"),
                   html.H1("Dynamically rendered tab content"),
                   html.Hr(),
                   dbc.Button(
                              "Regenerate graphs",
                              color="blue",
                              id="button",
                              className="mb-3",),
                   dbc.Tabs([
                dbc.Tab(label="Scatter", tab_id="scatter"),
                dbc.Tab(label="Histograms", tab_id="histogram"),
            ],
            id="tabs",
            active_tab="scatter",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)),
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
                        dcc.Graph(id="map",figure=fig)], className="create_container nine columns"),

                        ], className="row flex-display"),

### download button
     html.Div([html.Div([
                         html.Button("Download Excel", id="btn_xlsx",style={'background-color':'#1f2c56','color':'white'}),
                         dcc.Download(id="download-dataframe-xlsx"),],
                        className = "create_container2 two columns",),], className="row flex-display"),


                ], id="mainContainer",style={"display": "flex", "flex-direction": "column"}
                )

################################### Assignment ###########################

###########INFO

@app.callback(Output('info', 'children'),
              [Input('data', 'value')],)


def update_info(data):
    if data=='Vendor':
        return [
            html.H6(children='Vendor - DATA TO INPUT',
                    style = {'color': 'black','fontSize': 15,},),]

    elif data=='Customer':
        return [
            html.H6(children='Customer  - DATA TO INPUT',
                    style = {'color': 'black','fontSize': 15,},),]
    else:
        return [
            html.H6(children='Both  - DATA TO INPUT',
                    style = {'color': 'black','fontSize': 15,},),]


#########   TEXT 1

@app.callback(Output('text1', 'children'),
              [Input('tools', 'value')],
              [Input('data', 'value')])

def update_text1(tools,data):
    if data=='Vendor':
        return [html.H6(children='Data for',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(tools ,
                       style = {'textAlign':'center',
                               'color': 'orange',
                                'fontSize': 40,},),
               html.P('Vendor',
                      style = {'textAlign':'center',
                               'color': 'orange',
                               'fontSize': 20,},),]
    elif data=='Customer':
        return [html.H6(children='Data for',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(tools ,
                       style = {'textAlign':'center',
                               'color': 'orange',
                                'fontSize': 40,},),
               html.P('Customer',
                      style = {'textAlign':'center',
                               'color': 'orange',
                               'fontSize': 20,},),]
    else:
        return [html.H6(children='Data for',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(tools ,
                       style = {'textAlign':'center',
                               'color': 'orange',
                                'fontSize': 40,},),]




@app.callback(
    Output("data1", "children"),
    [Input("tools", "value"),],
    [Input("data", "value"),],)


def data1(tools,data):
    dff1=df1[df1['MDM SOLUTION']==tools][['MDM SOLUTION','ERP','BU','COMPANY CODE','COUNTRY','ENTITY NAME','DATA']]
    dff2=df2[df2['MDM SOLUTION']==tools][['MDM SOLUTION','ERP','BU','COMPANY CODE','COUNTRY','ENTITY NAME','DATA']]
    dff3=dff1.append(dff2)

    if data=='Vendor':
        return [dbc.Table.from_dataframe(dff1, striped=True, bordered=True, hover=True)]
    elif data=='Customer':
        return [dbc.Table.from_dataframe(dff2, striped=True, bordered=True, hover=True)]
    else:
        return [dbc.Table.from_dataframe(dff3, striped=True, bordered=True, hover=True)]


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
              [Input('tools', 'value')],
              [Input('data', 'value')])

def update_text2(tools,data):
    c_ven=df1[df1['MDM SOLUTION']==tools]['COUNTRY'].unique()
    c_cus=df2[df2['MDM SOLUTION']==tools]['COUNTRY'].unique()
    Countries=len(c_ven)+len(c_cus)

    if data=='Vendor':
        return [html.H6(children='Implemented in ',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(len(c_ven),
                        style = {'textAlign':'center',
                                 'color': '#09F3F0',
                                 'fontSize': 40,},),
               html.P(' Countries',
                      style = {'textAlign':'center',
                               'color': '#09F3F0',
                               'fontSize': 20,},),]
    elif data=='Customer':
        return [html.H6(children='Implemented in ',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(len(c_cus) ,
                        style = {'textAlign':'center',
                                 'color': '#09F3F0',
                                 'fontSize': 40,},),
               html.P(' Countries',
                      style = {'textAlign':'center',
                               'color': '#09F3F0',
                               'fontSize': 20,},),]
    else:
        return [html.H6(children='Implemented in ',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(Countries ,
                        style = {'textAlign':'center',
                                 'color': '#09F3F0',
                                 'fontSize': 40,},),
               html.P(' Countries',
                      style = {'textAlign':'center',
                               'color': '#09F3F0',
                               'fontSize': 20,},),]

@app.callback(
    Output("data2", "children"),
    [Input("data", "value"),],)

def data2(data):
    if data=='Both':
        return[dbc.Card([dbc.CardHeader(dbc.Tabs([
                                                 dbc.Tab(label="Both", tab_id="tab-1"),
                                                 dbc.Tab(label="Vendor", tab_id="tab-2"),],
                                                 id="card-tabs",
                                                 active_tab="tab-1",)),
                        dbc.CardBody(html.P(id="card-content", className="card-text")),]),]
    elif data=='Vendor':
        return[dbc.Card([dbc.CardHeader(dbc.Tabs([
                                                 dbc.Tab(label="Vendor", tab_id="tab-1"),
                                                 dbc.Tab(label="Customer", tab_id="tab-2"),],
                                                 id="card-tabs",
                                                 active_tab="tab-1",)),
                        dbc.CardBody(html.P(id="card-content", className="card-text")),]),]
    else:
        return[dbc.Card([dbc.CardHeader(dbc.Tabs([
                                                 dbc.Tab(label="Customer", tab_id="tab-1"),
                                                 dbc.Tab(label="Both", tab_id="tab-2"),],
                                                 id="card-tabs",
                                                 active_tab="tab-1",)),
                        dbc.CardBody(html.P(id="card-content", className="card-text")),]),]


@app.callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    return "This is tab {}".format(active_tab)


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
              [Input('tools', 'value')],
              [Input('data', 'value')])

def update_text3(tools,data):
    b_ven=df1[df1['MDM SOLUTION']==tools]['BU'].unique()
    b_cus=df2[df2['MDM SOLUTION']==tools]['BU'].unique()
    BUs=len(b_ven)+len(b_cus)



    if data=='Vendor':
        return [html.H6(children='Implemented in ',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(len(b_ven),
                        style = {'textAlign':'center',
                                 'color': '#dd1e35',
                                 'fontSize': 40,},),
               html.P('BU / ERP',
                      style = {'textAlign':'center',
                               'color': '#dd1e35',
                               'fontSize': 20,},),]
    elif data=='Customer':
        return [html.H6(children='Implemented in ',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(len(b_cus) ,
                        style = {'textAlign':'center',
                                 'color': '#dd1e35',
                                 'fontSize': 40,},),
               html.P('BU / ERP',
                      style = {'textAlign':'center',
                               'color': '#dd1e35',
                               'fontSize': 20,},),]
    else:
        return [html.H6(children='Implemented in ',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(BUs ,
                        style = {'textAlign':'center',
                                 'color': '#dd1e35',
                                 'fontSize': 40,},),
               html.P('BU / ERP',
                      style = {'textAlign':'center',
                               'color': '#dd1e35',
                               'fontSize': 20,},),]

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab and data is not None:
        if active_tab == "scatter":
            return dcc.Graph(figure=data["scatter"])
        elif active_tab == "histogram":
            return dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
                    dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
                ]
            )
    return "No tab selected"


@app.callback(Output("store", "data"), [Input("button", "n_clicks")])
def generate_graphs(n):
    """
    This callback generates three simple graphs from random data.
    """
    if not n:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["scatter", "hist_1", "hist_2"]}

    # simulate expensive graph generation process
    time.sleep(2)

    # generate 100 multivariate normal samples
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    scatter = go.Figure(
        data=[go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers")]
    )
    hist_1 = go.Figure(data=[go.Histogram(x=data[:, 0])])
    hist_2 = go.Figure(data=[go.Histogram(x=data[:, 1])])

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}

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
              [Input('tools', 'value')],
              [Input('data', 'value')])




def update_text4(tools,data):
    e_ven=df1[df1['MDM SOLUTION']==tools]['COMPANY CODE'].unique()
    e_cus=df2[df2['MDM SOLUTION']==tools]['COMPANY CODE'].unique()
    Entities=len(e_ven)+len(e_cus)



    if data=='Vendor':
        return [html.H6(children='Implemented in ',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(len(e_ven),
                        style = {'textAlign':'center',
                                 'color': '#e55467',
                                 'fontSize': 40,},),
               html.P(' Entities',
                      style = {'textAlign':'center',
                               'color': '#e55467',
                               'fontSize': 20,},),]
    elif data=='Customer':
        return [html.H6(children='Implemented in ',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(len(e_cus) ,
                        style = {'textAlign':'center',
                                 'color': '#e55467',
                                 'fontSize': 40,},),
               html.P(' Entities',
                      style = {'textAlign':'center',
                               'color': '#e55467',
                               'fontSize': 20,},),]
    else:
        return [html.H6(children='Implemented in ',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(Entities ,
                        style = {'textAlign':'center',
                                 'color': '#e55467',
                                 'fontSize': 40,},),
               html.P(' Entities',
                      style = {'textAlign':'center',
                               'color': '#e55467',
                               'fontSize': 20,},),]


@app.callback(
    Output("data4", "children"),
    [Input("tools", "value"),],
    [Input("data", "value"),],)

def data4(tools,data):
    dff1_en=df1[df1['MDM SOLUTION']==tools][['MDM SOLUTION','COMPANY CODE']]
    dff1_en=pd.pivot_table(dff1_en,values=('COMPANY CODE'),index=['MDM SOLUTION','COMPANY CODE'],aggfunc='count')
    dff1_en=dff1_en.reset_index()
    dff2_en=df2[df2['MDM SOLUTION']==tools][['MDM SOLUTION','COMPANY CODE']]
    dff2_en=pd.pivot_table(dff2_en,values=('COMPANY CODE'),index=['MDM SOLUTION','COMPANY CODE'],aggfunc='count')
    dff2_en=dff2_en.reset_index()
    dff3_en=dff1_en.append(dff2_en)
    dff3_en=pd.pivot_table(dff3_en,values=('COMPANY CODE'),index=['MDM SOLUTION','COMPANY CODE'],aggfunc='count')
    dff3_en=dff3_en.reset_index()

    if data=='Vendor':
        return [dbc.Table.from_dataframe(dff1_en, striped=True, bordered=True, hover=True)]
    elif data=='Customer':
        return [dbc.Table.from_dataframe(dff2_en, striped=True, bordered=True, hover=True)]
    else:
        return [dbc.Table.from_dataframe(dff3_en, striped=True, bordered=True, hover=True)]

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
    vendor=df1[df1['MDM SOLUTION']==tools]['DATA'].count()
    customer=df2[df2['MDM SOLUTION']==tools]['DATA'].count()
    colors = ['#09F3F0',  '#e55467']

    return {
        'data': [go.Pie(labels=['Vendor', 'Cutomer'],
                        values=[vendor, customer, ],
                        marker=dict(colors=colors),
                        hoverinfo='label+value+percent',
                        textinfo='label+value',
                        textfont=dict(size=13),
                        hole=.7,
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
                'text': 'Vendor - Customer Implemenation for  ' + '<br>' + (tools),


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
                family="sans-serif",
                size=12,
                color='white')
            ),


        }



################@ CREATE MAP

@app.callback(
    Output("map", "figure"),
    Input("tools", "value"),
    State("map", "figure"),
)
def updateGraphCB(tools, fig):
    # filter traces...
    fig = go.Figure(fig).update_traces(visible=False)
    fig.update_traces(visible=True, selector={"meta":tools})
    return fig

############################# dwnload excel

@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,)
def func(n_clicks):
    df=df1.append(df2)
    df=df[["MDM SOLUTION","ERP","BU","COUNTRY","COMPANY CODE","ENTITY NAME","DATA"]]
    return dcc.send_data_frame(df.to_excel, "MDM_DATA.xlsx", sheet_name="Customer - Vendor",index=False)


if __name__ == '__main__':
    app.run_server(debug=False)
