import os
import json
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

# --- Load environment ---
load_dotenv()
POWER_BI_URL = os.getenv("POWER_BI_EMBED_URL", "")

# --- Load trained model---
MODEL_PATH = 'sales_prediction_model.pkl'
try:
    with open(MODEL_PATH, 'rb') as f:
        data = pickle.load(f)
    model = data.get('model')
    model_features = data.get('features', [])
except Exception:
    model = None
    model_features = []
    print("⚠️ Model not found or failed to load. Predictions disabled.")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "dev-secret-key")

# ---------- Helper ----------
def create_prediction_df(form_values, model_features):
    X = pd.DataFrame(0, index=[0], columns=model_features)
    X['Item Weight'] = float(form_values.get('Item_Weight', 0))
    X['Item Visibility'] = float(form_values.get('Item_Visibility', 0))
    X['Outlet Age'] = int(form_values.get('Outlet_Age', 0))

    def set_ohe(key, value):
        if not value:
            return
        col = f'{key}_{value}'
        if col in model_features:
            X.loc[0, col] = 1

    set_ohe('Item Fat Content', form_values.get('Item_Fat_Content'))
    set_ohe('Outlet Type', form_values.get('Outlet_Type'))
    set_ohe('Outlet Location Type', form_values.get('Outlet_Location_Type'))
    set_ohe('Outlet Size', form_values.get('Outlet_Size'))
    set_ohe('Item Type', form_values.get('Item_Type'))
    return X.values.reshape(1, -1)

# ---------- Load CSV ----------
CSV_PATH = 'BlinkIT Grocery Data_fully_cleaned (2).csv'

def load_blinkit_csv(path=CSV_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found at {path}")

    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    rename_map = {
        'total sales': 'Item_Outlet_Sales',
        'total_sales': 'Item_Outlet_Sales',
        'item outlet sales': 'Item_Outlet_Sales',
        'sales': 'Item_Outlet_Sales',
        'revenue': 'Item_Outlet_Sales'
    }
    for col in df.columns:
        if col.lower() in rename_map:
            df.rename(columns={col: rename_map[col.lower()]}, inplace=True)

    if 'Item Fat Content' in df.columns:
        df['Item Fat Content'] = df['Item Fat Content'].replace({
            'LF': 'Low Fat', 'low fat': 'Low Fat', 'reg': 'Regular', 'regular': 'Regular'
        })

    df = df.dropna(axis=1, how='all')
    return df

# ---------- Routes ----------
@app.route('/')
def login_page():
    if session.get('logged_in'):
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/set-session', methods=['POST'])
def set_session():
    session['logged_in'] = True
    session['email'] = request.json.get('email')
    return jsonify({'status': 'ok'})

@app.route('/logout-backend', methods=['POST'])
def logout_backend():
    session.pop('logged_in', None)
    session.pop('email', None)
    return jsonify({'status': 'logged_out'})

@app.route('/guest-login')
def guest_login():
    session['logged_in'] = True
    session['email'] = 'Guest'
    flash('Guest access granted.', 'success')
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    return render_template('home.html')

# ---------- DASHBOARD ----------
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login_page'))

    try:
        df = load_blinkit_csv()
    except FileNotFoundError as e:
        return render_template('dashboard.html', error=str(e))

    # Ensure numeric and clean columns
    df['Item_Outlet_Sales'] = pd.to_numeric(df.get('Item_Outlet_Sales', 0), errors='coerce').fillna(0)
    if 'Rating' in df.columns:
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # ------------ KPIs ------------
    kpis = {
        'total_revenue': float(df['Item_Outlet_Sales'].sum()),
        'avg_revenue': float(df['Item_Outlet_Sales'].mean()),
        'unique_items': int(df['Item Identifier'].nunique()) if 'Item Identifier' in df.columns else 0,
        'unique_outlets': int(df['Outlet Identifier'].nunique()) if 'Outlet Identifier' in df.columns else 0,
        'avg_rating': float(df['Rating'].mean()) if 'Rating' in df.columns else None
    }

    # ------------ Charts ------------
    graphs = []

    if 'Item Fat Content' in df.columns:
        g1 = df.groupby('Item Fat Content', as_index=False)['Item_Outlet_Sales'].sum()
        fig1 = px.pie(g1, names='Item Fat Content', values='Item_Outlet_Sales', title='Sales by Fat Content', hole=0.4)
        fig1.update_traces(textinfo='percent+label')
        graphs.append(fig1)

    if 'Item Type' in df.columns:
        g2 = df.groupby('Item Type', as_index=False)['Item_Outlet_Sales'].sum()
        fig2 = px.bar(g2, x='Item Type', y='Item_Outlet_Sales', title='Sales by Item Type')
        fig2.update_layout(xaxis_tickangle=-45)
        graphs.append(fig2)

    if all(c in df.columns for c in ['Outlet Identifier', 'Item Fat Content']):
        g3 = df.groupby(['Outlet Identifier', 'Item Fat Content'], as_index=False)['Item_Outlet_Sales'].sum()
        fig3 = px.bar(g3, x='Outlet Identifier', y='Item_Outlet_Sales', color='Item Fat Content', barmode='stack', title='Fat Content Sales by Outlet')
        graphs.append(fig3)

    if 'Outlet Age' in df.columns:
        g4 = df.groupby('Outlet Age', as_index=False)['Item_Outlet_Sales'].sum().sort_values('Outlet Age')
        fig4 = px.line(g4, x='Outlet Age', y='Item_Outlet_Sales', markers=True, title='Sales by Outlet Age')
        graphs.append(fig4)

    if 'Outlet Size' in df.columns:
        g5 = df.groupby('Outlet Size', as_index=False)['Item_Outlet_Sales'].sum()
        fig5 = px.pie(g5, names='Outlet Size', values='Item_Outlet_Sales', hole=0.4, title='Sales by Outlet Size')
        graphs.append(fig5)

    if 'Outlet Location Type' in df.columns:
        g6 = df.groupby('Outlet Location Type', as_index=False)['Item_Outlet_Sales'].sum()
        fig6 = px.bar(g6, x='Outlet Location Type', y='Item_Outlet_Sales', title='Sales by Outlet Location Type')
        graphs.append(fig6)

    # ---------- Table ----------
    table_html = ""
    if 'Outlet Type' in df.columns:
        g7 = df.groupby('Outlet Type').agg(
            total_sales=('Item_Outlet_Sales', 'sum'),
            avg_sales=('Item_Outlet_Sales', 'mean'),
            num_items=('Item Identifier', 'nunique'),
            avg_rating=('Rating', 'mean')
        ).reset_index()

        rows = []
        for _, r in g7.iterrows():
            avg_rating = f"{r['avg_rating']:.2f}" if pd.notna(r['avg_rating']) else "N/A"
            rows.append(
                f"<tr><td>{r['Outlet Type']}</td>"
                f"<td>${r['total_sales']:,.0f}</td>"
                f"<td>{r['num_items']}</td>"
                f"<td>{avg_rating}</td>"
                f"<td>${r['avg_sales']:,.0f}</td></tr>"
            )

        table_html = f"""
        <table class='matrix-table'>
        <thead><tr><th>Outlet Type</th><th>Total Sales ($)</th><th>Items</th><th>Avg Rating</th><th>Avg Sales ($)</th></tr></thead>
        <tbody>{''.join(rows)}</tbody></table>
        """

    
    graphs_json = json.dumps(
        [{"data": fig.data, "layout": fig.layout} for fig in graphs],
        cls=PlotlyJSONEncoder
    )

    return render_template('dashboard.html', kpis=kpis, graphs_json=graphs_json, table_html=table_html, error=None)

# ---------- PREDICT ----------
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if not session.get('logged_in'):
        flash('Please log in to access forecasting.', 'danger')
        return redirect(url_for('login_page'))

    data_for_form = {
        'outlet_types': ['Supermarket Type1', 'Supermarket Type2', 'Grocery Store', 'Supermarket Type3'],
        'location_types': ['Tier 1', 'Tier 2', 'Tier 3'],
        'outlet_sizes': ['Small', 'Medium', 'High', 'Unknown'],
        'item_types': ['Dairy', 'Soft Drinks', 'Meat', 'Fruits and Vegetables', 'Household', 'Baking Goods', 'Snack Foods',
                       'Frozen Foods', 'Canned', 'Breads', 'Starchy Foods', 'Others', 'Breakfast', 'Hard Drinks', 'Seafood'],
        'item_fats': ['Regular', 'Low Fat']
    }

    if request.method == 'POST':
        form_values = request.form.to_dict()
        try:
            if model is None:
                flash("Model not loaded. Prediction unavailable.", "danger")
                return redirect(url_for('predict'))
            feats = create_prediction_df(form_values, model_features)
            y = float(model.predict(feats)[0])
            y = max(0.0, y)
            session['prediction_text'] = f"{y:,.2f}"
            flash('Forecast successful.', 'success')
        except Exception as e:
            print("Prediction error:", e)
            flash('Prediction failed. Check inputs.', 'danger')
        return redirect(url_for('predict'))

    pred = session.pop('prediction_text', None)
    return render_template('predict.html', data_for_form=data_for_form, prediction_text=pred)

# ---------- MAIN ----------
if __name__ == "__main__":
    app.run(debug=True)
