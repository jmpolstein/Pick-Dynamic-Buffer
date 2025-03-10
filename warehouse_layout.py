import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Sample data for racks
data = {
    'rack_id': ['R1', 'R2', 'R3', 'R4'],
    'x': [10, 20, 40, 60],  # x-coordinate
    'y': [10, 10, 25, 25],  # y-coordinate
    'width': [5, 5, 8, 8],  # rack width
    'depth': [2, 2, 3, 3],  # rack depth
    'category': ['storage', 'storage', 'pickup', 'pickup']  # rack type/category
}
racks = pd.DataFrame(data)

# Define colors for different rack categories
rack_colors = {
    'storage': 'lightblue',
    'pickup': 'lightgreen',
    'shipping': 'salmon'
}

# Function to draw the warehouse layout
def draw_warehouse_layout(racks_df, warehouse_length=100, warehouse_width=50, show_grid=True, highlight_aisles=True):
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Add grid if requested
    if show_grid:
        ax.grid(color='lightgray', linestyle='--', linewidth=0.5)
    
    # Highlight aisles if requested
    if highlight_aisles:
        # Simplified aisle highlighting - just for demonstration
        ax.axhspan(15, 20, alpha=0.2, color='yellow', label='Main Aisle')
        ax.axhspan(35, 40, alpha=0.2, color='yellow')
    
    # Draw racks
    for _, rack in racks_df.iterrows():
        # Get color based on category, defaulting to gray if not found
        color = rack_colors.get(rack['category'], 'gray')
        
        # Draw the rack
        rect = plt.Rectangle(
            (rack['x'], rack['y']), 
            rack['width'], 
            rack['depth'], 
            fill=True, 
            color=color,
            edgecolor='black',
            linewidth=1
        )
        ax.add_patch(rect)
        
        # Add rack ID label in the center of the rack
        ax.text(
            rack['x'] + rack['width']/2, 
            rack['y'] + rack['depth']/2,
            rack['rack_id'],
            ha='center',
            va='center',
            fontweight='bold'
        )
    
    # Set limits and labels
    ax.set_xlim(0, warehouse_length)
    ax.set_ylim(0, warehouse_width)
    ax.set_aspect('equal', adjustable='box')
    plt.xlabel('Length (units)')
    plt.ylabel('Width (units)')
    plt.title('Warehouse Layout')
    
    # Add a legend for rack categories
    handles = [plt.Rectangle((0,0),1,1, color=color) for color in rack_colors.values()]
    labels = list(rack_colors.keys())
    plt.legend(handles, labels, loc='upper right')
    
    return fig, ax

# Plot the warehouse layout
fig, ax = draw_warehouse_layout(racks)
plt.show()

# Example of how to use the function with different parameters
# Uncomment to see alternative layouts
# fig, ax = draw_warehouse_layout(racks, warehouse_length=150, warehouse_width=80, show_grid=False)
# plt.show() 