import pandas as pd          
import numpy as np          


# Parameters    
notional= 100000000     
fixed_rate = 0.035    # IRS fixed leg (pay) rate
initial_float_rate = 0.02   # 2% Starting SOFR
loan_rate= 0.03 # Fixed income on loan 
term_years= 5 
payments_per_year= 4   # Quarterly payments 

# Generate rate forecast (floating rate increases 0.25% per year)

periods = term_years * payments_per_year 
float_rate_path= initial_float_rate + np.linspace(0, 0.01, periods)  # rising from 2% to 3%

# Time Periods 

dates = pd.date_range(start= "2024-01-01", periods=periods, freq= "Q")
# print(dates)

# Build CASH FLOW TABLE 

df= pd.DataFrame({
    "Date": dates,
    "Float_Rate": float_rate_path, 
})

df["Fixed_IRS_Payment"] =notional * fixed_rate/payments_per_year

df["Float_IRS_Receipt"] = notional * df["Float_Rate"] / payments_per_year

df["IRS_Net_Cashflow"] = df["Float_IRS_Receipt"] -df["Fixed_IRS_Payment"]


# Loan income and interest expense

df["Loan_Income"] = notional * loan_rate / payments_per_year

df["PnL_Unhedged"] = df["Loan_Income"] - notional * df["Float_Rate"]/ payments_per_year

df["PnL_Hedged"] = df["PnL_Unhedged"] + df["IRS_Net_Cashflow"]

# Cumulative P&L

df["Cumulative_PnL_Unhedged"] = df["PnL_Unhedged"].cumsum()
df["Cumulative_PnL_Hedged"] =df["PnL_Hedged"].cumsum()

# Save to Excel 

file_path= "IRS_vs_Loan_PnL_Calculator.xlsx"
df.to_excel(file_path, index=False)

