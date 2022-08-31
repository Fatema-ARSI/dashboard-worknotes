from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import tools
from apps import ssc


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('saint-gobain.png'),
                     id='sg-image',
                     style={
                            "height": "100px",
                            "width": "auto",
                            "margin-bottom": "15px","margin-top": "15px"},),],className="one-third column",),
                         
        html.Div([
            html.Div([
                html.H4("AP SOLUTIONS AROUND SAINT-GOBAIN", style={"margin-bottom": "0px", 'color': 'white'}),
                html.H6("Track AP tool Implementation",style={"margin-top": "0px", 'color': 'white'}),])], className="one-half column", id="title"),

        html.Div([
            html.H6('Data Last Updated: August 24, 2022' ,
                    style={'color': 'orange'}),
            dcc.Link('Contact Us' , href="mailto:DL-IDS-Digital-Finance-FINTECH" ,target="mailto:DL-IDS-Digital-Finance-FINTECH" ,
                    style={'color': 'orange','text-indent':'1em'})], className="one-third column", id='title1'), ], 
                  id="header", className="row flex-display1", style={"margin-bottom": "25px"}),

    html.Div([
         html.Div([
             dcc.Link('Filter by Tools', href='/apps/tools', style={'color': '#1f2c56','font-weight': 'bold',"margin-right": "25px"}, className="tab"),
             dcc.Link('Filter by SSC', href='/apps/ssc', style={'color': '#1f2c56','font-weight': 'bold',"margin-right": "25px"}, className="tab"),], 
             
          className = "create_container3 twelve columns", id = "filter"),], id = "header1", className = "row flex-display"),

    html.Div(id='page-content', children=[])])


################################################# TILTE/HEADER LAYOUT ######################################
  

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/tools':
        return tools.layout
    elif pathname == '/apps/ssc':
        return ssc.layout
    
    


if __name__ == '__main__':
    app.run_server(debug=True)
