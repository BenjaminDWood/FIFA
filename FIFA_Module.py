import pandas as pd
from datetime import datetime
raw_data = pd.read_csv('FIFA_raw_data.csv')
df = raw_data.copy()
df = df.drop(['ID', 'LongName', 'photoUrl', 'playerUrl'], axis = 1)
df = df.rename(columns={'↓OVA':'OVA'})
df["Club"]=df["Club"].str.strip("\n\n\n\n")
df['Height'] = df['Height'].str.replace('cm', '')
def ft_to_cm(x):
    if "'" in x:
        parts = x.replace('"', '').split("'")
        feet = float(parts[0])
        inches = float(parts[1]) if parts[1] else 0
        cm = round((feet * 30.48) + (inches * 2.54), 0)
        return int(cm)
    else:
        return int(x)

df["Height"]=df["Height"].apply(ft_to_cm)
df["Height"].unique()
df['Weight'] = df['Weight'].str.replace('kg', '')
def lbs_to_kg(x):
    if "lbs" in x:
        lbs = x.replace("lbs", "")
        kg = round(int(lbs) / 2.2, 0)
        return int(kg)
    else:
        return int(x)

df['Weight'] = df['Weight'].apply(lbs_to_kg)
df.rename(columns={'Height':'Height(cm)','Weight':'Weight(kg)'},inplace =True)
def money(x):
    if "€" in x:
        x = x.replace("€", "")
    if "M" in x:
        x=x.replace("M", "")
        return int(float(x) * 1000000)
    elif "K" in x:
        x = x.replace("K", "")
        return int(float(x) * 1000)

    return int(x)

df['Value'] = df['Value'].apply(money)
df['Wage'] = df['Wage'].apply(money)
df['Release Clause'] = df['Release Clause'].apply(money)

df.rename(columns = {'Value':'Value (€)', "Wage":"Wage (€)"})

df['W/F'] = df['W/F'].str.replace("★", "")
df['SM'] = df['SM'].str.replace("★", "")
df['IR'] = df['IR'].str.replace("★", "")

df.rename(columns = {'W/F':'Weak Foot /5', "SM":"Skill Moves /5", "IR": "International Reputation /5"}, inplace = True)

def type(x):
    if "Free" in x:
        return "Free"
    if "Loan" in x:
        return "Loan"
    if "~" in x:
        return "Contract"
    else:
        return pd.na

def start_time_contract(x):
    if "~" in x:
        return  int(x[:4])
    if "Loan" in x:
        x=x.strip(" On Loan")
        x= datetime.strptime(x, "%b %d, %Y")
        return x.date()
    else:
        return pd.NA

def end_time_contract(type,contract,loan):
    if type == "Contract":
        return int(contract[-4:])
    if type == "Loan":
        loan = datetime.strptime(loan, "%b %d, %Y")
        return loan.date()

    else:
        return pd.NA

df["Type of contract"] = df["Contract"].apply(type)
df["Start year"] = df["Contract"].apply(start_time_contract)
df["End year"] = df.apply(lambda row: end_time_contract(row["Type of contract"],row["Contract"],row["Loan Date End"] ), axis=1)