from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server


from apps import mdm
from apps import index


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
      html.Div([
        html.Div([
          html.Img(src=app.get_asset_url('fintech.png'),style={"height": "70px","width": "auto","margin-left":"20px"}),]),
        html.Div([
          dcc.Link('HOME', href='#', target="#",className="list"),
          dcc.Link('FINTECH', href='#', target="#" ,className="list"),
          dcc.Link('CONTACT US', href='#',target="#" ,className="list"),],className = "ul")],className='navbar'),],className='hero'),


     html.Div([
       html.Div([
          html.Div([
            html.P('Track Tools Around Saint-Gobain',style={'font-size':'45px','margin-left':'50px ','margin-top':'50px ','color':' #5A5A5A'}),
            html.P('To add small discription here ',style={'font-size':'20px','margin-left':'50px ','color':'#949494'}),
            html.Button(dcc.Link("MDM Dashboard", href='/apps/mdm',className='link'),id="btn1",className='togo'),
                     dbc.Modal([
                       dbc.ModalHeader(html.Button("HOME", id="close1",
                                                   style={'font-size':'15px','color':'#1f2c56','border':'none','text-align':'right','flex':'1'}),
                                      style={'background-color':'#D3D3D3'},close_button=False),
                       dbc.ModalBody(id='body1'),],


                       id="dashboard1",
                       fullscreen=True,    # True, False

                       ),
            html.Button(dcc.Link("AP Solutions Dashboard", href='/apps/index',className='link'),id="btn2",className='togo'),
                     dbc.Modal([
                       dbc.ModalHeader(html.Button("HOME", id="close2",
                                                   style={'font-size':'15px','color':'#1f2c56','border':'none','text-align':'right','flex':'1'}),
                                      style={'background-color':'#D3D3D3'},close_button=False),
                       dbc.ModalBody(id='body2'),],


                       id="dashboard2",
                       fullscreen=True, ),   # True, False

            ],className="left-column"),
          html.Div([
            html.Img(src=app.get_asset_url('main.png'),
            style={"width": "100%",},),],className="right-column")
          ],className="banner")]),])

#############################################################################

@app.callback(Output('body1', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname=='/apps/mdm':
       return mdm.layout


@app.callback(
    Output("dashboard1", "is_open"),
    [Input("btn1", "n_clicks"), Input("close1", "n_clicks")],
    [State("dashboard1", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open




@app.callback(Output('body2', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname=='/apps/index':
       return mdm.layout


@app.callback(
    Output("dashboard2", "is_open"),
    [Input("btn2", "n_clicks"), Input("close2", "n_clicks")],
    [State("dashboard2", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



if __name__ == '__main__':
    app.run_server(debug=True)
