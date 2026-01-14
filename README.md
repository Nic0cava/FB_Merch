# FB Merch

A custom-built inventory management web application designed for **Funky Buddha Brewery** to modernize, centralize, and streamline merchandise inventory tracking and reporting.

---

## 🧾 Overview

**FB Merch** was created to solve long-standing inefficiencies in how Funky Buddha Brewery managed its merchandise inventory across a large 100,000 sq. ft. facility. Merchandise is stored across multiple physical locations, often far from the taproom floor. When customers requested items that were not immediately available, employees could spend 5–10 minutes searching for stock, leading to longer wait times, lost sales opportunities, and unnecessary labor — especially during peak hours.

This application provides **instant visibility into inventory levels**, item locations, and value metrics. What once took **3–4 hours of manual counting and reconciliation** can now be reviewed, updated, and exported **within minutes**, dramatically improving operational efficiency and accuracy.

---

## ⚙️ Built With

* **Backend:** Python, Flask  
* **Database:** PostgreSQL (managed with pgAdmin)  
* **ORM & Migrations:** SQLAlchemy, Flask-Migrate  
* **Forms & Security:** Flask-WTF, Werkzeug (password hashing & authentication)  
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5  
* **Templating:** Jinja2  
* **Deployment:** Gunicorn + Nginx on a VPS  

---

## 💡 Features

### Inventory Management
* Track inventory **per item and per location**:
  * Front of House (FOH)
  * Back of House (BOH)
  * Room 300
* Real-time quantity updates with automatic total recalculations
* Item-level timestamps showing **when inventory was last updated**
* Live search and category-based filtering

### Financial & Historical Tracking
* Track **item cost to the company**
* Automatically calculate **total inventory value per item**
* Store and compare **prior month inventory totals**
* Calculate **month-over-month inventory differences** for better auditing and forecasting

### Reporting & Data Export
* Export **all inventory data** to `.xlsx` format
* Optionally export **per-category inventory reports**
* Excel-compatible output for long-term record keeping, audits, and reporting
* Enables the company to **archive monthly inventory snapshots** effortlessly

### UX & Security
* Clean, reorganized app layout focused on clarity and usability
* Mobile-friendly, responsive design
* Secure authentication for internal company access only

---

## 🖼️ Screenshots

<img width="1278" height="1524" alt="fb_merch_example1" src="https://github.com/user-attachments/assets/6b452eb9-0144-46d7-b517-0e5caed798fb" />
<img width="1279" height="1522" alt="fb_merch_example2" src="https://github.com/user-attachments/assets/1f0923b0-03a9-4a73-8a8b-fcc320e5d4d2" />

---

## 🚀 Impact

**FB Merch** transforms merchandise tracking from a slow, error-prone manual process into a **fast, reliable, and data-driven system**. It improves inventory accuracy, reduces labor time, enables historical tracking, and gives the company powerful reporting tools — all while remaining intuitive for day-to-day employee use.

This project reflects real-world operational needs and demonstrates full-stack development, database design, reporting automation, and production deployment best practices.
