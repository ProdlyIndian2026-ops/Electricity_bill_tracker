import streamlit as st
import time
import pandas as pd
import os
import json
import plotly.express as px
from datetime import datetime

# --- SETTINGS & FILES ---
HISTORY_FILE = "billing_history.csv"
ACTIVE_FILE = "active_devices.json"
DEVICES_LIBRARY_FILE = "devices_library.json"
CUSTOM_DEVICES_FILE = "custom_devices.json"

# --- PRE-INSTALLED DEVICE DATABASE ---
PRE_INSTALLED_DEVICES = {
    "AC": {
        "LG": {
            "Dual Inverter": 1200,
            "Dual Cool": 1400,
            "Ultra": 1600
        },
        "Daikin": {
            "FTKM Series": 1100,
            "ATKL Series": 1300,
            "S Series": 1500
        },
        "Voltas": {
            "Copper Series": 1300,
            "Adjustable": 1450,
            "Bold Series": 1550
        },
        "Blue Star": {
            "IC Series": 1250,
            "5 Star": 1400,
            "Deluxe": 1600
        },
        "Samsung": {
            "WindFree": 1200,
            "AR Series": 1350,
            "Triple Inverter": 1500
        },
        "Panasonic": {
            "Nanoe": 1150,
            "Eco Mode": 1250,
            "Smart": 1400
        },
        "Carrier": {
            "Estrella": 1300,
            "Midea": 1400,
            "Neo": 1500
        },
        "Hitachi": {
            "Kashikoi": 1200,
            "iClean": 1350,
            "Sensei": 1480
        },
        "Godrej": {
            "Nxw": 1250,
            "Edge": 1350,
            "GIC": 1450
        },
        "Whirlpool": {
            "Magicool": 1300,
            "3D Cool": 1400,
            "Intelli Sense": 1550
        }
    },
    "Refrigerator": {
        "Samsung": {
            "Digital Inverter": 200,
            "Convertible": 220,
            "Side by Side": 300
        },
        "LG": {
            "Smart Inverter": 180,
            "Door Cooling": 210,
            "Linear Cooling": 250
        },
        "Whirlpool": {
            "IntelliFresh": 190,
            "Protton": 210,
            "Neo Frost": 230
        },
        "Godrej": {
            "Platinum": 170,
            "Edge": 190,
            "Powercool": 220
        },
        "Haier": {
            "Convertible": 200,
            "Inverter": 220,
            "Hassle Free": 240
        },
        "Bosch": {
            "Series 2": 180,
            "Series 4": 210,
            "Series 6": 250
        }
    },
    "Washing Machine": {
        "Samsung": {
            "Eco Bubble": 400,
            "QuickDrive": 500,
            "AddWash": 450
        },
        "LG": {
            "Direct Drive": 380,
            "TwinWash": 550,
            "TurboWash": 420
        },
        "Whirlpool": {
            "6th Sense": 400,
            "ACE": 450,
            "Fabric Care": 480
        },
        "Bosch": {
            "VarioPerfect": 420,
            "EcoSilence": 460,
            "SpeedPerfect": 500
        },
        "IFB": {
            "Aqua Energie": 450,
            "Senator": 500,
            "Diva": 480
        }
    },
    "TV": {
        "Samsung": {
            "Crystal 4K": 100,
            "The Frame": 120,
            "Neo QLED": 150
        },
        "LG": {
            "OLED": 130,
            "NanoCell": 110,
            "UHD": 90
        },
        "Sony": {
            "Bravia XR": 140,
            "Bravia": 110,
            "Triluminos": 120
        },
        "Mi": {
            "Mi TV 4K": 80,
            "Mi QLED": 95,
            "Mi LED": 70
        },
        "OnePlus": {
            "Q Series": 100,
            "U Series": 85,
            "Y Series": 70
        },
        "TCL": {
            "QLED": 110,
            "Android": 90,
            "C Series": 100
        }
    },
    "Heater": {
        "Havells": {
            "Mariner": 2000,
            "Instanio": 2200,
            "Solace": 1800
        },
        "Bajaj": {
            "Flash": 2000,
            "Blow Hot": 1500,
            "Majesty": 2500
        },
        "Orient": {
            "Thermique": 2000,
            "Radiance": 1800,
            "DigiQ": 2200
        },
        "Usha": {
            "Heat Connect": 2000,
            "Maxxi": 1500,
            "Pro": 2500
        },
        "Maharaja": {
            "Whiteline": 2000,
            "Pro 2000": 2200,
            "Glory": 1800
        }
    },
    "Fan": {
        "Havells": {
            "Stealth": 50,
            "Glen": 55,
            "Esfera": 60
        },
        "Crompton": {
            "Greaves": 50,
            "Hill Breeze": 55,
            "High Speed": 65
        },
        "Usha": {
            "Aura": 45,
            "Prima": 50,
            "Stellar": 55
        },
        "Orient": {
            "Stand Fan": 55,
            "Ceiling Fan": 50,
            "Turbo": 60
        },
        "Bajaj": {
            "Classic": 50,
            "Neo": 55,
            "Marc": 45
        }
    },
    "Water Purifier": {
        "Kent": {
            "Grand": 35,
            "Ace": 40,
            "Elite": 45
        },
        "Aquaguard": {
            "Nova": 30,
            "Genius": 35,
            "Sure": 40
        },
        "Livpure": {
            "Glory": 35,
            "Smart": 40,
            "Active": 45
        },
        "Pureit": {
            "Classic": 30,
            "Advanced": 35,
            "Marvella": 40
        }
    },
    "Laptop": {
        "Dell": {
            "Inspiron": 45,
            "XPS": 65,
            "Latitude": 50
        },
        "HP": {
            "Pavilion": 50,
            "Envy": 60,
            "Spectre": 55
        },
        "Lenovo": {
            "ThinkPad": 45,
            "Legion": 80,
            "IdeaPad": 50
        },
        "Apple": {
            "MacBook Air": 30,
            "MacBook Pro": 60,
            "MacBook": 45
        },
        "Asus": {
            "ROG": 100,
            "TUF": 70,
            "ZenBook": 45
        }
    },
    "Desktop": {
        "Dell": {
            "OptiPlex": 150,
            "Precision": 250,
            "Inspiron": 120
        },
        "HP": {
            "EliteDesk": 150,
            "ProDesk": 130,
            "Pavilion": 160
        },
        "Lenovo": {
            "ThinkCentre": 140,
            "IdeaCentre": 120,
            "Legion": 300
        },
        "Custom": {
            "Gaming PC": 400,
            "Office PC": 150,
            "Workstation": 250
        }
    },
    "Microwave": {
        "Samsung": {
            "Grill": 800,
            "Convection": 1000,
            "Solo": 600
        },
        "LG": {
            "MC Series": 800,
            "MH Series": 1000,
            "MS Series": 1200
        },
        "Panasonic": {
            "Genius": 850,
            "Inverter": 950,
            "Compact": 750
        },
        "IFB": {
            "Copper Grill": 850,
            "Convection": 1050,
            "Solo": 650
        },
        "Bosch": {
            "Compact": 800,
            "Built-in": 1000,
            "Freestanding": 900
        }
    },
    "Geyser": {
        "Bajaj": {
            "Shakti": 2000,
            "Flora": 1500,
            "New Flora": 1800
        },
        "Havells": {
            "Instanio": 2000,
            "Solace": 2200,
            "Puro": 1800
        },
        "AO Smith": {
            "SECS": 2000,
            "SGS": 2500,
            "HSE": 3000
        },
        "Racold": {
            "Eterno": 2000,
            "Alero": 2500,
            "Optima": 2200
        },
        "V-Guard": {
            "Divino": 2000,
            "Anak": 1800,
            "Supremo": 2200
        }
    },
    "Iron": {
        "Philips": {
            "Steam": 1000,
            "EasyTouch": 1200,
            "GC Series": 1500
        },
        "Bajaj": {
            "MX Series": 1000,
            "DX Series": 1200,
            "Almond": 1500
        },
        "Havells": {
            "Pro": 1000,
            "Xpress": 1200,
            "Vibro": 1400
        },
        "Usha": {
            "Express": 1000,
            "Pro": 1200,
            "Pearl": 1500
        },
        "Panasonic": {
            "NI Series": 1000,
            "Compact": 1200,
            "Steam": 1500
        }
    }
}

# --- HELPER FUNCTIONS ---
def load_active_devices():
    if os.path.exists(ACTIVE_FILE):
        with open(ACTIVE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_active_devices(active_dict):
    with open(ACTIVE_FILE, "w") as f:
        json.dump(active_dict, f)

def load_devices_library():
    if os.path.exists(DEVICES_LIBRARY_FILE):
        with open(DEVICES_LIBRARY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_devices_library(library_dict):
    with open(DEVICES_LIBRARY_FILE, "w") as f:
        json.dump(library_dict, f)

def load_custom_devices():
    if os.path.exists(CUSTOM_DEVICES_FILE):
        with open(CUSTOM_DEVICES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_custom_devices(custom_dict):
    with open(CUSTOM_DEVICES_FILE, "w") as f:
        json.dump(custom_dict, f)

def save_to_history(name, units, cost, state_name, rate_used):
    new_data = pd.DataFrame([{
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Device": name,
        "Units_kWh": round(units, 4),
        "Cost_INR": round(cost, 2),
        "State": state_name,
        "Rate_Used": rate_used
    }])
    if not os.path.exists(HISTORY_FILE):
        new_data.to_csv(HISTORY_FILE, index=False)
    else:
        new_data.to_csv(HISTORY_FILE, mode='a', header=False, index=False)

def get_saving_tip(device_name, wattage, cost):
    """Generate energy saving tips"""
    device_lower = device_name.lower()
    if 'ac' in device_lower or 'air conditioner' in device_lower:
        return "💡 Set AC to 24°C - saves 6% per degree!"
    elif 'heater' in device_lower or 'geyser' in device_lower:
        return "💡 Limit to 10 minutes - saves 30% energy!"
    elif 'refrigerator' in device_lower or 'fridge' in device_lower:
        return "💡 Keep coils clean - saves 15% energy!"
    elif 'tv' in device_lower or 'television' in device_lower:
        return "💡 Lower brightness - saves 20% energy!"
    elif 'washing machine' in device_lower:
        return "💡 Use cold water - saves 90% energy!"
    elif wattage > 1000:
        return "💡 High power device! Use during off-peak hours"
    elif wattage > 500:
        return "💡 Consider timer or smart plug for this device"
    return "💡 Turn off when not in use! Every watt matters"

# --- PAGE CONFIG ---
st.set_page_config(page_title="India Energy Tracker", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'active_devices' not in st.session_state:
    st.session_state.active_devices = load_active_devices()
if 'devices_library' not in st.session_state:
    st.session_state.devices_library = load_devices_library()
if 'custom_devices' not in st.session_state:
    st.session_state.custom_devices = load_custom_devices()
if 'show_tips' not in st.session_state:
    st.session_state.show_tips = True

# --- SIDEBAR: CONFIGURATION ---
with st.sidebar:
    st.header("🌍 Tariff Configuration")
    
    state = st.selectbox("Select State/UT", ["Haryana", "Delhi", "Maharashtra", "Karnataka", "Other"], key="state_selector")
    
    default_rate = 5.50
    default_fixed = 115.0
    
    if state == "Delhi":
        default_rate = 3.00
        default_fixed = 40.0
    elif state == "Maharashtra":
        default_rate = 7.10
        default_fixed = 150.0
    elif state == "Karnataka":
        default_rate = 4.50
        default_fixed = 100.0
        
    rate = st.number_input("Rate per Unit (₹)", value=default_rate, min_value=0.0, step=0.5, key="rate_input")
    fixed_charge = st.number_input("Monthly Fixed Charge (₹)", value=default_fixed, min_value=0.0, step=10.0, key="fixed_charge_input")

    st.divider()
    
    # --- SMART DEVICE SEARCH & ADD ---
    st.header("🔍 Smart Device Search")
    st.caption("Search from 100+ pre-configured devices")
    
    # Search for device type
    device_types = list(PRE_INSTALLED_DEVICES.keys())
    search_type = st.selectbox("Select Device Type", device_types, key="search_device_type")
    
    if search_type:
        brands = list(PRE_INSTALLED_DEVICES[search_type].keys())
        selected_brand = st.selectbox("Select Brand", brands, key="selected_brand")
        
        if selected_brand:
            models = PRE_INSTALLED_DEVICES[search_type][selected_brand]
            selected_model = st.selectbox("Select Model", list(models.keys()), key="selected_model")
            
            if selected_model:
                wattage = models[selected_model]
                device_name = f"{selected_brand} {search_type} {selected_model}"
                
                st.info(f"⚡ Power: **{wattage}W**")
                
                col_add1, col_add2 = st.columns(2)
                with col_add1:
                    if st.button("📥 Add to Library", key="add_preinstalled_btn", use_container_width=True):
                        if device_name in st.session_state.devices_library:
                            st.warning(f"⚠️ {device_name} already in library!")
                        else:
                            st.session_state.devices_library[device_name] = {
                                "wattage": wattage,
                                "category": search_type,
                                "brand": selected_brand,
                                "model": selected_model,
                                "created": datetime.now().strftime("%Y-%m-%d")
                            }
                            save_devices_library(st.session_state.devices_library)
                            st.success(f"✅ {device_name} added to library!")
                            st.rerun()
    
    st.divider()
    
    # --- CUSTOM DEVICE ADDITION ---
    st.header("➕ Custom Device Entry")
    st.caption("For local/unbranded products or custom appliances")
    
    custom_name = st.text_input("Device Name", placeholder="e.g. Local AC, Philips Heater", key="custom_name")
    custom_category = st.selectbox("Category", ["Cooling", "Heating", "Entertainment", "Kitchen", "Lighting", "Other"], key="custom_category")
    custom_wattage = st.number_input("Wattage (W)", min_value=0.0, step=10.0, key="custom_wattage")
    custom_brand = st.text_input("Brand (Optional)", placeholder="Local / Unbranded / Unknown", key="custom_brand")
    
    col_cus1, col_cus2 = st.columns(2)
    with col_cus1:
        if st.button("💾 Add Custom Device", key="add_custom_btn", use_container_width=True):
            if custom_name and custom_wattage > 0:
                device_name = f"{custom_name} ({custom_brand if custom_brand else 'Local'})"
                if device_name in st.session_state.devices_library:
                    st.warning(f"⚠️ {device_name} already in library!")
                else:
                    st.session_state.devices_library[device_name] = {
                        "wattage": custom_wattage,
                        "category": custom_category,
                        "brand": custom_brand if custom_brand else "Local",
                        "custom": True,
                        "created": datetime.now().strftime("%Y-%m-%d")
                    }
                    # Save to custom devices file for persistence
                    st.session_state.custom_devices[device_name] = st.session_state.devices_library[device_name]
                    save_custom_devices(st.session_state.custom_devices)
                    save_devices_library(st.session_state.devices_library)
                    st.success(f"✅ Custom device '{custom_name}' added!")
                    st.rerun()
            else:
                st.error("Please enter device name and wattage")
    
    with col_cus2:
        if st.button("🔄 Quick Add from Recent", key="quick_add_btn", use_container_width=True):
            # Quick add common appliances
            quick_options = {
                "🏠 LED Bulb (9W)": 9,
                "🏠 Ceiling Fan (50W)": 50,
                "🏠 Fridge (200W)": 200,
                "🏠 Desktop (150W)": 150,
                "🏠 Laptop (50W)": 50,
                "🏠 TV (100W)": 100,
                "🏠 Water Pump (750W)": 750,
                "🏠 Iron (1000W)": 1000,
            }
            selected_quick = st.selectbox("Quick Add", list(quick_options.keys()), key="quick_select")
            if selected_quick:
                wattage = quick_options[selected_quick]
                name = selected_quick.split(") ")[1] + ")"
                if st.button(f"➕ Add {selected_quick}", key="quick_add_confirm"):
                    if name not in st.session_state.devices_library:
                        st.session_state.devices_library[name] = {
                            "wattage": wattage,
                            "category": "Lighting" if "Bulb" in name else "Kitchen",
                            "brand": "Quick Add",
                            "custom": True,
                            "created": datetime.now().strftime("%Y-%m-%d")
                        }
                        save_devices_library(st.session_state.devices_library)
                        st.success(f"✅ {name} added!")
                        st.rerun()
    
    st.divider()
    
    # --- DEVICE LIBRARY MANAGEMENT ---
    st.header("📚 My Device Library")
    
    if st.session_state.devices_library:
        st.caption(f"Total devices: {len(st.session_state.devices_library)}")
        
        # Show library stats
        categories = {}
        for device, info in st.session_state.devices_library.items():
            cat = info.get('category', 'Other')
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in categories.items():
            st.caption(f"• {cat}: {count} devices")
        
        st.divider()
        
        # Option to clear library
        if st.button("🗑️ Clear Entire Library", key="clear_library_btn", use_container_width=True):
            st.session_state.devices_library.clear()
            save_devices_library(st.session_state.devices_library)
            st.rerun()
    else:
        st.info("No devices in library. Add some from above!")

# --- MAIN DASHBOARD ---
st.title("🇮🇳 India Electricity Bill Optimizer")
st.markdown("*Smart Device Database | Real-time Tracking | Energy Insights*")

# Show library stats
if st.session_state.devices_library:
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("📚 Library Size", len(st.session_state.devices_library))
    with col_stat2:
        running_count = len([d for d in st.session_state.devices_library if d in st.session_state.active_devices])
        st.metric("🟢 Currently Running", running_count)
    with col_stat3:
        preinstalled_count = len([d for d in st.session_state.devices_library if not st.session_state.devices_library[d].get('custom', False)])
        custom_count = len([d for d in st.session_state.devices_library if st.session_state.devices_library[d].get('custom', False)])
        st.metric("📦 Devices", f"{preinstalled_count} Pre | {custom_count} Custom")
else:
    st.info("📭 No devices in library! Use the sidebar to add devices from our database or add custom ones.")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📡 Live Monitoring")
    
    # --- DISPLAY ALL LIBRARY DEVICES WITH START/STOP BUTTONS ---
    if st.session_state.devices_library:
        st.markdown("### 🏠 Your Devices")
        
        # Separate into Running and Available
        running_devices = {name: info for name, info in st.session_state.devices_library.items() 
                          if name in st.session_state.active_devices}
        available_devices = {name: info for name, info in st.session_state.devices_library.items() 
                            if name not in st.session_state.active_devices}
        
        # Show Running Devices First
        if running_devices:
            st.markdown("#### 🟢 Currently Running")
            for name, info in running_devices.items():
                device_active_info = st.session_state.active_devices[name]
                elapsed = time.time() - device_active_info['start_time']
                hours_used = elapsed / 3600
                current_kwh = (info['wattage'] * hours_used) / 1000
                current_cost = current_kwh * rate
                
                with st.container():
                    # IMPROVED GREEN BOX WITH BETTER VISIBILITY
                    brand_info = f" | {info.get('brand', 'Unknown')}" if info.get('brand') else ""
                    st.markdown(f"""
                    <div style='border:2px solid #1B5E20; padding:15px; border-radius:8px; margin-bottom:12px; background-color:#2E7D32; box-shadow: 0 2px 4px rgba(0,0,0,0.1)'>
                        <strong style='color:#FFFFFF; font-size:16px'>🟢 {name}</strong> 
                        <span style='color:#E8F5E9; font-size:14px'>({info['category']}{brand_info})</span><br>
                        <span style='color:#FFFFFF'>⚡ {info['wattage']}W | 📊 {current_kwh:.4f} kWh | 💰 ₹{current_cost:.2f}</span><br>
                        <span style='color:#E8F5E9'>⏱️ {int(hours_used)}h {int((hours_used % 1)*60)}m running</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_stop, col_tip = st.columns([1, 2])
                    with col_stop:
                        if st.button(f"⏹️ Stop {name}", key=f"stop_{name}", use_container_width=True):
                            final_cost = current_kwh * rate
                            save_to_history(name, current_kwh, final_cost, state, rate)
                            del st.session_state.active_devices[name]
                            save_active_devices(st.session_state.active_devices)
                            st.success(f"✅ {name} stopped! Cost: ₹{final_cost:.2f}")
                            st.rerun()
                    
                    with col_tip:
                        if st.session_state.show_tips:
                            tip = get_saving_tip(name, info['wattage'], current_cost)
                            st.caption(tip)
                    
                    st.divider()
        
        # Show Available Devices
        if available_devices:
            st.markdown("#### ⚪ Available to Start")
            
            # Create grid layout for available devices
            cols_per_row = 2
            available_list = list(available_devices.items())
            
            for i in range(0, len(available_list), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    idx = i + j
                    if idx < len(available_list):
                        name, info = available_list[idx]
                        with cols[j]:
                            brand_display = f"<br><span style='font-size:10px; color:#888'>{info.get('brand', '')}</span>" if info.get('brand') else ""
                            with st.container():
                                st.markdown(f"""
                                <div style='border:1px solid #ddd; padding:10px; border-radius:8px; margin-bottom:10px'>
                                    <strong>{name}</strong>{brand_display}<br>
                                    <span style='font-size:12px; color:#666'>{info['category']}</span><br>
                                    ⚡ {info['wattage']}W
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if st.button(f"▶️ Start {name}", key=f"start_{name}", use_container_width=True):
                                    if name not in st.session_state.active_devices:
                                        st.session_state.active_devices[name] = {
                                            "wattage": info['wattage'],
                                            "start_time": time.time()
                                        }
                                        save_active_devices(st.session_state.active_devices)
                                        st.success(f"✅ {name} started!")
                                        st.rerun()
                                    else:
                                        st.warning(f"⚠️ {name} is already running!")
        
        # Quick Action Buttons
        st.divider()
        col_quick1, col_quick2, col_quick3 = st.columns(3)
        with col_quick1:
            if st.button("⏹️ Stop All Devices", use_container_width=True, key="stop_all_btn"):
                for name in list(st.session_state.active_devices.keys()):
                    if name in st.session_state.devices_library:
                        # Calculate final cost before stopping
                        info = st.session_state.active_devices[name]
                        elapsed = time.time() - info['start_time']
                        hours_used = elapsed / 3600
                        current_kwh = (info['wattage'] * hours_used) / 1000
                        final_cost = current_kwh * rate
                        save_to_history(name, current_kwh, final_cost, state, rate)
                
                st.session_state.active_devices.clear()
                save_active_devices(st.session_state.active_devices)
                st.success("✅ All devices stopped!")
                st.rerun()
        
        with col_quick2:
            if st.button("🔄 Refresh Status", use_container_width=True, key="refresh_btn"):
                st.rerun()
        
        with col_quick3:
            st.caption(f"🟢 Active: {len(running_devices)} | ⚪ Idle: {len(available_devices)}")
            
    else:
        st.warning("📭 No devices in library! Use the sidebar to add devices.")

with col2:
    st.subheader("📊 Financial Analytics")
    
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        
        # Convert date to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Calculate totals
        var_cost = df['Cost_INR'].sum()
        total_units = df['Units_kWh'].sum()
        grand_total = var_cost + fixed_charge
        
        # Display metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Units", f"{total_units:.2f} kWh")
        m2.metric("Variable Cost", f"₹{var_cost:,.2f}")
        m3.metric("Final Bill", f"₹{grand_total:,.2f}")
        
        # Today's usage
        today = datetime.now().date()
        today_df = df[df['Date'].dt.date == today]
        if not today_df.empty:
            today_units = today_df['Units_kWh'].sum()
            today_cost = today_df['Cost_INR'].sum()
            st.info(f"📅 Today's usage: {today_units:.2f} kWh (₹{today_cost:.2f})")
        
        # Cost by device chart
        st.markdown("### Cost Distribution by Device")
        df_grouped = df.groupby('Device', as_index=False)['Cost_INR'].sum()
        df_grouped = df_grouped.sort_values('Cost_INR', ascending=True)
        
        fig = px.bar(df_grouped, x='Cost_INR', y='Device', 
                     orientation='h', color='Cost_INR',
                     color_continuous_scale='Viridis',
                     title="Total Cost by Device")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Monthly trend
        df['Month'] = df['Date'].dt.strftime('%B %Y')
        monthly = df.groupby('Month')['Cost_INR'].sum().reset_index()
        if len(monthly) > 1:
            st.markdown("### Monthly Trend")
            fig2 = px.line(monthly, x='Month', y='Cost_INR', 
                          markers=True, title="Cost Trend")
            st.plotly_chart(fig2, use_container_width=True)
        
        # Recent logs with expander
        with st.expander("📋 Recent Usage Log"):
            display_df = df.tail(10)[['Date', 'Device', 'Units_kWh', 'Cost_INR']].copy()
            display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(display_df, use_container_width=True)
        
        # --- DATA MANAGEMENT ---
        st.divider()
        st.markdown("### ⚙️ Data Management")
        
        tab1, tab2, tab3 = st.tabs(["Delete Entry", "Clear All", "Export Data"])
        
        with tab1:
            if len(df) > 0:
                # Create formatted options
                df_sorted = df.sort_values('Date', ascending=False)
                options = [f"{row['Date'].strftime('%Y-%m-%d %H:%M')} | {row['Device']} | {row['Units_kWh']:.2f} kWh" 
                          for _, row in df_sorted.iterrows()]
                selected_entry = st.selectbox("Select entry to delete:", options, key="delete_entry_selector")
                
                if st.button("🗑️ Delete Selected", use_container_width=True, key="delete_selected_btn"):
                    # Extract info from selection
                    date_str = selected_entry.split(" | ")[0]
                    device_name = selected_entry.split(" | ")[1]
                    
                    # Filter out the selected entry
                    df = df[~((df['Date'].dt.strftime('%Y-%m-%d %H:%M') == date_str) & 
                             (df['Device'] == device_name))]
                    
                    if df.empty:
                        if os.path.exists(HISTORY_FILE):
                            os.remove(HISTORY_FILE)
                        st.success("All history cleared!")
                    else:
                        df.to_csv(HISTORY_FILE, index=False)
                        st.success("Entry deleted!")
                    st.rerun()
        
        with tab2:
            st.warning("⚠️ This will delete ALL billing history!")
            if st.button("🗑️ Clear ALL History", type="primary", use_container_width=True, key="clear_all_btn"):
                if os.path.exists(HISTORY_FILE):
                    os.remove(HISTORY_FILE)
                st.success("All history cleared!")
                st.rerun()
        
        with tab3:
            if st.button("📥 Download Full History", use_container_width=True, key="download_btn"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="💾 Save CSV File",
                    data=csv,
                    file_name=f"electricity_history_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key="download_csv_btn"
                )
        
        # Settings
        st.session_state.show_tips = st.checkbox("💡 Show energy saving tips", 
                                                 value=st.session_state.show_tips,
                                                 key="show_tips_checkbox")
        
    else:
        st.warning("📭 No billing history yet. Stop a device to see analytics here!")
        
        st.info("""
        **🚀 Quick Start Guide:**
        
        1. **Add Devices (3 ways):**
           - 🔍 **Smart Search**: Select device type → Brand → Model
           - ➕ **Custom Entry**: Add local/unbranded devices
           - ⚡ **Quick Add**: One-click common appliances
        
        2. **Track Usage:**
           - Click 'Start' on any device from your library
           - Let it run while using the device
           - Click 'Stop' when done
        
        3. **View Analytics:**
           - Real-time cost calculation
           - Daily/monthly trends
           - Export data for records
        """)

# --- FOOTER WITH STATS ---
st.divider()
col_f1, col_f2, col_f3, col_f4 = st.columns(4)
with col_f1:
    st.caption(f"📍 State: {state} @ ₹{rate}/unit")
with col_f2:
    st.caption(f"📚 Library: {len(st.session_state.devices_library)} devices")
with col_f3:
    st.caption(f"🟢 Active: {len(st.session_state.active_devices)} devices")
with col_f4:
    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
        st.caption(f"📊 Total sessions: {len(df)}")