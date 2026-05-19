import geopandas as gpd
import pandas as pd

# =========================
# DEF DETECTION
# =========================
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


# =========================
# ADD HABITAT COLUMN
# =========================
def add_habitat(gdf, def_type):

    gdf = gdf.copy()
    gdf["Habitat"] = "Unknown"

    if def_type == "TH" and "HAB_TYPE" in gdf.columns:
        gdf["Habitat"] = gdf["HAB_TYPE"]

    elif def_type == "OH" and "ORIG_HAB" in gdf.columns:
        gdf["Habitat"] = gdf["ORIG_HAB"]

    elif def_type == "HD" and "ANNEXI" in gdf.columns:
        gdf["Habitat"] = gdf["ANNEXI"]

    return gdf


# =========================
# GEOMETRY VALIDATION
# =========================
def check_geometry(gdf):

    invalid = ~gdf.is_valid

    if invalid.sum() == 0:
        return pd.DataFrame({"Result": ["No geometry errors detected"]})

    return gdf.loc[invalid, ["POLYGON"]]


# =========================
# OVERLAP CHECK (simple but safe)
# =========================
def check_overlaps(gdf):

    overlaps = []

    for i in range(len(gdf)):
        for j in range(i + 1, len(gdf)):

            try:
                if gdf.geometry.iloc[i].intersects(gdf.geometry.iloc[j]):
                    overlaps.append((
                        gdf.iloc[i].get("POLYGON", i),
                        gdf.iloc[j].get("POLYGON", j)
                    ))
            except:
                continue

    if len(overlaps) == 0:
        return pd.DataFrame({"Result": ["No overlaps detected"]})

    return pd.DataFrame(overlaps, columns=["Polygon 1", "Polygon 2"])


# =========================
# CRS CHECK
# =========================
def check_crs(gdf):
    if gdf.crs is None:
        return "CRS not defined"

    return str(gdf.crs)


# =========================
# SAFE LOADER HELPERS
# =========================
def load_shapefile(path):
    return gpd.read_file(path)