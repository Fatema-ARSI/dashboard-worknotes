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

##################################################    LOAD THE DATA    #####################################################################

df=pd.read_excel(r'C:\Users\F8826135\Desktop\ds\Data\MDM_SCOPE.xlsx')
df['COMPANY CODE']=df['COMPANY CODE'].map(str)

df1=df[df['MASTER DATA']=="Vendor"][["MDM SOLUTION","MASTER DATA","ERP","BU","COMPANY CODE","LAT","LNG","COUNTRY","ENTITY NAME","FINTECH"]]
df2=df[df['MASTER DATA']=="Customer"][["MDM SOLUTION","MASTER DATA","ERP","BU","COMPANY CODE","LAT","LNG","COUNTRY","ENTITY NAME","FINTECH"]]
df3=df[df['MASTER DATA']=="Employee"][["MDM SOLUTION","MASTER DATA","ERP","BU","COMPANY CODE","LAT","LNG","COUNTRY","ENTITY NAME","FINTECH"]]


##############################################    MAP INPUT FOR THE MDM SOLUTION TO FILTER   ###############################################


    
def interactive_multi_plot(vendor,customer,employee, color,addAll = True):
    fig = go.Figure()

    gd_ven = vendor.groupby(['MDM SOLUTION'])
    group_name_d_ven = list(set(vendor['MDM SOLUTION']))

    for grx in group_name_d_ven:
      df_ven = gd_ven.get_group(grx)

      fig.add_trace(go.Scattermapbox(lon=df_ven ['LNG'],
                                    lat=df_ven ['LAT'],
                                    name=  grx +" "+ "Vendor",
                                    mode='markers',
                                    marker=dict(size=15,color=color[0]),
                                    meta=grx,
                                    hoverinfo='text',
                                    hovertext=
                                    '<b>Country</b>: ' + df_ven['COUNTRY'].astype(str) + '<br>' +
                                    '<b>Tool</b>: ' +grx + '<br>' +
                                    '<b>Master Data</b>: ' + df_ven['MASTER DATA'].astype(str) + '<br>' +
                                    '<b>BU</b>: ' +  df_ven['ERP'].astype(str) + '<br>' +
                                    '<b>Company Code</b>: ' + df_ven['COMPANY CODE'].astype(str) ))

    gd_cus = customer.groupby(['MDM SOLUTION'])
    group_name_d_cus = list(set(customer['MDM SOLUTION']))

    for grx in group_name_d_cus:
      df_cus = gd_cus.get_group(grx)
      fig.add_trace(go.Scattermapbox(lon=df_cus ['LNG'],
                                     lat=df_cus ['LAT'],
                                     name=  grx +" "+ "Customer",
                                     mode='markers',
                                     marker=dict(size=15,color=color[1]),
                                     meta=grx,
                                     hoverinfo='text',
                                     hovertext=
                                     '<b>Country</b>: ' + df_cus['COUNTRY'].astype(str) + '<br>' +
                                     '<b>Tool</b>: ' +grx + '<br>' +
                                     '<b>Master Data</b>: ' + df_ven['MASTER DATA'].astype(str) + '<br>' +
                                     '<b>BU</b>: ' +  df_cus['ERP'].astype(str) + '<br>' +
                                     '<b>Company Code</b>: ' + df_cus['COMPANY CODE'].astype(str) ))
                                     
    gd_emp = employee.groupby(['MDM SOLUTION'])
    group_name_d_emp = list(set(employee['MDM SOLUTION']))

    for grx in group_name_d_emp:
      df_emp = gd_emp.get_group(grx)
      fig.add_trace(go.Scattermapbox(lon=df_emp ['LNG'],
                                     lat=df_emp ['LAT'],
                                     name=  grx +" "+ "Employee",
                                     mode='markers',
                                     marker=dict(size=15,color=color[2]),
                                     meta=grx,
                                     hoverinfo='text',
                                     hovertext=
                                     '<b>Country</b>: ' + df_emp['COUNTRY'].astype(str) + '<br>' +
                                     '<b>Tool</b>: ' +grx + '<br>' +
                                     '<b>Master Data</b>: ' + df_ven['MASTER DATA'].astype(str) + '<br>' +
                                     '<b>BU</b>: ' +  df_emp['ERP'].astype(str) + '<br>' +
                                     '<b>Company Code</b>: ' + df_emp['COMPANY CODE'].astype(str) ))


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
                                  font=dict(color='#fff', size=12,family="Computer Modern"),
                                  title='Master Data'))


    return fig



######################################################  LAYOUT OF THE DASHBOARD   #########################################################

font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css" ##css design 
meta_tags = [{"name": "viewport", "content": "width=device-width"}] ##css design 

external_stylesheets = [meta_tags, font_awesome]


app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([                                
    html.Div([
################################################# TILTE/HEADER LAYOUT ######################################
        html.Div([
            html.Img(src=app.get_asset_url('saint-gobain.png'),
                     id='sg-image',
                     style={"height": "100px",
                            "width": "auto",
                            "margin-bottom": "15px","margin-top": "15px"},),],className="one-third column",),

        html.Div([
            html.Div([
                html.H4("MDM SCOPE AROUND SAINT-GOBAIN", style={"margin-bottom": "0px", 'color': 'white'}),
                html.H6("Track MDM Implementation", style={"margin-top": "0px", 'color': 'white'}),])], 
               className="one-half column", id="title"),

        html.Div([
            html.H6('Data Last Updated: August 24, 2022' ,
                    style={'color': 'orange'}),
            dcc.Link('Contact Us' , href="mailto:DL-IDS-Digital-Finance-FINTECH" ,target="mailto:DL-IDS-Digital-Finance-FINTECH" ,
                    style={'color': 'orange','text-indent':'1em'})], className="one-third column", id='title1'),], 
                id="header", className="row flex-display1", style={"margin-bottom": "25px"}),
  
  
#################################################### FILTER CONTAINER   ##################################################
    html.Div([
        html.Div([
            html.P('Select Tool', className = 'fix_label', style = {'color': 'white', 'margin-top': '2px'}),
            dcc.Dropdown(id='tools',
                         multi=False,
                         clearable=False,
                         value='GDI MDM V2',
                         placeholder='Please select your tool',
                         options=['GDI MDM V2','MDM HPS', 'SG Vendor Onboarding Portal/Jaegger', 'MDM PowerAutomate', 'Promenta'], className='dcc_compon'),
            dcc.RadioItems(id='data',
                          value='All',
                          options=['All','Vendor','Customer','Employee'],
                          style={'color': 'white','font-size':20,},
                          inputStyle={"margin-right": "5px","margin-left": "10px"},
                          inline=True,
                className='fix_label'),], 
                className = "create_container1 four columns", style = {'margin-bottom': '0px'}),], className = "row flex-display"),


########################################################## TEXT AREA  ##################################################
    html.Div([
         html.Div([html.Div(id= "info",),],className="div1",),], className="row flex-display"),


############################################## CARDS FOR COUNTRIES, ERP , ETC....  ########################################

    html.Div([html.Div([
        dbc.Button(id= "text1",className = 'card_size'),
        dbc.Modal([dbc.ModalHeader(
                                   html.Div(className="row", 
                                            children=[html.Div(className='six columns', 
                                                               children=[dbc.Label("Select Column",style={'font-weight': 'bold','color':'#1f2c56','fontSize': 20}),
                                                                         dcc.Dropdown(id='select',
                                                                                      options=['MDM SOLUTION','ERP','COMPANY CODE','COUNTRY','ENTITY NAME','MASTER DATA'],
                                                                                      clearable=True, )] , 
                                                                         style={'width': '500px'}),
                                                    html.Div(className='six columns', 
                                                             children=[dbc.Label("Select Value",style={'font-weight': 'bold','color':'#1f2c56','fontSize': 20}),
                                                                       dcc.Dropdown(id='dropdown', 
                                                                                    multi=True,
                                                                                    clearable=False, )],                                                       
                                                                        style={'width': '500px'})],
                                          style=dict(display='flex')),close_button=False),

                   dbc.ModalBody(dbc.Container([html.Div(id='table')])),          
                   dbc.ModalFooter(dbc.Button("Close", id="close1",style={'background-color':'#1f2c56','color':'white'}),),],
                 id="modal1",
                 centered=True,
                 is_open=False,
                 size="xl",        # "sm", "lg", "xl"
                 backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                 scrollable=True,  # False or True if modal has a lot of text
                 #fullscreen=True,    # True, False
                 fade=True,),], className="card_container big three columns",),

          html.Div([
              dbc.Button(id="text2",className = 'card_size'),
              dbc.Modal([dbc.ModalBody(id='data2'),
                         dbc.ModalFooter(dbc.Button("Close", id="close2",style={'background-color':'#1f2c56','color':'white'}),),],
                       id="modal2",
                       centered=True,
                       is_open=False,
                       size="xl",        # "sm", "lg", "xl"
                       backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                       scrollable=True,  # False or True if modal has a lot of text
                       #fullscreen=True,    # True, False
                       fade=True,),], className="card_container big three columns",),

          html.Div([
              dbc.Button(id="text3",className = 'card_size'),
              dbc.Modal([dbc.ModalBody(id='data3'),
                        dbc.ModalFooter(dbc.Button("Close", id="close3",style={'background-color':'#1f2c56','color':'white'}),),],
                      id="modal3",
                      centered=True,
                      is_open=False,
                      size="xl",        # "sm", "lg", "xl"
                      backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                      scrollable=True,  # False or True if modal has a lot of text
                      #fullscreen=True,    # True, False
                      fade=True,),], className="card_container big three columns",),

          html.Div([
              dbc.Button(id="text4",className = 'card_size'),
              dbc.Modal([dbc.ModalBody(id='data4'),
                         dbc.ModalFooter(dbc.Button("Close", id="close4",style={'background-color':'#1f2c56','color':'white'}),),],
                       id="modal4",
                       centered=True,
                       is_open=False,
                       size="xl",        # "sm", "lg", "xl"
                       backdrop=True,    # True, False or Static for modal to not be closed by clicking on backdrop
                       scrollable=True,  # False or True if modal has a lot of text
                       #fullscreen=True,    # True, False
                       fade=True,),], className="card_container big three columns")], className="row flex-display"),
                       
                       
                       
################################################## GRAPHS ##########################################

    html.Div([
        html.Div([
############################################## PIE CHART CONTAINER ############################
                    dcc.Graph(id='pie_chart',
                            config={'displayModeBar': 'hover'}),], className="create_container four columns", id="cross-filter-options"),
                            
############################################### MAP CONTAINER  ####################################################

        html.Div([dcc.Graph(id="map")], className="create_container nine columns"),], className="row flex-display"),

#################################################### DOWNLOAD DATA ######################################################

     html.Div([html.Div([html.Button("Download Excel", id="btn_xlsx",style={'background-color':'#1f2c56','color':'white'}),
                        dcc.Download(id="download-dataframe-xlsx"),], className = "create_container2 two columns",),], 
                className="row flex-display"),], id="mainContainer",style={"display": "flex", "flex-direction": "column"})
                

##################################################### CALLBACK ASIIGNMENT FUNCTION ####################################################

############################################   INFO CONTAINER #################################################

@app.callback(Output('info', 'children'),
              [Input('tools', 'value')],
              [Input('data', 'value')])
              

def update_info(tools,data):
    if data=='Vendor':
        info=df1[df1['MDM SOLUTION']==tools][["MDM SOLUTION","MASTER DATA","ERP","FINTECH"]]
        dt='Vendor'
    elif data=='Customer':
        info=df2[df2['MDM SOLUTION']==tools][["MDM SOLUTION","MASTER DATA","ERP","FINTECH"]]
        dt='Customer'
    elif data=='Employee':
        info=df3[df3['MDM SOLUTION']==tools][["MDM SOLUTION","MASTER DATA","ERP","FINTECH"]]
        dt='Employee'
    else:
        info=df[df['MDM SOLUTION']==tools][["MDM SOLUTION","MASTER DATA","ERP","FINTECH"]]
        dt=''
    
    def join_and(items):
        if len(items)==0:
            return ''
        if len(items)==1:
            return items[0]
        return ', '.join(items[:-1]) + ' and '+items[-1]    
    
    info.ERP = info.ERP.str.lstrip("SAP")
    ERP=list(info["ERP"].unique())
    ERP=join_and(ERP)
    RESPO=list(info["FINTECH"].unique())
    RESPO=join_and(RESPO)
    

    def text(x,y):
       text = ["FinTech team is accountable to ",x," for ",tools," ",dt," in ",y,"."]
       return text
    
    
    if RESPO=='':
        return [html.H6(children='Not implemented for '+dt+ ' Master Data Management',
                        style = {'color': 'red','fontSize': 20,},),]
    else: 
        return [html.H6(children=text(RESPO,ERP),
                        style = {'color': ' #1f2c56','fontSize': 20,},),]

   
   
    



############################################   TEXT1 #################################################

@app.callback(Output('text1', 'children'),
              [Input('tools', 'value')],)

def update_text1(tools):
    ven_cus_emp=df[df['MDM SOLUTION']==tools]["MASTER DATA"].unique()

    def join_and(items):
        if len(items)==0:
            return '' 
        if len(items)==1:
            return items[0]
        return ' - '.join(items[:-1]) +' - '+items[-1]
        

    ven_cus_emp=join_and(ven_cus_emp)
    ven_cus_emp=ven_cus_emp.split('-')
   
    if len(ven_cus_emp)==3:
        return [html.H6(children='Used for',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(ven_cus_emp[0:2],
                        style = {'textAlign':'center',
                                 'color': 'orange',
                                 'fontSize':20,}),
                html.P(ven_cus_emp[-1],
                       style = {'textAlign':'center',
                                'color': 'orange',
                                'fontSize':20,}),

                html.P('Data Management',
                        style = {'textAlign':'center',
                                 'color': 'orange',
                                 'fontSize': 20,},),]
                            
    else:
        return [html.H6(children='Used for',
                        style = {'textAlign':'center',
                                 'color': 'white',},),
                html.P(ven_cus_emp[0:2],
                        style = {'textAlign':'center',
                                 'color': 'orange',
                                 'fontSize':20,}),

                html.P('Data Management',
                        style = {'textAlign':'center',
                                 'color': 'orange',
                                 'fontSize': 20,},),]
                            
############################################   MODAL1 #################################################

@app.callback(Output('dropdown', 'options'),
             [Input("tools", "value"),],
             [Input("data", "value"),],              
             [Input("select", "value")],)
             
def output(tools,data,select):
    if data=='Vendor':
        modal_data=df1[df1['MDM SOLUTION']==tools][['MDM SOLUTION','ERP','COMPANY CODE','COUNTRY','ENTITY NAME','MASTER DATA']]
    elif data=='Customer':
        modal_data=df2[df2['MDM SOLUTION']==tools][['MDM SOLUTION','ERP','COMPANY CODE','COUNTRY','ENTITY NAME','MASTER DATA']]
    elif data=='Employee':
        modal_data=df3[df3['MDM SOLUTION']==tools][['MDM SOLUTION','ERP','COMPANY CODE','COUNTRY','ENTITY NAME','MASTER DATA']]
    else:
        modal_data=df[df['MDM SOLUTION']==tools][['MDM SOLUTION','ERP','COMPANY CODE','COUNTRY','ENTITY NAME','MASTER DATA']]
    
    if select is None:
        options=list(set(modal_data['MDM SOLUTION']))
        return [{'label': i, 'value': i} for i in options]
        
    options=list(set(modal_data[select]))
    return [{'label': i, 'value': i} for i in options]

@app.callback(Output('table', 'children'),
             [Input("tools", "value"),], 
             [Input("data", "value"),], 
             [Input("select", "value")],
             [Input("dropdown", "value")],)
             
def output_table(tools,data,select,dropdown):
    if data=='Vendor':
        modal_data=df1[df1['MDM SOLUTION']==tools][['MDM SOLUTION','ERP','COMPANY CODE','COUNTRY','ENTITY NAME','MASTER DATA']]
    elif data=='Customer':
        modal_data=df2[df2['MDM SOLUTION']==tools][['MDM SOLUTION','ERP','COMPANY CODE','COUNTRY','ENTITY NAME','MASTER DATA']]
    elif data=='Employee':
        modal_data=df3[df3['MDM SOLUTION']==tools][['MDM SOLUTION','ERP','COMPANY CODE','COUNTRY','ENTITY NAME','MASTER DATA']]
    
    else:
        modal_data=df[df['MDM SOLUTION']==tools][['MDM SOLUTION','ERP','COMPANY CODE','COUNTRY','ENTITY NAME','MASTER DATA']]
    
    if select is not None:
        if dropdown is not None:
           dff = modal_data[modal_data[select].str.contains('|'.join(dropdown),na=False)]
        
           return [dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True)]
    return [dbc.Table.from_dataframe(modal_data, striped=True, bordered=True, hover=True)]




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


############################################   TEXT2 #################################################

@app.callback(Output('text2', 'children'),
              [Input('tools', 'value')],
              [Input('data', 'value')])

def update_text2(tools,data):
    if data=='Vendor':
        Countries=df1[df1['MDM SOLUTION']==tools]['COUNTRY'].unique()
        
    elif data=='Customer':
        Countries=df2[df2['MDM SOLUTION']==tools]['COUNTRY'].unique()
        
    elif data=='Employee':
        Countries=df3[df3['MDM SOLUTION']==tools]['COUNTRY'].unique()
        
    else:
        Countries=df[df['MDM SOLUTION']==tools]['COUNTRY'].unique()
       

    return [html.H6(children='Implemented in ',
                    style = {'textAlign':'center',
                             'color': 'white',},),
            html.P(len(Countries),
                       style = {'textAlign':'center',
                                'color': 'orange',
                                'fontSize': 40,},),
            html.P(' Countries',
                    style = {'textAlign':'center',
                             'color': 'orange',
                             'fontSize': 20,},),]
 
############################################   MODAL2 ################################################# 

@app.callback(
    Output("data2", "children"),
    [Input("tools", "value"),],
    [Input("data", "value"),],)


def data2(tools,data):
    if data=='Vendor':
        dff_cnt=df1[df1['MDM SOLUTION']==tools][['MDM SOLUTION','COUNTRY']]
        
    elif data=='Customer':
        dff_cnt=df2[df2['MDM SOLUTION']==tools][['MDM SOLUTION','COUNTRY']]
    
    elif data=='Employee':
        dff_cnt=df3[df3['MDM SOLUTION']==tools][['MDM SOLUTION','COUNTRY']]
        
    else:
        dff_cnt=df[df['MDM SOLUTION']==tools][['MDM SOLUTION','COUNTRY']]
        
    dff_cnt=pd.pivot_table(dff_cnt,values=('COUNTRY'),index=['MDM SOLUTION','COUNTRY'],aggfunc='count')
    dff_cnt=dff_cnt.reset_index()
        
    return [dbc.Table.from_dataframe(dff_cnt, )]


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




############################################   TEXT3 #################################################

@app.callback(Output('text3', 'children'),
              [Input('tools', 'value')],
              [Input('data', 'value')])

def update_text3(tools,data):
    if data=='Vendor':
        BUs=df1[df1['MDM SOLUTION']==tools]['ERP'].unique()
        
    elif data=='Customer':
        BUs=df2[df2['MDM SOLUTION']==tools]['ERP'].unique()
    
    elif data=='Employee':
        BUs=df3[df3['MDM SOLUTION']==tools]['ERP'].unique()
        
    else:
        BUs=df[df['MDM SOLUTION']==tools]['ERP'].unique()
    
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

@app.callback(
    Output("data3", "children"),
    [Input("tools", "value"),],
    [Input("data", "value"),],)


def data3(tools,data):
    if data=='Vendor':
        dff_bu=df1[df1['MDM SOLUTION']==tools][['MDM SOLUTION','ERP']]
        
    elif data=='Customer':
        dff_bu=df2[df2['MDM SOLUTION']==tools][['MDM SOLUTION','ERP']]
    
    elif data=='Employee':
        dff_bu=df3[df3['MDM SOLUTION']==tools][['MDM SOLUTION','ERP']]
        
    else:
        dff_bu=df[df['MDM SOLUTION']==tools][['MDM SOLUTION','ERP']]
        
    dff_bu=pd.pivot_table(dff_bu,values=('ERP'),index=['MDM SOLUTION','ERP'],aggfunc='count')
    dff_bu=dff_bu.reset_index()
    
    return [dbc.Table.from_dataframe(dff_bu, striped=True, bordered=True, hover=True)]





@app.callback(Output("modal3", "is_open"),
    [Input("text3", "n_clicks"), Input("close3", "n_clicks")],
    [State("modal3", "is_open")],)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


############################################   TEXT4 #################################################

@app.callback(Output('text4', 'children'),
              [Input('tools', 'value')],
              [Input('data', 'value')])




def update_text4(tools,data):
    if data=='Vendor':
        Entities=df1[df1['MDM SOLUTION']==tools]['COMPANY CODE'].unique()
        
    elif data=='Customer':
        Entities=df2[df2['MDM SOLUTION']==tools]['COMPANY CODE'].unique()
        
    elif data=='Employee':
        Entities=df3[df3['MDM SOLUTION']==tools]['COMPANY CODE'].unique()
        
    else:
        Entities=df[df['MDM SOLUTION']==tools]['COMPANY CODE'].unique()
    
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


@app.callback(
    Output("data4", "children"),
    [Input("tools", "value"),],
    [Input("data", "value"),],)

def data4(tools,data):
    if data=='Vendor':
        dff_en=df1[df1['MDM SOLUTION']==tools][['MDM SOLUTION','COMPANY CODE']]
           
    elif data=='Customer':
        dff_en=df2[df2['MDM SOLUTION']==tools][['MDM SOLUTION','COMPANY CODE']]
        
    elif data=='Employee':
        dff_en=df3[df3['MDM SOLUTION']==tools][['MDM SOLUTION','COMPANY CODE']]
           
        
    else:
        dff_en=df[df['MDM SOLUTION']==tools][['MDM SOLUTION','COMPANY CODE']]
           
    dff_en=pd.pivot_table(dff_en,values=('COMPANY CODE'),index=['MDM SOLUTION','COMPANY CODE'],aggfunc='count')
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

############################################   PIE CHART #################################################

@app.callback(Output('pie_chart', 'figure'),
              [Input('tools', 'value')])

def update_graph(tools):
    labels=list(Counter(df["MDM SOLUTION"]).keys())
    values=list(Counter(df["MDM SOLUTION"]).values())
    colors = ['#ff7c43','#3d708f','#d45087','#a05195','#6b9e3c']
    
    line_color=[]
    pull=[]
    for tool in labels:
        if tool==tools:
            pull.append(0.1)
            line_color.append('white')
        else:
            pull.append(0)
            line_color.append('#1f2c56')
            

    return {
        'data': [go.Pie(labels=labels,
                        values=values,
                        pull=pull,
                        marker=dict(colors=colors,line=dict(color=line_color, width=2)),
                        hoverinfo='label+value+percent',
                        textinfo='label+value',
                        textfont=dict(size=1,color='#1f2c56'),
                        textposition='outside',
                        hole=.3,
                        rotation=45
                        # insidetextorientation='radial',
                        )],

        'layout': go.Layout(
            #width=800,
            # height=520,
            
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            hovermode='closest',
            title={
                'text': 'MDM Solutions',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                       'color': 'white',
                       'size': 25},
            legend={ 
                
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.010},
                
            font=dict(
                family="Computer Modern",
                size=17,
                color='white')),}


############################################   MAP #################################################

@app.callback(Output("map", "figure"),
              Input("tools", "value"),)
            
             
def updateGraphCB(tools):
    if tools== 'MDM HPS':
         color=['black','#5d8daa','black']
    
    elif tools== 'SG Vendor Onboarding Portal/Jaegger':
        color=['#ff9562','black','black']

    elif tools=='GDI MDM V2':
        color=['#da6393','#ec95b6','#ffd5e5']
    
    elif tools== 'MDM PowerAutomate':
        color=['#c653bd','#ec8ee9','black']
    
    elif tools=='Promenta':
       color=['#6ac42f','#b1df84','black']
    
    # filter traces...
    fig = interactive_multi_plot(df1, df2,df3,color).update_traces(visible=False)
    fig.update_traces(visible=True, selector={"meta":tools})
    return fig

############################################  DOWNLOAD EXCEL #################################################

@app.callback(Output("download-dataframe-xlsx", "data"),
              Input("btn_xlsx", "n_clicks"),
              prevent_initial_call=True,)
              
def func(n_clicks):
    df=df[["MDM SOLUTION","MASTER DATA","ERP","COMPANY CODE","ENTITY NAME","COUNTRY","FINTECH"]]
    return dcc.send_data_frame(df.to_excel, "MDM_DATA.xlsx", sheet_name="Master Data",index=False)




if __name__ == '__main__':
    app.run_server(debug=True)
