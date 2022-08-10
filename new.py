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


#####################################################################    EXTRACT DATA    ################################################################################

df=pd.read_excel('AP SCOPE.xlsx')


###############################################################    MAP INPUT to update according the filter    ###############################################

def interactive_multi_plot(data):
    fig = go.Figure()

    gd = data.groupby(['ACCOUNTING TOOL'])
    group_name = list(set(data['ACCOUNTING TOOL']))

    for grx in group_name:
      map_data = gd.get_group(grx)

      fig.add_trace(go.Scattermapbox(lon=map_data ['LNG'],
                                    lat=map_data ['LAT'],
                                    name=  grx ,
                                    mode='markers',
                                    marker=dict(size=15),
                                    meta=grx,
                                    hoverinfo='text',
                                    hovertext=
                                    '<b>Country</b>: ' + map_data['COUNTRY'].astype(str) + '<br>' +
                                    '<b>Tool</b>: ' +grx+'<br>' +
                                    '<b>BU</b>: ' +  map_data['ERP'].astype(str) + '<br>' +
                                    '<b>Company Code</b>: ' + map_data['COMPANY CODE'].astype(str) ))



    fig.layout.plot_bgcolor = '#1f2c56'
    fig.layout.paper_bgcolor = '#1f2c56'

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      width=900,
                      height=550,
                      hovermode='closest',
                      mapbox=dict(accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',),
                      legend=dict(itemclick= 'toggleothers',
                                  # when you are clicking an item in legend all that are not in the same group are hidden
                                  orientation="v",
                                  x=1.05,
                                  y=0.8,
                                  font=dict(color='#fff', size=12,family="AmstelvarAlpha"),
                                  title='Master Data'))


    return fig

fig = interactive_multi_plot(df)

##############################################################  FRAME CONTAINERS (layout of the dashboard    #####################################################

font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css" ##css design
meta_tags = [{"name": "viewport", "content": "width=device-width"}] ##css design

external_stylesheets = [meta_tags, font_awesome]


app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

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
                        dcc.Graph(id="map",figure=fig)], className="create_container nine columns"),

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
    return [html.H6(children='Used for ',
                    style = {'textAlign':'center',
                             'color': 'white',},),
            html.P(len(scn) ,
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
    dff1=df[df['ACCOUNTING TOOL']==tools][['ACCOUNTING TOOL','ERP','COMPANY CODE','COUNTRY','ENTITY NAME']]

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
                            'color': '#09F3F0',
                            'fontSize': 40,},),
            html.P(' Countries',
                   style = {'textAlign':'center',
                             'color': '#09F3F0',
                             'fontSize': 20,},),]

@app.callback(
    Output("data2", "children"),
    [Input("tools", "value"),],)


def data2(tools):

    dff2_cnt=df[df['ACCOUNTING TOOL']==tools][['ACCOUNTING TOOL','COUNTRY']]
    dff2_cnt=pd.pivot_table(dff2_cnt,values=('COUNTRY'),index=['ACCOUNTING TOOL','COUNTRY'],aggfunc='count')
    dff2_cnt=dff2_cnt.reset_index()

    return [dbc.Table.from_dataframe(dff2_cnt, )]


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
                             'color': '#dd1e35',
                             'fontSize': 40,},),
            html.P('BU / ERP',
                   style = {'textAlign':'center',
                            'color': '#dd1e35',
                            'fontSize': 20,},),]

@app.callback(
    Output("data3", "children"),
    [Input("tools", "value"),],)


def data3(tools):

    dff3_bu=df[df['ACCOUNTING TOOL']==tools][['ACCOUNTING TOOL','ERP']]
    dff3_bu=pd.pivot_table(dff3_bu,values=('ERP'),index=['ACCOUNTING TOOL','ERP'],aggfunc='count')
    dff3_bu=dff3_bu.reset_index()

    return [dbc.Table.from_dataframe(dff3_bu, striped=True, bordered=True, hover=True)]





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
    dff_en=df[df['ACCOUNTING TOOL']==tools][['ACCOUNTING TOOL','COMPANY CODE']]
    dff_en=pd.pivot_table(dff_en,values=('COMPANY CODE'),index=['ACCOUNTING TOOL','COMPANY CODE'],aggfunc='count')
    dff_en=dff_en.reset_index()

    return [dbc.Table.from_dataframe(dff_en, striped=True, bordered=True, hover=True)]

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
    pie_data=df[df['ACCOUNTING TOOL']==tools][["SCANNING SOLUTION","ACCOUNTING TOOL"]]

    labels=list(Counter(pie_data["SCANNING SOLUTION"]).keys()) # equals to list(set(words))
    values=list(Counter(pie_data["SCANNING SOLUTION"]).values()) # counts the elements' frequency
    colors = ['#09F3F0',  '#e55467','orange','red']

    return {
        'data': [go.Pie(labels=labels,
                        values=values,
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
    Input("tools", "value"),
    State("map", "figure"),
)
def updateGraphCB(tools, fig):
    # filter traces...
    fig = go.Figure(fig).update_traces(visible=False)
    fig.update_traces(visible=True, selector={"meta":tools})
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
    app.run_server(debug=False)
