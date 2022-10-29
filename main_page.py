import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

from jupyter_dash import JupyterDash




font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css" ##css design
meta_tags = [{"name": "viewport", "content": "width=device-width"}] ##css design

external_stylesheets = [meta_tags, font_awesome]


app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
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
            html.Button(dcc.Link('MDM Dashboard',
                                 href='https://www.google.com/imgres?imgurl=https://cdn1.vectorstock.com/i/1000x1000/79/10/cartoon-color-characters-people-build-dashboard-vector-35307910.jpg&imgrefurl=https://www.vectorstock.com/royalty-free-vector/cartoon-color-characters-people-build-dashboard-vector-35307910&tbnid=68Ry4ejyR9A3BM&vet=1&docid=R0H7vV40X_u8MM&w=1000&h=820&hl=en_GB&source=sh/x/im',
                                 target="https://www.google.com/imgres?imgurl=https://cdn1.vectorstock.com/i/1000x1000/79/10/cartoon-color-characters-people-build-dashboard-vector-35307910.jpg&imgrefurl=https://www.vectorstock.com/royalty-free-vector/cartoon-color-characters-people-build-dashboard-vector-35307910&tbnid=68Ry4ejyR9A3BM&vet=1&docid=R0H7vV40X_u8MM&w=1000&h=820&hl=en_GB&source=sh/x/im" ,
                                 className='link'),className='btn'),
            html.Button(dcc.Link('AP Solution Dashboard',
                                  href='https://www.google.com/imgres?imgurl=https://cdn1.vectorstock.com/i/1000x1000/79/10/cartoon-color-characters-people-build-dashboard-vector-35307910.jpg&imgrefurl=https://www.vectorstock.com/royalty-free-vector/cartoon-color-characters-people-build-dashboard-vector-35307910&tbnid=68Ry4ejyR9A3BM&vet=1&docid=R0H7vV40X_u8MM&w=1000&h=820&hl=en_GB&source=sh/x/im',
                                  target="https://www.google.com/imgres?imgurl=https://cdn1.vectorstock.com/i/1000x1000/79/10/cartoon-color-characters-people-build-dashboard-vector-35307910.jpg&imgrefurl=https://www.vectorstock.com/royalty-free-vector/cartoon-color-characters-people-build-dashboard-vector-35307910&tbnid=68Ry4ejyR9A3BM&vet=1&docid=R0H7vV40X_u8MM&w=1000&h=820&hl=en_GB&source=sh/x/im" ,
                        className='link'),className='btn'),
            ],className="left-column"),
          html.Div([
            html.Img(src=app.get_asset_url('main.png'),
            style={"width": "100%",},),],className="right-column")
          ],className="banner")]),])


if __name__ == '__main__':
    app.run_server(debug=True)
