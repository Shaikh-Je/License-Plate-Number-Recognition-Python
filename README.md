# License-Plate-Number-Recognition-Python
This Project is to upload a photo license number plate of a vehicle on a website and just see the output of the scanned license plate.


### **System Requirements**  
To run this project smoothly, your computer should meet the following minimum requirements:

#### **1. Hardware Requirements:**  
- **Processor:** Intel i3 (or equivalent) and above  
- **RAM:** Minimum 4GB (Recommended: 8GB or higher)  
- **Storage:** At least 2GB free space  
- **Graphics:** Integrated or dedicated GPU (for image processing)  
- **OS:** Windows 10/11, Linux (Ubuntu 20.04+), macOS  

#### **2. Software Requirements:**  
- **Python:** Version 3.7 or higher  
- **pip:** Latest version  
- **Flask:** For web framework  
- **OpenCV:** For image processing  
- **EasyOCR:** For Optical Character Recognition  
- **NumPy:** For handling image data  
- **Logging Module:** For logging information  

---

### **Python Modules to Install**  
Use the following command to install all required modules:  
bash : 
pip install flask opencv-python easyocr numpy
                Or 
create a **`requirements.txt`** file with the following content:  

flask
opencv-python
easyocr
numpy
```
Then install everything at once using:  
```bash
pip install -r requirements.txt
```

---

### **Additional Dependencies for EasyOCR**  
Since **EasyOCR** requires additional dependencies, install them manually:  
#### **For Windows:**
```bash
pip install torch torchvision torchaudio
```
#### **For Ubuntu/Linux:**
```bash
sudo apt update
sudo apt install tesseract-ocr
pip install torch torchvision torchaudio
```
---

### **Running the Project**  
After installing dependencies, run the Flask app:  
```bash
python app.py
```
Then open a browser and go to:  
```
http://127.0.0.1:5000/
```
