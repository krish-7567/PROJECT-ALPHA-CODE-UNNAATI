import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your cleaned dataset
data = pd.read_csv("cleaned_data.csv")

# Get unique phone models for dropdown options
all_models = sorted(data['model'].unique())

# --- Graph Analysis Dashboard Layout ---
def create_graph_analysis_layout():
    # Bar Chart: Smartphone Brand Popularity
    brand_counts = data["brand"].value_counts()
    bar_chart = px.bar(
        x=brand_counts.index,
        y=brand_counts.values,
        title="Smartphone Brand Popularity",
        labels={"x": "Brand", "y": "Number of Smartphones"},
        color_discrete_sequence=["#636EFA"]
    )

    # Heatmap: Ratings by Brand and Battery Capacity
    pivot_table = data.pivot_table(index="brand", columns="battery_capacity", values="ratings", aggfunc="mean")

    # Create Heatmap
    heatmap = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale="Viridis",  # Use a valid Plotly colorscale
        colorbar_title="Ratings"
    ))
    heatmap.update_layout(
        title="Ratings by Brand and Battery Capacity",
        xaxis_title="Battery Capacity (mAh)",
        yaxis_title="Brand"
    )


    # Scatter Plot: Ratings vs Price
    scatter_plot = px.scatter(
        data,
        x="discounted_price",
        y="ratings",
        title="Ratings vs Price",
        labels={"discounted_price": "Price (INR)", "ratings": "Ratings"},
        color="ratings",
        color_continuous_scale=px.colors.sequential.Plasma
    )

    # Histogram: Price Distribution
    histogram = px.histogram(
        data,
        x="discounted_price",
        nbins=20,
        title="Price Distribution of Smartphones",
        labels={"discounted_price": "Price (INR)"},
        color_discrete_sequence=["#FF851B"]
    )

    # Line Plot: Battery Capacity vs Price
    avg_prices = data.groupby("battery_capacity")["discounted_price"].mean()
    line_chart = px.line(
        x=avg_prices.index,
        y=avg_prices.values,
        title="Battery Capacity vs Price",
        labels={"x": "Battery Capacity (mAh)", "y": "Average Price (INR)"},
        markers=True
    )
    line_chart.update_traces(line_color="#0074D9") # Setting line color using update_traces

    # Pie Chart: Battery Type Distribution
    battery_counts = data["battery_type"].value_counts()
    pie_chart = px.pie(
        values=battery_counts.values,
        names=battery_counts.index,
        title="Battery Type Distribution",
        color_discrete_sequence=px.colors.qualitative.Prism
    )

    # Box Plot: Price Distribution by Brand
    box_plot = px.box(
        data,
        x="brand",
        y="discounted_price",
        title="Price Distribution by Brand",
        labels={"brand": "Brand", "discounted_price": "Price (INR)"},
        color="brand",
        color_discrete_sequence=px.colors.qualitative.Dark2
    )

    go_back_button = html.Div(style={"text-align": "center", "margin-top": "30px", "margin-bottom": "30px"})
    go_back_button.children = dcc.Link(html.Button("Go to Previous Page", style={"padding": "10px 20px", "font-size": "1.1em", "background-color": "#555", "color": "#fff", "border": "none", "border-radius": "5px", "cursor": "pointer"}), href='/')


    return html.Div([
        html.Div([
            html.H1("Flipkart Smartphone Dashboard", style={"text-align": "center", "margin-bottom": "10px", "font-family": "Segoe UI, sans-serif", "font-size": "4.0em", "color": "#eee", "text-transform": "uppercase"}),
            html.P("Interactive visualizations and insights about smartphone listings on Flipkart.", style={"font-size": "1.3em", "color": "#ccc", "text-align": "center", "font-family": "Roboto, sans-serif", "margin-bottom": "20px"})
        ], style={"padding": "20px 0", "background-color": "#111", "box-shadow": "0 2px 4px rgba(0, 0, 0, 0.5)"}),

        go_back_button, # Go to previous page button right after the title

        html.Div([
            html.H2("1. Smartphone Brand Popularity", style={"font-family": "Georgia, serif", "font-size": "2.4em", "color": "#ddd"}), # Increased font size
            html.P("This graph shows the number of smartphones listed for each brand. It helps identify the most dominant and least represented brands in the dataset. Use case: Useful for understanding brand presence or market dominance on Flipkart.", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}), # Added more padding-left
            dcc.Graph(figure=bar_chart, className="dash-graph"),
            html.P("Insights: Xiaomi leads in popularity with the highest number of listings. Realme is a strong second, followed by Samsung. A long tail of less represented brands indicates a fragmented market share.", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}) # Added more padding-left
        ], style={"margin-bottom": "50px", "background-color": "#222", "padding": "20px", "border-radius": "5px"}),

        html.Div([
            html.H2("2. Ratings by Brand and Battery Capacity", style={"font-family": "Georgia, serif", "font-size": "2.4em", "color": "#ddd"}), # Increased font size
            html.P("The heatmap highlights the average ratings across brands and battery capacity ranges. It helps identify patterns and preferences.", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}), # Added more padding-left
            dcc.Graph(figure=heatmap, className="dash-graph"),
            html.P("Insights: Some brands show higher average ratings for specific battery capacity ranges. Rating patterns vary across battery capacities for many brands. There might be 'sweet spots' for battery capacity that correlate with higher ratings.", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}) # Added more padding-left
        ], style={"margin-bottom": "50px", "background-color": "#222", "padding": "20px", "border-radius": "5px"}),

        html.Div([
            html.H2("3. Ratings vs Price", style={"font-family": "Georgia, serif", "font-size": "2.4em", "color": "#ddd"}), # Increased font size
            html.P("This plot shows how smartphone ratings vary with price. Patterns may reveal whether higher-priced phones consistently receive better ratings or if ratings are independent of cost.", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}), # Added more padding-left
            dcc.Graph(figure=scatter_plot, className="dash-graph"),
            html.P("Insights: Higher concentration of high ratings is observed in lower price ranges (below INR 40,000). Fewer high-rated phones appear at higher prices. Lower ratings are scattered across all price ranges, suggesting potential value for money in the budget segment.", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}) # Added more padding-left
        ], style={"margin-bottom": "50px", "background-color": "#222", "padding": "20px", "border-radius": "5px"}),

        html.Div([
            html.H2("4. Price Distribution", style={"font-family": "Georgia, serif", "font-size": "2.4em", "color": "#ddd"}), # Increased font size
            html.P("This graph displays the distribution of smartphone prices. Peaks in the histogram can reveal popular price ranges, while gaps indicate underrepresented price points.", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}), # Added more padding-left
            dcc.Graph(figure=histogram, className="dash-graph"),
            html.P("Insights: The majority of smartphones are priced below INR 20,000. The number of listings decreases as the price increases, indicating a competitive budget market and fewer options for premium buyers.", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}) # Added more padding-left
        ], style={"margin-bottom": "50px", "background-color": "#222", "padding": "20px", "border-radius": "5px"}),

        html.Div([
            html.H2("5. Battery Capacity vs Price", style={"font-family": "Georgia, serif", "font-size": "2.4em", "color": "#ddd"}), # Increased font size
            html.P("This graph demonstrates how battery capacity affects average smartphone prices. A positive correlation may suggest that higher battery capacities are valued more.", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}), # Added more padding-left
            dcc.Graph(figure=line_chart, className="dash-graph"),
            html.P("Insights: The average price fluctuates with increasing battery capacity, with a peak around 3500-4000 mAh. Prices stabilize for higher capacities, and lower average prices are observed for very low and very high battery capacities.", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}) # Added more padding-left
        ], style={"margin-bottom": "50px", "background-color": "#222", "padding": "20px", "border-radius": "5px"}),

        html.Div([
            html.H2("6. Battery Type Distribution", style={"font-family": "Georgia, serif", "font-size": "2.4em", "color": "#ddd"}), # Increased font size
            html.P("This chart breaks down the share of each type of battery in the dataset. It shows the prevalence of different battery types (e.g., Li-ion, Li-polymer).", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}), # Added more padding-left
            dcc.Graph(figure=pie_chart, className="dash-graph"),
            html.P("Insights: Lithium Ion is the most common battery type (42.9%), followed by Lithium Polymer (19.7%). A significant portion (23.7%) has an unknown battery type.", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}) # Added more padding-left
        ], style={"margin-bottom": "50px", "background-color": "#222", "padding": "20px", "border-radius": "5px"}),

        html.Div([
            html.H2("7. Price Distribution by Brand", style={"font-family": "Georgia, serif", "font-size": "2.4em", "color": "#ddd"}), # Increased font size
            html.P("This graph visualizes the price range (minimum, median, maximum) for each brand. It highlights pricing strategies and reveals outliers (e.g., exceptionally expensive or cheap models).", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}), # Added more padding-left
            dcc.Graph(figure=box_plot, className="dash-graph"),
            html.P("Insights: Most brands show significant price variation. Apple has the highest median price and range. Xiaomi and Realme offer a wide price range. Brands like iKALL and Micromax generally have lower prices.", style={"color": "#bbb", "font-family": "Verdana, sans-serif", "font-size": "1.2em", "padding-left": "40px"}) # Added more padding-left
        ], style={"margin-bottom": "50px", "background-color": "#222", "padding": "20px", "border-radius": "5px"}),

        html.Div([
            html.P("Dashboard created by Krish", style={"text-align": "center", "font-size": "1.1em", "color": "#ccc", "font-family": "Roboto, sans-serif"})
        ], style={"padding": "10px 0", "background-color": "#111"})
    ])

# --- Initial Layout with Options ---
initial_layout = html.Div([
    html.Div([
        # Main Title
        html.H1("FLIPKART SMARTPHONE ANALYSIS", style={"text-align": "center", "color": "#eee", "font-family": "Montserrat, sans-serif", "margin-bottom": "40px", "font-size": "3.5em"}),

        # Introduction
        html.Div([
            html.P(
                "Explore comprehensive insights into smartphone listings on Flipkart. Analyze brand popularity, compare specifications of different models, and understand pricing trends with our interactive dashboard.",
                style={"color": "#ddd", "font-size": "1.3em", "font-family": "Montserrat, sans-serif", "text-align": "center", "line-height": "1.7", "padding": "0 80px"}
            )
        ], style={"margin-bottom": "50px"}),

        # Options Buttons
        html.Div([
            dcc.Link(
                html.Button("Explore Data", style={
                    "padding": "20px 45px",
                    "font-size": "1.6em", # Increased font size
                    "margin-bottom": "30px",
                    "background-color": "#333", # Darker button background
                    "color": "#fff",
                    "border": "none",
                    "border-radius": "12px",
                    "cursor": "pointer",
                    "font-family": "Lato, sans-serif", # Changed font to Lato
                    "box-shadow": "0 0 22px 2px #007bff, 0 0 8px 1px #007bff",
                    "transition": "box-shadow 0.3s ease-in-out",
                    "width": "350px", # Increased button width
                    "text-align": "center"
                }),
                href='/graph_analysis',
                id="graph-analysis-button"
            ),
            html.Br(), # Adding a line break for vertical stacking
            dcc.Link(
                html.Button("Phone Comparison", style={
                    "padding": "20px 45px",
                    "font-size": "1.6em", # Increased font size
                    "background-color": "#333", # Darker button background
                    "color": "#fff",
                    "border": "none",
                    "border-radius": "12px",
                    "cursor": "pointer",
                    "font-family": "Lato, sans-serif", # Changed font to Lato
                    "box-shadow": "0 0 22px 2px #a78bfa, 0 0 8px 1px #a78bfa",
                    "transition": "box-shadow 0.3s ease-in-out",
                    "width": "350px", # Increased button width
                    "text-align": "center"
                }),
                href='/compare_phones',
                id="compare-phones-button"
            ),
        ], style={"display": "flex", "flex-direction": "column", "align-items": "center"})
    ], style={
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
        "justify-content": "flex-start", # Align content to the top
        "min-height": "100vh",
        "background-color": "#111",
        "padding": "0 30px" # Adjusted side padding
    })
], style={"min-height": "100vh", "background-color": "#111"})

# --- Compare Phones Layout ---
compare_phones_layout = html.Div([
    html.Div([
        html.H1("Compare 2 Mobile Phones", style={"text-align": "center", "color": "#eee", "font-family": "Montserrat, sans-serif", "margin-bottom": "30px"}),
        html.P("This section will allow you to compare the specifications of two different mobile phones.", style={"color": "#ddd", "font-size": "1.2em", "font-family": "Montserrat, sans-serif", "text-align": "center", "margin-bottom": "40px"}),
        html.Div([
            html.Label("Select Phone 1:", style={'color': '#fff', 'font-size': '1.1em', 'margin-right': '10px'}),
            dcc.Dropdown(
                id='phone1-dropdown',
                options=[{'label': model, 'value': model} for model in all_models],
                style={'width': '300px', 'margin-bottom': '20px', 'color': '#333'}
            ),
            html.Label("Select Phone 2:", style={'color': '#fff', 'font-size': '1.1em', 'margin-right': '10px'}),
            dcc.Dropdown(
                id='phone2-dropdown',
                options=[{'label': model, 'value': model} for model in all_models],
                style={'width': '300px', 'margin-bottom': '20px', 'color': '#333'}
            ),
            html.Div(id='comparison-output') # Placeholder for comparison table
        ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),
        dcc.Link(html.Button("Go to Previous Page", style={"padding": "10px 20px", "font-size": "1.1em", "background-color": "#555", "color": "#fff", "border": "none", "border-radius": "5px", "cursor": "pointer"}), href='/')
    ], style={
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
        "justify-content": "center",
        "min-height": "80vh",
        "background-color": "#222",
        "padding": "40px"
    })
], style={"min-height": "100vh", "background-color": "#111"})

# Initialize Dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback to render content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return initial_layout
    elif pathname == '/graph_analysis':
        return create_graph_analysis_layout()
    elif pathname == '/compare_phones':
        return compare_phones_layout # This line will now find the defined variable
    else:
        return '404: Page not found'

# Callback to update comparison output
@app.callback(
    Output('comparison-output', 'children'),
    [Input('phone1-dropdown', 'value'),
     Input('phone2-dropdown', 'value')]
)
def update_comparison(phone1, phone2):
    if phone1 and phone2:
        phone1_data = data[data['model'] == phone1].iloc[0]
        phone2_data = data[data['model'] == phone2].iloc[0]

        comparison_table = html.Table(
            style={'width': '100%', 'borderCollapse': 'collapse'},
            children=[
                html.Thead(
                    html.Tr([
                        html.Th("Feature", style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'left'}),
                        html.Th(phone1, style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Th(phone2, style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td("Brand", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['brand'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['brand'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                    html.Tr([
                        html.Td("Model", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['model'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['model'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                    html.Tr([
                        html.Td("Colour", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['colour'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['colour'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                    html.Tr([
                        html.Td("Original Price (INR)", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['original_price'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['original_price'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                    html.Tr([
                        html.Td("Discounted Price (INR)", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['discounted_price'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['discounted_price'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                    html.Tr([
                        html.Td("Ratings", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['ratings'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['ratings'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                    html.Tr([
                        html.Td("RAM (Memory)", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['memory'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['memory'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                    html.Tr([
                        html.Td("Storage", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['storage'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['storage'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                    html.Tr([
                        html.Td("Processor", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['processor'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['processor'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                    html.Tr([
                        html.Td("Rear Camera", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['rear_camera'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['rear_camera'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                    html.Tr([
                        html.Td("Front Camera", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['front_camera'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['front_camera'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                    html.Tr([
                        html.Td("Display Size (cm)", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['display_size'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['display_size'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                    html.Tr([
                        html.Td("Battery Capacity (mAh)", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['battery_capacity'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['battery_capacity'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                    html.Tr([
                        html.Td("Battery Type", style={'border': '1px solid #555', 'padding': '8px'}),
                        html.Td(phone1_data['battery_type'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                        html.Td(phone2_data['battery_type'], style={'border': '1px solid #555', 'padding': '8px', 'text-align': 'center'}),
                    ]),
                ])
            ]
        )
        return comparison_table
    else:
        return html.P("Please select two phones to compare.", style={"color": "#ccc", "font-size": "1.2em", "text-align": "center"})

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)