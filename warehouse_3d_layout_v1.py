import plotly.graph_objects as go

# Warehouse parameters
N = 10  # Number of bays per row
bay_width = 101  # inches
bay_depth = 50   # inches
aisle_width = 128  # inches
separation = 18  # inches between back-to-back racks
beam_thickness = 4  # inches

# Beam Z-positions
beam_Z = [
    {'level': 'B', 'Z_bottom': 52, 'Z_top': 52 + beam_thickness},
    {'level': 'C', 'Z_bottom': 99, 'Z_top': 99 + beam_thickness},
    {'level': 'D', 'Z_bottom': 145, 'Z_top': 145 + beam_thickness},
    {'level': 'E', 'Z_bottom': 191, 'Z_top': 191 + beam_thickness},
    {'level': 'F', 'Z_bottom': 237, 'Z_top': 237 + beam_thickness},
    {'level': 'G', 'Z_bottom': 283, 'Z_top': 283 + beam_thickness}
]

# Y-boundaries
Y_boundaries = [i * bay_width for i in range(N + 1)]

# Function to generate rack rows
def generate_rack_rows():
    rack_rows = []
    X_current = 0
    # Single-sided rack facing right
    rack_rows.append({'id': 1, 'X_start': X_current, 'X_end': X_current + bay_depth, 'facing': 'right'})
    X_current += bay_depth
    # Aisle
    X_current += aisle_width
    for i in range(5):
        # Rack facing left
        rack_rows.append({'id': 2 + 2*i, 'X_start': X_current, 'X_end': X_current + bay_depth, 'facing': 'left'})
        X_current += bay_depth
        # Separation
        X_current += separation
        # Rack facing right
        rack_rows.append({'id': 3 + 2*i, 'X_start': X_current, 'X_end': X_current + bay_depth, 'facing': 'right'})
        X_current += bay_depth
        # Aisle
        X_current += aisle_width
    # Single-sided rack facing left
    rack_rows.append({'id': 12, 'X_start': X_current, 'X_end': X_current + bay_depth, 'facing': 'left'})
    return rack_rows

rack_rows = generate_rack_rows()

# Function to create a 3D box
def create_box(x0, x1, y0, y1, z0, z1):
    vertices = [
        [x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],
        [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]
    ]
    i = [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6]
    j = [1, 2, 3, 4, 5, 6, 7, 2, 3, 6, 4, 5, 7, 0, 1, 3]
    k = [2, 3, 1, 5, 6, 7, 0, 1, 4, 5, 7, 6, 0, 3, 4, 7]
    return vertices, i, j, k

# Initialize figure
fig = go.Figure()

# Add racks
for rack in rack_rows:
    if rack['facing'] == 'right':
        X_front = [rack['X_end'] - beam_thickness, rack['X_end']]
        X_back = [rack['X_start'], rack['X_start'] + beam_thickness]
    else:  # facing left
        X_front = [rack['X_start'], rack['X_start'] + beam_thickness]
        X_back = [rack['X_end'] - beam_thickness, rack['X_end']]
    
    # Add uprights at each Y-boundary
    for Y_boundary in Y_boundaries:
        # Front upright
        vertices, i, j, k = create_box(X_front[0], X_front[1], Y_boundary - 2, Y_boundary + 2, 0, 287)
        fig.add_trace(go.Mesh3d(
            x=[v[0] for v in vertices],
            y=[v[1] for v in vertices],
            z=[v[2] for v in vertices],
            i=i, j=j, k=k,
            color='gray',
            opacity=0.7
        ))
        # Back upright
        vertices, i, j, k = create_box(X_back[0], X_back[1], Y_boundary - 2, Y_boundary + 2, 0, 287)
        fig.add_trace(go.Mesh3d(
            x=[v[0] for v in vertices],
            y=[v[1] for v in vertices],
            z=[v[2] for v in vertices],
            i=i, j=j, k=k,
            color='gray',
            opacity=0.7
        ))
    
    # Add horizontal beams for each level
    for beam in beam_Z:
        Z_bottom = beam['Z_bottom']
        Z_top = beam['Z_top']
        # Front beam
        vertices, i, j, k = create_box(X_front[0], X_front[1], 0, N * bay_width, Z_bottom, Z_top)
        fig.add_trace(go.Mesh3d(
            x=[v[0] for v in vertices],
            y=[v[1] for v in vertices],
            z=[v[2] for v in vertices],
            i=i, j=j, k=k,
            color='blue',
            opacity=0.5
        ))
        # Back beam
        vertices, i, j, k = create_box(X_back[0], X_back[1], 0, N * bay_width, Z_bottom, Z_top)
        fig.add_trace(go.Mesh3d(
            x=[v[0] for v in vertices],
            y=[v[1] for v in vertices],
            z=[v[2] for v in vertices],
            i=i, j=j, k=k,
            color='blue',
            opacity=0.5
        ))

# Update layout
fig.update_layout(
    scene=dict(
        xaxis_title='Depth (X, inches)',
        yaxis_title='Width along Aisle (Y, inches)',
        zaxis_title='Height (Z, inches)',
        aspectmode='data'
    ),
    title='Warehouse Racking System with 18-inch Separation',
    showlegend=False
)

# Display the figure
fig.show()