# 💊 Kenya Pharmacy Dashboard

**Executive-grade remote monitoring dashboard for Kenyan chemist/pharmacy chains with 3 outlets.**

Built with Streamlit, optimized for mobile-first, low-data usage common in Kenya. Features M-Pesa reconciliation, fraud detection, expiry management, and multi-outlet benchmarking.

![Dashboard Preview](https://via.placeholder.com/800x400?text=Kenya+Pharmacy+Dashboard+Preview)

## 🌟 Features

### Core Analytics
- **Real-time Sales & Inventory Monitoring** - Track KES sales, units, margins across all outlets
- **M-Pesa vs Cash Reconciliation** - Simulated variance detection between POS and payment statements
- **Multi-Outlet Benchmarking** - Compare Nairobi, Mombasa, Kisumu performance

### Advanced Capabilities (Beyond Basic POS)
1. **📈 Demand Forecasting** - 7-day rolling average predictions for inventory planning
2. **📅 Expiry Risk Heatmap** - Color-coded urgency with suggested discounts/disposals
3. **🚨 Fraud Detection** - Rule-based scoring (void rate, unusual discounts, negative margins)
4. **👥 Cashier Scorecards** - Transactions/hour, error rates, performance ranking
5. **🏪 Outlet Comparison** - Sales rankings, margin analysis, category mix
6. **💰 Profit Optimization** - Flag low-margin items with pricing suggestions
7. **📉 Shrinkage Analysis** - Root-cause drill-down by cashier, outlet, time
8. **📱 Refill Reminders** - Chronic medication patient follow-up logic

### Kenyan Market Focus
- 🇰🇪 KES currency throughout
- 📱 75% M-Pesa payment simulation (realistic Kenya ratio)
- 🌧️ Seasonal patterns (rainy season flu/malaria spikes)
- 💊 Common Kenyan pharmacy products (Paracetamol, Amoxicillin, Artemether, etc.)
- 📶 Mobile-first design for low-data connections

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Local Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/kenya-pharmacy-dashboard.git
cd kenya-pharmacy-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Generate Test Data (Optional)

```bash
# Generate CSV file for external use
python generate_data.py
```

This creates `simulated_data.csv` with 1,500 transactions.

## 📁 Project Structure

```
kenya-pharmacy-dashboard/
├── app.py                 # Main Streamlit application
├── generate_data.py       # Standalone data generation script
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── simulated_data.csv    # Generated test data (after running generate_data.py)
```

## 🖥️ Dashboard Tabs

| Tab | Description |
|-----|-------------|
| **📊 Overview** | KPI cards (sales, margins, M-Pesa %), payment mix, category breakdown |
| **📈 Sales Trends** | Daily/weekly performance vs targets, top products, 7-day forecast |
| **📦 Inventory & Expiry** | Expiry heatmap, action items, profit optimization, refill reminders |
| **🚨 Fraud & Reconciliation** | Cashier fraud scores, void analysis, cash/M-Pesa variance tracking |
| **🏪 Outlet Comparison** | Multi-location benchmarking, rankings, trend comparisons |

## 📊 Key Metrics Computed

1. Total Sales (KES)
2. M-Pesa Sales Percentage
3. Daily/Weekly Sales vs Target
4. Shrinkage Rate
5. Expiry Risk Count (30/60/90 days)
6. Profit Margin %
7. Cash/M-Pesa Reconciliation Variance
8. Fraud Risk Score (per cashier)
9. Top 10 Fast-Moving SKUs
10. Prescription Compliance Rate

## ☁️ Deploy to Streamlit Community Cloud (Free)

### Step 1: Push to GitHub
```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit: Kenya Pharmacy Dashboard"

# Create repo on GitHub, then:
git remote add origin https://github.com/yourusername/kenya-pharmacy-dashboard.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Connect your GitHub account
4. Select:
   - Repository: `yourusername/kenya-pharmacy-dashboard`
   - Branch: `main`
   - Main file path: `app.py`
5. Click **"Deploy"**

### Step 3: Get Your Live URL
Your app will be available at:
```
https://yourusername-kenya-pharmacy-dashboard.streamlit.app
```

### Private App Options
For private dashboards (not free on Streamlit Cloud):
- Add password protection via `st.secrets`
- Self-host on AWS/GCP/Azure
- Use Streamlit for Teams (paid)

## 🔒 Adding Password Protection

Create `.streamlit/secrets.toml`:
```toml
[passwords]
admin = "your_secure_password"
```

Add to `app.py`:
```python
def check_password():
    if "authenticated" not in st.session_state:
        password = st.text_input("Password", type="password")
        if password == st.secrets["passwords"]["admin"]:
            st.session_state.authenticated = True
            st.rerun()
        elif password:
            st.error("Incorrect password")
        st.stop()

check_password()
```

## 🛠️ Extending the Dashboard

### Connect to Real Data Sources
Replace `generate_pharmacy_data()` with:
- **Loyverse API**: Export transactions via their REST API
- **M-Pesa Daraja API**: Fetch payment confirmations
- **PostgreSQL/MySQL**: Connect to your POS database

### Add More Features
- WhatsApp/SMS alerts via Twilio
- Export reports to PDF
- Integration with Kenya Revenue Authority (KRA) for tax compliance
- Supplier management module

## 📱 Mobile Optimization Notes

- Sidebar collapsed by default
- Compact metric cards
- Responsive chart sizing
- Low-data Plotly configurations (simplified animations)
- Touch-friendly filters

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push: `git push origin feature/new-feature`
5. Submit a Pull Request

## 📄 License

MIT License - feel free to use for commercial purposes.

## 👨‍💻 Author

Built for Kenyan SME pharmacies seeking executive-grade analytics beyond basic POS systems.

---

**Live Demo**: `https://yourusername-kenya-pharmacy-dashboard.streamlit.app`

*Data shown is simulated for demonstration purposes only.*
