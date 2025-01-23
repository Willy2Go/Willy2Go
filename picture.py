from PIL import Image

# Load the uploaded image
input_path = "Willy2GoSmall.png"
output_path = "Willy2GoSmall_edited.png"

# Open the image
image = Image.open(input_path).convert("RGBA")
pixels = image.load()

# Define the colors
old_white = (255, 255, 255, 255)  # Hex #FFFFFF
new_colors = [(124, 73, 236, 255), (106, 13, 173, 255)]  # Hex #7C49EC, #6A0DAD
default_color = (255, 255, 255, 255)  # Hex #FFFFFF

# Update the colors in the image
for y in range(image.height):
    for x in range(image.width):
        current_color = pixels[x, y]
        if current_color == old_white:
            # Alternate between the two new colors for variety
            pixels[x, y] = new_colors[(x + y) % 2]
        else:
            pixels[x, y] = default_color

# Save the edited image
image.save(output_path)
output_path
