import os
import cv2
import numpy as np
from flask import Flask, request, render_template, send_from_directory
from shapely.geometry import MultiPoint
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt

app = Flask(__name__)
STATIC_FOLDER = 'static'
app.config['STATIC_FOLDER'] = STATIC_FOLDER

if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

def find_hotspots(image_path):
    
    image = cv2.imread(image_path)
    if image is None:
        return None, "Error: Could not read the image file. It might be corrupted or in an unsupported format."
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower_range1 = np.array([0, 150, 150])
    upper_range1 = np.array([10, 255, 255])
    
    lower_range2 = np.array([20, 150, 150])
    upper_range2 = np.array([30, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_range1, upper_range1)
    mask2 = cv2.inRange(hsv, lower_range2, upper_range2)
    
    combined_mask = cv2.bitwise_or(mask1, mask2)

    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    hotspot_coords = []
    if not contours:
        return None, "No hotspots found. (Try adjusting color range in app.py or use a different image)"

    for c in contours:
        M = cv2.moments(c)
        
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            hotspot_coords.append((cX, image.shape[0] - cY))
        
    return hotspot_coords, None


def analyze_and_plot(hotspot_coords, result_filename):
    if not hotspot_coords or len(hotspot_coords) < 3:
        return 0, None, "Error: Fewer than 3 hotspots detected. Cannot form a perimeter."

    points = MultiPoint(hotspot_coords)
    
    convex_hull = points.convex_hull
    
    area = convex_hull.area
    
    x_hotspots, y_hotspots = zip(*hotspot_coords)
    hull_x, hull_y = convex_hull.exterior.xy
    
    plt.figure(figsize=(10, 8))
    plt.plot(hull_x, hull_y, 'r-', linewidth=2, label=f'Wildfire Boundary (Convex Hull)\nArea: {area:.2f} sq. units')
    plt.scatter(x_hotspots, y_hotspots, c='orange', edgecolor='black', label=f'Hotspots ({len(hotspot_coords)} points)')
    plt.fill(hull_x, hull_y, 'red', alpha=0.3, label='Affected Zone')
    
    plt.title('Wildfire Boundary Detection')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    
    plot_path = os.path.join(app.config['STATIC_FOLDER'], result_filename)
    plt.savefig(plot_path)
    plt.close() 
    
    return area, f"/{plot_path}", None


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file selected.")
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('index.html', error="No file selected.")

        if file:
            temp_path = os.path.join("temp_image.png")
            file.save(temp_path)
            
            hotspots, error = find_hotspots(temp_path)
            if error:
                os.remove(temp_path) 
                return render_template('index.html', error=error)
            result_image_name = f"result_{hash(file.filename)}.png"
            area, plot_url, error = analyze_and_plot(hotspots, result_image_name)
            if error:
                os.remove(temp_path) 
                return render_template('index.html', error=error)

            os.remove(temp_path) 
            return render_template('index.html', 
                                   plot_url=plot_url, 
                                   area=f"{area:.2f}",
                                   hotspot_count=len(hotspots))

    return render_template('index.html', plot_url=None, area=None)

@app.route('/static/<filename>')
def send_static_file(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)