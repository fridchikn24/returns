import pandas as pd
from dash import Dash, Input, Output,dcc, html





data = (
    pd.read_csv("returns.csv")
    #.query("HOWTOFINDUS == 'ebay'")
    .assign(Date=lambda data: pd.to_datetime(data["year-month"], format="%Y-%m"))
    .sort_values(by="Date")
)
data["vendors"].fillna("blank",inplace=True)

vendors = data["vendors"].sort_values().unique()
#print(vendors)
#print(data["Date"].head(10))

app = Dash(__name__)


app.layout = html.Div(
    children=[
        html.H1(children="Total returns by marketplace"),
        html.P(
            children=(
               
            ),
        ),
        html.Div(
            children = [
                html.Div(
             children=[
                html.Div(children="Vendor", className="menu-title"),
                dcc.Dropdown(
                    id="vendor-filter",
                    options=[
                    {"label": vendor, "value": vendor}
                    for vendor in vendors
                    ] ,#+ [{'label': 'All', 'value': 'All'}],
                    value="ebay",
                    clearable=False,
                    className="dropdown",
        ),
            ]
        ),
         html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["Date"].min().date(),
                            max_date_allowed=data["Date"].max().date(),
                            start_date=data["Date"].min().date(),
                            end_date=data["Date"].max().date(),
                        ),
                    ]
                ),
            ],
            className="dropdown",
        ),

        html.Div(
            children=[
            html.Div(
                children=dcc.Graph(
                    id = "returns",
                    config={'displayModeBar': True}
                          ),
                className="card",
                ),
            ],
            className = 'wrapper',
        ),
        
    ]
)
@app.callback(
    Output("returns","figure"),
    Input("vendor-filter","value"),
    Input("date-range","start_date"),
    Input("date-range","end_date")
    )

def update_charts(vendors,start_date,end_date):
    filtered_data = data.query(
        "vendors == @vendors  and Date >= @start_date and Date <= @end_date")

    returns_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["returns"],
                "type": "bar",
                "hovertemplate": '<br>'.join([ ":%{y:.2f}<extra></extra>",'Date:%{x}'])
            },
        ]
    }
    return(returns_figure)


if __name__ == "__main__":
    app.run_server(debug=False)