<h1 align="center">🧹 AutoCleanX — Automated Data Cleaning & Quality Reporting Platform</h1>

<p align="center">
  AutoCleanX is a web-based data preprocessing platform built with <b>Django</b> and <b>Pandas</b>.<br>
  It automates data cleaning, preprocessing, and quality reporting for CSV and Excel datasets through a simple and intuitive interface.
</p>

---

## 🚀 Features

### 📂 Dataset Upload
- Supports CSV and Excel file uploads  
- Secure file handling using Django’s media framework  

### 🧼 Automated Data Cleaning
- Handles missing values using configurable strategies  
- Removes duplicate records automatically  
- Converts incorrect datatypes to appropriate formats  

### 📊 Outlier Detection
- Detects and removes outliers using the **Interquartile Range (IQR)** method  

### 🔤 Encoding & Scaling
- Encodes categorical variables  
- Applies feature scaling for numerical columns  

### 📈 Data Quality Reports
- Generates **before-and-after** data quality metrics  
- Visualizes the impact of cleaning using charts  

### ⬇️ Secure Download
- Users can download cleaned datasets safely  

---

## 🛠️ Tech Stack

| **Layer**        | **Technology**            |
| ---------------- | ------------------------- |
| **Frontend**     | HTML5, CSS3, Bootstrap    |
| **Backend**      | Django, Python            |
| **Data Handling**| Pandas, NumPy             |
| **Visualization**| Matplotlib, Seaborn       |
| **Storage**      | Django Media Framework    |

---

## 📸 Application Preview

<p align="center">
  <img src="screenshots/frontend.png" width="600" alt="AutoCleanX Dashboard"/>
</p>

---

## 🔄 Workflow

1. Upload CSV or Excel dataset  
2. Choose preprocessing options  
3. Automated cleaning using Pandas pipeline  
4. Generate before-and-after data quality reports  
5. Download cleaned dataset securely  

---

## 📂 Folder Structure

```bash
AutoCleanX/
├── AutoCleanX/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── cleaner/
│   ├── templates/
│   │   └── dashboard.html
│   ├── static/
│   ├── views.py
│   ├── utils.py
│   └── preprocessing.py
├── media/
│   └── cleaned_files/
├── screenshots/
│   └── frontend.png
├── manage.py
├── requirements.txt
└── README.md
