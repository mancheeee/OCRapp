# OCRapp
A desktop OCR application built with PyQt5 and EasyOCR that scans images and extracts text, with an optional student ID card autofill feature. Uses a pretrained deep learning model to recognize English text from uploaded images.


# 🧠 OCR Desktop App (PyQt5 + EasyOCR)

A simple yet effective desktop application for scanning images and extracting text using deep learning-based OCR. Built with **PyQt5** for the UI and **EasyOCR** under the hood, this app can process images, extract readable text, and annotate the results live — with a bonus feature for scanning student ID cards and auto-filling form fields.

---

## 🔍 Features

- 📤 **Upload and Preview Images**  
  Easily select and preview `.png`, `.jpg`, or `.jpeg` images inside the app.

- 🧠 **OCR Text Extraction**  
  Uses a pretrained **CRNN (Convolutional Recurrent Neural Network)** model via **EasyOCR** to detect English text in the uploaded image.

- 🧾 **Formatted Text Output**  
  Outputs scanned text in readable lines by grouping based on vertical position.
<p align="center">
<img width="975" height="600" alt="image" src="https://github.com/user-attachments/assets/98c2319d-645f-434d-9e39-71c7f81ae2f6" />
</p>

  
- 🖼️ **Annotated Image Output**  
  Detected text is shown over the original image with bounding boxes and overlays and the most recently scanned picture is saved with annotations with the name of "ocr_output.jpg"
  <br>

<p align="center">
<img width="477" height="303" alt="image" src="https://github.com/user-attachments/assets/3956308f-9391-45f3-912f-0d118c59394d" />
</p>

  
  ----------------------------------------------------------------------------------

- 🎓 **ID Card Auto-Fill** *(Incomplete Feature)*  
  Includes an optional window to scan student ID cards and auto-populate fields like:
  - University Name  
  - Location  
  - Name  
  - Student Number  
  - Date  
  > This layout-based logic is still experimental and may not work reliably across formats.

<br>
<p align="center">
<img width="327" height="405" alt="image" src="https://github.com/user-attachments/assets/cff3de79-b6dd-40b4-a64a-fb74f4258800" />

</p>


---

## 🧠 Model Details

- **Library:** [EasyOCR](https://github.com/JaidedAI/EasyOCR)  
- **Language:** English (`["en"]`)  
- **Model Type:** CRNN (pretrained, PyTorch backend)

---
--------------------------------------------------------------------------------------

## 🧪 Project Note

This application is a **test project** built to explore and compare the **hassle between using a prebuilt OCR model (EasyOCR)** versus training a custom OCR model from scratch.

It stands as a **functioning prototype** with some **incomplete walls** — especially around layout-specific extraction and generalization. However, the core mechanics are in place, and the foundation is solid.

> 🛠️ **Feel free to build on top of it and take it further.**

--------------------------------------------------------------------------------------------

## 🖥️ Requirements

Install dependencies with:

```bash
pip install -r requirements.txt

