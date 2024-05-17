import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Create dummy data indexed by state and with multi-columns [product, revenue]
index = ["California", "Texas", "Arizona", "Nevada", "Louisiana"]
df = pd.concat(
    [
        pd.DataFrame(
            np.random.rand(5, 2) * 1.25 + 0.25,
            index=index,
            columns=["Revenue1", "Revenue2"]
        ),
        pd.DataFrame(
            np.random.rand(5, 2) + 0.5,
            index=index,
            columns=["Revenue1", "Revenue2"]
        ),
    ],
    axis=1,
    keys=["Product1", "Product2"]
)

# Create a figure with the right layout
fig = go.Figure(
    layout=go.Layout(
        height=600,
        width=1000,
        barmode="relative",
        yaxis_showticklabels=False,
        yaxis_showgrid=False,
        yaxis_range=[0, df.groupby(axis=1, level=0).sum().max().max() * 1.5],
       # Secondary y-axis overlayed on the primary one and not visible
        yaxis2=go.layout.YAxis(
            visible=False,
            matches="y",
            overlaying="y",
            anchor="x",
        ),
        font=dict(size=24),
        legend_x=0,
        legend_y=1,
        legend_orientation="h",
        hovermode="x",
        margin=dict(b=0, t=10, l=0, r=10)
    )
)

# Define some colors for the product, revenue pairs
colors = {
    "Product1": {
        "Revenue1": "#F28F1D",
        "Revenue2": "#F6C619",
    },
    "Product2": {
        "Revenue1": "#2B6045",
        "Revenue2": "#5EB88A",
    }
}

# Add the traces
for i, t in enumerate(colors):
    for j, col in enumerate(df[t].columns):
        if (df[t][col] == 0).all():
            continue
        fig.add_bar(
            x=df.index,
            y=df[t][col],
            # Set the right yaxis depending on the selected product (from enumerate)
            yaxis=f"y{i + 1}",
            # Offset the bar trace, offset needs to match the width
            # For categorical traces, each category is spaced by 1
            offsetgroup=str(i),
            offset=(i - 1) * 1/3,
            width=1/3,
            legendgroup=t,
            legendgrouptitle_text=t,
            name=col,
            marker_color=colors[t][col],
            marker_line=dict(width=2, color="#333"),
            hovertemplate="%{y}<extra></extra>"
        )

# Display the plot in Streamlit
st.plotly_chart(fig)
