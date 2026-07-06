# Apollo Automation

A Python automation tool that integrates the **Apollo API** with **Google Sheets** to automate business lead generation. The application reads keywords from Google Sheets, searches Apollo for matching contacts, and exports structured results back into Google Sheets.

---

## 📌 Overview

Apollo Automation simplifies the process of finding business contacts by automating lead generation workflows. Instead of manually searching Apollo, the application retrieves contacts based on predefined keywords and stores the results in organized Google Sheets tabs.

---

## ✨ Features

- Read keywords from Google Sheets
- Search contacts using the Apollo API
- Filter results by job titles
- Export leads directly to Google Sheets
- Automatically create a worksheet for each keyword
- Store contact details including:
  - Name
  - Job Title
  - Company
  - Email Address
  - Email Status
- Supports multiple keywords
- Modular Python codebase

---

## 🛠️ Tech Stack

- Python
- Apollo API
- Google Sheets API
- HTTP Client
- JSON

---

## 📂 Project Structure

```text
Apollo-Automation/
│
├── README.md
├── main.py                 # Application entry point
├── apollo.py               # Apollo API integration
├── gsheet.py               # Google Sheets operations
├── google_sheets.py        # Google authentication
├── google_scraper.py       # Google search utilities
├── logger.py               # Logging configuration
└── requirements.txt
```

---

# ⚙️ Configuration

Before running the project, update the required configuration.

## 1. Configure Apollo API

Open **apollo.py** and add your Apollo API key.

```python
api_key = "YOUR_APOLLO_API_KEY"
```

---

## 2. Configure Google Sheets

Open **gsheet.py** and update the following values.

```python
SHEET_ID = "YOUR_GOOGLE_SHEET_ID"

SHEET_NAME = "YOUR_GOOGLE_SHEET_NAME"
```

Make sure your Google Service Account has permission to access the Google Sheet.

---

# 🚀 Installation

Clone the repository.

```bash
git clone https://github.com/JawwadIrshad/Apollo-Automation.git

cd Apollo-Automation
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# ▶️ Usage

Run the application.

```bash
python main.py
```

Enter:

```text
Y
```

to start the automation.

The application will automatically:

1. Connect to Google Sheets.
2. Read keywords from the configured sheet.
3. Search Apollo for matching contacts.
4. Retrieve business contact information.
5. Create a separate worksheet for each keyword.
6. Export the collected leads into Google Sheets.

---

# 📊 Output

Each worksheet contains:

| Name | Job Title | Company | Email | Email Status |
|------|-----------|----------|-------|--------------|

---

# 📷 Workflow

```
Google Sheets
      │
      ▼
 Read Keywords
      │
      ▼
 Apollo API Search
      │
      ▼
 Retrieve Contacts
      │
      ▼
 Format Data
      │
      ▼
 Export to Google Sheets
```

---

# 🔮 Future Improvements

- Environment Variable Support
- Pagination
- Retry Mechanism
- Duplicate Detection
- CSV / Excel Export
- Multi-country Search
- Logging Enhancements

---

# 👨‍💻 Author

**Syed Muhammad Jawwad Irshad**
---

## 📄 License

This project is intended for educational and automation purposes. Please ensure compliance with Apollo's API Terms of Service when using the Apollo API.
