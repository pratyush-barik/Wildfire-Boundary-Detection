🔥 Wildfire Boundary Detection
🌍 Image-Based Wildfire Analysis System

A web-based system that analyzes images to identify wildfire-prone regions by detecting fire-like hotspots, estimating the wildfire boundary using geometric analysis, and visualizing the affected area through automated graphical output.
This project illustrates how image processing and computational geometry can work together to approximate wildfire-affected regions from visual data. Users upload an image, and the system automatically identifies potential fire hotspots, computes the wildfire boundary, estimates the affected area, and generates a clear visual representation of the impact.

✨ How It Works
🔍 Converts images to HSV color space for effective fire detection
🔥 Isolates fire-like regions using color thresholding
📍 Extracts hotspot coordinates from detected regions
📐 Constructs a convex hull to approximate the wildfire boundary
📊 Visualizes hotspots, boundary, and affected zone automatically

🛠️ Technologies Used
Python
Flask
OpenCV
NumPy
Shapely
Matplotlib

Project structure:--

Project structure:

```text
Wildfire-Boundary-Detection/
├── app.py
├── templates/
│   └── index.html
└── README.md
```


📌 This project is intended for academic learning and demonstration purposes and does not represent a real-world wildfire monitoring system.
