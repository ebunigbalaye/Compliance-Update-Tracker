# **Oil & Gas Compliance Tracker — Nigeria**
*Automated Weekly Compliance Update Scraper & Email Notifier*

## **Overview**
The Oil & Gas Compliance Tracker is a Python application that automatically monitors regulatory and compliance updates relevant to the Nigerian oil & gas industry. It scrapes updates from a designated industry website, analyzes and stores new information, and sends subscribers a weekly email digest summarizing all newly published compliance-related items.

This project demonstrates practical automation, data collection, and notification system skills relevant to consulting, regulatory technology, and digital transformation roles.



## **Key Features**
### **Automated Web Scraping**

* Extracts regulatory updates from a designated website.
* Filters content to capture compliance-related news only.


### Change Detection
* Compares newly scraped items with previously saved data.
* Only stores and reports updates that didn’t exist before.

### Weekly Email Digest
* Aggregates new updates from the week.
* Sends clean, formatted summaries to all subscribers.
* Uses secure email authentication.

### Subscriber Management

* Simple database-backed email list.
* Easy to add/remove subscribers.

### Deployable Anywhere

* Works on Render, Railway, Docker, or a local cron job.
* Lightweight and dependency-minimal.


## **Tech Stack**
* **Python 3.10+**
* **Requests / BeautifulSoup4** — scraping
* **smtplib / email.message** — sending digest emails
* **SQLite  — storing updates
* **FastAPI** if deployed as a web service



## **How It Works**
### **1. Scraping**

The scraper visits the industry website, parses recent articles, and automatically identifies compliance-related ones using keywords or classification logic.

### **2. Storing Updates**
Each scraped update includes:

* Title
* Date
* Article Description
* Source URL

If a new update isn’t found in the existing database, it's stored.

### **3. Weekly Digest Generation**
Every week, the system:

* Loads all updates collected since the previous digest
* Formats them into a clean email summary

### **4. Email Delivery**
Subscribers receive a human-readable email with:

* Titles
* Short descriptions
* Links to full articles

The email uses secure authentication (e.g., Gmail App Password).



## **Why This Project Matters**

Compliance in Nigeria’s oil & gas sector is rapidly evolving. Automating monitoring helps:

* Reduce manual tracking effort
* Improve information accuracy
* Support risk management
* Enhance regulatory readiness

This project is a practical demonstration of how automation improves transparency and operational efficiency in regulated industries.

