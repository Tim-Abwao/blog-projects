import plotly.graph_objects as go
import plotly.express as px
from utils import get_extremes, get_extremes_style
import json
from plotly.subplots import make_subplots


# Load geo-json for maps
with open("kenya_regions.geojson") as file:
    kenya_provinces = json.load(file)


def customize_figure(fig):
    fig.update_layout(
        font_family="serif",
        plot_bgcolor="#fff",
        titlefont_size=18,
        title_x=0.5,
    )
    fig.update_xaxes(fixedrange=True, title_font_size=16)
    fig.update_yaxes(fixedrange=True, title_font_size=16)
    return fig


def customize_cartesian_plot(fig):
    fig = customize_figure(fig)
    fig.update_layout(
        hovermode="x unified",
        margin={"l": 60, "t": 40, "r": 10, "b": 10},
    )
    return fig


def comparative_bar(
    data, title: str, unit: str, x_label, y_label: str, color_sequence: list
):
    fig = px.bar(
        data,
        barmode="group",
        color_discrete_sequence=color_sequence,
    )
    fig.update_traces(hovertemplate=f"<b>%{{y:.1f}}{unit}</b>")
    fig.update_layout(legend_title_text="Period", title=title)
    fig.update_xaxes(title=x_label)
    fig.update_yaxes(title=f"{y_label} ({unit})")
    return customize_cartesian_plot(fig)


def line_plot(
    data,
    title: str,
    line_color: str,
    max_color: str,
    min_color: str,
    marker_colorscale: str,
    hover_text: str,
    x_label: str,
    y_label: str,
    unit: str,
):

    fig = go.Figure(
        go.Scatter(
            x=data.index,
            y=data,
            line={"color": line_color},
            mode="lines+markers",
            marker={
                "color": data,
                "colorscale": marker_colorscale,
                "size": 5,
                "symbol": "diamond",
            },
            hovertemplate=f"<i>{hover_text}</i>: <b>%{{y:.2f}}{unit}</b><extra></extra>",
            showlegend=False,
        )
    )
    # Plot labelled markers at the maximum and minimum
    temp_extremes = get_extremes(data)
    fig.add_trace(
        go.Scatter(
            x=temp_extremes.index,
            y=temp_extremes,
            mode="markers+text",
            marker={
                "color": get_extremes_style(
                    temp_extremes, max_color, min_color
                ),
                "size": 8,
                "symbol": "x",
            },
            text=get_extremes_style(temp_extremes),
            textposition=get_extremes_style(
                temp_extremes, "top center", "bottom center"
            ),
            textfont={
                "color": get_extremes_style(
                    temp_extremes, max_color, min_color
                )
            },
            hovertemplate=f"<i>%{{text}}:</i> %{{y}}{unit} (%{{x}})<extra></extra>",
            showlegend=False,
        )
    )

    fig.add_hline(
        y=data.mean(),
        line_dash="dot",
        line_color="#aaa",
        annotation=dict(text=f"Mean ({data.mean():.1f}{unit})"),
    )
    fig.update_layout(title=title)
    fig.update_xaxes(title_text=x_label)
    fig.update_yaxes(title_text=y_label)
    return customize_cartesian_plot(fig)


def choropleth_map(data, color_scale: str, title: str, unit: str):
    fig = px.choropleth(
        data,
        locations=data.index,
        color=data,
        color_continuous_scale=color_scale,
        geojson=kenya_provinces,
        featureidkey="properties.name_1",
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_coloraxes(
        colorbar=dict(
            len=0.5,
            thickness=0.03,
            thicknessmode="fraction",
            tickfont_size=9,
            title="",
        )
    )
    fig.update_traces(
        hovertemplate=(
            f"<i>%{{location}}:</i> <b>%{{z:.1f}}{unit}</b><extra></extra>"
        )
    )
    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        dragmode=False,
        title=title,
    )
    return customize_figure(fig)


def climate_plot(precipitation_data, temperature_data):
    fig = make_subplots(
        rows=2,
        shared_xaxes=True,
        specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
        subplot_titles=("1961-1990", "1991-2020"),
    )

    for idx, period in enumerate(["1961_1990", "1991_2020"], start=1):
        fig.add_trace(
            go.Bar(
                x=precipitation_data[period].columns,
                y=precipitation_data[period].mean(),
                name="Precipitation (1961-1990)",
            ),
            secondary_y=False,
            row=idx,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=temperature_data[period].columns,
                y=temperature_data[period].mean(),
                name="Temperature (1961-1990)",
            ),
            secondary_y=True,
            row=idx,
            col=1,
        )

    # Add figure title
    fig.update_layout(
        margin={"l": 60, "t": 60, "r": 10, "b": 10},
        showlegend=False,
        title_text="Kenya's Climate",
        xaxis_showticklabels=True,
        xaxis2_title_text="Month",
    )
    fig.update_traces(hovertemplate="<b>%{x}</b>: %{y}")

    # Set y-axes titles
    fig.update_yaxes(title_text="Precipitation (mm)", secondary_y=False)
    fig.update_yaxes(title_text="Temperature (&deg;C)", secondary_y=True)
    return customize_figure(fig)
