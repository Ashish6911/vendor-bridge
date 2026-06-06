# VendorBridge

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34C26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

VendorBridge is a procurement and vendor management platform designed to streamline the complete purchasing lifecycle. The system enables organizations to manage vendors, create RFQs, collect quotations, and process purchase orders with secure, role-based access control.

---

## Features

### Authentication & Security

- User Registration
- User Login
- JWT Authentication
- Protected API Routes
- Role-Based Access Control

### Vendor Management

- Add New Vendors
- View Vendor Records
- Manage Vendor Information
- Vendor Status Tracking

### RFQ Management

- Create Request for Quotations (RFQs)
- View Active RFQs
- Manage Procurement Requests
- Track RFQ Status

### Quotation Management

- Vendor Quotation Submission
- View Submitted Quotations
- Compare Vendor Responses
- Quotation Evaluation Workflow

### Approval Workflow

- Approve Quotations
- Reject Quotations
- Approval Tracking
- Procurement Monitoring

### Purchase Orders

- Generate Purchase Orders
- Track Purchase Order Status
- Procurement Documentation

### Invoice Management

- Generate Invoices
- Invoice Tracking
- Financial Record Management

### Activity Tracking

- Procurement Activity Monitoring
- Workflow Visibility
- Audit-Friendly Record Keeping

---

## Technology Stack

### Backend

- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication

### Frontend

- HTML
- CSS
- JavaScript

---

## Project Structure

```
vendorbridge/
│
├── routers/
│   ├── auth.py
│   ├── vendors.py
│   ├── rfqs.py
│   ├── quotations.py
│   ├── purchase_orders.py
│   ├── invoices.py
│   ├── activity.py
│   └── reports.py
│
├── db.py
├── models.py
├── config.py
├── main.py
└── requirements.txt
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Ashish6911/vendor-bridge.git
cd vendor-bridge
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
uvicorn main:app --reload
```

### API Documentation

http://127.0.0.1:8000/docs

---

## User Roles

### Admin

- Full System Access
- Vendor Management
- RFQ Management
- Approval Management
- Purchase Order Monitoring

### Procurement Officer

- Create RFQs
- Review Quotations
- Generate Purchase Orders
- Track Procurement Activities

### Vendor

- Submit Quotations
- View Assigned RFQs
- Manage Vendor Responses

### Manager

- Review Procurement Activities
- Approve Quotations
- Monitor Workflow Status

---

## Security

- Password Hashing
- JWT-Based Authentication
- Protected Endpoints
- Role-Based Authorization
- Secure Access Control

---

## Future Enhancements

- Email Notifications
- PDF Generation
- Dashboard Analytics
- Advanced Reporting
- Multi-Organization Support
- Cloud Deployment

---

## Team

Developed as a procurement workflow automation solution for hackathon and enterprise procurement use cases.

---

## License

This project is intended for educational, demonstration, and hackathon purposes.