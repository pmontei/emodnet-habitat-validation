import streamlit as st
import geopandas as gpd
import pandas as pd
import zipfile
import tempfile
import os
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="EMODnet Validation Tool", layout="wide")

st.title("🌊 EMODnet Data Validation Tool")

# =========================
# DEF LABEL MAP (FIX PRINCIPAL)
# =========================
DEF_LABELS = {
    "OH": "Original Habitat DEF",
    "TH": "Translated EUNIS Habitat DEF",
    "HD": "Habitats Directive DEF",
    "SA": "Study Area DEF"
}

# =========================
# FILE UPLOAD
# =========================
file = st.file_uploader("Upload ZIP shapefile", type="zip")

# =========================
# FUNCTIONS
# =========================
def extract_zip(zip_path):
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(temp_dir)
    return temp_dir


def load_shapefile(folder):
    shp = None
    for f in os.listdir(folder):
        if f.endswith(".shp"):
            shp = os.path.join(folder, f)
    if shp is None:
        raise ValueError("No shapefile found in ZIP")
    return gpd.read_file(shp)


def detect_def(gdf):
    cols = gdf.columns

    if "HAB_TYPE" in cols:
        return "TH"
    elif "ANNEXI" in cols:
        return "HD"
    elif "UUID" in cols:
        return "SA"
    else:
        return "OH"


def add_habitat(gdf, def_type):
    gdf["Habitat"] = "Unknown"

    if def_type == "TH" and "HAB_TYPE" in gdf.columns:
        gdf["Habitat"] = gdf["HAB_TYPE"]

    elif def_type == "OH" and "ORIG_HAB" in gdf.columns:
        gdf["Habitat"] = gdf["ORIG_HAB"]

    elif def_type == "HD" and "ANNEXI" in gdf.columns:
        gdf["Habitat"] = gdf["ANNEXI"]

    return gdf


def check_geometry(gdf):
    invalid = gdf[~gdf.is_valid]

    if invalid.empty:
        return pd.DataFrame({"Result": ["No geometry errors detected"]})

    return invalid[["POLYGON"]]


def check_overlaps(gdf):
    overlaps = []

    for i in range(len(gdf)):
        for j in range(i + 1, len(gdf)):
            if gdf.geometry.iloc[i].intersects(gdf.geometry.iloc[j]):
                overlaps.append(
                    (gdf.iloc[i]["POLYGON"], gdf.iloc[j]["POLYGON"])
                )

    if len(overlaps) == 0:
        return pd.DataFrame({"Result": ["No overlaps detected"]})

    return pd.DataFrame(overlaps, columns=["Poly1", "Poly2"])


# =========================
# MAIN APP
# =========================
if file:

    # save zip
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.read())
        zip_path = tmp.name

    # extract
    folder = extract_zip(zip_path)

    # load data
    gdf = load_shapefile(folder)

    # detect DEF
    def_type = detect_def(gdf)
    def_label = DEF_LABELS.get(def_type, def_type)

    # add habitat field
    gdf = add_habitat(gdf, def_type)

    # =========================
    # UI INFO (FIXED)
    # =========================
    st.success(f"Detected DEF: {def_label}")

    # =========================
    # TABS
    # =========================
    tab1, tab2, tab3 = st.tabs(["Map", "Validation", "Data"])

    # -------------------------
    # MAP
    # -------------------------
    with tab1:

        st.subheader("Interactive Map")

        fig = px.choropleth_mapbox(
            gdf,
            geojson=gdf.__geo_interface__,
            locations=gdf.index,
            color="Habitat",
            mapbox_style="open-street-map",
            center={
                "lat": gdf.geometry.centroid.y.mean(),
                "lon": gdf.geometry.centroid.x.mean()
            },
            zoom=5
        )

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # VALIDATION
    # -------------------------
    with tab2:

        st.subheader("Geometry validation")
        st.dataframe(check_geometry(gdf))

        st.subheader("Overlap validation")
        st.dataframe(check_overlaps(gdf))

        st.subheader("CRS")
        st.write(str(gdf.crs))

    # -------------------------
    # DATA
    # -------------------------
    with tab3:

        st.subheader("Dataset preview")
        st.dataframe(gdf.head())