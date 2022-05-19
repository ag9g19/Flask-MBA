import pandas as pd
import dash
from dash import dash_table
from dash import html
from dash import dcc
from .data import (
    create_dataframe,
    process_bakery,
    items_by_day,
    items_by_month,
    pre_processing,
)
from .layout import html_layout


import plotly.express as px


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(server=server, routes_pathname_prefix="/dashapp/",)

    df = create_dataframe()
    analysis_data = df.copy()
    data = df.copy()

    lift = pre_processing(analysis_data, "lift", 1)
    support = pre_processing(analysis_data, "support", 0.03)
    confidence = pre_processing(analysis_data, "confidence", 0.03)

    items_count = process_bakery(data)
    per_day = items_by_day(data)
    per_month = items_by_month(data)

    # most selling
    fig = px.bar(
        items_count.head(20),
        title="20 Most Selling Items",
        color=items_count.head(20),
        color_continuous_scale=px.colors.sequential.Mint,
    )
    fig.update_layout(
        margin=dict(t=50, b=0, l=0, r=0),
        titlefont=dict(size=20),
        xaxis_tickangle=-45,
        plot_bgcolor="white",
        coloraxis_showscale=False,
    )
    fig.update_yaxes(showticklabels=False, title=" ")
    fig.update_xaxes(title=" ")
    fig.update_traces(
        texttemplate="%{y}",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>No. of Transactions: %{y}",
    )

    # least selling
    figs = px.bar(
        items_count.nsmallest(20),
        title="20 Least Selling Items",
        color=items_count.head(20),
        color_continuous_scale=px.colors.sequential.Mint,
    )
    figs.update_layout(
        margin=dict(t=50, b=0, l=0, r=0),
        titlefont=dict(size=20),
        xaxis_tickangle=-45,
        plot_bgcolor="white",
        coloraxis_showscale=False,
    )
    figs.update_yaxes(showticklabels=False, title=" ")
    figs.update_xaxes(title=" ")
    figs.update_traces(
        texttemplate="%{y}",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>No. of Transactions: %{y}",
    )

    # items per day
    figt1 = px.bar(
        per_day,
        title="Most Productive Day",
        color=per_day,
        color_continuous_scale=px.colors.sequential.Mint,
    )
    figt1.update_layout(
        margin=dict(t=50, b=0, l=0, r=0),
        titlefont=dict(size=20),
        xaxis_tickangle=0,
        plot_bgcolor="white",
        coloraxis_showscale=False,
    )
    figt1.update_yaxes(showticklabels=False, title=" ")
    figt1.update_xaxes(title=" ")
    figt1.update_traces(
        texttemplate="%{y}",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>No. of Transactions: %{y}",
    )

    # items per month
    figt2 = px.bar(
        per_month,
        title="Most Productive Month",
        color=per_month,
        color_continuous_scale=px.colors.sequential.Mint,
    )
    figt2.update_layout(
        margin=dict(t=50, b=0, l=0, r=0),
        titlefont=dict(size=20),
        xaxis_tickangle=0,
        plot_bgcolor="white",
        coloraxis_showscale=False,
    )
    figt2.update_yaxes(showticklabels=False, title=" ")
    figt2.update_xaxes(title=" ")
    figt2.update_traces(
        texttemplate="%{y}",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>No. of Transactions: %{y}",
    )

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            html.H1("Bakery.csv"),
            create_data_table(df),
            dcc.Graph(figure=fig),
            dcc.Graph(figure=figs),
            dcc.Graph(figure=figt1),
            dcc.Graph(figure=figt2),
            html.H1("Association rules for metric LIFT"),
            html.P(
                "Lift indicates whether there is a relationship between the antecendent and the consequent, or whether the two items are occuring together in the same orders simply by chance (ie: at random). In other words we get know how many more times the antecedent and consequent actually appear in the same order, compared to if there was no relationship between them. The greater the lift is, the higher is the possibility that the two items appear together in the same order."
            ),
            create_lift_table(lift),
            html.H1("Association rules for metric SUPPORT"),
            html.P(
                "This is the percentage of transactions that contain both items. The minimum support threshold required by apriori can be set based on knowledge of the specific dataset."
            ),
            create_support_table(support),
            html.H1("Association rules for metric CONFIDENCE"),
            html.P(
                "Given two items, antecedent and consequent, confidence measures the percentage of times that the consequent is purchased, given that the antecedent was purchased. Confidence values range from 0 to 1, where 0 indicates that the consequent is never purchased when the antecedent is purchased, and 1 indicates that the consequent is always purchased whenever the antecedent is purchased."
            ),
            create_confidence_table(confidence),
            html.P(
                "To download the report as a PDF, press 'Command + p' on Mac or 'Ctrl + p' on Windows and then select from the dropdown menu 'Save as PDF' and click the 'Save' button!"
            ),
        ],
        id="dash-container",
    )
    return dash_app.server


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id="database-table",
        columns=[{"name": i, "id": i, "selectable": True} for i in df.columns],
        data=df.to_dict("records"),
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        row_selectable="single",
        page_current=0,
        page_size=10,
        style_cell={
            "minWidth": 95,
            "maxWidth": 95,
            "width": 95,
            "whiteSpace": "normal",
        },
        style_header={"backgroundColor": "white", "fontWeight": "bold"},
        style_cell_conditional=[
            {
                "if": {"column_id": "TransactionNo"},
                "width": "20%",
                "textAlign": "right",
            },
            {"if": {"column_id": "Items"}, "width": "40%", "textAlign": "right"},
            {"if": {"column_id": "date"}, "width": "40%", "textAlign": "right"},
        ],
    )
    return table


def create_lift_table(lift):
    table = dash_table.DataTable(
        id="lift-datatable",
        columns=[{"name": i, "id": i, "selectable": True} for i in lift.columns],
        data=lift.to_dict("records"),
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        row_selectable="single",
        page_current=0,
        page_size=10,
        style_cell={
            "minWidth": 95,
            "maxWidth": 95,
            "width": 95,
            "whiteSpace": "normal",
        },
        style_header={"backgroundColor": "white", "fontWeight": "bold"},
    )

    return table


def create_support_table(support):
    table = dash_table.DataTable(
        id="support-datatable",
        columns=[{"name": i, "id": i, "selectable": True} for i in support.columns],
        data=support.to_dict("records"),
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        row_selectable="single",
        page_current=0,
        page_size=10,
        style_cell={
            "minWidth": 95,
            "maxWidth": 95,
            "width": 95,
            "whiteSpace": "normal",
        },
        style_header={"backgroundColor": "white", "fontWeight": "bold"},
    )

    return table


def create_confidence_table(confidence):
    table = dash_table.DataTable(
        id="confidence-datatable",
        columns=[{"name": i, "id": i, "selectable": True} for i in confidence.columns],
        data=confidence.to_dict("records"),
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        row_selectable="single",
        page_current=0,
        page_size=10,
        style_cell={
            "minWidth": 95,
            "maxWidth": 95,
            "width": 95,
            "whiteSpace": "normal",
        },
        style_header={"backgroundColor": "white", "fontWeight": "bold"},
    )

    return table
