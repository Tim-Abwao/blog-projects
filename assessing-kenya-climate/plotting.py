import json
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame, Series
from plotly.subplots import make_subplots

from utils import get_extremes, get_extremes_style

# Load geo-json for maps
with open("kenya_regions.geojson") as file:
    kenya_provinces = json.load(file)


def customize_figure(fig: go.Figure) -> go.Figure:
    """Update the font style, plot background, axes labels, and more.

    Args:
        fig (plotly.graph_objs._figure.Figure): Figure to edit.

    Returns:
        plotly.graph_objs._figure.Figure: Customized figure.
    """
    fig.update_layout(
        font_family="serif",
        plot_bgcolor="#fff",
        titlefont=dict(size=18, color="#444"),
        title_x=0.1,
    )
    fig.update_xaxes(fixedrange=True, title_font_size=16)
    fig.update_yaxes(fixedrange=True, title_font_size=16)
    return fig


def customize_cartesian_plot(fig: go.Figure) -> go.Figure:
    """Update the hover-mode and margin specifically for cartesian plots e.g.
    line-plots & bar-plots; further to `customize figure`.

    Args:
        fig (plotly.graph_objs._figure.Figure): Figure to edit.

    Returns:
        plotly.graph_objs._figure.Figure: Updated figure.
    """
    fig = customize_figure(fig)
    fig.update_layout(
        hovermode="x unified",
        margin={"l": 60, "t": 60, "r": 10, "b": 10},
    )
    return fig


def comparative_bar(
    data: DataFrame,
    color_sequence: list,
    title: str,
    legend_title_text: str,
    unit: str,
    x_label: str,
    y_label: str,
) -> go.Figure:
    """Create a comparative bar plot using the provided `data`.

    Args:
        data (pandas.DataFrame): Values to plot.
        color_sequence (list): Colors to apply to groups.
        title (str): Graph title.
        legend_title_text (str): Title for the legend.
        unit (str): Metric/empirical unit for values.
        x_label (str): X-axis label.
        y_label (str): Y-axis label.

    Returns:
        plotly.graph_objs._figure.Figure: A comparative bar plot.
    """
    fig = px.bar(
        data,
        barmode="group",
        color_discrete_sequence=color_sequence,
    )
    fig.update_traces(hovertemplate=f"<b>%{{y:.1f}}{unit}</b>")
    fig.update_layout(legend_title_text=legend_title_text, title=title)
    fig.update_xaxes(title=x_label)
    fig.update_yaxes(title=f"{y_label} ({unit})")
    return customize_cartesian_plot(fig)


def line_plot(
    data: Series,
    line_color: str,
    marker_colorscale: str,
    max_color: str,
    min_color: str,
    hover_text: str,
    title: str,
    unit: str,
    x_label: str,
    y_label: str,
) -> go.Figure:
    """Get a line-plot with extreme values highlighted, and a horizontal
    dotted line at the average value.

    Args:
        data (pandas.Series): Values to plot.
        line_color (str): Color for the line-plot.
        marker_colorscale (str): Colorscale for marker values.
        max_color (str): Color for the maximum value(s) marker & label.
        min_color (str): Color for the minimum value(s) marker & label.
        hover_text (str): Text to display on hover.
        title (str): Graph title.
        unit (str): Metric/empirical unit for values.
        x_label (str): X-axis label.
        y_label (str): Y-axis label.

    Returns:
        plotly.graph_objs._figure.Figure: A line-plot.
    """
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

    # Add horizontal line at the mean value
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


def choropleth_map(
    data: Series, color_scale: str, title: str, unit: str
) -> go.Figure:
    """Get a choropleth map of Kenya's regions (provinces).

    Args:
        data (pandas.Series): Values to plot.
        color_scale (str): Colorscale for values.
        title (str): Graph title.
        unit (str): Metric/empirical unit for values

    Returns:
        plotly.graph_objs._figure.Figure: A choropleth map.
    """
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
        dragmode=False,
        margin={"r": 0, "t": 60, "l": 0, "b": 0},
        title=title,
    )
    return customize_figure(fig)


def climate_plot(
    precipitation_data: DataFrame, temperature_data: DataFrame
) -> go.Figure:
    """Get a sub-plot pair of temperature(lines) and precipitation(bars) data
    for periods 1961-1990 and 1991-2020.

    Args:
        precipitation_data (DataFrame): Precipitation climatology data.
        temperature_data (DataFrame): Temperature climatology data.

    Returns:
        plotly.graph_objs._figure.Figure: Graph of climate data.
    """
    fig = make_subplots(
        rows=2,
        shared_xaxes=True,
        specs=[[{"secondary_y": True}], [{"secondary_y": True}]],
        subplot_titles=("1961-1990", "1991-2020"),
    )

    for idx, period in enumerate(["1961-1990", "1991-2020"], start=1):
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

    fig.update_layout(
        margin={"l": 60, "t": 60, "r": 10, "b": 10},
        showlegend=False,
        title_text="Kenya's Climate",
        xaxis_showticklabels=True,
        xaxis2_title_text="Month",
    )
    fig.update_traces(hovertemplate="<b>%{x}</b>: %{y}")
    fig.update_yaxes(title_text="Precipitation (mm)", secondary_y=False)
    fig.update_yaxes(title_text="Temperature (&deg;C)", secondary_y=True)
    return customize_figure(fig)


def savefig(fig: go.Figure, destination_dir: Path, filename: str) -> None:
    """Write the figure to a html file named `filename` in the specified
    `destination_dir`.

    Args:
        fig (plotly.graph_objs._figure.Figure): Figure to save.
        destination_dir (Path): Folder to save the figure in.
        filename (str): Desired file name for the saved figure.
    """
    fig.write_html(
        destination_dir / filename,
        config={"displayModeBar": False},
        include_plotlyjs="cdn",
    )
