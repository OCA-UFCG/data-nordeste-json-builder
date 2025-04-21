# Data Nordeste - Excel to JSON Converter

This is a small Flask app that lets you upload an Excel file and converts it into multiple JSON files, zipped and ready to download. It is specifically designed for creating the "minicards" displayed on the Data Nordeste website

## How to run (local setup)

1. **Clone the repository**

2. **if you need it, create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate 
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
python run.py
```

5. Open your browser and go to http://localhost:5000

## 📁 Upload Excel File

### The Excel file should have two sheets:
- The first one with regional indicators
- The second one with state data

Once uploaded, the app will convert the content into multiple JSON files and return a ZIP for download.

