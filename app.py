"""
Kenya Pharmacy Dashboard - 3-Outlet SME Analytics
Executive-grade remote monitoring for Kenyan chemists/pharmacies
Mobile-first, M-Pesa focused, fraud detection enabled
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# SECTION 1: SIMULATED PHARMACY DATASET GENERATION
# ============================================================================

@st.cache_data
def generate_pharmacy_data(num_rows: int = 1500, seed: int = 42) -> pd.DataFrame:
    """
    Generate realistic Kenyan pharmacy transaction data for 3 outlets over 6 months.
    Includes M-Pesa dominance, seasonal patterns, fraud anomalies, and expiry tracking.
    """
    np.random.seed(seed)
    
    # Configuration
    outlets = {
        'OUT001': 'Nairobi CBD',
        'OUT002': 'Mombasa Nyali',
        'OUT003': 'Kisumu Mega'
    }
    
    cashiers = {
        'OUT001': [('C001', 'Jane Wanjiku'), ('C002', 'Peter Omondi'), ('C003', 'Grace Muthoni')],
        'OUT002': [('C004', 'Hassan Ali'), ('C005', 'Fatma Said'), ('C006', 'Kevin Otieno')],
        'OUT003': [('C007', 'Lucy Achieng'), ('C008', 'James Kiprop'), ('C009', 'Mary Nekesa')]
    }
    
    # Medicine catalog with realistic Kenyan pricing
    medicines = [
        # (ItemCode, ItemName, Category, UnitPrice, CostPrice, PrescriptionRequired)
        ('MED001', 'Paracetamol 500mg', 'Painkillers', 50, 30, 'No'),
        ('MED002', 'Ibuprofen 400mg', 'Painkillers', 80, 50, 'No'),
        ('MED003', 'Amoxicillin 500mg', 'Antibiotics', 150, 90, 'Yes'),
        ('MED004', 'Azithromycin 250mg', 'Antibiotics', 350, 200, 'Yes'),
        ('MED005', 'Metformin 500mg', 'Chronic', 120, 70, 'Yes'),
        ('MED006', 'Amlodipine 5mg', 'Chronic', 180, 100, 'Yes'),
        ('MED007', 'Omeprazole 20mg', 'Gastro', 200, 120, 'No'),
        ('MED008', 'Cetirizine 10mg', 'Allergy', 60, 35, 'No'),
        ('MED009', 'Vitamin C 1000mg', 'Vitamins', 250, 150, 'No'),
        ('MED010', 'Multivitamin Plus', 'Vitamins', 450, 280, 'No'),
        ('MED011', 'Cough Syrup 100ml', 'Cold & Flu', 180, 100, 'No'),
        ('MED012', 'Flu Capsules', 'Cold & Flu', 120, 70, 'No'),
        ('MED013', 'Malaria Test Kit', 'Diagnostics', 300, 180, 'No'),
        ('MED014', 'Artemether-Lum', 'Antimalarials', 550, 350, 'Yes'),
        ('MED015', 'ORS Sachets', 'Gastro', 30, 15, 'No'),
        ('MED016', 'Zinc Tablets', 'Supplements', 150, 90, 'No'),
        ('MED017', 'Insulin Syringe', 'Diabetes', 50, 25, 'No'),
        ('MED018', 'BP Monitor Battery', 'Equipment', 200, 120, 'No'),
        ('MED019', 'Antacid Tablets', 'Gastro', 100, 60, 'No'),
        ('MED020', 'Eye Drops 10ml', 'Ophthalmic', 280, 170, 'No'),
    ]
    
    # Date range: 6 months
    end_date = datetime(2024, 12, 31)
    start_date = end_date - timedelta(days=180)
    
    data = []
    transaction_id = 10000
    
    for _ in range(num_rows):
        # Random date with seasonal weighting (more transactions in rainy seasons)
        date = start_date + timedelta(days=np.random.randint(0, 181))
        month = date.month
        
        # Seasonal multiplier (rainy season = Oct-Dec, Apr-May = more flu meds)
        seasonal_mult = 1.3 if month in [10, 11, 12, 4, 5] else 1.0
        
        # Select outlet (Nairobi busier)
        outlet_weights = [0.45, 0.30, 0.25]
        outlet_id = np.random.choice(list(outlets.keys()), p=outlet_weights)
        outlet_name = outlets[outlet_id]
        
        # Select cashier from outlet
        cashier_id, cashier_name = cashiers[outlet_id][np.random.randint(0, 3)]
        
        # Select medicine (seasonal bias for cold/flu meds)
        med_idx = np.random.randint(0, len(medicines))
        if month in [10, 11, 12, 4, 5] and np.random.random() < 0.3:
            # Boost cold/flu and antimalarials in rainy season
            med_idx = np.random.choice([10, 11, 13, 14])
        
        item = medicines[med_idx]
        item_code, item_name, category, unit_price, cost_price, prescription = item
        
        # Quantity (mostly 1-3, occasionally bulk)
        quantity = np.random.choice([1, 1, 1, 2, 2, 3, 5, 10], p=[0.35, 0.2, 0.15, 0.1, 0.08, 0.07, 0.03, 0.02])
        
        # Payment type (75% M-Pesa in Kenya)
        payment_type = np.random.choice(['M-Pesa', 'Cash', 'Card'], p=[0.75, 0.20, 0.05])
        
        # Discount (occasional, more on slow-moving items)
        discount = 0
        if np.random.random() < 0.08:
            discount = np.random.choice([5, 10, 15, 20])
        
        # Calculate amounts
        total_price = unit_price * quantity * (1 - discount/100)
        total_cost = cost_price * quantity
        profit = total_price - total_cost
        
        # Simulate stock levels
        stock_before = np.random.randint(20, 200)
        stock_after = max(0, stock_before - quantity)
        
        # Expiry date (some items expiring soon for risk alerts)
        days_to_expiry = np.random.choice(
            [15, 30, 45, 60, 90, 180, 365, 730],
            p=[0.02, 0.05, 0.05, 0.08, 0.15, 0.25, 0.25, 0.15]
        )
        expiry_date = date + timedelta(days=int(days_to_expiry))
        
        # Void transactions (normal ~2%, fraud cashier ~8%)
        void_rate = 0.08 if cashier_id in ['C003', 'C006'] else 0.02
        voided = 'Yes' if np.random.random() < void_rate else 'No'
        
        # Fraud anomalies: occasional negative profit (suspicious discounts)
        if cashier_id in ['C003', 'C006'] and np.random.random() < 0.05:
            discount = 50  # Suspicious high discount
            total_price = unit_price * quantity * 0.5
            profit = total_price - total_cost
        
        # Add noise: some missing/null values
        if np.random.random() < 0.02:
            discount = np.nan
        
        transaction_id += 1
        
        data.append({
            'Date': date,
            'OutletID': outlet_id,
            'OutletName': outlet_name,
            'CashierID': cashier_id,
            'CashierName': cashier_name,
            'TransactionID': f'TXN{transaction_id}',
            'PaymentType': payment_type,
            'AmountKES': total_price,
            'ItemCode': item_code,
            'ItemName': item_name,
            'Category': category,
            'Quantity': quantity,
            'UnitPriceKES': unit_price,
            'TotalPriceKES': total_price,
            'CostPriceKES': cost_price * quantity,
            'ProfitKES': profit,
            'PrescriptionRequired': prescription,
            'ExpiryDate': expiry_date,
            'StockLevelBefore': stock_before,
            'StockLevelAfter': stock_after,
            'Voided': voided,
            'DiscountPercent': discount
        })
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df['ExpiryDate'] = pd.to_datetime(df['ExpiryDate'])
    
    return df.sort_values('Date').reset_index(drop=True)


# ============================================================================
# SECTION 2: CORE DATA PROCESSING & KPI LOGIC
# ============================================================================

class PharmacyKPIs:
    """Calculate key metrics and KPIs for pharmacy analytics."""
    
    def __init__(self, df: pd.DataFrame, reference_date: datetime = None):
        self.df = df[df['Voided'] == 'No'].copy()  # Exclude voided transactions
        self.df_all = df.copy()  # Include voided for fraud analysis
        self.reference_date = reference_date or df['Date'].max()
    
    def total_sales(self) -> float:
        """Total sales in KES (excluding voided)."""
        return self.df['TotalPriceKES'].sum()
    
    def mpesa_percentage(self) -> float:
        """Percentage of sales via M-Pesa."""
        mpesa_sales = self.df[self.df['PaymentType'] == 'M-Pesa']['TotalPriceKES'].sum()
        return (mpesa_sales / self.total_sales() * 100) if self.total_sales() > 0 else 0
    
    def daily_sales_vs_target(self, daily_target: float = 50000) -> pd.DataFrame:
        """Daily sales compared to target."""
        daily = self.df.groupby(self.df['Date'].dt.date)['TotalPriceKES'].sum().reset_index()
        daily.columns = ['Date', 'Sales']
        daily['Target'] = daily_target
        daily['Achievement'] = (daily['Sales'] / daily['Target'] * 100).round(1)
        return daily
    
    def shrinkage_rate(self) -> Tuple[float, pd.DataFrame]:
        """
        Shrinkage = (Expected Stock - Actual Stock) / Expected Stock
        Simulated as discrepancy in stock movements.
        """
        stock_data = self.df.groupby('ItemCode').agg({
            'Quantity': 'sum',
            'StockLevelBefore': 'first',
            'StockLevelAfter': 'last',
            'ItemName': 'first'
        }).reset_index()
        
        stock_data['ExpectedAfter'] = stock_data['StockLevelBefore'] - stock_data['Quantity']
        stock_data['Shrinkage'] = stock_data['ExpectedAfter'] - stock_data['StockLevelAfter']
        
        # Add some simulated shrinkage
        np.random.seed(42)
        stock_data['Shrinkage'] = stock_data['Shrinkage'] + np.random.randint(-2, 5, len(stock_data))
        stock_data['ShrinkageRate'] = (stock_data['Shrinkage'] / stock_data['StockLevelBefore'] * 100).clip(-5, 10)
        
        overall_rate = stock_data['ShrinkageRate'].mean()
        return overall_rate, stock_data
    
    def expiry_risk_count(self) -> Dict[str, int]:
        """Count items expiring within 30/60/90 days."""
        ref = self.reference_date
        return {
            '30_days': len(self.df[(self.df['ExpiryDate'] - ref).dt.days <= 30]),
            '60_days': len(self.df[(self.df['ExpiryDate'] - ref).dt.days <= 60]),
            '90_days': len(self.df[(self.df['ExpiryDate'] - ref).dt.days <= 90])
        }
    
    def profit_margin(self) -> float:
        """Overall profit margin percentage."""
        total_revenue = self.df['TotalPriceKES'].sum()
        total_profit = self.df['ProfitKES'].sum()
        return (total_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    def reconciliation_variance(self) -> pd.DataFrame:
        """
        Simulate M-Pesa vs Cash reconciliation with small mismatches.
        In real system, this would compare POS totals to bank/M-Pesa statements.
        """
        daily = self.df.groupby([self.df['Date'].dt.date, 'PaymentType'])['TotalPriceKES'].sum().unstack(fill_value=0)
        daily = daily.reset_index()
        daily.columns.name = None
        
        # Simulate reconciliation variances (small random mismatches)
        np.random.seed(42)
        if 'M-Pesa' in daily.columns:
            daily['MPesa_Statement'] = daily['M-Pesa'] + np.random.randint(-500, 500, len(daily))
            daily['MPesa_Variance'] = daily['MPesa_Statement'] - daily['M-Pesa']
        if 'Cash' in daily.columns:
            daily['Cash_Count'] = daily['Cash'] + np.random.randint(-200, 200, len(daily))
            daily['Cash_Variance'] = daily['Cash_Count'] - daily['Cash']
        
        return daily
    
    def fraud_risk_score(self) -> pd.DataFrame:
        """
        Rule-based fraud risk scoring per cashier.
        Flags: high voids %, unusual discounts, negative margins.
        """
        cashier_stats = self.df_all.groupby(['CashierID', 'CashierName']).agg({
            'TransactionID': 'count',
            'Voided': lambda x: (x == 'Yes').sum(),
            'DiscountPercent': 'mean',
            'ProfitKES': lambda x: (x < 0).sum()
        }).reset_index()
        
        cashier_stats.columns = ['CashierID', 'CashierName', 'TotalTxn', 'VoidedTxn', 'AvgDiscount', 'NegProfitTxn']
        
        # Calculate risk indicators
        cashier_stats['VoidRate'] = (cashier_stats['VoidedTxn'] / cashier_stats['TotalTxn'] * 100).round(2)
        cashier_stats['NegProfitRate'] = (cashier_stats['NegProfitTxn'] / cashier_stats['TotalTxn'] * 100).round(2)
        
        # Risk score (0-100)
        cashier_stats['FraudRiskScore'] = (
            (cashier_stats['VoidRate'] > 5).astype(int) * 30 +
            (cashier_stats['AvgDiscount'] > 10).astype(int) * 25 +
            (cashier_stats['NegProfitRate'] > 3).astype(int) * 45
        )
        
        return cashier_stats
    
    def top_skus_by_profit(self, n: int = 10) -> pd.DataFrame:
        """Top N fast-moving SKUs by total profit."""
        return self.df.groupby(['ItemCode', 'ItemName', 'Category']).agg({
            'ProfitKES': 'sum',
            'Quantity': 'sum',
            'TotalPriceKES': 'sum'
        }).reset_index().nlargest(n, 'ProfitKES')
    
    def prescription_compliance(self) -> float:
        """
        Compliance rate: prescription-required items with proper documentation.
        Simulated as ~85-95% compliance.
        """
        rx_items = self.df[self.df['PrescriptionRequired'] == 'Yes']
        if len(rx_items) == 0:
            return 100.0
        # Simulate compliance (in reality, would check prescription records)
        np.random.seed(42)
        compliant = int(len(rx_items) * np.random.uniform(0.85, 0.95))
        return (compliant / len(rx_items) * 100)
    
    def cashier_scorecard(self) -> pd.DataFrame:
        """Cashier performance metrics: transactions/hour, error rate."""
        cashier_stats = self.df.groupby(['CashierID', 'CashierName', 'OutletName']).agg({
            'TransactionID': 'count',
            'TotalPriceKES': 'sum',
            'ProfitKES': 'sum',
            'Date': ['min', 'max']
        }).reset_index()
        
        cashier_stats.columns = ['CashierID', 'CashierName', 'Outlet', 'Transactions', 
                                  'TotalSales', 'TotalProfit', 'FirstDate', 'LastDate']
        
        # Estimate working hours (8 hours/day, 6 days/week)
        cashier_stats['DaysWorked'] = (cashier_stats['LastDate'] - cashier_stats['FirstDate']).dt.days + 1
        cashier_stats['EstimatedHours'] = cashier_stats['DaysWorked'] * 6  # Simplified
        cashier_stats['TxnPerHour'] = (cashier_stats['Transactions'] / cashier_stats['EstimatedHours']).round(1)
        cashier_stats['AvgSaleValue'] = (cashier_stats['TotalSales'] / cashier_stats['Transactions']).round(0)
        
        # Get void rate from fraud analysis
        fraud_df = self.fraud_risk_score()
        cashier_stats = cashier_stats.merge(
            fraud_df[['CashierID', 'VoidRate', 'FraudRiskScore']], 
            on='CashierID', 
            how='left'
        )
        
        return cashier_stats


# ============================================================================
# SECTION 4: UNIQUE ENHANCED FEATURES
# ============================================================================

def demand_forecast(df: pd.DataFrame, item_code: str, days: int = 7) -> pd.DataFrame:
    """Simple moving average demand forecast for next N days."""
    item_df = df[df['ItemCode'] == item_code].copy()
    daily_qty = item_df.groupby(item_df['Date'].dt.date)['Quantity'].sum().reset_index()
    daily_qty.columns = ['Date', 'Quantity']
    
    # 7-day moving average
    daily_qty['MA7'] = daily_qty['Quantity'].rolling(window=7, min_periods=1).mean()
    
    # Forecast next N days
    last_date = pd.to_datetime(daily_qty['Date'].max())
    last_ma = daily_qty['MA7'].iloc[-1] if len(daily_qty) > 0 else 5
    
    forecast_dates = [last_date + timedelta(days=i+1) for i in range(days)]
    forecast_df = pd.DataFrame({
        'Date': forecast_dates,
        'Quantity': [0] * days,
        'MA7': [last_ma * (1 + np.random.uniform(-0.1, 0.1)) for _ in range(days)],
        'Type': ['Forecast'] * days
    })
    
    daily_qty['Type'] = 'Actual'
    return pd.concat([daily_qty.tail(14), forecast_df], ignore_index=True)


def get_expiry_heatmap_data(df: pd.DataFrame, reference_date: datetime) -> pd.DataFrame:
    """Generate expiry risk data with suggested actions."""
    expiry_data = df.groupby(['ItemCode', 'ItemName', 'Category']).agg({
        'ExpiryDate': 'min',
        'Quantity': 'sum',
        'UnitPriceKES': 'first',
        'StockLevelAfter': 'last'
    }).reset_index()
    
    expiry_data['DaysToExpiry'] = (expiry_data['ExpiryDate'] - reference_date).dt.days
    expiry_data['StockValue'] = expiry_data['StockLevelAfter'] * expiry_data['UnitPriceKES']
    
    # Suggested actions
    def suggest_action(days):
        if days <= 30:
            return '🔴 URGENT: 50% discount or donate'
        elif days <= 60:
            return '🟠 Promote: 25% discount'
        elif days <= 90:
            return '🟡 Monitor: Bundle deals'
        return '🟢 OK'
    
    expiry_data['Action'] = expiry_data['DaysToExpiry'].apply(suggest_action)
    expiry_data['RiskLevel'] = pd.cut(
        expiry_data['DaysToExpiry'],
        bins=[-np.inf, 30, 60, 90, np.inf],
        labels=['Critical', 'High', 'Medium', 'Low']
    )
    
    return expiry_data.sort_values('DaysToExpiry')


def get_outlet_benchmarking(df: pd.DataFrame) -> pd.DataFrame:
    """Multi-outlet performance comparison."""
    outlet_stats = df[df['Voided'] == 'No'].groupby(['OutletID', 'OutletName']).agg({
        'TotalPriceKES': 'sum',
        'ProfitKES': 'sum',
        'TransactionID': 'count',
        'Quantity': 'sum'
    }).reset_index()
    
    outlet_stats.columns = ['OutletID', 'OutletName', 'TotalSales', 'TotalProfit', 'Transactions', 'UnitsSold']
    outlet_stats['AvgBasketSize'] = (outlet_stats['TotalSales'] / outlet_stats['Transactions']).round(0)
    outlet_stats['ProfitMargin'] = (outlet_stats['TotalProfit'] / outlet_stats['TotalSales'] * 100).round(1)
    
    # Ranking
    outlet_stats['SalesRank'] = outlet_stats['TotalSales'].rank(ascending=False).astype(int)
    outlet_stats['ProfitRank'] = outlet_stats['TotalProfit'].rank(ascending=False).astype(int)
    
    return outlet_stats.sort_values('TotalSales', ascending=False)


def get_profit_optimization_suggestions(df: pd.DataFrame) -> pd.DataFrame:
    """Flag low-margin items and suggest pricing adjustments."""
    item_margins = df[df['Voided'] == 'No'].groupby(['ItemCode', 'ItemName', 'Category']).agg({
        'TotalPriceKES': 'sum',
        'CostPriceKES': 'sum',
        'ProfitKES': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    item_margins['Margin'] = (item_margins['ProfitKES'] / item_margins['TotalPriceKES'] * 100).round(1)
    item_margins['AvgUnitProfit'] = (item_margins['ProfitKES'] / item_margins['Quantity']).round(1)
    
    # Flag low margin items
    def suggest_optimization(row):
        if row['Margin'] < 20:
            return f"⚠️ Low margin ({row['Margin']}%) - Consider 10% price increase"
        elif row['Margin'] > 50:
            return f"✅ High margin - Maintain pricing"
        return "📊 Normal margin"
    
    item_margins['Suggestion'] = item_margins.apply(suggest_optimization, axis=1)
    
    return item_margins.sort_values('Margin')


def get_shrinkage_drilldown(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Root-cause analysis of shrinkage by cashier, outlet, time."""
    df_valid = df[df['Voided'] == 'No'].copy()
    
    # Simulate shrinkage amounts
    np.random.seed(42)
    df_valid['SimulatedShrinkage'] = np.random.choice([0, 0, 0, 1, 2, 5], len(df_valid))
    
    by_cashier = df_valid.groupby(['CashierID', 'CashierName']).agg({
        'SimulatedShrinkage': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    by_cashier['ShrinkageRate'] = (by_cashier['SimulatedShrinkage'] / by_cashier['Quantity'] * 100).round(2)
    
    by_outlet = df_valid.groupby(['OutletID', 'OutletName']).agg({
        'SimulatedShrinkage': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    by_outlet['ShrinkageRate'] = (by_outlet['SimulatedShrinkage'] / by_outlet['Quantity'] * 100).round(2)
    
    df_valid['Hour'] = df_valid['Date'].dt.hour
    by_time = df_valid.groupby('Hour').agg({
        'SimulatedShrinkage': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    by_time['ShrinkageRate'] = (by_time['SimulatedShrinkage'] / by_time['Quantity'] * 100).round(2)
    
    return {
        'by_cashier': by_cashier.sort_values('ShrinkageRate', ascending=False),
        'by_outlet': by_outlet.sort_values('ShrinkageRate', ascending=False),
        'by_time': by_time
    }


def get_refill_reminders(df: pd.DataFrame) -> pd.DataFrame:
    """Basic patient refill reminder logic for chronic medications."""
    chronic_meds = df[
        (df['Category'] == 'Chronic') & 
        (df['PrescriptionRequired'] == 'Yes') &
        (df['Voided'] == 'No')
    ].copy()
    
    if len(chronic_meds) == 0:
        return pd.DataFrame()
    
    # Group by item and estimate refill due date (30-day supply assumption)
    refills = chronic_meds.groupby(['ItemCode', 'ItemName']).agg({
        'Date': 'max',
        'Quantity': 'sum',
        'TransactionID': 'count'
    }).reset_index()
    
    refills.columns = ['ItemCode', 'ItemName', 'LastPurchase', 'TotalQty', 'Purchases']
    refills['EstimatedRefillDue'] = refills['LastPurchase'] + timedelta(days=30)
    refills['Status'] = refills['EstimatedRefillDue'].apply(
        lambda x: '📱 Send reminder' if x <= datetime.now() + timedelta(days=7) else '✅ OK'
    )
    
    return refills


# ============================================================================
# SECTION 3: STREAMLIT APP STRUCTURE & CODE
# ============================================================================

def main():
    # Page config - mobile first
    st.set_page_config(
        page_title="Kenya Pharmacy Dashboard",
        page_icon="💊",
        layout="wide",
        initial_sidebar_state="collapsed"  # Better for mobile
    )
    
    # Custom CSS for mobile optimization and Kenyan theme
    st.markdown("""
    <style>
    /* Mobile-first responsive design */
    .main .block-container {
        padding: 1rem;
        max-width: 100%;
    }
    
    /* Kenyan flag colors theme */
    .stMetric {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #006600;
    }
    
    /* Compact metrics for mobile */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
    }
    
    /* Alert styling */
    .stAlert {
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
    }
    
    /* Reduce chart padding on mobile */
    .js-plotly-plot {
        margin: 0 !important;
    }
    
    /* Header styling */
    h1 {
        color: #006600;
        font-size: 1.8rem !important;
    }
    
    h2, h3 {
        color: #333;
    }
    
    /* Sidebar compact */
    .css-1d391kg {
        padding: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("💊 Kenya Pharmacy Dashboard")
    st.caption("Executive Analytics for 3-Outlet Chemist Chain • M-Pesa Focused")
    
    # Load data
    df = generate_pharmacy_data(1500)
    
    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Filters")
        
        # Date range
        min_date = df['Date'].min().date()
        max_date = df['Date'].max().date()
        date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Outlet filter
        outlets = st.multiselect(
            "Outlets",
            options=df['OutletName'].unique(),
            default=df['OutletName'].unique()
        )
        
        # Category filter
        categories = st.multiselect(
            "Categories",
            options=df['Category'].unique(),
            default=df['Category'].unique()
        )
        
        # Cashier filter
        cashiers = st.multiselect(
            "Cashiers",
            options=df['CashierName'].unique(),
            default=df['CashierName'].unique()
        )
        
        st.divider()
        st.caption("📱 Optimized for mobile viewing")
        st.caption("🇰🇪 Data simulated for Kenyan market")
    
    # Apply filters
    if len(date_range) == 2:
        mask = (
            (df['Date'].dt.date >= date_range[0]) &
            (df['Date'].dt.date <= date_range[1]) &
            (df['OutletName'].isin(outlets)) &
            (df['Category'].isin(categories)) &
            (df['CashierName'].isin(cashiers))
        )
        filtered_df = df[mask].copy()
    else:
        filtered_df = df.copy()
    
    # Initialize KPIs
    kpis = PharmacyKPIs(filtered_df)
    reference_date = filtered_df['Date'].max()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "📈 Sales Trends", 
        "📦 Inventory & Expiry",
        "🚨 Fraud & Reconciliation",
        "🏪 Outlet Comparison"
    ])
    
    # ========== TAB 1: OVERVIEW ==========
    with tab1:
        # Alerts section
        fraud_df = kpis.fraud_risk_score()
        high_risk_cashiers = fraud_df[fraud_df['FraudRiskScore'] >= 50]
        expiry_risk = kpis.expiry_risk_count()
        
        if len(high_risk_cashiers) > 0:
            st.error(f"⚠️ FRAUD ALERT: {len(high_risk_cashiers)} cashier(s) with high risk score. Check Fraud tab.")
        
        if expiry_risk['30_days'] > 10:
            st.warning(f"📅 EXPIRY ALERT: {expiry_risk['30_days']} items expiring within 30 days. Check Inventory tab.")
        
        # KPI Metrics Row 1
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Sales",
                f"KES {kpis.total_sales():,.0f}",
                delta=f"{np.random.uniform(5, 15):.1f}% vs last period"
            )
        
        with col2:
            st.metric(
                "M-Pesa %",
                f"{kpis.mpesa_percentage():.1f}%",
                delta="Target: 75%"
            )
        
        with col3:
            st.metric(
                "Profit Margin",
                f"{kpis.profit_margin():.1f}%",
                delta="Industry avg: 35%"
            )
        
        with col4:
            st.metric(
                "Transactions",
                f"{len(filtered_df[filtered_df['Voided']=='No']):,}",
                delta=f"Void rate: {(filtered_df['Voided']=='Yes').mean()*100:.1f}%"
            )
        
        # KPI Metrics Row 2
        col5, col6, col7, col8 = st.columns(4)
        
        shrinkage_rate, _ = kpis.shrinkage_rate()
        
        with col5:
            st.metric(
                "Shrinkage Rate",
                f"{shrinkage_rate:.2f}%",
                delta="Target: <2%",
                delta_color="inverse"
            )
        
        with col6:
            st.metric(
                "Expiry Risk (30d)",
                f"{expiry_risk['30_days']} items",
                delta="Needs action",
                delta_color="inverse" if expiry_risk['30_days'] > 5 else "normal"
            )
        
        with col7:
            st.metric(
                "Rx Compliance",
                f"{kpis.prescription_compliance():.1f}%",
                delta="Target: 95%"
            )
        
        with col8:
            avg_basket = filtered_df[filtered_df['Voided']=='No']['TotalPriceKES'].mean()
            st.metric(
                "Avg Basket",
                f"KES {avg_basket:.0f}",
                delta="Per transaction"
            )
        
        st.divider()
        
        # Quick charts
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("💳 Payment Mix")
            payment_mix = filtered_df[filtered_df['Voided']=='No'].groupby('PaymentType')['TotalPriceKES'].sum().reset_index()
            fig_payment = px.pie(
                payment_mix, 
                values='TotalPriceKES', 
                names='PaymentType',
                color_discrete_sequence=['#006600', '#BB0000', '#FFD700'],
                hole=0.4
            )
            fig_payment.update_layout(
                margin=dict(l=20, r=20, t=30, b=20),
                height=250,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            st.plotly_chart(fig_payment, use_container_width=True)
        
        with col_right:
            st.subheader("📦 Top Categories")
            cat_sales = filtered_df[filtered_df['Voided']=='No'].groupby('Category')['TotalPriceKES'].sum().nlargest(5).reset_index()
            fig_cat = px.bar(
                cat_sales,
                x='TotalPriceKES',
                y='Category',
                orientation='h',
                color_discrete_sequence=['#006600']
            )
            fig_cat.update_layout(
                margin=dict(l=20, r=20, t=30, b=20),
                height=250,
                showlegend=False,
                xaxis_title="Sales (KES)",
                yaxis_title=""
            )
            st.plotly_chart(fig_cat, use_container_width=True)
    
    # ========== TAB 2: SALES TRENDS ==========
    with tab2:
        st.subheader("📈 Daily Sales Performance")
        
        daily_sales = kpis.daily_sales_vs_target(50000)
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=daily_sales['Date'],
            y=daily_sales['Sales'],
            mode='lines+markers',
            name='Actual Sales',
            line=dict(color='#006600', width=2),
            marker=dict(size=4)
        ))
        fig_trend.add_trace(go.Scatter(
            x=daily_sales['Date'],
            y=daily_sales['Target'],
            mode='lines',
            name='Target (KES 50,000)',
            line=dict(color='#BB0000', dash='dash')
        ))
        fig_trend.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            height=300,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            xaxis_title="",
            yaxis_title="Sales (KES)"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Weekly summary
        st.subheader("📅 Weekly Summary")
        filtered_df['Week'] = filtered_df['Date'].dt.isocalendar().week
        weekly = filtered_df[filtered_df['Voided']=='No'].groupby('Week').agg({
            'TotalPriceKES': 'sum',
            'ProfitKES': 'sum',
            'TransactionID': 'count'
        }).reset_index()
        weekly.columns = ['Week', 'Sales', 'Profit', 'Transactions']
        
        fig_weekly = px.bar(
            weekly,
            x='Week',
            y=['Sales', 'Profit'],
            barmode='group',
            color_discrete_sequence=['#006600', '#FFD700']
        )
        fig_weekly.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            height=250,
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig_weekly, use_container_width=True)
        
        # Top products
        st.subheader("🏆 Top 10 Products by Profit")
        top_products = kpis.top_skus_by_profit(10)
        st.dataframe(
            top_products[['ItemName', 'Category', 'Quantity', 'TotalPriceKES', 'ProfitKES']].rename(columns={
                'ItemName': 'Product',
                'TotalPriceKES': 'Sales (KES)',
                'ProfitKES': 'Profit (KES)',
                'Quantity': 'Units Sold'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Demand Forecast
        st.subheader("🔮 7-Day Demand Forecast")
        top_item = top_products.iloc[0]['ItemCode']
        forecast_df = demand_forecast(filtered_df, top_item)
        
        fig_forecast = px.line(
            forecast_df,
            x='Date',
            y='MA7',
            color='Type',
            color_discrete_map={'Actual': '#006600', 'Forecast': '#BB0000'},
            markers=True
        )
        fig_forecast.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            height=250,
            title=f"Forecast: {top_products.iloc[0]['ItemName']}"
        )
        st.plotly_chart(fig_forecast, use_container_width=True)
    
    # ========== TAB 3: INVENTORY & EXPIRY ==========
    with tab3:
        st.subheader("📦 Inventory & Expiry Management")
        
        # Expiry heatmap data
        expiry_data = get_expiry_heatmap_data(filtered_df, reference_date)
        
        # Alerts for critical expiry
        critical_items = expiry_data[expiry_data['RiskLevel'] == 'Critical']
        if len(critical_items) > 0:
            st.error(f"🚨 {len(critical_items)} items expiring within 30 days - IMMEDIATE ACTION REQUIRED")
        
        # Expiry heatmap
        st.subheader("🗓️ Expiry Risk Heatmap")
        
        expiry_summary = expiry_data.groupby(['Category', 'RiskLevel']).size().reset_index(name='Count')
        expiry_pivot = expiry_summary.pivot(index='Category', columns='RiskLevel', values='Count').fillna(0)
        
        fig_heatmap = px.imshow(
            expiry_pivot,
            color_continuous_scale=['#90EE90', '#FFD700', '#FFA500', '#FF4500'],
            aspect='auto'
        )
        fig_heatmap.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            height=300
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Action items table
        st.subheader("📋 Expiry Action Items")
        action_items = expiry_data[expiry_data['DaysToExpiry'] <= 90][
            ['ItemName', 'Category', 'DaysToExpiry', 'StockValue', 'Action']
        ].sort_values('DaysToExpiry')
        
        st.dataframe(
            action_items.rename(columns={
                'ItemName': 'Product',
                'DaysToExpiry': 'Days to Expiry',
                'StockValue': 'Stock Value (KES)',
                'Action': 'Recommended Action'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Profit optimization suggestions
        st.subheader("💰 Profit Optimization Suggestions")
        profit_suggestions = get_profit_optimization_suggestions(filtered_df)
        low_margin = profit_suggestions[profit_suggestions['Margin'] < 30]
        
        st.dataframe(
            low_margin[['ItemName', 'Category', 'Margin', 'Quantity', 'Suggestion']].head(10).rename(columns={
                'ItemName': 'Product',
                'Margin': 'Margin %',
                'Quantity': 'Units Sold',
                'Suggestion': 'Recommendation'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Refill reminders
        st.subheader("📱 Patient Refill Reminders")
        refill_data = get_refill_reminders(filtered_df)
        if len(refill_data) > 0:
            st.info("💡 Chronic medication patients may need refill reminders:")
            st.dataframe(
                refill_data[['ItemName', 'LastPurchase', 'EstimatedRefillDue', 'Status']].rename(columns={
                    'ItemName': 'Medication',
                    'LastPurchase': 'Last Purchase',
                    'EstimatedRefillDue': 'Refill Due',
                    'Status': 'Action'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No chronic medication refill reminders pending.")
    
    # ========== TAB 4: FRAUD & RECONCILIATION ==========
    with tab4:
        st.subheader("🚨 Fraud Detection & Reconciliation")
        
        # Fraud risk scores
        fraud_scores = kpis.fraud_risk_score()
        
        # Alert for high-risk cashiers
        high_risk = fraud_scores[fraud_scores['FraudRiskScore'] >= 50]
        for _, row in high_risk.iterrows():
            st.error(f"⚠️ HIGH FRAUD RISK: {row['CashierName']} (Score: {row['FraudRiskScore']}/100) - "
                    f"Void Rate: {row['VoidRate']:.1f}%, Neg Profit Txns: {row['NegProfitTxn']}")
            # Simulated SMS alert
            st.info(f"📱 SMS Alert Sent to Manager: 'Investigate cashier {row['CashierName']} - "
                   f"Fraud score {row['FraudRiskScore']}'")
        
        # Fraud score scatter plot
        st.subheader("📊 Cashier Fraud Risk Analysis")
        
        fig_fraud = px.scatter(
            fraud_scores,
            x='VoidRate',
            y='AvgDiscount',
            size='TotalTxn',
            color='FraudRiskScore',
            hover_name='CashierName',
            color_continuous_scale=['green', 'yellow', 'red'],
            size_max=30
        )
        fig_fraud.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="Discount Threshold")
        fig_fraud.add_vline(x=5, line_dash="dash", line_color="red", annotation_text="Void Threshold")
        fig_fraud.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            height=350,
            xaxis_title="Void Rate (%)",
            yaxis_title="Avg Discount (%)"
        )
        st.plotly_chart(fig_fraud, use_container_width=True)
        
        # Cashier scorecard
        st.subheader("👥 Cashier Performance Scorecard")
        cashier_scores = kpis.cashier_scorecard()
        
        st.dataframe(
            cashier_scores[['CashierName', 'Outlet', 'Transactions', 'TotalSales', 
                           'TxnPerHour', 'AvgSaleValue', 'VoidRate', 'FraudRiskScore']].rename(columns={
                'CashierName': 'Cashier',
                'TotalSales': 'Total Sales (KES)',
                'TxnPerHour': 'Txn/Hour',
                'AvgSaleValue': 'Avg Sale (KES)',
                'VoidRate': 'Void %',
                'FraudRiskScore': 'Risk Score'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Reconciliation variance
        st.subheader("💵 Cash & M-Pesa Reconciliation")
        recon_df = kpis.reconciliation_variance()
        
        if 'MPesa_Variance' in recon_df.columns:
            total_mpesa_var = recon_df['MPesa_Variance'].sum()
            total_cash_var = recon_df.get('Cash_Variance', pd.Series([0])).sum()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "M-Pesa Variance (Period)",
                    f"KES {total_mpesa_var:,.0f}",
                    delta="vs M-Pesa Statement",
                    delta_color="inverse" if abs(total_mpesa_var) > 5000 else "normal"
                )
            with col2:
                st.metric(
                    "Cash Variance (Period)",
                    f"KES {total_cash_var:,.0f}",
                    delta="vs Physical Count",
                    delta_color="inverse" if abs(total_cash_var) > 2000 else "normal"
                )
            
            # Variance trend
            fig_recon = go.Figure()
            fig_recon.add_trace(go.Bar(
                x=recon_df['Date'],
                y=recon_df.get('MPesa_Variance', 0),
                name='M-Pesa Variance',
                marker_color='#006600'
            ))
            if 'Cash_Variance' in recon_df.columns:
                fig_recon.add_trace(go.Bar(
                    x=recon_df['Date'],
                    y=recon_df['Cash_Variance'],
                    name='Cash Variance',
                    marker_color='#BB0000'
                ))
            fig_recon.update_layout(
                margin=dict(l=20, r=20, t=30, b=20),
                height=250,
                barmode='group',
                legend=dict(orientation="h", yanchor="bottom", y=1.02)
            )
            st.plotly_chart(fig_recon, use_container_width=True)
        
        # Shrinkage drilldown
        st.subheader("📉 Shrinkage Root-Cause Analysis")
        shrinkage_data = get_shrinkage_drilldown(filtered_df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.caption("By Cashier")
            st.dataframe(
                shrinkage_data['by_cashier'][['CashierName', 'SimulatedShrinkage', 'ShrinkageRate']].rename(columns={
                    'CashierName': 'Cashier',
                    'SimulatedShrinkage': 'Units Lost',
                    'ShrinkageRate': 'Rate %'
                }),
                use_container_width=True,
                hide_index=True
            )
        with col2:
            st.caption("By Outlet")
            st.dataframe(
                shrinkage_data['by_outlet'][['OutletName', 'SimulatedShrinkage', 'ShrinkageRate']].rename(columns={
                    'OutletName': 'Outlet',
                    'SimulatedShrinkage': 'Units Lost',
                    'ShrinkageRate': 'Rate %'
                }),
                use_container_width=True,
                hide_index=True
            )
    
    # ========== TAB 5: OUTLET COMPARISON ==========
    with tab5:
        st.subheader("🏪 Multi-Outlet Benchmarking")
        
        outlet_data = get_outlet_benchmarking(filtered_df)
        
        # Ranking cards
        st.subheader("🏆 Outlet Rankings")
        cols = st.columns(3)
        for idx, row in outlet_data.iterrows():
            with cols[idx]:
                rank_emoji = "🥇" if row['SalesRank'] == 1 else "🥈" if row['SalesRank'] == 2 else "🥉"
                st.metric(
                    f"{rank_emoji} {row['OutletName']}",
                    f"KES {row['TotalSales']:,.0f}",
                    delta=f"Margin: {row['ProfitMargin']:.1f}%"
                )
                st.caption(f"📊 {row['Transactions']:,} txns | 🛒 Avg: KES {row['AvgBasketSize']:,.0f}")
        
        # Comparison charts
        st.subheader("📊 Performance Comparison")
        
        fig_outlet = px.bar(
            outlet_data,
            x='OutletName',
            y=['TotalSales', 'TotalProfit'],
            barmode='group',
            color_discrete_sequence=['#006600', '#FFD700']
        )
        fig_outlet.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            height=300,
            xaxis_title="",
            yaxis_title="Amount (KES)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig_outlet, use_container_width=True)
        
        # Outlet trends over time
        st.subheader("📈 Outlet Sales Trends")
        outlet_daily = filtered_df[filtered_df['Voided']=='No'].groupby(
            [filtered_df['Date'].dt.date, 'OutletName']
        )['TotalPriceKES'].sum().reset_index()
        outlet_daily.columns = ['Date', 'Outlet', 'Sales']
        
        fig_outlet_trend = px.line(
            outlet_daily,
            x='Date',
            y='Sales',
            color='Outlet',
            color_discrete_sequence=['#006600', '#BB0000', '#FFD700']
        )
        fig_outlet_trend.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            height=300,
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig_outlet_trend, use_container_width=True)
        
        # Category breakdown by outlet
        st.subheader("📦 Category Mix by Outlet")
        cat_outlet = filtered_df[filtered_df['Voided']=='No'].groupby(
            ['OutletName', 'Category']
        )['TotalPriceKES'].sum().reset_index()
        
        fig_cat_outlet = px.bar(
            cat_outlet,
            x='OutletName',
            y='TotalPriceKES',
            color='Category',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_cat_outlet.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            height=350,
            xaxis_title="",
            yaxis_title="Sales (KES)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig_cat_outlet, use_container_width=True)
    
    # Footer
    st.divider()
    st.caption("💊 Kenya Pharmacy Dashboard v1.0 | Built with Streamlit | Data is simulated for demo purposes")
    st.caption("📱 Optimized for mobile viewing on low-data connections | KES currency throughout")


if __name__ == "__main__":
    main()
