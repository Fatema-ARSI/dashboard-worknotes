import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from jupyter_dash import JupyterDash


###############################    DATA    #####################################

df1=pd.read_excel('Vendor_ALL.xlsx')
df2=pd.read_excel('Customer_ALL.xlsx')


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
                                    '<b>Tool</b>: ' + df_ven['MDM SOLUTION'].astype(str) + '<br>' +
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
                                     '<b>Tool</b>: ' + df_cus['MDM SOLUTION'].astype(str) + '<br>' +
                                     '<b>BU</b>: ' +  df_cus['BU'].astype(str) + '<br>' +
                                     '<b>Company Code</b>: ' + df_cus['COMPANY CODE'].astype(str) ))
    

    fig.layout.plot_bgcolor = '#010028'
    fig.layout.paper_bgcolor = '#010028'
    
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
################################  FRAME CONTAINERS    #######################################

font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
meta_tags = [{"name": "viewport", "content": "width=device-width"}]
external_stylesheets = [meta_tags, font_awesome]

app = JupyterDash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div([
    html.Div([
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
                html.H3("MDM SCOPE AROUND SAINT-GOBAIN", style={"margin-bottom": "0px", 'color': 'white'}),
                html.H5("Track MDM Implementation", style={"margin-top": "0px", 'color': 'white'}),
            ])
        ], className="one-half column", id="title"),

        html.Div([
            html.H6('Data Last Updated: June 18, 2022' ,
                    style={'color': 'orange'}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            html.P('Select Tool', className = 'fix_label', style = {'color': 'white', 'margin-top': '2px'}),
            dcc.Dropdown(id='tools',
                         multi=False,
                         clearable=True,
                         value='MDM_V2',
                         placeholder='Please select your tool',
                         options=['MDM_V2','Jagger','Promenta','TIBCO'], className='dcc_compon'),
            dcc.Checklist(id='data',
                          value='Vendor',
                          options=['Vendor','Customer'],
                          style={'color': 'white','font-size':20},
                          inline=True,
                          className='fix_label'),


            ], className = "create_container1 four columns", style = {'margin-bottom': '0px'}),
        ], className = "row flex-display"),
  


    html.Div([html.Div([
        html.Div(id= "text1",className = 'card_size'
                ),



        ], className="card_container big three columns",),

          html.Div([
              html.Div(id="text2",className = 'card_size'
                      ),

            ], className="card_container big three columns",
          ),

          html.Div([
              html.Div(id="text3",className = 'card_size'
                      ),

            ], className="card_container big three columns",
          ),

          html.Div([
              html.Div(id="text4",className = 'card_size'
                      ),

              ], className="card_container big three columns")

      ], className="row flex-display"),




    html.Div([
        html.Div([

                    dcc.Graph(id='pie_chart',
                            config={'displayModeBar': 'hover'}),

        ], className="create_container four columns", id="cross-filter-options"),

        html.Div([
                        dcc.Graph(id="map",figure=fig)], className="create_container nine columns"),

                        ], className="row flex-display"),

                ], id="mainContainer",
                style={"display": "flex", "flex-direction": "column"})

################################### Assignment ###########################


@app.callback(Output('text1', 'children'),
              [Input('tools', 'value')])

def update_text1(tools):


    return [
            html.H6(children='Selected MDM Tool',
                   style = {'textAlign':'center',
                            'color': 'white',

                   },

                   ),
             html.P(tools ,
                       style = {'textAlign':'center',
                               'color': 'orange',
                                'fontSize': 40,
                                },
                       ),

                       ]








@app.callback(Output('text2', 'children'),
              [Input('tools', 'value')])

def update_text2(tools):
    c_ven=df1[df1['MDM SOLUTION']==tools]['COUNTRY'].unique()
    c_cus=df2[df2['MDM SOLUTION']==tools]['COUNTRY'].unique()
    Countries=len(c_ven)+len(c_cus)



    return [
            html.H6(children='Implemented in ',
                   style = {'textAlign':'center',
                            'color': 'white',

                   },

                   ),
             html.P(Countries ,
                       style = {'textAlign':'center',
                               'color': '#dd1e35',
                                'fontSize': 40,
                                },
                       ),
             html.P(' Countries',
                   style = {'textAlign':'center',
                            'color': '#dd1e35',
                            'fontSize': 20,

                   },

                   ),
                       ]


@app.callback(Output('text3', 'children'),
              [Input('tools', 'value')])

def update_text3(tools):
    b_ven=df1[df1['MDM SOLUTION']==tools]['BU'].unique()
    b_cus=df2[df2['MDM SOLUTION']==tools]['BU'].unique()
    BUs=len(b_ven)+len(b_cus)



    return [
            html.H6(children='Total ',
                   style = {'textAlign':'center',
                            'color': 'white',

                   },

                   ),
             html.P(BUs ,
                       style = {'textAlign':'center',
                               'color': '#09F3F0',
                                'fontSize': 40,
                                },
                       ),
             html.P('BUs',
                   style = {'textAlign':'center',
                            'color': '#09F3F0',
                            'fontSize': 20,

                   },

                   ),
                       ]

@app.callback(Output('text4', 'children'),
              [Input('tools', 'value')])

def update_text4(tools):
    e_ven=df1[df1['MDM SOLUTION']==tools]['COMPANY CODE'].unique()
    e_cus=df2[df2['MDM SOLUTION']==tools]['COMPANY CODE'].unique()
    Entities=len(e_ven)+len(e_cus)



    return [
            html.H6(children='Implemented in ',
                   style = {'textAlign':'center',
                            'color': 'white',

                   },

                   ),
             html.P(Entities ,
                       style = {'textAlign':'center',
                               'color': '#e55467',
                                'fontSize': 40,
                                },
                       ),
             html.P('Entities',
                   style = {'textAlign':'center',
                            'color': '#e55467',
                            'fontSize': 20,

                   },

                   ),
                       ]

# Create pie chart :
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

app.run_server()
if __name__ == '__main__':
    app.run_server(debug=False)
