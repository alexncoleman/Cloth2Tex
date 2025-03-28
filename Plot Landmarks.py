import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Function to plot points on an image
def plot_points_on_image(json_path, img_path):
    # Load JSON data
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Load image
    img = mpimg.imread(img_path)

    # Extract points and labels
    points = []
    labels = []
    for shape in data['shapes']:
        if shape['shape_type'] == 'point':
            points.append(shape['points'][0])
            labels.append(shape['label'])

    # Separate x and y coordinates
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]

    # Plot the image
    plt.figure(figsize=(10, 10))
    plt.imshow(img)

    # Plot each point
    for x, y, label in zip(x_coords, y_coords, labels):
        plt.plot(x, y, 'ro')  # Red dot for points
        plt.text(x + 5, y - 5, label, color='white', fontsize=8, bbox=dict(facecolor='black', alpha=0.5))

    # Show the plot
    plt.axis('off')
    plt.show()

# Paths to the JSON and image files
json_path = '4_2.json'  # Replace with your JSON file path
img_path = '4_2.jpg'        # Replace with your image file path

# Plot points on the image
plot_points_on_image(json_path, img_path)


