# BlinkIT Retail Sales Forecasting and Analysis System

A machine learning and analytics web application built with Flask, Firebase, and a Random Forest Regressor to forecast sales across BlinkIT outlets. The system integrates interactive visualizations (Plotly) and secure user authentication (Firebase) to provide an end-to-end retail intelligence dashboard.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Model Details](#model-details)
- [Data & Analysis](#data--analysis)
- [Business Insights](#business-insights)
- [Testing Summary](#testing-summary)
- [Future Enhancements](#future-enhancements)
- [References](#references)
- [Author](#author)
- [License](#license)

---

## Project Overview

The BlinkIT Retail Sales Forecasting and Analysis System helps analyze historical sales data, visualize KPIs and trends, and forecast product-level sales for BlinkIT grocery outlets. Users log in securely via Firebase Authentication, explore an interactive dashboard, and generate sales forecasts using a trained Random Forest model.

---

## Features

- 🔐 Firebase Authentication
  - Secure login, guest access, and session handling
  - Prevents unauthorized access to forecasting and dashboards
- 📊 Interactive Sales Dashboard
  - KPIs and charts built with Plotly (Python)
  - Outlet-level and item-level visualizations
- 🤖 Sales Prediction Module
  - Predicts future sales using a Random Forest Regressor
  - Inputs: Item Type, Outlet Size, Location Type, Fat Content, etc.
- 🧠 Data Analysis
  - Correlation heatmap and exploratory analysis for key features
- 🌐 Responsive Design
  - Flask templates and custom CSS for a responsive UI

---

## Tech Stack

- Frontend: HTML, CSS, Plotly.js
- Backend: Flask (Python)
- Authentication: Firebase Authentication (REST API with Flask)
- Machine Learning: Scikit-learn (Random Forest Regressor)
- Libraries: pandas, numpy, scikit-learn, plotly, python-dotenv, pickle
- Tools/IDE: Visual Studio Code, Google Colab, Power BI

---

## Project Structure

BlinkIT_Analysis/
│
├── app.py                        # Flask backend
├── templates/                    # HTML templates
│   ├── login.html
│   ├── home.html
│   ├── dashboard.html
│   └── predict.html
├── static/                       # CSS and static assets
│   └── styles.css
├── BlinkIT Grocery Data_fully_cleaned.csv
├── sales_prediction_model.pkl
├── .env
├── README.md
└── requirements.txt

---

## Installation & Setup

1. Clone the repository
   ```
   git clone https://github.com/rajatvir006/blinkit_analysis.git
   cd blinkit_analysis
   ```

2. Create and activate a virtual environment
   - Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - macOS / Linux:
     ```
     python -m venv venv
     source venv/bin/activate
     ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Configure Firebase and environment variables

   Create a `.env` file in the root directory with the following entries:

   ```
   FLASK_SECRET=your_flask_secret_key
   FIREBASE_API_KEY=your_firebase_api_key
   FIREBASE_AUTH_URL=https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=your_api_key
   ```

   - Replace `your_flask_secret_key` with a secure random string.
   - Replace `your_firebase_api_key` and `your_api_key` with your Firebase project's API key.

5. Run the app
   ```
   python app.py
   ```

   Then open your browser and visit:
   http://127.0.0.1:5000/

---

## Configuration

- .env — Environment variables for Flask secret and Firebase configuration.
- sales_prediction_model.pkl — Trained Random Forest model used by the prediction endpoint.
- BlinkIT Grocery Data_fully_cleaned.csv — Cleaned dataset used for EDA and training.

Security notes:
- No user credentials are stored locally.
- Session tokens are designed to auto-expire.
- Logging out clears Flask and Firebase session states.

---

## Usage

- Login using Firebase-authenticated credentials or use guest access (if enabled).
- Navigate to the Dashboard to view KPIs (total revenue, average sales, outlet performance).
- Use the Prediction page to input product/outlet attributes and get a sales forecast from the Random Forest model.
- Logout to clear the session.

---

## Model Details

- Algorithm: Random Forest Regressor (scikit-learn)
- Dataset Size: ~8,500 records
- Target: Item_Outlet_Sales
- R² Score: ≈ 0.54
- Mean Absolute Error (MAE): ≈ 130
- Notes: The model performs best on known Item–Outlet combinations. Consider re-training with more features or advanced models for improved accuracy.

---

## Data & Analysis

- Correlation heatmap visualizes relationships between:
  - Item Weight, Item Rating, Outlet Age, and Sales
- Key findings:
  - Older outlets show a positive correlation with total sales.
  - Tier 3 outlets generate the highest total revenue.
  - Medium-sized outlets tend to be more profitable.
  - Regular Fat products outperform Low Fat in sales.
  - Higher item visibility tends to slightly reduce sales in this dataset.

---

## Testing Summary

- Firebase Auth: Login and guest access validated
- Model Testing: Random Forest predictions verified against test splits
- Dashboard Validation: Sales KPIs match dataset metrics
- Performance: Prediction latency < 0.5 seconds (typical)
- UI/UX: Responsive and stable across Chrome and Edge

---

## Future Enhancements

- Integrate Firebase Firestore for live data sync and multi-user analytics
- Replace or augment Random Forest with XGBoost / Gradient Boosting for higher accuracy
- Build real-time APIs for streaming sales updates
- Modernize frontend using Bootstrap or React for improved UX
- Add automated retraining pipelines to refresh the model periodically
- Add unit and integration tests around key routes and prediction endpoints

---

## References

- BlinkIT Grocery Dataset — (Google Drive link, if available)
- Flask Documentation — https://flask.palletsprojects.com/
- Firebase Authentication REST API — https://firebase.google.com/docs/reference/rest/auth
- Scikit-learn — https://scikit-learn.org/
- Plotly Python — https://plotly.com/python/

---

## Author

Rajatvir Pandhi  
B.Tech CSE (AI & FT), Semester 3  
Chitkara University, Rajpura

Faculty Mentor: Mr. Vivek Singh Parmar

---
