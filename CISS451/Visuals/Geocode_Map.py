import pandas as pd
import re
import json
from geopy.geocoders import Nominatim
import folium

# ========== TESTING ==========
# Uncomment below to enable test mode 
# (Only geocode first 30 new addresses for faster processing)
# GEOCODE_LIMIT = 30
# ===================================

# Initialize geolocator
geolocator = Nominatim(user_agent="geo_cluster_app")

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Data Loaded from {file_path}")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def load_cache(cache_file='In-Progress/SeniorProjects/Visuals/geocode_cache.json'):
    try:
        with open(cache_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_cache(cache, cache_file='In-Progress/SeniorProjects/Visuals/geocode_cache.json'):
    with open(cache_file, 'w') as file:
        json.dump(cache, file, indent=2)

def geocode_address(row, cache):
    address = f"{row['City']}, {row['State']}, {row['County']}"
    if address in cache:
        print(f"Using cached result for {address}")
        return cache[address]
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            cache[address] = (location.latitude, location.longitude)
            return location.latitude, location.longitude
        return None, None
    except Exception as e:
        print(f"Geocoding error for {address}: {e}")
        return None, None

ethnicity_mapping = {
    'Black': 'Black or African American',
    'African American': 'Black or African American',
    'Latino': 'Hispanic/Latino',
    'Latina': 'Hispanic/Latino',
    'American Indian': 'Native American/Alaska Native',
    'Pacific Islander': 'Native Hawaiian/Pacific Islander',
    'Multiple': 'Multi-Racial',
    'Two or More': 'Multi-Racial'
}

ethnicity_palette = {
    'White': '#4e79a7',
    'Black or African American': '#f28e2b',
    'Hispanic/Latino': '#e15759',
    'Asian': '#76b7b2',
    'Native American/Alaska Native': '#59a14f',
    'Native Hawaiian/Pacific Islander': '#edc948',
    'Multi-Racial': '#ff9da7',
    'Other': '#9c755f',
    'Unknown': '#bab0ac'
}

def standardize_ethnicity(entry):
    if pd.isna(entry):
        return 'Unknown'
    
    entry = str(entry).strip().title()
    if not entry:
        return 'Unknown'
    
    if entry in ethnicity_palette:
        return entry
    
    mapped_entry = ethnicity_mapping.get(entry, entry)
    if mapped_entry in ethnicity_palette:
        return mapped_entry
    
    parts = re.split(r'\s*[/,;&]\s*|\s+and\s+', entry, flags=re.IGNORECASE)
    parts = [p.strip().title() for p in parts if p.strip()]
    
    valid_components = []
    for part in parts:
        mapped = ethnicity_mapping.get(part, part)
        if mapped in ethnicity_palette:
            valid_components.append(mapped)
    
    if len(valid_components) > 1:
        return 'Multi-Racial'
    return valid_components[0] if valid_components else 'Unknown'

def add_geocode_columns(data, cache):
    latitudes = []
    longitudes = []
    new_geocode_count = 0
    
    for _, row in data.iterrows():
        if 'GEOCODE_LIMIT' in globals() and new_geocode_count >= GEOCODE_LIMIT: # type: ignore
            if f"{row['City']}, {row['State']}, {row['County']}" not in cache:
                latitudes.append(None)
                longitudes.append(None)
                continue
                
        lat, lon = geocode_address(row, cache)
        latitudes.append(lat)
        longitudes.append(lon)
        
        if f"{row['City']}, {row['State']}, {row['County']}" not in cache:
            new_geocode_count += 1

    data = data.copy()
    data.loc[:, 'Latitude'] = latitudes
    data.loc[:, 'Longitude'] = longitudes
    return data

def age_groups(age):
    try:
        age = float(age)
        if age <= 13: return 'Child'
        if age <= 19: return 'Teen'
        if age <= 35: return 'Young Adult'
        if age <= 64: return 'Adult'
        return 'Senior'
    except:
        return 'Unknown'

def assign_colors(data):
    age_palette = {
        'Child': '#6A8CAF',  # Soft blue
        'Teen': '#A5C7D9',   # Light teal
        'Young Adult': '#4BACC6',  # Bright cyan
        'Adult': '#F79646',  # Warm orange
        'Senior': '#9BBB59',  # Fresh green
        'Unknown': '#999999'
    }

    ethnicity_palette = {
        'White': '#5B9BD5',  # Corporate blue
        'Black or African American': '#FFC000',  # Gold
        'Hispanic/Latino': '#C00000',  # Deep red
        'Asian': '#70AD47',  # Green
        'Native American/Alaska Native': '#7030A0',  # Purple
        'Native Hawaiian/Pacific Islander': '#FF6600',  # Vibrant orange
        'Multi-Racial': '#FF99CC',  # Pink
        'Other': '#A5A5A5',
        'Unknown': '#666666'
    }

    sex_palette = {
        'Male': '#0070C0',  # Deep blue
        'Female': '#FF3399',  # Pink
        'Unknown': '#808080'
    }

    data = data.copy()
    data.loc[:, 'AgeGroup'] = data['Age'].apply(age_groups)
    data.loc[:, 'AgeColor'] = data['AgeGroup'].map(age_palette)
    data.loc[:, 'EthnicityColor'] = data['Race / Ethnicity'].map(
        lambda x: ethnicity_palette.get(x, '#bab0ac'))
    data.loc[:, 'SexColor'] = data['Sex'].map(
        lambda x: sex_palette.get(x, '#737373'))
    
    return data, age_palette, ethnicity_palette, sex_palette

def plot_map(data):
    data, age_palette, ethnicity_palette, sex_palette = assign_colors(data)
    map_center = [data['Latitude'].mean(), data['Longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=5)

    # Create feature groups
    age_group = folium.FeatureGroup(name="Age Groups", show=True)
    ethnicity_group = folium.FeatureGroup(name="Ethnicity", show=False)
    sex_group = folium.FeatureGroup(name="Sex", show=False)

    # Add markers with popups
    for _, row in data.iterrows():
        if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
            popup_content = f"""
            <div style="font-family: Arial; font-size: 12px">
                <b>Location:</b> {row['City']}, {row['State']}<br>
                <b>Age:</b> {row['Age']} ({row['AgeGroup']})<br>
                <b>Ethnicity:</b> {row['Race / Ethnicity']}<br>
                <b>Sex:</b> {row['Sex']}<br>
                <b>County:</b> {row['County']}
            </div>
            """
            
            # Age markers
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=5,
                color=row['AgeColor'],
                fill=True,
                fill_color=row['AgeColor'],
                fill_opacity=0.7,
                popup=folium.Popup(popup_content, max_width=250)
            ).add_to(age_group)
            
            # Ethnicity markers
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=5,
                color=row['EthnicityColor'],
                fill=True,
                fill_color=row['EthnicityColor'],
                fill_opacity=0.7,
                popup=folium.Popup(popup_content, max_width=250)
            ).add_to(ethnicity_group)
            
            # Sex markers
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=5,
                color=row['SexColor'],
                fill=True,
                fill_color=row['SexColor'],
                fill_opacity=0.7,
                popup=folium.Popup(popup_content, max_width=250)
            ).add_to(sex_group)

    # Add groups to map
    age_group.add_to(m)
    ethnicity_group.add_to(m)
    sex_group.add_to(m)

    # Add layer control
    folium.LayerControl(collapsed=False).add_to(m)

    # DYNAMIC LEGEND THAT MATCHES YOUR PALETTES
    def create_legend_items(palette):
        items = []
        for label, color in palette.items():
            items.append(f'<p><i style="color:{color}">●</i> {label}</p>')
        return '\n'.join(items)

    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 20px;
        left: 20px;
        width: 260px;
        background: white;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
        z-index: 9999;
        font-family: Arial;
        font-size: 13px;
    ">
        <h4 style="margin-top:0; margin-bottom:10px; border-bottom:1px solid #eee; padding-bottom:5px;">
            Map Legend
        </h4>
        
        <select id="legendSelect" onchange="switchLegend()" style="
            width: 100%;
            padding: 5px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 3px;
        ">
            <option value="age">Age Groups</option>
            <option value="ethnicity">Ethnicity</option>
            <option value="sex">Sex</option>
        </select>
        
        <div id="ageLegend">
            {create_legend_items(age_palette)}
        </div>
        
        <div id="ethnicityLegend" style="display:none">
            {create_legend_items(ethnicity_palette)}
        </div>
        
        <div id="sexLegend" style="display:none">
            {create_legend_items(sex_palette)}
        </div>
    </div>

    <script>
    function switchLegend() {{
        document.getElementById('ageLegend').style.display = 'none';
        document.getElementById('ethnicityLegend').style.display = 'none';
        document.getElementById('sexLegend').style.display = 'none';
        
        var selection = document.getElementById('legendSelect').value;
        document.getElementById(selection + 'Legend').style.display = 'block';
    }}
    </script>
    """

    m.get_root().html.add_child(folium.Element(legend_html))
    
    m.save("In-Progress/SeniorProjects/Visuals/geocoded_map.html")
    print("Map with perfectly synchronized legend saved successfully!")

def main(): 
    train_path = 'In-Progress/SeniorProjects/Data-Management/NamUS_training_data.csv'
    test_path = 'In-Progress/SeniorProjects/Data-Management/NamUS_testing_data.csv'

    train_data = load_data(train_path)
    test_data = load_data(test_path)

    if train_data is not None and test_data is not None:
        selected_cols = ['City', 'State', 'County', 'Age', 'Sex', 'Race / Ethnicity']
        
        train_df = train_data[selected_cols].copy()
        test_df = test_data[selected_cols].copy()

        combined_df = pd.concat([train_df, test_df], ignore_index=True)

        # Standardize ethnicity
        combined_df = combined_df.copy()
        combined_df.loc[:, 'Race / Ethnicity'] = combined_df['Race / Ethnicity'].apply(standardize_ethnicity)
        
        # Geocode addresses
        cache = load_cache()
        combined_df = add_geocode_columns(combined_df, cache)
        combined_df = combined_df.dropna(subset=['Latitude', 'Longitude'])
        
        # Clean data
        combined_df = combined_df.copy()
        combined_df.loc[:, 'Sex'] = combined_df['Sex'].fillna('Unknown')
        
        # Generate map
        plot_map(combined_df)
        save_cache(cache)

if __name__ == "__main__":
    main()