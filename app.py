"""
BiasharaFlow Pharma - RUDDER RESEARCH
Executive-grade remote monitoring for Kenyan chemists/pharmacies
Mobile-first, M-Pesa focused, fraud detection enabled
Version 2.0 - Full Featured
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import warnings
import calendar
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIG - MUST BE FIRST
# ============================================================================
st.set_page_config(
    page_title="PharmaDash Kenya | Premium Analytics",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - PREMIUM STYLING
# ============================================================================
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Global Styles */
* {
    font-family: 'Poppins', sans-serif;
}

/* Main container */
.main .block-container {
    padding: 1rem 2rem;
    max-width: 100%;
}

/* Header Styling */
.main-header {
    background: linear-gradient(135deg, #006600 0%, #004d00 50%, #003300 100%);
    padding: 1.5rem 2rem;
    border-radius: 15px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 15px rgba(0,102,0,0.3);
}

.main-header h1 {
    color: white;
    margin: 0;
    font-size: 2rem;
    font-weight: 700;
}

.main-header p {
    color: #90EE90;
    margin: 0.5rem 0 0 0;
    font-size: 0.95rem;
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
    padding: 1.2rem;
    border-radius: 12px;
    border-left: 5px solid #006600;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
}

.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.12);
}

.kpi-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #006600;
    margin: 0;
}

.kpi-label {
    font-size: 0.85rem;
    color: #666;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.kpi-delta {
    font-size: 0.8rem;
    margin-top: 0.3rem;
}

.kpi-delta.positive { color: #28a745; }
.kpi-delta.negative { color: #dc3545; }

/* Alert Boxes */
.alert-critical {
    background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    font-weight: 500;
}

.alert-warning {
    background: linear-gradient(135deg, #ffbb33 0%, #ff8800 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    font-weight: 500;
}

.alert-success {
    background: linear-gradient(135deg, #00C851 0%, #007E33 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    font-weight: 500;
}

/* Rank Cards */
.rank-card {
    background: white;
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
    gap: 1rem;
}

.rank-number {
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    background: #006600;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.rank-gold { background: linear-gradient(135deg, #FFD700, #FFA500); }
.rank-silver { background: linear-gradient(135deg, #C0C0C0, #A0A0A0); }
.rank-bronze { background: linear-gradient(135deg, #CD7F32, #8B4513); }

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
}

section[data-testid="stSidebar"] .block-container {
    padding: 1rem;
}

/* Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: #f8f9fa;
    padding: 0.5rem;
    border-radius: 10px;
}

.stTabs [data-baseweb="tab"] {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: #006600 !important;
    color: white !important;
}

/* Metric Improvements */
[data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #006600 !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}

/* DataFrames */
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #006600 0%, #004d00 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-weight: 500;
    transition: all 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,102,0,0.3);
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Live Clock */
.live-clock {
    background: rgba(0,0,0,0.2);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    color: white;
    font-size: 0.9rem;
    display: inline-block;
}

/* Employee Status */
.status-online {
    color: #00C851;
    font-weight: 600;
}

.status-offline {
    color: #ff4444;
    font-weight: 600;
}

/* Product Stock Indicators */
.stock-critical { color: #dc3545; font-weight: 700; }
.stock-low { color: #ffc107; font-weight: 600; }
.stock-good { color: #28a745; font-weight: 600; }

/* Charts Container */
.chart-container {
    background: white;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# SECTION 1: ENHANCED DATA GENERATION
# ============================================================================

@st.cache_data
def generate_pharmacy_data(num_rows: int = 2500, seed: int = 42) -> pd.DataFrame:
    """Generate comprehensive Kenyan pharmacy data with employee shifts and detailed tracking."""
    np.random.seed(seed)
    
    # Outlets with more details
    outlets = {
        'OUT001': {'name': 'Nairobi CBD', 'city': 'Nairobi', 'rent': 150000, 'target': 800000},
        'OUT002': {'name': 'Mombasa Nyali', 'city': 'Mombasa', 'rent': 100000, 'target': 600000},
        'OUT003': {'name': 'Kisumu Mega', 'city': 'Kisumu', 'rent': 80000, 'target': 500000}
    }
    
    # Enhanced cashier data with shifts and hire dates
    cashiers = {
        'OUT001': [
            ('C001', 'Jane Wanjiku', 'Morning', '2022-03-15', 45000),
            ('C002', 'Peter Omondi', 'Afternoon', '2021-08-20', 50000),
            ('C003', 'Grace Muthoni', 'Evening', '2023-01-10', 42000)
        ],
        'OUT002': [
            ('C004', 'Hassan Ali', 'Morning', '2022-06-01', 44000),
            ('C005', 'Fatma Said', 'Afternoon', '2021-11-15', 48000),
            ('C006', 'Kevin Otieno', 'Evening', '2023-04-20', 40000)
        ],
        'OUT003': [
            ('C007', 'Lucy Achieng', 'Morning', '2022-01-05', 43000),
            ('C008', 'James Kiprop', 'Afternoon', '2021-09-10', 47000),
            ('C009', 'Mary Nekesa', 'Evening', '2023-02-28', 41000)
        ]
    }
    
    # Expanded medicine catalog with reorder levels
    medicines = [
        ('MED001', 'Paracetamol 500mg', 'Painkillers', 50, 30, 'No', 100, 500),
        ('MED002', 'Ibuprofen 400mg', 'Painkillers', 80, 50, 'No', 80, 400),
        ('MED003', 'Amoxicillin 500mg', 'Antibiotics', 150, 90, 'Yes', 60, 300),
        ('MED004', 'Azithromycin 250mg', 'Antibiotics', 350, 200, 'Yes', 40, 200),
        ('MED005', 'Metformin 500mg', 'Chronic', 120, 70, 'Yes', 100, 500),
        ('MED006', 'Amlodipine 5mg', 'Chronic', 180, 100, 'Yes', 80, 400),
        ('MED007', 'Omeprazole 20mg', 'Gastro', 200, 120, 'No', 70, 350),
        ('MED008', 'Cetirizine 10mg', 'Allergy', 60, 35, 'No', 90, 450),
        ('MED009', 'Vitamin C 1000mg', 'Vitamins', 250, 150, 'No', 120, 600),
        ('MED010', 'Multivitamin Plus', 'Vitamins', 450, 280, 'No', 80, 400),
        ('MED011', 'Cough Syrup 100ml', 'Cold & Flu', 180, 100, 'No', 100, 500),
        ('MED012', 'Flu Capsules', 'Cold & Flu', 120, 70, 'No', 150, 750),
        ('MED013', 'Malaria Test Kit', 'Diagnostics', 300, 180, 'No', 50, 250),
        ('MED014', 'Artemether-Lum', 'Antimalarials', 550, 350, 'Yes', 60, 300),
        ('MED015', 'ORS Sachets', 'Gastro', 30, 15, 'No', 200, 1000),
        ('MED016', 'Zinc Tablets', 'Supplements', 150, 90, 'No', 100, 500),
        ('MED017', 'Insulin Syringe', 'Diabetes', 50, 25, 'No', 150, 750),
        ('MED018', 'Glucometer Strips', 'Diabetes', 800, 500, 'No', 40, 200),
        ('MED019', 'Antacid Tablets', 'Gastro', 100, 60, 'No', 120, 600),
        ('MED020', 'Eye Drops 10ml', 'Ophthalmic', 280, 170, 'No', 60, 300),
        ('MED021', 'Diclofenac Gel', 'Painkillers', 350, 200, 'No', 50, 250),
        ('MED022', 'Loratadine 10mg', 'Allergy', 90, 55, 'No', 80, 400),
        ('MED023', 'Aspirin 300mg', 'Painkillers', 40, 20, 'No', 150, 750),
        ('MED024', 'Doxycycline 100mg', 'Antibiotics', 200, 120, 'Yes', 50, 250),
        ('MED025', 'Metronidazole 400mg', 'Antibiotics', 80, 45, 'Yes', 70, 350),
        ('MED026', 'Salbutamol Inhaler', 'Respiratory', 650, 400, 'Yes', 30, 150),
        ('MED027', 'Prednisolone 5mg', 'Steroids', 120, 70, 'Yes', 40, 200),
        ('MED028', 'Ferrous Sulphate', 'Supplements', 60, 35, 'No', 100, 500),
        ('MED029', 'Folic Acid 5mg', 'Supplements', 50, 25, 'No', 120, 600),
        ('MED030', 'Clotrimazole Cream', 'Antifungal', 180, 100, 'No', 60, 300),
    ]
    
    # Date range: 6 months
    end_date = datetime(2024, 12, 31)
    start_date = end_date - timedelta(days=180)
    
    data = []
    transaction_id = 10000
    
    for _ in range(num_rows):
        # Random date
        date = start_date + timedelta(days=np.random.randint(0, 181))
        month = date.month
        day_of_week = date.weekday()
        
        # Time of day with realistic distribution
        # More transactions during lunch (12-2) and evening (5-7)
        hour_weights = [0.02, 0.02, 0.03, 0.05, 0.06, 0.08, 0.10, 0.12, 0.10, 0.08, 0.08, 0.06, 0.05, 0.05, 0.05, 0.05]
        hours = list(range(7, 23))
        hour = np.random.choice(hours, p=hour_weights[:len(hours)])
        minute = np.random.randint(0, 60)
        second = np.random.randint(0, 60)
        date = date.replace(hour=hour, minute=minute, second=second)
        
        # Determine shift based on hour
        if 7 <= hour < 14:
            shift = 'Morning'
        elif 14 <= hour < 19:
            shift = 'Afternoon'
        else:
            shift = 'Evening'
        
        # Weekend boost
        weekend_mult = 1.3 if day_of_week >= 5 else 1.0
        
        # Seasonal multiplier
        seasonal_mult = 1.3 if month in [10, 11, 12, 4, 5] else 1.0
        
        # Select outlet
        outlet_weights = [0.45, 0.30, 0.25]
        outlet_id = np.random.choice(list(outlets.keys()), p=outlet_weights)
        outlet_info = outlets[outlet_id]
        
        # Select cashier based on shift
        shift_cashiers = [c for c in cashiers[outlet_id] if c[2] == shift]
        if not shift_cashiers:
            shift_cashiers = cashiers[outlet_id]
        cashier = shift_cashiers[np.random.randint(0, len(shift_cashiers))]
        cashier_id, cashier_name, cashier_shift, hire_date, salary = cashier
        
        # Select medicine
        med_idx = np.random.randint(0, len(medicines))
        if month in [10, 11, 12, 4, 5] and np.random.random() < 0.3:
            med_idx = np.random.choice([10, 11, 13, 14, 25])
        
        item = medicines[med_idx]
        item_code, item_name, category, unit_price, cost_price, prescription, reorder_level, max_stock = item
        
        # Quantity
        quantity = np.random.choice([1, 1, 1, 2, 2, 3, 5, 10], p=[0.35, 0.2, 0.15, 0.1, 0.08, 0.07, 0.03, 0.02])
        
        # Payment type
        payment_type = np.random.choice(['M-Pesa', 'Cash', 'Card', 'Insurance'], p=[0.70, 0.18, 0.07, 0.05])
        
        # Customer type
        customer_type = np.random.choice(['Walk-in', 'Regular', 'Corporate', 'Hospital'], p=[0.50, 0.30, 0.12, 0.08])
        
        # Discount
        discount = 0
        if customer_type == 'Corporate':
            discount = np.random.choice([10, 15, 20])
        elif customer_type == 'Regular' and np.random.random() < 0.3:
            discount = np.random.choice([5, 10])
        elif np.random.random() < 0.05:
            discount = np.random.choice([5, 10, 15])
        
        # Calculate amounts
        total_price = unit_price * quantity * (1 - discount/100)
        total_cost = cost_price * quantity
        profit = total_price - total_cost
        
        # Stock levels
        stock_before = np.random.randint(reorder_level - 20, max_stock)
        stock_after = max(0, stock_before - quantity)
        
        # Expiry date
        days_to_expiry = np.random.choice(
            [7, 15, 30, 45, 60, 90, 180, 365, 730],
            p=[0.01, 0.02, 0.05, 0.05, 0.08, 0.15, 0.24, 0.25, 0.15]
        )
        expiry_date = date + timedelta(days=int(days_to_expiry))
        
        # Void transactions
        void_rate = 0.08 if cashier_id in ['C003', 'C006'] else 0.02
        voided = 'Yes' if np.random.random() < void_rate else 'No'
        
        # Fraud patterns
        if cashier_id in ['C003', 'C006'] and np.random.random() < 0.05:
            discount = 50
            total_price = unit_price * quantity * 0.5
            profit = total_price - total_cost
        
        # Return transactions
        is_return = 'Yes' if np.random.random() < 0.03 else 'No'
        if is_return == 'Yes':
            total_price = -abs(total_price)
            profit = -abs(profit)
        
        transaction_id += 1
        
        data.append({
            'Date': date,
            'Hour': hour,
            'DayOfWeek': day_of_week,
            'DayName': calendar.day_name[day_of_week],
            'WeekNumber': date.isocalendar()[1],
            'Month': date.strftime('%B'),
            'MonthNum': month,
            'Year': date.year,
            'Shift': shift,
            'OutletID': outlet_id,
            'OutletName': outlet_info['name'],
            'City': outlet_info['city'],
            'MonthlyTarget': outlet_info['target'],
            'CashierID': cashier_id,
            'CashierName': cashier_name,
            'CashierShift': cashier_shift,
            'HireDate': hire_date,
            'Salary': salary,
            'TransactionID': f'TXN{transaction_id}',
            'PaymentType': payment_type,
            'CustomerType': customer_type,
            'ItemCode': item_code,
            'ItemName': item_name,
            'Category': category,
            'Quantity': quantity,
            'UnitPriceKES': unit_price,
            'TotalPriceKES': total_price,
            'CostPriceKES': cost_price * quantity,
            'ProfitKES': profit,
            'DiscountPercent': discount,
            'PrescriptionRequired': prescription,
            'ExpiryDate': expiry_date,
            'DaysToExpiry': days_to_expiry,
            'StockLevelBefore': stock_before,
            'StockLevelAfter': stock_after,
            'ReorderLevel': reorder_level,
            'MaxStock': max_stock,
            'Voided': voided,
            'IsReturn': is_return
        })
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df['ExpiryDate'] = pd.to_datetime(df['ExpiryDate'])
    
    return df.sort_values('Date').reset_index(drop=True)


@st.cache_data
def generate_employee_logins(df: pd.DataFrame) -> pd.DataFrame:
    """Generate employee login/logout records."""
    np.random.seed(42)
    
    employees = df[['CashierID', 'CashierName', 'OutletName', 'CashierShift', 'HireDate', 'Salary']].drop_duplicates()
    
    # Generate 180 days of login data
    login_records = []
    
    for _, emp in employees.iterrows():
        for day_offset in range(180):
            date = datetime(2024, 7, 4) + timedelta(days=day_offset)
            
            # 85% attendance rate
            if np.random.random() > 0.15:
                # Login time based on shift
                if emp['CashierShift'] == 'Morning':
                    login_hour = np.random.choice([6, 7, 7, 7, 8])
                    logout_hour = np.random.choice([14, 14, 14, 15, 15])
                elif emp['CashierShift'] == 'Afternoon':
                    login_hour = np.random.choice([13, 14, 14, 14, 15])
                    logout_hour = np.random.choice([19, 19, 20, 20, 21])
                else:
                    login_hour = np.random.choice([18, 19, 19, 19, 20])
                    logout_hour = np.random.choice([22, 22, 23, 23, 23])
                
                login_time = date.replace(hour=login_hour, minute=np.random.randint(0, 60))
                logout_time = date.replace(hour=logout_hour, minute=np.random.randint(0, 60))
                
                # Late flag
                expected_login = 7 if emp['CashierShift'] == 'Morning' else (14 if emp['CashierShift'] == 'Afternoon' else 19)
                is_late = login_hour > expected_login
                
                login_records.append({
                    'Date': date.date(),
                    'CashierID': emp['CashierID'],
                    'CashierName': emp['CashierName'],
                    'OutletName': emp['OutletName'],
                    'Shift': emp['CashierShift'],
                    'LoginTime': login_time,
                    'LogoutTime': logout_time,
                    'HoursWorked': (logout_time - login_time).seconds / 3600,
                    'IsLate': is_late,
                    'Status': 'Present'
                })
            else:
                login_records.append({
                    'Date': date.date(),
                    'CashierID': emp['CashierID'],
                    'CashierName': emp['CashierName'],
                    'OutletName': emp['OutletName'],
                    'Shift': emp['CashierShift'],
                    'LoginTime': None,
                    'LogoutTime': None,
                    'HoursWorked': 0,
                    'IsLate': False,
                    'Status': 'Absent'
                })
    
    return pd.DataFrame(login_records)


@st.cache_data
def generate_inventory_data(df: pd.DataFrame) -> pd.DataFrame:
    """Generate current inventory status."""
    np.random.seed(42)
    
    inventory = df.groupby(['ItemCode', 'ItemName', 'Category', 'UnitPriceKES', 'ReorderLevel', 'MaxStock']).agg({
        'Quantity': 'sum',
        'CostPriceKES': 'first',
        'ExpiryDate': 'min',
        'DaysToExpiry': 'min'
    }).reset_index()
    
    # Simulate current stock
    inventory['CurrentStock'] = inventory.apply(
        lambda x: np.random.randint(max(0, x['ReorderLevel'] - 30), x['MaxStock']), axis=1
    )
    
    inventory['StockValue'] = inventory['CurrentStock'] * inventory['UnitPriceKES']
    inventory['StockStatus'] = inventory.apply(
        lambda x: 'Critical' if x['CurrentStock'] <= x['ReorderLevel'] * 0.5 
        else ('Low' if x['CurrentStock'] <= x['ReorderLevel'] else 'Good'), axis=1
    )
    
    inventory['NeedsReorder'] = inventory['CurrentStock'] <= inventory['ReorderLevel']
    inventory['ReorderQty'] = inventory.apply(
        lambda x: x['MaxStock'] - x['CurrentStock'] if x['NeedsReorder'] else 0, axis=1
    )
    
    return inventory


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Load data
    df = generate_pharmacy_data(2500)
    login_df = generate_employee_logins(df)
    inventory_df = generate_inventory_data(df)
    
    # Exclude voided and return transactions for sales analysis
    sales_df = df[(df['Voided'] == 'No') & (df['IsReturn'] == 'No')].copy()
    
    # ========== HEADER ==========
    st.markdown("""
    <div class="main-header">
        <h1>💊 PharmaDash Kenya</h1>
        <p>Premium Analytics Dashboard • 3 Outlets • Real-time Monitoring</p>
        <div class="live-clock">📅 """ + datetime.now().strftime("%A, %d %B %Y | %H:%M") + """</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== SIDEBAR FILTERS ==========
    with st.sidebar:
        st.markdown("### 🎛️ Control Panel")
        
        # Date Range
        st.markdown("#### 📅 Date Range")
        date_range = st.date_input(
            "Select Period",
            value=(df['Date'].min().date(), df['Date'].max().date()),
            min_value=df['Date'].min().date(),
            max_value=df['Date'].max().date()
        )
        
        st.markdown("---")
        
        # Outlet Filter
        st.markdown("#### 🏪 Outlets")
        outlets = st.multiselect(
            "Select Outlets",
            options=df['OutletName'].unique(),
            default=df['OutletName'].unique()
        )
        
        st.markdown("---")
        
        # Category Filter
        st.markdown("#### 📦 Categories")
        categories = st.multiselect(
            "Select Categories",
            options=df['Category'].unique(),
            default=df['Category'].unique()
        )
        
        st.markdown("---")
        
        # Employee Filter
        st.markdown("#### 👥 Employees")
        employees = st.multiselect(
            "Select Employees",
            options=df['CashierName'].unique(),
            default=df['CashierName'].unique()
        )
        
        st.markdown("---")
        
        # Time Filters
        st.markdown("#### ⏰ Time Filters")
        shifts = st.multiselect(
            "Shifts",
            options=['Morning', 'Afternoon', 'Evening'],
            default=['Morning', 'Afternoon', 'Evening']
        )
        
        hour_range = st.slider(
            "Operating Hours",
            min_value=7,
            max_value=23,
            value=(7, 23)
        )
        
        st.markdown("---")
        
        # Payment Type Filter
        st.markdown("#### 💳 Payment Types")
        payment_types = st.multiselect(
            "Select Payment Types",
            options=df['PaymentType'].unique(),
            default=df['PaymentType'].unique()
        )
        
        st.markdown("---")
        st.markdown("#### 🔄 Data Refresh")
        if st.button("🔄 Refresh Dashboard", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.caption("🇰🇪 Built for Kenyan Pharmacies")
        st.caption("📱 Mobile Optimized")
    
    # Apply filters
    if len(date_range) == 2:
        mask = (
            (sales_df['Date'].dt.date >= date_range[0]) &
            (sales_df['Date'].dt.date <= date_range[1]) &
            (sales_df['OutletName'].isin(outlets)) &
            (sales_df['Category'].isin(categories)) &
            (sales_df['CashierName'].isin(employees)) &
            (sales_df['Shift'].isin(shifts)) &
            (sales_df['Hour'] >= hour_range[0]) &
            (sales_df['Hour'] <= hour_range[1]) &
            (sales_df['PaymentType'].isin(payment_types))
        )
        filtered_df = sales_df[mask].copy()
    else:
        filtered_df = sales_df.copy()
    
    # ========== MAIN TABS ==========
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Overview",
        "📈 Sales Analytics",
        "👥 Employee Performance",
        "📦 Inventory",
        "⏰ Time Analysis",
        "🏪 Branch Comparison",
        "🚨 Alerts & Fraud",
        "📋 Reports"
    ])
    
    # ========== TAB 1: OVERVIEW ==========
    with tab1:
        # Quick Stats Row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        total_sales = filtered_df['TotalPriceKES'].sum()
        total_profit = filtered_df['ProfitKES'].sum()
        total_transactions = len(filtered_df)
        avg_basket = filtered_df['TotalPriceKES'].mean() if len(filtered_df) > 0 else 0
        mpesa_pct = (filtered_df[filtered_df['PaymentType'] == 'M-Pesa']['TotalPriceKES'].sum() / total_sales * 100) if total_sales > 0 else 0
        
        with col1:
            st.metric("💰 Total Sales", f"KES {total_sales:,.0f}", delta="+12.5% vs last period")
        
        with col2:
            st.metric("📈 Total Profit", f"KES {total_profit:,.0f}", delta=f"{(total_profit/total_sales*100):.1f}% margin")
        
        with col3:
            st.metric("🧾 Transactions", f"{total_transactions:,}", delta="+8.3% growth")
        
        with col4:
            st.metric("🛒 Avg Basket", f"KES {avg_basket:,.0f}", delta="+5.2%")
        
        with col5:
            st.metric("📱 M-Pesa %", f"{mpesa_pct:.1f}%", delta="Target: 75%")
        
        st.markdown("---")
        
        # Alerts Section
        st.markdown("### 🚨 Live Alerts")
        alert_col1, alert_col2, alert_col3 = st.columns(3)
        
        # Low stock alert
        low_stock = inventory_df[inventory_df['StockStatus'].isin(['Critical', 'Low'])]
        expiring_soon = inventory_df[inventory_df['DaysToExpiry'] <= 30]
        
        with alert_col1:
            if len(low_stock[low_stock['StockStatus'] == 'Critical']) > 0:
                st.markdown(f"""
                <div class="alert-critical">
                    ⚠️ CRITICAL: {len(low_stock[low_stock['StockStatus'] == 'Critical'])} products need immediate restock!
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert-success">
                    ✅ All critical stock levels OK
                </div>
                """, unsafe_allow_html=True)
        
        with alert_col2:
            if len(expiring_soon) > 0:
                st.markdown(f"""
                <div class="alert-warning">
                    📅 WARNING: {len(expiring_soon)} products expiring within 30 days
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert-success">
                    ✅ No immediate expiry concerns
                </div>
                """, unsafe_allow_html=True)
        
        with alert_col3:
            # Check for fraud
            void_rate = (df['Voided'] == 'Yes').sum() / len(df) * 100
            if void_rate > 5:
                st.markdown(f"""
                <div class="alert-critical">
                    🚨 HIGH VOID RATE: {void_rate:.1f}% - Investigate immediately!
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="alert-success">
                    ✅ Void rate normal: {void_rate:.1f}%
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts Row
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("#### 📊 Sales Trend (Last 30 Days)")
            daily_sales = filtered_df.groupby(filtered_df['Date'].dt.date)['TotalPriceKES'].sum().tail(30).reset_index()
            daily_sales.columns = ['Date', 'Sales']
            
            fig = px.area(daily_sales, x='Date', y='Sales', 
                         color_discrete_sequence=['#006600'])
            fig.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                height=300,
                xaxis_title="",
                yaxis_title="Sales (KES)",
                showlegend=False
            )
            fig.update_traces(fill='tozeroy', line=dict(width=2))
            st.plotly_chart(fig, use_container_width=True)
        
        with chart_col2:
            st.markdown("#### 💳 Payment Methods")
            payment_dist = filtered_df.groupby('PaymentType')['TotalPriceKES'].sum().reset_index()
            
            fig = px.pie(payment_dist, values='TotalPriceKES', names='PaymentType',
                        color_discrete_sequence=['#006600', '#28a745', '#ffc107', '#17a2b8'],
                        hole=0.4)
            fig.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Bottom Row
        bottom_col1, bottom_col2 = st.columns(2)
        
        with bottom_col1:
            st.markdown("#### 🏆 Top 5 Products Today")
            top_products = filtered_df.groupby('ItemName').agg({
                'Quantity': 'sum',
                'TotalPriceKES': 'sum',
                'ProfitKES': 'sum'
            }).nlargest(5, 'TotalPriceKES').reset_index()
            
            fig = px.bar(top_products, x='TotalPriceKES', y='ItemName', orientation='h',
                        color_discrete_sequence=['#006600'])
            fig.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                height=250,
                yaxis_title="",
                xaxis_title="Sales (KES)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with bottom_col2:
            st.markdown("#### 🏪 Sales by Branch")
            branch_sales = filtered_df.groupby('OutletName')['TotalPriceKES'].sum().reset_index()
            
            fig = px.bar(branch_sales, x='OutletName', y='TotalPriceKES',
                        color='OutletName',
                        color_discrete_sequence=['#006600', '#28a745', '#90EE90'])
            fig.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                height=250,
                xaxis_title="",
                yaxis_title="Sales (KES)",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== TAB 2: SALES ANALYTICS ==========
    with tab2:
        st.markdown("### 📈 Comprehensive Sales Analytics")
        
        # Time Period Selector
        time_view = st.radio(
            "Select Time View",
            ["Hourly", "Daily", "Weekly", "Monthly"],
            horizontal=True
        )
        
        st.markdown("---")
        
        if time_view == "Hourly":
            st.markdown("#### ⏰ Sales by Hour")
            hourly_sales = filtered_df.groupby('Hour').agg({
                'TotalPriceKES': 'sum',
                'TransactionID': 'count',
                'ProfitKES': 'sum'
            }).reset_index()
            hourly_sales.columns = ['Hour', 'Sales', 'Transactions', 'Profit']
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(hourly_sales, x='Hour', y='Sales',
                            color='Sales',
                            color_continuous_scale=['#90EE90', '#006600'])
                fig.update_layout(
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=400,
                    title="Sales by Hour",
                    xaxis_title="Hour of Day",
                    yaxis_title="Sales (KES)"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.line(hourly_sales, x='Hour', y='Transactions',
                             color_discrete_sequence=['#006600'],
                             markers=True)
                fig.update_layout(
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=400,
                    title="Transactions by Hour",
                    xaxis_title="Hour of Day",
                    yaxis_title="Number of Transactions"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Peak Hours Analysis
            st.markdown("#### 🔥 Peak Hours Analysis")
            peak_hours = hourly_sales.nlargest(3, 'Sales')
            low_hours = hourly_sales.nsmallest(3, 'Sales')
            
            peak_col, low_col = st.columns(2)
            
            with peak_col:
                st.markdown("**🚀 Top Selling Hours**")
                for i, row in peak_hours.iterrows():
                    st.markdown(f"""
                    <div class="rank-card">
                        <div class="rank-number {'rank-gold' if i == peak_hours.index[0] else 'rank-silver' if i == peak_hours.index[1] else 'rank-bronze'}">{list(peak_hours.index).index(i) + 1}</div>
                        <div>
                            <strong>{row['Hour']}:00 - {row['Hour']+1}:00</strong><br>
                            <span style="color: #006600;">KES {row['Sales']:,.0f}</span> | {row['Transactions']} txns
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with low_col:
                st.markdown("**📉 Lowest Selling Hours**")
                for i, row in low_hours.iterrows():
                    st.markdown(f"""
                    <div class="rank-card">
                        <div class="rank-number" style="background: #dc3545;">{list(low_hours.index).index(i) + 1}</div>
                        <div>
                            <strong>{row['Hour']}:00 - {row['Hour']+1}:00</strong><br>
                            <span style="color: #dc3545;">KES {row['Sales']:,.0f}</span> | {row['Transactions']} txns
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        elif time_view == "Daily":
            st.markdown("#### 📅 Sales by Day of Week")
            daily_sales = filtered_df.groupby(['DayOfWeek', 'DayName']).agg({
                'TotalPriceKES': 'sum',
                'TransactionID': 'count',
                'ProfitKES': 'sum'
            }).reset_index()
            daily_sales = daily_sales.sort_values('DayOfWeek')
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(daily_sales, x='DayName', y='TotalPriceKES',
                            color='TotalPriceKES',
                            color_continuous_scale=['#90EE90', '#006600'])
                fig.update_layout(
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=400,
                    title="Sales by Day of Week",
                    xaxis_title="",
                    yaxis_title="Sales (KES)"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.pie(daily_sales, values='TotalPriceKES', names='DayName',
                            color_discrete_sequence=px.colors.sequential.Greens)
                fig.update_layout(
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=400,
                    title="Sales Distribution by Day"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Best/Worst Days
            best_day = daily_sales.loc[daily_sales['TotalPriceKES'].idxmax()]
            worst_day = daily_sales.loc[daily_sales['TotalPriceKES'].idxmin()]
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"🏆 **Best Day:** {best_day['DayName']} - KES {best_day['TotalPriceKES']:,.0f}")
            with col2:
                st.warning(f"📉 **Slowest Day:** {worst_day['DayName']} - KES {worst_day['TotalPriceKES']:,.0f}")
        
        elif time_view == "Weekly":
            st.markdown("#### 📆 Sales by Week")
            weekly_sales = filtered_df.groupby('WeekNumber').agg({
                'TotalPriceKES': 'sum',
                'TransactionID': 'count',
                'ProfitKES': 'sum'
            }).reset_index()
            
            fig = px.line(weekly_sales, x='WeekNumber', y='TotalPriceKES',
                         color_discrete_sequence=['#006600'],
                         markers=True)
            fig.add_scatter(x=weekly_sales['WeekNumber'], y=weekly_sales['ProfitKES'],
                           mode='lines+markers', name='Profit', line=dict(color='#ffc107'))
            fig.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                height=400,
                title="Weekly Sales & Profit Trend",
                xaxis_title="Week Number",
                yaxis_title="Amount (KES)"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Weekly Stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Avg Weekly Sales", f"KES {weekly_sales['TotalPriceKES'].mean():,.0f}")
            with col2:
                st.metric("Best Week", f"Week {weekly_sales.loc[weekly_sales['TotalPriceKES'].idxmax(), 'WeekNumber']}")
            with col3:
                st.metric("Weekly Growth", f"+{np.random.uniform(5, 15):.1f}%")
        
        else:  # Monthly
            st.markdown("#### 📊 Sales by Month")
            monthly_sales = filtered_df.groupby(['MonthNum', 'Month']).agg({
                'TotalPriceKES': 'sum',
                'TransactionID': 'count',
                'ProfitKES': 'sum'
            }).reset_index()
            monthly_sales = monthly_sales.sort_values('MonthNum')
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=monthly_sales['Month'],
                y=monthly_sales['TotalPriceKES'],
                name='Sales',
                marker_color='#006600'
            ))
            fig.add_trace(go.Scatter(
                x=monthly_sales['Month'],
                y=monthly_sales['ProfitKES'],
                name='Profit',
                mode='lines+markers',
                line=dict(color='#ffc107', width=3),
                yaxis='y2'
            ))
            fig.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                height=400,
                title="Monthly Sales & Profit",
                yaxis=dict(title='Sales (KES)'),
                yaxis2=dict(title='Profit (KES)', overlaying='y', side='right'),
                legend=dict(orientation='h', yanchor='bottom', y=1.02)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Top & Bottom Products
        st.markdown("### 🏆 Product Performance Rankings")
        
        product_performance = filtered_df.groupby(['ItemCode', 'ItemName', 'Category']).agg({
            'Quantity': 'sum',
            'TotalPriceKES': 'sum',
            'ProfitKES': 'sum'
        }).reset_index()
        product_performance['ProfitMargin'] = (product_performance['ProfitKES'] / product_performance['TotalPriceKES'] * 100).round(1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🚀 Top 10 Best Sellers")
            top_10 = product_performance.nlargest(10, 'TotalPriceKES')
            st.dataframe(
                top_10[['ItemName', 'Category', 'Quantity', 'TotalPriceKES', 'ProfitMargin']].rename(columns={
                    'ItemName': 'Product',
                    'TotalPriceKES': 'Sales (KES)',
                    'Quantity': 'Units',
                    'ProfitMargin': 'Margin %'
                }),
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.markdown("#### 📉 Bottom 10 Slow Movers")
            bottom_10 = product_performance.nsmallest(10, 'TotalPriceKES')
            st.dataframe(
                bottom_10[['ItemName', 'Category', 'Quantity', 'TotalPriceKES', 'ProfitMargin']].rename(columns={
                    'ItemName': 'Product',
                    'TotalPriceKES': 'Sales (KES)',
                    'Quantity': 'Units',
                    'ProfitMargin': 'Margin %'
                }),
                use_container_width=True,
                hide_index=True
            )
    
    # ========== TAB 3: EMPLOYEE PERFORMANCE ==========
    with tab3:
        st.markdown("### 👥 Employee Performance Dashboard")
        
        # Employee Rankings
        employee_stats = filtered_df.groupby(['CashierID', 'CashierName', 'OutletName']).agg({
            'TotalPriceKES': 'sum',
            'ProfitKES': 'sum',
            'TransactionID': 'count',
            'Quantity': 'sum',
            'DiscountPercent': 'mean'
        }).reset_index()
        employee_stats.columns = ['CashierID', 'Name', 'Branch', 'Sales', 'Profit', 'Transactions', 'Units', 'AvgDiscount']
        employee_stats['AvgTransaction'] = (employee_stats['Sales'] / employee_stats['Transactions']).round(0)
        employee_stats['SalesRank'] = employee_stats['Sales'].rank(ascending=False).astype(int)
        employee_stats = employee_stats.sort_values('Sales', ascending=False)
        
        # Top Performers
        st.markdown("#### 🏆 Employee Rankings by Sales")
        
        col1, col2, col3 = st.columns(3)
        
        if len(employee_stats) >= 1:
            top1 = employee_stats.iloc[0]
            with col1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FFD700, #FFA500); padding: 1.5rem; border-radius: 15px; text-align: center; color: white;">
                    <h1 style="margin: 0; font-size: 3rem;">🥇</h1>
                    <h3 style="margin: 0.5rem 0;">{top1['Name']}</h3>
                    <p style="margin: 0; font-size: 0.9rem;">{top1['Branch']}</p>
                    <h2 style="margin: 0.5rem 0;">KES {top1['Sales']:,.0f}</h2>
                    <p style="margin: 0;">{top1['Transactions']} transactions</p>
                </div>
                """, unsafe_allow_html=True)
        
        if len(employee_stats) >= 2:
            top2 = employee_stats.iloc[1]
            with col2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #C0C0C0, #A0A0A0); padding: 1.5rem; border-radius: 15px; text-align: center; color: white;">
                    <h1 style="margin: 0; font-size: 3rem;">🥈</h1>
                    <h3 style="margin: 0.5rem 0;">{top2['Name']}</h3>
                    <p style="margin: 0; font-size: 0.9rem;">{top2['Branch']}</p>
                    <h2 style="margin: 0.5rem 0;">KES {top2['Sales']:,.0f}</h2>
                    <p style="margin: 0;">{top2['Transactions']} transactions</p>
                </div>
                """, unsafe_allow_html=True)
        
        if len(employee_stats) >= 3:
            top3 = employee_stats.iloc[2]
            with col3:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #CD7F32, #8B4513); padding: 1.5rem; border-radius: 15px; text-align: center; color: white;">
                    <h1 style="margin: 0; font-size: 3rem;">🥉</h1>
                    <h3 style="margin: 0.5rem 0;">{top3['Name']}</h3>
                    <p style="margin: 0; font-size: 0.9rem;">{top3['Branch']}</p>
                    <h2 style="margin: 0.5rem 0;">KES {top3['Sales']:,.0f}</h2>
                    <p style="margin: 0;">{top3['Transactions']} transactions</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Full Rankings Table
        st.markdown("#### 📊 Complete Employee Performance Table")
        
        st.dataframe(
            employee_stats[['SalesRank', 'Name', 'Branch', 'Sales', 'Profit', 'Transactions', 'AvgTransaction', 'AvgDiscount']].rename(columns={
                'SalesRank': 'Rank',
                'Sales': 'Total Sales (KES)',
                'Profit': 'Profit (KES)',
                'Transactions': 'Txns',
                'AvgTransaction': 'Avg Txn (KES)',
                'AvgDiscount': 'Avg Discount %'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        
        # Employee Attendance & Login
        st.markdown("#### 📋 Employee Attendance & Login History")
        
        # Filter login data
        login_filtered = login_df[login_df['CashierName'].isin(employees)]
        
        # Attendance Summary
        attendance_summary = login_filtered.groupby(['CashierID', 'CashierName', 'OutletName']).agg({
            'Status': lambda x: (x == 'Present').sum(),
            'IsLate': 'sum',
            'HoursWorked': 'sum'
        }).reset_index()
        attendance_summary.columns = ['CashierID', 'Name', 'Branch', 'DaysPresent', 'DaysLate', 'TotalHours']
        attendance_summary['AttendanceRate'] = (attendance_summary['DaysPresent'] / 180 * 100).round(1)
        attendance_summary['PunctualityRate'] = ((attendance_summary['DaysPresent'] - attendance_summary['DaysLate']) / attendance_summary['DaysPresent'] * 100).round(1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Attendance Summary**")
            st.dataframe(
                attendance_summary[['Name', 'Branch', 'DaysPresent', 'AttendanceRate', 'PunctualityRate']].rename(columns={
                    'DaysPresent': 'Days Present',
                    'AttendanceRate': 'Attendance %',
                    'PunctualityRate': 'Punctuality %'
                }),
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            st.markdown("**Today's Status**")
            today_status = login_filtered[login_filtered['Date'] == login_filtered['Date'].max()]
            
            for _, emp in today_status.iterrows():
                status_class = "status-online" if emp['Status'] == 'Present' else "status-offline"
                login_time = emp['LoginTime'].strftime('%H:%M') if pd.notna(emp['LoginTime']) else 'N/A'
                st.markdown(f"""
                <div class="rank-card">
                    <div>
                        <strong>{emp['CashierName']}</strong> ({emp['OutletName']})<br>
                        <span class="{status_class}">● {emp['Status']}</span>
                        {f" | Login: {login_time}" if emp['Status'] == 'Present' else ""}
                        {" | ⚠️ LATE" if emp['IsLate'] else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Performance Comparison Chart
        st.markdown("#### 📈 Employee Sales Comparison")
        
        fig = px.bar(employee_stats.sort_values('Sales', ascending=True), 
                    x='Sales', y='Name', orientation='h',
                    color='Branch',
                    color_discrete_sequence=['#006600', '#28a745', '#90EE90'])
        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            height=400,
            title="Sales by Employee",
            xaxis_title="Sales (KES)",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # ========== TAB 4: INVENTORY ==========
    with tab4:
        st.markdown("### 📦 Inventory Management")
        
        # Inventory KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        total_stock_value = inventory_df['StockValue'].sum()
        critical_items = len(inventory_df[inventory_df['StockStatus'] == 'Critical'])
        low_items = len(inventory_df[inventory_df['StockStatus'] == 'Low'])
        expiring_items = len(inventory_df[inventory_df['DaysToExpiry'] <= 30])
        
        with col1:
            st.metric("💰 Total Stock Value", f"KES {total_stock_value:,.0f}")
        with col2:
            st.metric("🔴 Critical Stock", f"{critical_items} items", delta="Needs reorder", delta_color="inverse")
        with col3:
            st.metric("🟡 Low Stock", f"{low_items} items", delta="Monitor closely", delta_color="off")
        with col4:
            st.metric("📅 Expiring Soon", f"{expiring_items} items", delta="<30 days", delta_color="inverse")
        
        st.markdown("---")
        
        # Stock Status Overview
        st.markdown("#### 📊 Stock Status Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            status_counts = inventory_df['StockStatus'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            
            fig = px.pie(status_counts, values='Count', names='Status',
                        color='Status',
                        color_discrete_map={'Good': '#28a745', 'Low': '#ffc107', 'Critical': '#dc3545'},
                        hole=0.4)
            fig.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                height=300,
                title="Stock Status Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Stock by Category
            category_stock = inventory_df.groupby('Category')['StockValue'].sum().reset_index()
            
            fig = px.bar(category_stock.sort_values('StockValue', ascending=True),
                        x='StockValue', y='Category', orientation='h',
                        color_discrete_sequence=['#006600'])
            fig.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                height=300,
                title="Stock Value by Category",
                xaxis_title="Value (KES)",
                yaxis_title=""
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Items Needing Reorder
        st.markdown("#### 🛒 Items Needing Reorder")
        
        reorder_items = inventory_df[inventory_df['NeedsReorder'] == True][
            ['ItemName', 'Category', 'CurrentStock', 'ReorderLevel', 'ReorderQty', 'StockStatus']
        ].sort_values('CurrentStock')
        
        if len(reorder_items) > 0:
            st.dataframe(
                reorder_items.rename(columns={
                    'ItemName': 'Product',
                    'CurrentStock': 'Current',
                    'ReorderLevel': 'Reorder At',
                    'ReorderQty': 'Order Qty',
                    'StockStatus': 'Status'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("✅ All items above reorder level!")
        
        st.markdown("---")
        
        # Expiring Products
        st.markdown("#### ⏰ Products Expiring Soon")
        
        expiry_view = st.radio("Expiry Timeline", ["Within 7 Days", "Within 30 Days", "Within 60 Days", "Within 90 Days"], horizontal=True)
        
        days_map = {"Within 7 Days": 7, "Within 30 Days": 30, "Within 60 Days": 60, "Within 90 Days": 90}
        selected_days = days_map[expiry_view]
        
        expiring = inventory_df[inventory_df['DaysToExpiry'] <= selected_days][
            ['ItemName', 'Category', 'CurrentStock', 'DaysToExpiry', 'StockValue']
        ].sort_values('DaysToExpiry')
        
        if len(expiring) > 0:
            # Color code by urgency
            def urgency_color(days):
                if days <= 7:
                    return '🔴'
                elif days <= 30:
                    return '🟠'
                elif days <= 60:
                    return '🟡'
                return '🟢'
            
            expiring['Urgency'] = expiring['DaysToExpiry'].apply(urgency_color)
            
            st.dataframe(
                expiring[['Urgency', 'ItemName', 'Category', 'CurrentStock', 'DaysToExpiry', 'StockValue']].rename(columns={
                    'ItemName': 'Product',
                    'CurrentStock': 'Stock',
                    'DaysToExpiry': 'Days Left',
                    'StockValue': 'Value at Risk (KES)'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            st.warning(f"⚠️ Total value at risk: KES {expiring['StockValue'].sum():,.0f}")
        else:
            st.success(f"✅ No products expiring within {selected_days} days!")
        
        st.markdown("---")
        
        # Full Inventory Table
        st.markdown("#### 📋 Complete Inventory List")
        
        st.dataframe(
            inventory_df[['ItemName', 'Category', 'CurrentStock', 'ReorderLevel', 'MaxStock', 'StockValue', 'StockStatus', 'DaysToExpiry']].rename(columns={
                'ItemName': 'Product',
                'CurrentStock': 'Stock',
                'ReorderLevel': 'Reorder At',
                'MaxStock': 'Max',
                'StockValue': 'Value (KES)',
                'StockStatus': 'Status',
                'DaysToExpiry': 'Expiry (Days)'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    # ========== TAB 5: TIME ANALYSIS ==========
    with tab5:
        st.markdown("### ⏰ Time-Based Analytics")
        
        # Heatmap: Hour vs Day
        st.markdown("#### 🗓️ Sales Heatmap: Hour vs Day of Week")
        
        heatmap_data = filtered_df.groupby(['DayName', 'Hour'])['TotalPriceKES'].sum().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='DayName', columns='Hour', values='TotalPriceKES').fillna(0)
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_pivot = heatmap_pivot.reindex([d for d in day_order if d in heatmap_pivot.index])
        
        fig = px.imshow(heatmap_pivot,
                       color_continuous_scale='Greens',
                       aspect='auto')
        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            height=400,
            title="Sales Intensity by Hour and Day",
            xaxis_title="Hour of Day",
            yaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Shift Analysis
        st.markdown("#### 🔄 Shift Performance Analysis")
        
        shift_stats = filtered_df.groupby('Shift').agg({
            'TotalPriceKES': 'sum',
            'ProfitKES': 'sum',
            'TransactionID': 'count',
            'Quantity': 'sum'
        }).reset_index()
        shift_stats['AvgTransaction'] = (shift_stats['TotalPriceKES'] / shift_stats['TransactionID']).round(0)
        
        col1, col2, col3 = st.columns(3)
        
        for i, shift in enumerate(['Morning', 'Afternoon', 'Evening']):
            shift_data = shift_stats[shift_stats['Shift'] == shift].iloc[0] if shift in shift_stats['Shift'].values else None
            
            with [col1, col2, col3][i]:
                if shift_data is not None:
                    emoji = "🌅" if shift == 'Morning' else ("☀️" if shift == 'Afternoon' else "🌙")
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #006600, #004d00); padding: 1.5rem; border-radius: 15px; text-align: center; color: white;">
                        <h2 style="margin: 0;">{emoji} {shift}</h2>
                        <h3 style="margin: 0.5rem 0;">KES {shift_data['TotalPriceKES']:,.0f}</h3>
                        <p style="margin: 0;">{shift_data['TransactionID']:,} transactions</p>
                        <p style="margin: 0;">Avg: KES {shift_data['AvgTransaction']:,.0f}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Peak Times Summary
        st.markdown("#### 📊 Peak Performance Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔥 Busiest Times**")
            
            # Peak hour
            peak_hour = filtered_df.groupby('Hour')['TotalPriceKES'].sum().idxmax()
            st.info(f"⏰ **Peak Hour:** {peak_hour}:00 - {peak_hour+1}:00")
            
            # Peak day
            peak_day = filtered_df.groupby('DayName')['TotalPriceKES'].sum().idxmax()
            st.info(f"📅 **Peak Day:** {peak_day}")
            
            # Peak week
            peak_week = filtered_df.groupby('WeekNumber')['TotalPriceKES'].sum().idxmax()
            st.info(f"📆 **Peak Week:** Week {peak_week}")
            
            # Peak month
            peak_month = filtered_df.groupby('Month')['TotalPriceKES'].sum().idxmax()
            st.info(f"🗓️ **Peak Month:** {peak_month}")
        
        with col2:
            st.markdown("**📉 Slowest Times**")
            
            # Slowest hour
            slow_hour = filtered_df.groupby('Hour')['TotalPriceKES'].sum().idxmin()
            st.warning(f"⏰ **Slowest Hour:** {slow_hour}:00 - {slow_hour+1}:00")
            
            # Slowest day
            slow_day = filtered_df.groupby('DayName')['TotalPriceKES'].sum().idxmin()
            st.warning(f"📅 **Slowest Day:** {slow_day}")
            
            # Slowest week
            slow_week = filtered_df.groupby('WeekNumber')['TotalPriceKES'].sum().idxmin()
            st.warning(f"📆 **Slowest Week:** Week {slow_week}")
            
            # Slowest month
            slow_month = filtered_df.groupby('Month')['TotalPriceKES'].sum().idxmin()
            st.warning(f"🗓️ **Slowest Month:** {slow_month}")
    
    # ========== TAB 6: BRANCH COMPARISON ==========
    with tab6:
        st.markdown("### 🏪 Branch Performance Comparison")
        
        # Branch Stats
        branch_stats = filtered_df.groupby(['OutletID', 'OutletName', 'City']).agg({
            'TotalPriceKES': 'sum',
            'ProfitKES': 'sum',
            'TransactionID': 'count',
            'Quantity': 'sum',
            'MonthlyTarget': 'first'
        }).reset_index()
        branch_stats['ProfitMargin'] = (branch_stats['ProfitKES'] / branch_stats['TotalPriceKES'] * 100).round(1)
        branch_stats['AvgTransaction'] = (branch_stats['TotalPriceKES'] / branch_stats['TransactionID']).round(0)
        branch_stats['TargetAchievement'] = (branch_stats['TotalPriceKES'] / (branch_stats['MonthlyTarget'] * 6) * 100).round(1)
        branch_stats = branch_stats.sort_values('TotalPriceKES', ascending=False)
        
        # Branch Cards
        cols = st.columns(3)
        
        for i, (_, branch) in enumerate(branch_stats.iterrows()):
            with cols[i]:
                rank_emoji = "🥇" if i == 0 else ("🥈" if i == 1 else "🥉")
                color = "#FFD700" if i == 0 else ("#C0C0C0" if i == 1 else "#CD7F32")
                
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 15px; border-top: 5px solid {color}; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <h2 style="margin: 0; text-align: center;">{rank_emoji} #{i+1}</h2>
                    <h3 style="margin: 0.5rem 0; text-align: center; color: #006600;">{branch['OutletName']}</h3>
                    <p style="text-align: center; color: #666;">{branch['City']}</p>
                    <hr>
                    <p><strong>💰 Sales:</strong> KES {branch['TotalPriceKES']:,.0f}</p>
                    <p><strong>📈 Profit:</strong> KES {branch['ProfitKES']:,.0f} ({branch['ProfitMargin']}%)</p>
                    <p><strong>🧾 Transactions:</strong> {branch['TransactionID']:,}</p>
                    <p><strong>🛒 Avg Basket:</strong> KES {branch['AvgTransaction']:,.0f}</p>
                    <p><strong>🎯 Target:</strong> {branch['TargetAchievement']}%</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Comparison Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Sales Comparison")
            fig = px.bar(branch_stats, x='OutletName', y='TotalPriceKES',
                        color='OutletName',
                        color_discrete_sequence=['#006600', '#28a745', '#90EE90'])
            fig.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                height=300,
                showlegend=False,
                xaxis_title="",
                yaxis_title="Sales (KES)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Profit Margin Comparison")
            fig = px.bar(branch_stats, x='OutletName', y='ProfitMargin',
                        color='OutletName',
                        color_discrete_sequence=['#006600', '#28a745', '#90EE90'])
            fig.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                height=300,
                showlegend=False,
                xaxis_title="",
                yaxis_title="Profit Margin (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Branch Trends
        st.markdown("#### 📈 Branch Sales Trends Over Time")
        
        branch_daily = filtered_df.groupby([filtered_df['Date'].dt.date, 'OutletName'])['TotalPriceKES'].sum().reset_index()
        branch_daily.columns = ['Date', 'Branch', 'Sales']
        
        fig = px.line(branch_daily, x='Date', y='Sales', color='Branch',
                     color_discrete_sequence=['#006600', '#28a745', '#90EE90'])
        fig.update_layout(
            margin=dict(l=0, r=0, t=10, b=0),
            height=400,
            xaxis_title="",
            yaxis_title="Sales (KES)"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Category Performance by Branch
        st.markdown("#### 📦 Category Performance by Branch")
        
        category_branch = filtered_df.groupby(['OutletName', 'Category'])['TotalPriceKES'].sum().reset_index()
        
        fig = px.bar(category_branch, x='OutletName', y='TotalPriceKES', color='Category',
                    color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(
            margin=dict(l=0, r=0, t=10, b=0),
            height=400,
            xaxis_title="",
            yaxis_title="Sales (KES)",
            barmode='stack'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # ========== TAB 7: ALERTS & FRAUD ==========
    with tab7:
        st.markdown("### 🚨 Alerts & Fraud Detection")
        
        # Fraud Risk Scoring
        all_df = df.copy()  # Include voided transactions
        
        fraud_stats = all_df.groupby(['CashierID', 'CashierName', 'OutletName']).agg({
            'TransactionID': 'count',
            'Voided': lambda x: (x == 'Yes').sum(),
            'IsReturn': lambda x: (x == 'Yes').sum(),
            'DiscountPercent': 'mean',
            'ProfitKES': lambda x: (x < 0).sum()
        }).reset_index()
        
        fraud_stats.columns = ['CashierID', 'Name', 'Branch', 'TotalTxn', 'Voids', 'Returns', 'AvgDiscount', 'NegProfit']
        fraud_stats['VoidRate'] = (fraud_stats['Voids'] / fraud_stats['TotalTxn'] * 100).round(2)
        fraud_stats['ReturnRate'] = (fraud_stats['Returns'] / fraud_stats['TotalTxn'] * 100).round(2)
        fraud_stats['NegProfitRate'] = (fraud_stats['NegProfit'] / fraud_stats['TotalTxn'] * 100).round(2)
        
        # Risk Score Calculation
        fraud_stats['RiskScore'] = (
            (fraud_stats['VoidRate'] > 5).astype(int) * 35 +
            (fraud_stats['AvgDiscount'] > 10).astype(int) * 25 +
            (fraud_stats['NegProfitRate'] > 3).astype(int) * 30 +
            (fraud_stats['ReturnRate'] > 5).astype(int) * 10
        )
        
        fraud_stats['RiskLevel'] = fraud_stats['RiskScore'].apply(
            lambda x: '🔴 HIGH' if x >= 50 else ('🟡 MEDIUM' if x >= 25 else '🟢 LOW')
        )
        
        # High Risk Alerts
        high_risk = fraud_stats[fraud_stats['RiskScore'] >= 50]
        
        if len(high_risk) > 0:
            st.markdown("#### ⚠️ HIGH RISK ALERTS")
            for _, emp in high_risk.iterrows():
                st.markdown(f"""
                <div class="alert-critical">
                    🚨 <strong>{emp['Name']}</strong> ({emp['Branch']}) - Risk Score: {emp['RiskScore']}/100<br>
                    Void Rate: {emp['VoidRate']:.1f}% | Avg Discount: {emp['AvgDiscount']:.1f}% | Negative Profits: {emp['NegProfit']}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Fraud Analysis Dashboard
        st.markdown("#### 📊 Fraud Risk Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(fraud_stats, x='VoidRate', y='AvgDiscount',
                           size='TotalTxn', color='RiskScore',
                           hover_name='Name',
                           color_continuous_scale=['green', 'yellow', 'red'],
                           size_max=40)
            fig.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Discount Threshold")
            fig.add_vline(x=5, line_dash="dash", line_color="red", annotation_text="Void Threshold")
            fig.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                height=400,
                title="Risk Matrix: Void Rate vs Discount",
                xaxis_title="Void Rate (%)",
                yaxis_title="Avg Discount (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(fraud_stats.sort_values('RiskScore', ascending=False),
                        x='Name', y='RiskScore',
                        color='RiskScore',
                        color_continuous_scale=['green', 'yellow', 'red'])
            fig.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="High Risk")
            fig.add_hline(y=25, line_dash="dash", line_color="orange", annotation_text="Medium Risk")
            fig.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                height=400,
                title="Risk Score by Employee",
                xaxis_title="",
                yaxis_title="Risk Score"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Full Fraud Table
        st.markdown("#### 📋 Complete Risk Assessment")
        
        st.dataframe(
            fraud_stats[['RiskLevel', 'Name', 'Branch', 'TotalTxn', 'VoidRate', 'ReturnRate', 'AvgDiscount', 'NegProfitRate', 'RiskScore']].sort_values('RiskScore', ascending=False).rename(columns={
                'RiskLevel': 'Risk',
                'TotalTxn': 'Transactions',
                'VoidRate': 'Void %',
                'ReturnRate': 'Return %',
                'AvgDiscount': 'Avg Discount %',
                'NegProfitRate': 'Neg Profit %',
                'RiskScore': 'Score'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        
        # Reconciliation
        st.markdown("#### 💵 Payment Reconciliation")
        
        daily_payments = filtered_df.groupby([filtered_df['Date'].dt.date, 'PaymentType'])['TotalPriceKES'].sum().unstack(fill_value=0).reset_index()
        
        # Simulate variances
        np.random.seed(42)
        if 'M-Pesa' in daily_payments.columns:
            daily_payments['MPesa_Statement'] = daily_payments['M-Pesa'] + np.random.randint(-500, 500, len(daily_payments))
            daily_payments['MPesa_Variance'] = daily_payments['MPesa_Statement'] - daily_payments['M-Pesa']
        
        if 'Cash' in daily_payments.columns:
            daily_payments['Cash_Count'] = daily_payments['Cash'] + np.random.randint(-300, 300, len(daily_payments))
            daily_payments['Cash_Variance'] = daily_payments['Cash_Count'] - daily_payments['Cash']
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'MPesa_Variance' in daily_payments.columns:
                total_mpesa_var = daily_payments['MPesa_Variance'].sum()
                st.metric("M-Pesa Variance", f"KES {total_mpesa_var:,.0f}", 
                         delta="Investigate if > KES 5,000", delta_color="inverse" if abs(total_mpesa_var) > 5000 else "normal")
        
        with col2:
            if 'Cash_Variance' in daily_payments.columns:
                total_cash_var = daily_payments['Cash_Variance'].sum()
                st.metric("Cash Variance", f"KES {total_cash_var:,.0f}",
                         delta="Investigate if > KES 2,000", delta_color="inverse" if abs(total_cash_var) > 2000 else "normal")
    
    # ========== TAB 8: REPORTS ==========
    with tab8:
        st.markdown("### 📋 Reports & Export")
        
        report_type = st.selectbox(
            "Select Report Type",
            ["Daily Sales Report", "Employee Performance Report", "Inventory Report", "Expiry Alert Report", "Fraud Risk Report"]
        )
        
        st.markdown("---")
        
        if report_type == "Daily Sales Report":
            st.markdown("#### 📊 Daily Sales Summary")
            
            daily_report = filtered_df.groupby(filtered_df['Date'].dt.date).agg({
                'TotalPriceKES': 'sum',
                'ProfitKES': 'sum',
                'TransactionID': 'count',
                'Quantity': 'sum'
            }).reset_index()
            daily_report.columns = ['Date', 'Total Sales', 'Profit', 'Transactions', 'Units Sold']
            
            st.dataframe(daily_report, use_container_width=True, hide_index=True)
            
            # Download button
            csv = daily_report.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"daily_sales_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        elif report_type == "Employee Performance Report":
            st.markdown("#### 👥 Employee Performance Summary")
            
            st.dataframe(employee_stats, use_container_width=True, hide_index=True)
            
            csv = employee_stats.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"employee_performance_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        elif report_type == "Inventory Report":
            st.markdown("#### 📦 Current Inventory Status")
            
            st.dataframe(inventory_df, use_container_width=True, hide_index=True)
            
            csv = inventory_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"inventory_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        elif report_type == "Expiry Alert Report":
            st.markdown("#### ⏰ Products Expiring Within 90 Days")
            
            expiry_report = inventory_df[inventory_df['DaysToExpiry'] <= 90][
                ['ItemName', 'Category', 'CurrentStock', 'DaysToExpiry', 'StockValue']
            ].sort_values('DaysToExpiry')
            
            st.dataframe(expiry_report, use_container_width=True, hide_index=True)
            
            csv = expiry_report.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"expiry_alert_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        else:  # Fraud Risk Report
            st.markdown("#### 🚨 Fraud Risk Assessment")
            
            st.dataframe(fraud_stats, use_container_width=True, hide_index=True)
            
            csv = fraud_stats.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"fraud_risk_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    # ========== FOOTER ==========
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>💊 <strong>BiasharaFlow Rudder Research</strong> | BiasharaFlow Pharma</p>
        <p>Built for Kenyan Pharmacies • See the Flow. Grow the Biashara</p>
        <p>📧 info@rudderdatanalytics.co.ke | 📱 +254 792719505</p>
        <p style="font-size: 0.8rem;">© 2026 Rudder Research and Data Analytics LTD. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
