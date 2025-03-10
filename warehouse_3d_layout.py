import plotly.graph_objects as go

# Warehouse parameters
N = 10  # Number of bays per row
bay_width = 101  # inches
bay_depth = 50   # inches
aisle_width = 128  # inches
separation = 18  # inches between back-to-back racks
beam_thickness = 4  # inches

# Beam Z-positions (top of each beam where pallets sit)
beam_Z = [
    {'level': 'B', 'Z_bottom': 52, 'Z_top': 52 + beam_thickness},
    {'level': 'C', 'Z_bottom': 99, 'Z_top': 99 + beam_thickness},
    {'level': 'D', 'Z_bottom': 145, 'Z_top': 145 + beam_thickness},
    {'level': 'E', 'Z_bottom': 191, 'Z_top': 191 + beam_thickness},
    {'level': 'F', 'Z_bottom': 237, 'Z_top': 237 + beam_thickness},
    {'level': 'G', 'Z_bottom': 283, 'Z_top': 283 + beam_thickness}
]

# Z-levels for each level (where pallets sit)
Z_levels = {
    'A': 0,    # Floor level
    'B': 52,   # Top of beam at 52
    'C': 99,
    'D': 145,
    'E': 191,
    'F': 237,
    'G': 283
}

# Mapping racks to aisles and sides
aisles = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F']
sides = ['L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'L', 'R']

# Y-boundaries for bays
Y_boundaries = [i * bay_width for i in range(N + 1)]

# Function to generate rack rows
def generate_rack_rows():
    rack_rows = []
    X_current = 0
    # Single-sided rack facing right (Aisle A, Left)
    rack_rows.append({'id': 1, 'X_start': X_current, 'X_end': X_current + bay_depth, 'facing': 'right'})
    X_current += bay_depth + aisle_width
    # Back-to-back racks for aisles B to E
    for i in range(5):
        # Rack facing left (Right side of aisle)
        rack_rows.append({'id': 2 + 2*i, 'X_start': X_current, 'X_end': X_current + bay_depth, 'facing': 'left'})
        X_current += bay_depth + separation
        # Rack facing right (Left side of next aisle)
        rack_rows.append({'id': 3 + 2*i, 'X_start': X_current, 'X_end': X_current + bay_depth, 'facing': 'right'})
        X_current += bay_depth + aisle_width
    # Single-sided rack facing left (Aisle F, Right)
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

# Lists for labels
X_labels, Y_labels, Z_labels, texts = [], [], [], []

# Add racks and labels
for rack in rack_rows:
    aisle = aisles[rack['id'] - 1]
    side = sides[rack['id'] - 1]
    X_front = rack['X_end'] if rack['facing'] == 'right' else rack['X_start']
    
    # Add bay labels at floor level (Z=5)
    for bay_number in range(1, N + 1):
        address = f"{aisle}-{side}-{bay_number}"
        Y_center = (bay_number - 0.5) * bay_width
        X_labels.append(X_front)
        Y_labels.append(Y_center)
        Z_labels.append(5)
        texts.append(address)
    
    # Add level labels for racks 1 and 12 only
    if rack['id'] in [1, 12]:
        for level in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            level_label = f"Level {level}"
            Y_label = 50  # Inside first bay
            Z_label = Z_levels[level] + 5  # Slightly above the level
            X_labels.append(X_front)
            Y_labels.append(Y_label)
            Z_labels.append(Z_label)
            texts.append(level_label)
    
    # Add uprights and beams
    if rack['facing'] == 'right':
        X_front_beam = [rack['X_end'] - beam_thickness, rack['X_end']]
        X_back_beam = [rack['X_start'], rack['X_start'] + beam_thickness]
    else:
        X_front_beam = [rack['X_start'], rack['X_start'] + beam_thickness]
        X_back_beam = [rack['X_end'] - beam_thickness, rack['X_end']]
    
    for Y_boundary in Y_boundaries:
        # Front upright
        vertices, i, j, k = create_box(X_front_beam[0], X_front_beam[1], Y_boundary - 2, Y_boundary + 2, 0, 287)
        fig.add_trace(go.Mesh3d(x=[v[0] for v in vertices], y=[v[1] for v in vertices], z=[v[2] for v in vertices], i=i, j=j, k=k, color='gray', opacity=0.7))
        # Back upright
        vertices, i, j, k = create_box(X_back_beam[0], X_back_beam[1], Y_boundary - 2, Y_boundary + 2, 0, 287)
        fig.add_trace(go.Mesh3d(x=[v[0] for v in vertices], y=[v[1] for v in vertices], z=[v[2] for v in vertices], i=i, j=j, k=k, color='gray', opacity=0.7))
    
    for beam in beam_Z:
        Z_bottom = beam['Z_bottom']
        Z_top = beam['Z_top']
        # Front beam
        vertices, i, j, k = create_box(X_front_beam[0], X_front_beam[1], 0, N * bay_width, Z_bottom, Z_top)
        fig.add_trace(go.Mesh3d(x=[v[0] for v in vertices], y=[v[1] for v in vertices], z=[v[2] for v in vertices], i=i, j=j, k=k, color='blue', opacity=0.5))
        # Back beam
        vertices, i, j, k = create_box(X_back_beam[0], X_back_beam[1], 0, N * bay_width, Z_bottom, Z_top)
        fig.add_trace(go.Mesh3d(x=[v[0] for v in vertices], y=[v[1] for v in vertices], z=[v[2] for v in vertices], i=i, j=j, k=k, color='blue', opacity=0.5))

# Add labels to the figure
fig.add_trace(go.Scatter3d(
    x=X_labels,
    y=Y_labels,
    z=Z_labels,
    mode='text',
    text=texts,
    textposition='middle center',
    textfont=dict(size=8),  # Smaller text to reduce clutter
    showlegend=False
))

# Update layout with camera view for better visibility
fig.update_layout(
    scene=dict(
        xaxis_title='Depth (X, inches)',
        yaxis_title='Width along Aisle (Y, inches)',
        zaxis_title='Height (Z, inches)',
        aspectmode='data',
        camera=dict(eye=dict(x=1.5, y=1.5, z=0.5))  # Angle for clear view
    ),
    title='Warehouse Racking System with Address Labels',
    showlegend=False
)

# Display the figure
fig.show()