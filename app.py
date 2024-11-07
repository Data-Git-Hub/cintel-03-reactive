import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
import seaborn as sns
import matplotlib.pyplot as plt
from shiny import render, reactive

# Load the palmerpenguins dataset
penguins = load_penguins()

# Set up the UI with tabs and sidebar layout
ui.page_opts(title="Penguins are Cool", fillable=True)

with ui.navset_pill(id="tab"):
    # Graphics tab with sidebar layout
    with ui.nav_panel("Graphics"):
        with ui.layout_sidebar():
            with ui.sidebar(open="open", bg="#f8f8f8"):
                ui.h2("Sidebar")
                ui.input_slider(
                    "slider", "Max Bill Length (mm)", min=33, max=60, value=45
                )
                ui.input_selectize(
                    "selected_attribute",
                    "Choose an Attribute",
                    [
                        "bill_length_mm",
                        "bill_depth_mm",
                        "flipper_length_mm",
                        "body_mass_g",
                    ],
                )
                ui.input_numeric("plotly_bin_count", "Number of Plotly Bins", value=10)
                ui.hr()
                ui.input_slider(
                    "seaborn_bin_count",
                    "Number of Seaborn Bins",
                    min=5,
                    max=50,
                    value=20,
                )
                ui.input_checkbox_group(
                    "selected_species_list",
                    "Select Species to Display in Scatterplot",
                    ["Adelie", "Gentoo", "Chinstrap"],
                    selected=["Adelie", "Gentoo", "Chinstrap"],
                    inline=True,
                )
                ui.hr()
                ui.a(
                    "Data-Git-Hub",
                    href="https://github.com/Data-Git-Hub",
                    target="_blank",
                )

            # Main content area for plots
            with ui.layout_columns():
                with ui.card():
                    ui.card_header("Penguins Bill Length Histogram")

                    @render_plotly
                    def plot1():
                        fig = px.histogram(
                            penguins[penguins["bill_length_mm"] <= input.slider()],
                            x="bill_length_mm",
                            title="Penguins Bill Length Histogram",
                        )
                        fig.update_traces(
                            marker_line_color="black", marker_line_width=1.5
                        )
                        return fig

                with ui.card():
                    ui.card_header("Penguins Attribute Histogram")

                    @render_plotly
                    def plot2():
                        selected_attribute = input.selected_attribute()
                        bin_count = (
                            input.plotly_bin_count()
                            if input.plotly_bin_count()
                            else None
                        )
                        fig = px.histogram(
                            penguins,
                            x=selected_attribute,
                            title=f"Penguins {selected_attribute.replace('_', ' ').title()} Histogram",
                            nbins=bin_count,
                            color_discrete_sequence=["red"],
                        )
                        fig.update_traces(
                            marker_line_color="black", marker_line_width=1.5
                        )
                        return fig

            with ui.layout_columns():
                with ui.card():
                    ui.card_header("Seaborn Histogram")

                    @render.plot
                    def plot3():
                        fig, ax = plt.subplots()
                        sns.histplot(
                            data=penguins,
                            x="bill_length_mm",  # Fixed attribute for Seaborn histogram
                            bins=input.seaborn_bin_count(),
                            hue="species",
                            multiple="stack",
                            ax=ax,
                        )
                        ax.set_title("Palmer Penguins by Species")
                        ax.set_xlabel("Bill Length (mm)")
                        ax.set_ylabel("Number")
                        return fig

                with ui.card():
                    ui.card_header("Plotly Scatterplot: Species")

                    @render_plotly
                    def plotly_scatterplot():
                        filtered_penguins = penguins[
                            penguins["species"].isin(input.selected_species_list())
                        ]
                        fig = px.scatter(
                            filtered_penguins,
                            x="body_mass_g",
                            y="bill_depth_mm",
                            color="species",
                            title="Penguins Scatterplot: Body Mass vs. Bill Depth",
                            labels={
                                "body_mass_g": "Body Mass (g)",
                                "bill_depth_mm": "Bill Depth (mm)",
                            },
                        )
                        return fig

    # Data tab with sidebar for filtering data and display as Plotly Table
    with ui.nav_panel("Data"):
        with ui.layout_sidebar():
            with ui.sidebar():
                ui.h2("Sidebar")  # Header for the sidebar
                ui.input_slider(
                    "bill_length_slider",
                    "Filter by Bill Length (mm)",
                    min=33,
                    max=60,
                    value=45,
                )
                ui.input_slider(
                    "flipper_length_slider",
                    "Filter by Flipper Length (mm)",
                    min=170,
                    max=230,
                    value=200,
                )

            # Main content area with Plotly Tables
            with ui.layout_columns():
                with ui.card():
                    ui.card_header("Filtered Penguins Table")

                    @render_plotly
                    def penguins_table():
                        filtered_data_table = penguins[
                            penguins["bill_length_mm"] <= input.bill_length_slider()
                        ]
                        fig = px.histogram(
                            filtered_data_table,
                            x="bill_length_mm",
                            title="Filtered Penguins Table by Bill Length",
                        )
                        return fig

                with ui.card():
                    ui.card_header("Filtered Penguins Grid")

                    @render_plotly
                    def penguins_grid():
                        filtered_data_grid = penguins[
                            penguins["flipper_length_mm"]
                            <= input.flipper_length_slider()
                        ]
                        fig = px.histogram(
                            filtered_data_grid,
                            x="flipper_length_mm",
                            title="Filtered Penguins Grid by Flipper Length",
                        )
                        return fig
