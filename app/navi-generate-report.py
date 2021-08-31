import subprocess
import os
from dotenv import load_dotenv
import pandas as pd
import sqlite3

load_dotenv()

# Define T.io variables
TIO_ACCESS_KEY = os.getenv('TIO_ACCESS_KEY')
TIO_SECRET_KEY = os.getenv('TIO_SECRET_KEY')

# Configure Navi with keys
subprocess.call(["navi", "keys", "--a", TIO_ACCESS_KEY, "--s", TIO_SECRET_KEY])

# Pull asset and vuln data
subprocess.call(["navi", "update", "assets", "--days", "7"])
subprocess.call(["navi", "update", "vulns", "--days", "7"])

# Create dataframe from navi sqlite3 db
navi_db = sqlite3.connect("navi.db")
df_vulns = pd.read_sql_query("SELECT * FROM vulns", navi_db)

# Rename columns
df_vulns = df_vulns.rename({"asset_ip": "IP Address",
                            "asset_uuid": "UUID",
                            "asset_hostname": "Hostname",
                            "fist_found": "First Discovered",
                            "last_found": "Last Discovered",
                            "output": "Plugin Output",
                            "plugin_id": "Plugin ID",
                            "plugin_name": "Plugin Name",
                            "plugin_family": "Plugin Family",
                            "port": "Port",
                            "protocol": "Protocol",
                            "severity": "Severity",
                            "scan_completed": "Scan Completed Time",
                            "scan_started": "Scan Start Time",
                            "scan_uuid": "Scan UUID",
                            "schedule_id": "Scan Schedule ID",
                            "state": "Vulnerability State",
                            "cves": "CVEs",
                            "score": "CVSS Score",
                            "exploit": "Exploit Available"}, axis=1)

# Sort and trim columns
# Mdify as needed from the renamed columns above
df_vulns = df_vulns[['UUID',
                     'IP Address',
                     'Hostname',
                     'Plugin ID',
                     'Plugin Name',
                     'Severity',
                     'Plugin Output',
                     'Vulnerability State',
                     'CVEs',
                     'CVSS Score',
                     'Exploit Available'
                     ]]

# Filter on data
# Plugin 11219 - Filters to only include entries for this plugin
df_vulns['Plugin ID'] = df_vulns['Plugin ID'].astype('str')
df_vulns['Plugin ID'] = df_vulns['Plugin ID'].str.match("11219")

# Write data to excel file
df_vulns.to_excel('tenable_io_vulns.xlsx',
                  sheet_name='T.io Data', engine='xlsxwriter', index=False)

# Close sqlite3 db connection
navi_db.close()

# Stand up built-in http server to download data
subprocess.call(["navi", "http"])
