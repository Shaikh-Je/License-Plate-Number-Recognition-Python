from flask import Flask, request, render_template_string
import cv2
import easyocr
import numpy as np
import os
import logging

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# HTML for Upload Page
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>License Plate Recognition</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            min-height: 100vh;
        }
        h1 {
            color: #555;
        }
        form {
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
        }
        input[type="file"] {
            margin: 10px 0;
            padding: 10px;
            width: 100%;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #007BFF;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <h1>Upload a License Plate Image</h1>
        <input type="file" name="image" required>
        <button type="submit">Upload and Process</button>
    </form>
</body>
</html>
"""

# HTML for Result Page
result_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Result</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            min-height: 100vh;
        }
        h1, h3 {
            color: #555;
        }
        p {
            font-size: 1.1rem;
        }
        img {
            max-width: 100%;
            height: auto;
            border: 2px solid #ddd;
            border-radius: 10px;
            margin: 10px 0;
        }
        a {
            color: #007BFF;
            text-decoration: none;
            margin-top: 20px;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>License Plate Recognition Result</h1>
    <p><strong>Extracted Text:</strong> {{ text }}</p>
    <p><strong>State Info:</strong> {{ state_info }}</p>
    <h3>Uploaded Image:</h3>
    <img src="{{ uploaded_image }}" alt="Uploaded Image">
    <h3>Processed Image:</h3>
    <img src="{{ result_image }}" alt="Processed Image">
    <a href="/">Go Back</a>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(index_html)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file uploaded", 400

    file = request.files['image']
    if file.filename == '':
        return "No file selected", 400

    # Save the uploaded image
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Process the image
    img = cv2.imread(filepath)
    if img is None:
        return "Invalid image file", 400

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    reader = easyocr.Reader(['en'])
    result = reader.readtext(gray)

    # Extract text
    text = ""
    for res in result:
        text += res[-2] + " "

    if not text.strip():
        text = "No text detected"

    # Determine state information
    if text[:2] == "MH":
        state_info = "Vehicle registered in MAHARASHTRA."
        logging.info(state_info)
    elif text[:2] == "KA":
        state_info = "Vehicle registered in KARNATAKA."
        logging.info(state_info)
    elif text[:2] == "TN":
        state_info = "Vehicle registered in TAMILNADU."
        logging.info(state_info)
    elif text[:2] == "KL":
        state_info = "Vehicle registered in KERALA."
        logging.info(state_info)
    else:
        state_info = "Unknown vehicle registration state."
        logging.warning(state_info)

    # Draw result on image
    for (bbox, detected_text, _) in result:
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(img, detected_text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result.jpg')
    cv2.imwrite(output_path, img)

    return render_template_string(result_html, uploaded_image=filepath, result_image=output_path, text=text, state_info=state_info)

if __name__ == '__main__':
    app.run(debug=True)
