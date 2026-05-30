# EMODnet Habitat Map Validation Tool (Python / Streamlit)

Interactive web application for validating marine habitat shapefiles according to EMODnet Data Exchange Formats (DEF). This tool is a Python (Streamlit + GeoPandas) version of a traditional R/Shiny validation workflow.

---

## Features

- Upload ZIP shapefiles (ESRI format)
- Automatic DEF detection (OH / TH / HD / SA)
- Interactive map visualization (Plotly)
- Geometry validation (invalid polygons)
- Spatial overlap detection
- CRS validation (EPSG check)
- Attribute preview and inspection

---

## Project Structure

habitat-map-validation/  
├── habitat_map_validation_master.py  
├── validation.py  
├── requirements.txt  
├── run_app.bat  
└── README.md  

---

## Installation

### Create environment (recommended)

conda create -n habitat_env python=3.10  
conda activate habitat_env  

### Install dependencies

pip install -r requirements.txt  

OR (recommended for GIS stability)

conda install geopandas plotly streamlit -c conda-forge  

---

## Run the application

streamlit run habitat_map_validation_master.py  

OR double-click:

run_app.bat  

---

## Input data

Upload a ZIP file containing a shapefile:
- .shp  
- .shx  
- .dbf  
- .prj (recommended)  

---

## Supported DEF types

OH = Original Habitat DEF  
TH = Translated EUNIS Habitat DEF  
HD = Habitats Directive DEF  
SA = Study Area DEF  

---

## Validation checks

Geometry:
- Invalid polygons detection
- Geometry integrity check

Spatial:
- Overlapping polygons detection

Data:
- Field completeness
- Attribute inspection
- CRS validation

---

## Outputs

- Interactive map
- Validation tables
- Data preview
- CRS report

---

## Limitations

- Not optimized for very large datasets
- Overlap check is O(n²)
- File-based (no database)

---

## Author

Python version of EMODnet-style R/Shiny validation workflow.
