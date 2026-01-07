from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)

# Folder to save resized images
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        image_file = request.files.get("image")
        width = int(request.form.get("width"))
        height = int(request.form.get("height"))
        keep_ratio = request.form.get("ratio")

        # Basic validation
        if width <= 0 or height <= 0:
            return "Width and Height must be greater than zero"

        # Open image
        img = Image.open(image_file)

        # Resize logic
        if keep_ratio:
            img.thumbnail((width, height))
        else:
            img = img.resize((width, height))

        # Save resized image
        output_path = os.path.join(UPLOAD_FOLDER, "resized_image.png")
        img.save(output_path)

        # Download file
        return send_file(output_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
