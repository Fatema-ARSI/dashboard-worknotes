from collections import Counter

import dash

# from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output, State

################################## APP CREATION ####################################################

font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"  ##css design
meta_tags = [{"name": "viewport", "content": "width=device-width"}]


external_stylesheets = [meta_tags, font_awesome]

# app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(
    __name__,
    title="MDM Dashboard",
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    assets_url_path="/mdm-dashboard/dev/init/assets/",
    requests_pathname_prefix="/mdm-dashboard/dev/init/",
)


server = app.server
app.css.config.serve_locally = True
app.scripts.config.serve_locally = False


##################################################    LOAD THE DATA    #####################################################################

df = pd.read_excel(r"./data/MDM_SCOPE.xlsx")
df["COMPANY CODE"] = df["COMPANY CODE"].map(str)

df1 = df[df["MASTER DATA"] == "Vendor"][
    [
        "MDM SOLUTION",
        "MASTER DATA",
        "ERP",
        "BU",
        "COMPANY CODE",
        "LAT",
        "LNG",
        "COUNTRY",
        "ENTITY NAME",
        "FINTECH",
    ]
]
df2 = df[df["MASTER DATA"] == "Customer"][
    [
        "MDM SOLUTION",
        "MASTER DATA",
        "ERP",
        "BU",
        "COMPANY CODE",
        "LAT",
        "LNG",
        "COUNTRY",
        "ENTITY NAME",
        "FINTECH",
    ]
]
df3 = df[df["MASTER DATA"] == "Employee"][
    [
        "MDM SOLUTION",
        "MASTER DATA",
        "ERP",
        "BU",
        "COMPANY CODE",
        "LAT",
        "LNG",
        "COUNTRY",
        "ENTITY NAME",
        "FINTECH",
    ]
]


def dash_data(tools, data):
    if tools == "All":
        if data == "Vendor":
            dash_data = df1
        elif data == "Customer":
            dash_data = df2
        elif data == "Employee":
            dash_data = df3
        else:
            dash_data = df
    else:
        if data == "Vendor":
            dash_data = df1[df1["MDM SOLUTION"] == tools][
                [
                    "MDM SOLUTION",
                    "ERP",
                    "COMPANY CODE",
                    "COUNTRY",
                    "ENTITY NAME",
                    "MASTER DATA",
                ]
            ]
        elif data == "Customer":
            dash_data = df2[df2["MDM SOLUTION"] == tools][
                [
                    "MDM SOLUTION",
                    "ERP",
                    "COMPANY CODE",
                    "COUNTRY",
                    "ENTITY NAME",
                    "MASTER DATA",
                ]
            ]
        elif data == "Employee":
            dash_data = df3[df3["MDM SOLUTION"] == tools][
                [
                    "MDM SOLUTION",
                    "ERP",
                    "COMPANY CODE",
                    "COUNTRY",
                    "ENTITY NAME",
                    "MASTER DATA",
                ]
            ]
        else:
            dash_data = df[df["MDM SOLUTION"] == tools][
                [
                    "MDM SOLUTION",
                    "ERP",
                    "COMPANY CODE",
                    "COUNTRY",
                    "ENTITY NAME",
                    "MASTER DATA",
                ]
            ]
    return dash_data


##############################################    MAP INPUT FOR THE MDM SOLUTION TO FILTER   ###############################################


def interactive_multi_plot(vendor, customer, employee, addAll=True):
    fig = go.Figure()

    gd_ven = vendor.groupby(["MDM SOLUTION"])
    group_name_d_ven = list(set(vendor["MDM SOLUTION"]))

    for grx in group_name_d_ven:
        df_ven = gd_ven.get_group(grx)
        fig.add_trace(
            go.Scattermapbox(
                lon=df_ven["LNG"],
                lat=df_ven["LAT"],
                name=grx + " " + "Vendor",
                mode="markers",
                marker=dict(
                    size=15,
                    symbol="circle",
                    color=df_ven["MDM SOLUTION"].map(
                        {
                            "MDM HPS": "black",
                            "SG Vendor Onboarding Portal/Jaeger": "#ff9562",
                            "GDI MDM V2": "#da6393",
                            "MDM PowerAutomate": "#c653bd",
                            "Promenta": "#6ac42f",
                        }
                    ),
                ),
                meta=grx,
                hoverinfo="text",
                hovertext="<b>Country</b>: "
                + df_ven["COUNTRY"].astype(str)
                + "<br>"
                + "<b>Tool</b>: "
                + grx
                + "<br>"
                + "<b>Master Data</b>: "
                + df_ven["MASTER DATA"].astype(str)
                + "<br>"
                + "<b>BU</b>: "
                + df_ven["ERP"].astype(str)
                + "<br>"
                + "<b>Company Code</b>: "
                + df_ven["COMPANY CODE"].astype(str),
            )
        )

    gd_cus = customer.groupby(["MDM SOLUTION"])
    group_name_d_cus = list(set(customer["MDM SOLUTION"]))

    for grx in group_name_d_cus:
        df_cus = gd_cus.get_group(grx)
        fig.add_trace(
            go.Scattermapbox(
                lon=df_cus["LNG"],
                lat=df_cus["LAT"],
                name=grx + " " + "Customer",
                mode="markers",
                marker=dict(
                    size=15,
                    symbol="circle",
                    color=df_cus["MDM SOLUTION"].map(
                        {
                            "MDM HPS": "#5d8daa",
                            "SG Vendor Onboarding Portal/Jaeger": "black",
                            "GDI MDM V2": "#ec95b6",
                            "MDM PowerAutomate": "#ec8ee9",
                            "Promenta": "#b1df84",
                        }
                    ),
                ),
                meta=grx,
                hoverinfo="text",
                hovertext="<b>Country</b>: "
                + df_cus["COUNTRY"].astype(str)
                + "<br>"
                + "<b>Tool</b>: "
                + grx
                + "<br>"
                + "<b>Master Data</b>: "
                + df_ven["MASTER DATA"].astype(str)
                + "<br>"
                + "<b>BU</b>: "
                + df_cus["ERP"].astype(str)
                + "<br>"
                + "<b>Company Code</b>: "
                + df_cus["COMPANY CODE"].astype(str),
            )
        )

    gd_emp = employee.groupby(["MDM SOLUTION"])
    group_name_d_emp = list(set(employee["MDM SOLUTION"]))

    for grx in group_name_d_emp:
        df_emp = gd_emp.get_group(grx)
        fig.add_trace(
            go.Scattermapbox(
                lon=df_emp["LNG"],
                lat=df_emp["LAT"],
                name=grx + " " + "Employee",
                mode="markers",
                marker=dict(
                    size=15,
                    symbol="circle",
                    color=df_emp["MDM SOLUTION"].map(
                        {
                            "MDM HPS": "black",
                            "SG Vendor Onboarding Portal/Jaeger": "black",
                            "GDI MDM V2": "#ffd5e5",
                            "MDM PowerAutomate": "black",
                            "Promenta": "black",
                        }
                    ),
                ),
                meta=grx,
                hoverinfo="text",
                hovertext="<b>Country</b>: "
                + df_emp["COUNTRY"].astype(str)
                + "<br>"
                + "<b>Tool</b>: "
                + grx
                + "<br>"
                + "<b>Master Data</b>: "
                + df_ven["MASTER DATA"].astype(str)
                + "<br>"
                + "<b>BU</b>: "
                + df_emp["ERP"].astype(str)
                + "<br>"
                + "<b>Company Code</b>: "
                + df_emp["COMPANY CODE"].astype(str),
            )
        )

    fig.layout.plot_bgcolor = "#1f2c56"
    fig.layout.paper_bgcolor = "#1f2c56"

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        width=900,
        height=550,
        hovermode="closest",
        mapbox=dict(
            accesstoken="pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw",
        ),
        legend=dict(
            itemclick="toggleothers",
            # when you are clicking an item in legend all that are not in the same group are hidden
            orientation="v",
            x=1.05,
            y=0.8,
            font=dict(color="#fff", size=12, family="Computer Modern"),
            title="Master Data",
        ),
    )

    return fig


######################################################  LAYOUT OF THE DASHBOARD   #########################################################


app.layout = html.Div(
    [
        html.Div(
            [
                ################################################# TILTE/HEADER LAYOUT ######################################
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("saint-gobain.png"),
                            id="sg-image",
                            style={
                                "height": "100px",
                                "width": "auto",
                                "margin-bottom": "15px",
                                "margin-top": "15px",
                            },
                        ),
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4(
                                    "MDM SCOPE AROUND SAINT-GOBAIN",
                                    style={"margin-bottom": "0px", "color": "white"},
                                ),
                                html.H6(
                                    "Track MDM Implementation",
                                    style={"margin-top": "0px", "color": "white"},
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.H6(
                            "Data Last Updated: September 21, 2022",
                            style={"color": "orange"},
                        ),
                        dcc.Link(
                            "Contact Us",
                            href="mailto:DL-IDS-Digital-Finance-FINTECH",
                            target="mailto:DL-IDS-Digital-Finance-FINTECH",
                            style={"color": "orange", "text-indent": "1em"},
                        ),
                    ],
                    className="one-third column",
                    id="title1",
                ),
            ],
            id="header",
            className="row flex-display1",
            style={"margin-bottom": "25px"},
        ),
        #################################################### FILTER CONTAINER   ##################################################
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Select Tool",
                            className="fix_label",
                            style={"color": "white", "margin-top": "2px"},
                        ),
                        dcc.Dropdown(
                            id="tools",
                            multi=False,
                            clearable=False,
                            value="GDI MDM V2",
                            placeholder="Please select your tool",
                            options=[
                                "All",
                                "GDI MDM V2",
                                "MDM HPS",
                                "SG Vendor Onboarding Portal/Jaeger",
                                "MDM PowerAutomate",
                                "Promenta",
                            ],
                            className="dcc_compon",
                        ),
                        dcc.RadioItems(
                            id="data",
                            value="All",
                            options=["All", "Vendor", "Customer", "Employee"],
                            style={
                                "color": "white",
                                "font-size": 20,
                            },
                            inputStyle={"margin-right": "5px", "margin-left": "10px"},
                            inline=True,
                            className="fix_label",
                        ),
                    ],
                    className="create_container1 four columns",
                    style={"margin-bottom": "0px"},
                ),
            ],
            className="row flex-display",
        ),
        ############################################## CARDS FOR COUNTRIES, ERP , ETC....  ########################################
        html.Div(
            [
                html.Div(
                    [
                        dbc.Button(id="text1", className="card_size"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(
                                    html.Div(
                                        className="row",
                                        children=[
                                            html.Div(
                                                className="six columns",
                                                children=[
                                                    dbc.Label(
                                                        "Select Column",
                                                        style={
                                                            "font-weight": "bold",
                                                            "color": "#1f2c56",
                                                            "fontSize": 20,
                                                        },
                                                    ),
                                                    dcc.Dropdown(
                                                        id="select",
                                                        options=[
                                                            "MDM SOLUTION",
                                                            "ERP",
                                                            "COMPANY CODE",
                                                            "COUNTRY",
                                                            "ENTITY NAME",
                                                            "MASTER DATA",
                                                        ],
                                                        clearable=True,
                                                    ),
                                                ],
                                                style={"width": "500px"},
                                            ),
                                            html.Div(
                                                className="six columns",
                                                children=[
                                                    dbc.Label(
                                                        "Select Value",
                                                        style={
                                                            "font-weight": "bold",
                                                            "color": "#1f2c56",
                                                            "fontSize": 20,
                                                        },
                                                    ),
                                                    dcc.Dropdown(
                                                        id="dropdown",
                                                        multi=True,
                                                        clearable=False,
                                                    ),
                                                ],
                                                style={"width": "500px"},
                                            ),
                                        ],
                                        style=dict(display="flex"),
                                    ),
                                    close_button=False,
                                ),
                                dbc.ModalBody(dbc.Container([html.Div(id="table")])),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Close",
                                        id="close1",
                                        style={
                                            "background-color": "#1f2c56",
                                            "color": "white",
                                        },
                                    ),
                                ),
                            ],
                            id="modal1",
                            centered=True,
                            is_open=False,
                            size="xl",  # "sm", "lg", "xl"
                            backdrop=True,  # True, False or Static for modal to not be closed by clicking on backdrop
                            scrollable=True,  # False or True if modal has a lot of text
                            # fullscreen=True,    # True, False
                            fade=True,
                        ),
                    ],
                    className="card_container big three columns",
                ),
                html.Div(
                    [
                        dbc.Button(id="text2", className="card_size"),
                        dbc.Modal(
                            [
                                dbc.ModalBody(id="data2"),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Close",
                                        id="close2",
                                        style={
                                            "background-color": "#1f2c56",
                                            "color": "white",
                                        },
                                    ),
                                ),
                            ],
                            id="modal2",
                            centered=True,
                            is_open=False,
                            size="xl",  # "sm", "lg", "xl"
                            backdrop=True,  # True, False or Static for modal to not be closed by clicking on backdrop
                            scrollable=True,  # False or True if modal has a lot of text
                            # fullscreen=True,    # True, False
                            fade=True,
                        ),
                    ],
                    className="card_container big three columns",
                ),
                html.Div(
                    [
                        dbc.Button(id="text3", className="card_size"),
                        dbc.Modal(
                            [
                                dbc.ModalBody(id="data3"),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Close",
                                        id="close3",
                                        style={
                                            "background-color": "#1f2c56",
                                            "color": "white",
                                        },
                                    ),
                                ),
                            ],
                            id="modal3",
                            centered=True,
                            is_open=False,
                            size="xl",  # "sm", "lg", "xl"
                            backdrop=True,  # True, False or Static for modal to not be closed by clicking on backdrop
                            scrollable=True,  # False or True if modal has a lot of text
                            # fullscreen=True,    # True, False
                            fade=True,
                        ),
                    ],
                    className="card_container big three columns",
                ),
                html.Div(
                    [
                        dbc.Button(id="text4", className="card_size"),
                        dbc.Modal(
                            [
                                dbc.ModalBody(id="data4"),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Close",
                                        id="close4",
                                        style={
                                            "background-color": "#1f2c56",
                                            "color": "white",
                                        },
                                    ),
                                ),
                            ],
                            id="modal4",
                            centered=True,
                            is_open=False,
                            size="xl",  # "sm", "lg", "xl"
                            backdrop=True,  # True, False or Static for modal to not be closed by clicking on backdrop
                            scrollable=True,  # False or True if modal has a lot of text
                            # fullscreen=True,    # True, False
                            fade=True,
                        ),
                    ],
                    className="card_container big three columns",
                ),
            ],
            className="row flex-display",
        ),
        ################################################## GRAPHS ##########################################
        html.Div(
            [
                html.Div(
                    [
                        ############################################## PIE CHART CONTAINER ############################
                        dcc.Graph(id="pie_chart", config={"displayModeBar": "hover"}),
                    ],
                    className="create_container four columns",
                    id="cross-filter-options",
                ),
                ############################################### MAP CONTAINER  ####################################################
                html.Div(
                    [dcc.Graph(id="map")], className="create_container nine columns"
                ),
            ],
            className="row flex-display",
        ),
        #################################################### DOWNLOAD DATA ######################################################
        html.Div(
            [
                html.Div(
                    [
                        html.Button(
                            "Download Excel",
                            id="btn_xlsx",
                            style={"background-color": "#1f2c56", "color": "white"},
                        ),
                        dcc.Download(id="download-dataframe-xlsx"),
                    ],
                    className="create_container2 two columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

##################################################### CALLBACK ASIIGNMENT FUNCTION ###################################################

############################################   INFO CONTAINER #################################################


@app.callback(
    Output("info", "children"), [Input("tools", "value")], [Input("data", "value")]
)
def update_info(tools, data):
    def join_and(items):
        if len(items) == 0:
            return ""
        if len(items) == 1:
            return items[0]
        return ", ".join(items[:-1]) + " and " + items[-1]

    if tools == "All":
        if data == "Vendor":
            info = pd.pivot_table(
                df1[["MDM SOLUTION", "MASTER DATA", "ERP", "FINTECH"]],
                values=("FINTECH"),
                index=["MDM SOLUTION", "MASTER DATA", "ERP", "FINTECH"],
                aggfunc="count",
            ).reset_index()
            dt = "Vendor"
        elif data == "Customer":
            info = pd.pivot_table(
                df2[["MDM SOLUTION", "MASTER DATA", "ERP", "FINTECH"]],
                values=("FINTECH"),
                index=["MDM SOLUTION", "MASTER DATA", "ERP", "FINTECH"],
                aggfunc="count",
            ).reset_index()
            dt = "Customer"
        elif data == "Employee":
            info = pd.pivot_table(
                df3[["MDM SOLUTION", "MASTER DATA", "ERP", "FINTECH"]],
                values=("FINTECH"),
                index=["MDM SOLUTION", "MASTER DATA", "ERP", "FINTECH"],
                aggfunc="count",
            ).reset_index()
            dt = "Employee"
        else:
            info = pd.pivot_table(
                df[["MDM SOLUTION", "MASTER DATA", "ERP", "FINTECH"]],
                values=("FINTECH"),
                index=["MDM SOLUTION", "MASTER DATA", "ERP", "FINTECH"],
                aggfunc="count",
            ).reset_index()
            dt = ""

        info.ERP = info.ERP.str.lstrip("SAP")
        tools_all = list(
            {k: v.tolist() for k, v in info.groupby("MDM SOLUTION")["ERP"]}.items()
        )
        RESPOs_all = list(info["FINTECH"].unique())

        if len(RESPOs_all) != len(tools_all):
            RESPOs_all = RESPOs_all + RESPOs_all
        else:
            RESPOs_all = RESPOs_all

        text_list = []
        for number in range(len(tools_all)):
            RESPOs_all = RESPOs_all
            RESPO_all = RESPOs_all[number]
            tool_all = tools_all[number][0]
            ERP_all = join_and(tools_all[number][1])
            text_list.append([f" to {RESPO_all} {tool_all} {dt} in {ERP_all} "])

        text_list = sum(text_list, [])

        if RESPO_all == "":
            return [
                html.H6(
                    children="Not implemented for " + dt + " Master Data Management",
                    style={
                        "color": "red",
                        "fontSize": 20,
                    },
                ),
            ]

        else:
            return html.H6(
                [
                    html.Span(
                        "FinTech team is accountable ",
                        style={
                            "color": " #1f2c56",
                            "fontSize": 15,
                        },
                    ),
                    html.Span(
                        f"{' - '.join(text_list)} .",
                        style={
                            "color": "#1f2c56",
                            "text-decoration": "underline",
                            "font-weight": " bolder",
                            "fontSize": 15,
                        },
                    ),
                ]
            )

    else:
        if data == "Vendor":
            info = df1[df1["MDM SOLUTION"] == tools][
                ["MDM SOLUTION", "MASTER DATA", "ERP", "FINTECH"]
            ]
            dt = "Vendor"
        elif data == "Customer":
            info = df2[df2["MDM SOLUTION"] == tools][
                ["MDM SOLUTION", "MASTER DATA", "ERP", "FINTECH"]
            ]
            dt = "Customer"
        elif data == "Employee":
            info = df3[df3["MDM SOLUTION"] == tools][
                ["MDM SOLUTION", "MASTER DATA", "ERP", "FINTECH"]
            ]
            dt = "Employee"
        else:
            info = df[df["MDM SOLUTION"] == tools][
                ["MDM SOLUTION", "MASTER DATA", "ERP", "FINTECH"]
            ]
            dt = ""

    info.ERP = info.ERP.str.lstrip("SAP")
    ERP = list(info["ERP"].unique())
    ERP = join_and(ERP)
    RESPO = list(info["FINTECH"].unique())
    RESPO = join_and(RESPO)

    if RESPO == "":
        return [
            html.H6(
                children="Not implemented for " + dt + " Master Data Management",
                style={
                    "color": "red",
                    "fontSize": 20,
                },
            ),
        ]

    else:
        return html.H6(
            [
                html.Span(
                    "FinTech team is accountable to ",
                    style={
                        "color": " #1f2c56",
                        "fontSize": 15,
                    },
                ),
                html.Span(
                    f"{RESPO} {tools} {dt} in {ERP} . ",
                    style={
                        "color": "#1f2c56",
                        "text-decoration": "underline",
                        "font-weight": " bolder",
                        "fontSize": 15,
                    },
                ),
            ]
        )


############################################   TEXT1 #################################################


@app.callback(
    Output("text1", "children"),
    [Input("tools", "value")],
)
def update_text1(tools):

    ven_cus_emp = df[df["MDM SOLUTION"] == tools][["MDM SOLUTION", "MASTER DATA"]]
    ven_cus_emp = ven_cus_emp["MASTER DATA"].unique()
    ven_cus_emp = " - ".join(ven_cus_emp)
    ven_cus_emp = ven_cus_emp.split("-")

    if len(ven_cus_emp) == 3:
        return [
            html.H6(
                children="Used for",
                style={
                    "textAlign": "center",
                    "color": "white",
                },
            ),
            html.P(
                ven_cus_emp[0:2],
                style={
                    "textAlign": "center",
                    "color": "orange",
                    "fontSize": 20,
                },
            ),
            html.P(
                ven_cus_emp[-1],
                style={
                    "textAlign": "center",
                    "color": "orange",
                    "fontSize": 20,
                },
            ),
            html.P(
                "Data Management",
                style={
                    "textAlign": "center",
                    "color": "orange",
                    "fontSize": 20,
                },
            ),
        ]

    else:
        return [
            html.H6(
                children="Used for",
                style={
                    "textAlign": "center",
                    "color": "white",
                },
            ),
            html.P(
                ven_cus_emp[0:2],
                style={
                    "textAlign": "center",
                    "color": "orange",
                    "fontSize": 20,
                },
            ),
            html.P(
                "Data Management",
                style={
                    "textAlign": "center",
                    "color": "orange",
                    "fontSize": 20,
                },
            ),
        ]


############################################   MODAL1 #################################################


@app.callback(
    Output("dropdown", "options"),
    [
        Input("tools", "value"),
    ],
    [
        Input("data", "value"),
    ],
    [Input("select", "value")],
)
def output(tools, data, select):

    dff = dash_data(tools, data)
    dff = dff[
        ["MDM SOLUTION", "ERP", "COMPANY CODE", "COUNTRY", "ENTITY NAME", "MASTER DATA"]
    ]

    if select is None:
        options = list(set(dff["MDM SOLUTION"]))
        return [{"label": i, "value": i} for i in options]

    options = list(set(dff[select]))
    return [{"label": i, "value": i} for i in options]


@app.callback(
    Output("table", "children"),
    [
        Input("tools", "value"),
    ],
    [
        Input("data", "value"),
    ],
    [Input("select", "value")],
    [Input("dropdown", "value")],
)
def output_table(tools, data, select, dropdown):

    dff = dash_data(tools, data)
    dff = dff[
        ["MDM SOLUTION", "ERP", "COMPANY CODE", "COUNTRY", "ENTITY NAME", "MASTER DATA"]
    ]

    if select is not None:
        if dropdown is not None:
            dff1 = dff[dff[select].str.contains("|".join(dropdown), na=False)]

            return [
                dbc.Table.from_dataframe(dff1, striped=True, bordered=True, hover=True)
            ]


@app.callback(
    Output("modal1", "is_open"),
    [
        Input("text1", "n_clicks"),
        Input("close1", "n_clicks"),
    ],
    [State("modal1", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


############################################   TEXT2 #################################################


@app.callback(
    Output("text2", "children"), [Input("tools", "value")], [Input("data", "value")]
)
def update_text2(tools, data):
    Countries = dash_data(tools, data)
    Countries = Countries["COUNTRY"].unique()

    return [
        html.H6(
            children="Implemented in ",
            style={
                "textAlign": "center",
                "color": "white",
            },
        ),
        html.P(
            len(Countries),
            style={
                "textAlign": "center",
                "color": "white",
            },
        ),
        html.P(
            len(Countries),
            style={
                "textAlign": "center",
                "color": "orange",
                "fontSize": 40,
            },
        ),
        html.P(
            " Countries",
            style={
                "textAlign": "center",
                "color": "orange",
                "fontSize": 20,
            },
        ),
    ]


############################################   MODAL2 #################################################


@app.callback(
    Output("data2", "children"),
    [
        Input("tools", "value"),
    ],
    [
        Input("data", "value"),
    ],
)
def data2(tools, data):
    dff = dash_data(tools, data)
    dff = dff[["MDM SOLUTION", "COUNTRY", "MASTER DATA"]]

    if tools == "All":

        names = dff["MDM SOLUTION"].unique()

        def tabdata(number):
            dff1_tab = dff[dff["MDM SOLUTION"] == names[number]][
                ["MDM SOLUTION", "COUNTRY", "MASTER DATA"]
            ]

            scn_data_tab = pd.pivot_table(
                dff1_tab,
                values=("COUNTRY"),
                index=["MDM SOLUTION", "MASTER DATA", "COUNTRY"],
                aggfunc="count",
            ).reset_index()

            scn_tab = dff1_tab["COUNTRY"].unique()

            return [
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H6(
                                                    children="IMPLEMENTED FOR ",
                                                    style={
                                                        "textAlign": "center",
                                                        "color": "white",
                                                        "fontSize": 25,
                                                    },
                                                ),
                                                html.P(
                                                    f"{len(scn_tab)} COUNTRY(ies)",
                                                    style={
                                                        "textAlign": "center",
                                                        "color": "#09F3F0",
                                                        "fontSize": 35,
                                                    },
                                                ),
                                            ]
                                        )
                                    )
                                ),
                            ]
                        ),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Table.from_dataframe(
                                    scn_data_tab,
                                    striped=True,
                                    bordered=True,
                                    hover=True,
                                )
                            ]
                        ),
                    ]
                )
            ]

        tabs = []
        for num in range(len(names)):
            tabs.append(
                dbc.Tab(
                    label=names[num], tab_id=f"tab_{num + 1}", children=tabdata(num)
                )
            )

        return [
            dbc.Container(
                [
                    html.Hr(),
                    dbc.Tabs(
                        children=tabs,
                        active_tab="tab_1",
                    ),
                ]
            )
        ]
    else:

        dff = pd.pivot_table(
            dff,
            values=("COUNTRY"),
            index=["MDM SOLUTION", "MASTER DATA", "COUNTRY"],
            aggfunc="count",
        ).reset_index()

        return [
            dbc.Table.from_dataframe(
                dff,
            )
        ]


@app.callback(
    Output("modal2", "is_open"),
    [
        Input("text2", "n_clicks"),
        Input("close2", "n_clicks"),
    ],
    [State("modal2", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


############################################   TEXT3 #################################################


@app.callback(
    Output("text3", "children"), [Input("tools", "value")], [Input("data", "value")]
)
def update_text3(tools, data):

    BUs = dash_data(tools, data)
    BUs = BUs["ERP"].unique()

    return [
        html.H6(
            children="Implemented in ",
            style={
                "textAlign": "center",
                "color": "white",
            },
        ),
        html.P(
            len(BUs),
            style={
                "textAlign": "center",
                "color": "orange",
                "fontSize": 40,
            },
        ),
        html.P(
            "BU / ERP",
            style={
                "textAlign": "center",
                "color": "orange",
                "fontSize": 20,
            },
        ),
    ]


############################################   MODAL3 #################################################


@app.callback(
    Output("data3", "children"),
    [
        Input("tools", "value"),
    ],
    [
        Input("data", "value"),
    ],
)
def data3(tools, data):
    dff = dash_data(tools, data)
    dff = dff[["MDM SOLUTION", "ERP", "MASTER DATA"]]

    if tools == "All":
        names = dff["MDM SOLUTION"].unique()

        def tabdata(number):
            dff1_tab = dff[dff["MDM SOLUTION"] == names[number]][
                ["MDM SOLUTION", "ERP", "MASTER DATA"]
            ]

            scn_data_tab = pd.pivot_table(
                dff1_tab,
                values=("ERP"),
                index=["MDM SOLUTION", "MASTER DATA", "ERP"],
                aggfunc="count",
            ).reset_index()

            scn_tab = dff1_tab["ERP"].unique()

            return [
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H6(
                                                    children="IMPLEMENTED FOR ",
                                                    style={
                                                        "textAlign": "center",
                                                        "color": "white",
                                                        "fontSize": 25,
                                                    },
                                                ),
                                                html.P(
                                                    f"{len(scn_tab)} ERP(s)",
                                                    style={
                                                        "textAlign": "center",
                                                        "color": "#09F3F0",
                                                        "fontSize": 35,
                                                    },
                                                ),
                                            ]
                                        )
                                    )
                                ),
                            ]
                        ),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Table.from_dataframe(
                                    scn_data_tab,
                                    striped=True,
                                    bordered=True,
                                    hover=True,
                                )
                            ]
                        ),
                    ]
                )
            ]

        tabs = []
        for num in range(len(names)):
            tabs.append(
                dbc.Tab(
                    label=names[num], tab_id=f"tab_{num + 1}", children=tabdata(num)
                )
            )

        return [
            dbc.Container(
                [
                    html.Hr(),
                    dbc.Tabs(
                        children=tabs,
                        active_tab="tab_1",
                    ),
                ]
            )
        ]
    else:

        dff = pd.pivot_table(
            dff,
            values=("ERP"),
            index=["MDM SOLUTION", "MASTER DATA", "ERP"],
            aggfunc="count",
        ).reset_index()

        return [dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True)]


@app.callback(
    Output("modal3", "is_open"),
    [Input("text3", "n_clicks"), Input("close3", "n_clicks")],
    [State("modal3", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


############################################   TEXT4 #################################################


@app.callback(
    Output("text4", "children"), [Input("tools", "value")], [Input("data", "value")]
)
def update_text4(tools, data):
    Entities = dash_data(tools, data)
    Entities = Entities["COMPANY CODE"].unique()

    return [
        html.H6(
            children="Implemented in ",
            style={
                "textAlign": "center",
                "color": "white",
            },
        ),
        html.P(
            len(Entities),
            style={
                "textAlign": "center",
                "color": "white",
            },
        ),
        html.P(
            len(Entities),
            style={
                "textAlign": "center",
                "color": "orange",
                "fontSize": 40,
            },
        ),
        html.P(
            " Entities",
            style={
                "textAlign": "center",
                "color": "orange",
                "fontSize": 20,
            },
        ),
    ]


############################################   MODAL4 #################################################


@app.callback(
    Output("data4", "children"),
    [
        Input("tools", "value"),
    ],
    [
        Input("data", "value"),
    ],
)
def data4(tools, data):
    dff = dash_data(tools, data)
    dff = dff[["MDM SOLUTION", "COMPANY CODE", "MASTER DATA"]]

    if tools == "All":
        names = dff["MDM SOLUTION"].unique()

        def tabdata(number):
            dff1_tab = dff[dff["MDM SOLUTION"] == names[number]][
                ["MDM SOLUTION", "COMPANY CODE", "MASTER DATA"]
            ]

            scn_data_tab = pd.pivot_table(
                dff1_tab,
                values=("COMPANY CODE"),
                index=["MDM SOLUTION", "MASTER DATA", "COMPANY CODE"],
                aggfunc="count",
            ).reset_index()

            scn_tab = dff1_tab["COMPANY CODE"].unique()

            return [
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H6(
                                                    children="IMPLEMENTED FOR ",
                                                    style={
                                                        "textAlign": "center",
                                                        "color": "white",
                                                        "fontSize": 25,
                                                    },
                                                ),
                                                html.P(
                                                    f"{len(scn_tab)} COMPANY CODE(s)",
                                                    style={
                                                        "textAlign": "center",
                                                        "color": "#09F3F0",
                                                        "fontSize": 35,
                                                    },
                                                ),
                                            ]
                                        )
                                    )
                                ),
                            ]
                        ),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Table.from_dataframe(
                                    scn_data_tab,
                                    striped=True,
                                    bordered=True,
                                    hover=True,
                                )
                            ]
                        ),
                    ]
                )
            ]

        tabs = []
        for num in range(len(names)):
            tabs.append(
                dbc.Tab(
                    label=names[num], tab_id=f"tab_{num + 1}", children=tabdata(num)
                )
            )

        return [
            dbc.Container(
                [
                    html.Hr(),
                    dbc.Tabs(
                        children=tabs,
                        active_tab="tab_1",
                    ),
                ]
            )
        ]
    else:
        dff = pd.pivot_table(
            dff,
            values=("COMPANY CODE"),
            index=["MDM SOLUTION", "MASTER DATA", "COMPANY CODE"],
            aggfunc="count",
        ).reset_index()
        return [dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True)]


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


@app.callback(Output("pie_chart", "figure"), [Input("tools", "value")])
def update_graph(tools):
    labels = list(Counter(df["MDM SOLUTION"]).keys())
    values = list(Counter(df["MDM SOLUTION"]).values())
    colors = ["#ff7c43", "#3d708f", "#d45087", "#a05195", "#6b9e3c"]

    line_color = []
    pull = []
    for tool in labels:
        if tool == tools:
            pull.append(0.1)
            line_color.append("white")
        else:
            pull.append(0)
            line_color.append("#1f2c56")

    return {
        "data": [
            go.Pie(
                labels=labels,
                values=values,
                pull=pull,
                marker=dict(colors=colors, line=dict(color=line_color, width=2)),
                hoverinfo="label+value+percent",
                textinfo="label+value",
                textfont=dict(size=1, color="#1f2c56"),
                textposition="outside",
                hole=0.3,
                rotation=45
                # insidetextorientation='radial',
            )
        ],
        "layout": go.Layout(
            # width=800,
            # height=520,
            plot_bgcolor="#1f2c56",
            paper_bgcolor="#1f2c56",
            hovermode="closest",
            title={
                "text": "MDM Solutions",
                "y": 0.93,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            titlefont={"color": "white", "size": 25},
            legend={
                "orientation": "h",
                "bgcolor": "#1f2c56",
                "xanchor": "center",
                "x": 0.5,
                "y": -0.010,
            },
            font=dict(family="Computer Modern", size=17, color="white"),
        ),
    }


############################################ MAP #################################################


@app.callback(
    Output("map", "figure"),
    Input("tools", "value"),
)
def updateGraphCB(tools):
    # filter traces...
    if tools == "All":
        fig = interactive_multi_plot(df1, df2, df3).update_traces(visible=True)
        return fig
    else:
        fig = interactive_multi_plot(df1, df2, df3).update_traces(visible=False)
        fig.update_traces(visible=True, selector={"meta": tools})
        return fig


############################################ DOWNLOAD EXCEL #################################################


@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    dwnld = df[
        [
            "MDM SOLUTION",
            "MASTER DATA",
            "ERP",
            "COMPANY CODE",
            "ENTITY NAME",
            "COUNTRY",
            "FINTECH",
        ]
    ]
    return dcc.send_data_frame(
        dwnld.to_excel, "MDM_DATA.xlsx", sheet_name="MDM_2022", index=False
    )


if __name__ == "__main__":
    app.run_server(port="8501")
