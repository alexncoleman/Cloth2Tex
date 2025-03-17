import json
import os

def resize_coordinates(x, y, original_shape, new_shape, rotate=False):
    """Rescale and optionally rotate coordinates from original image size to new image size."""
    if rotate:
        # Rotate 90 degrees counterclockwise before scaling
        x, y = y, original_shape[1] - x

    scale_x = new_shape[1] / original_shape[1]
    scale_y = new_shape[0] / original_shape[0]
    return round(x * scale_x, 2), round(y * scale_y, 2)

def update_json_coordinates(json_path, new_shape=(512, 512), rotate = False):
    with open(json_path, 'r') as file:
        data = json.load(file)

    original_shape = (data.get("imageHeight", 720), data.get("imageWidth", 1280))

    if "shapes" in data:
        for shape in data["shapes"]:
            if "points" in shape:
                shape["points"] = [resize_coordinates(x, y, original_shape, new_shape, rotate=rotate)
                                    for x, y in shape["points"]]

    # Save the updated JSON
    updated_json_path = f"updated_{os.path.basename(json_path)}"
    with open(updated_json_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Updated JSON saved to: {updated_json_path}")

