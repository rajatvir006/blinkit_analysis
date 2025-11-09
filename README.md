# 🛒 BlinkIT Retail Sales Forecasting and Analysis System

A **machine learning and analytics web application** built using **Flask**, **Firebase**, and **Random Forest Regressor** to forecast sales across BlinkIT outlets.  
It integrates **data visualization (Plotly)** and **secure user authentication (Firebase)** to provide an end-to-end retail intelligence dashboard.

---

## 📘 Project Overview

The **BlinkIT Retail Sales Forecasting and Analysis System** helps analyze sales data, visualize performance metrics, and predict future sales trends.  
Users can log in securely via **Firebase Authentication**, explore interactive dashboards, and use a **trained ML model** to forecast product-level sales.

This project combines **data science**, **machine learning**, and **web development** to deliver a real-world predictive analytics solution for retail optimization.

---

## 🚀 Features

- 🔐 **Firebase Authentication**
  - Secure login, guest access, and session handling.
  - Prevents unauthorized access to forecasting and dashboards.

- 📊 **Interactive Sales Dashboard**
  - Real-time charts and KPIs built using Plotly (Python).
  - Displays total revenue, average sales, and outlet-based performance.

- 🤖 **Sales Prediction Module**
  - Predicts future sales using a **Random Forest Regressor** (R² ≈ 0.54).
  - Input fields for Item Type, Outlet Size, Location Type, and Fat Content.

- 🧠 **Data Analysis**
  - Correlation heatmap between Item Weight, Rating, Outlet Age, and Sales.
  - Clear insights on outlet and item-level performance.

- 🌐 **Responsive Web Design**
  - Built using Flask templates and custom CSS.

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML, CSS, Plotly.js |
| **Backend** | Flask (Python) |
| **Authentication** | Firebase Authentication (REST API with Flask) |
| **Machine Learning** | Random Forest Regressor (Scikit-learn) |
| **Libraries** | Pandas, NumPy, Scikit-learn, Plotly, dotenv, pickle |
| **IDE / Tools** | Visual Studio Code, Google Colab, Power BI |
| **Dataset Source** | BlinkIT Grocery Sales Dataset (Google Drive) |

---

## 🔧 Functional Workflow

User → Login (Firebase Auth) → Home Page
↳ Dashboard → KPIs & Visual Insights
↳ Prediction → Input Form → ML Model (Random Forest)
Result Output → Forecast Display → Logout / Session End
---

## 📂 Project Structure

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/rajatvir006/blinkit_analysis.git
cd blinkit_analysis

