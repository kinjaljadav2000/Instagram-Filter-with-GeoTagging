import os
import glob
import shutil
import exifread
# from PIL import Image
# from instagram.filters import *

# Open the camera app on Windows
os.system("start microsoft.windows.camera:")

# Wait for the user to capture an image and save it
input("Press Enter to save the captured image...")

# Find the latest image in the Camera Roll directory
file_list = glob.glob('C:/Users/Neer Gosrani/Pictures/Camera Roll/*.jpg')

if not file_list:
    print("No JPG files found in Camera Roll directory")
else:
    latest_file = max(file_list, key=os.path.getctime)
    # Specify the desired file path to save the captured image
    save_path = "D:/Degree/Friends/Kinjal/Filtering and Geotagging/myphoto.jpg"

    # with Image.open(latest_file) as image:
    #     filtered_image = Juno()(image)
        
    # filtered_image.save(save_path)
    
    # os.remove(latest_file)
    # # Move the latest image to the desired file path
    shutil.move(latest_file, save_path)

# Open the image file in binary mode
with open("myphoto.jpg", "rb") as image_file:
    # Read the EXIF tags
    tags = exifread.process_file(image_file)

    # Extract the GPS location data
    lat_ref = tags.get("GPS GPSLatitudeRef")
    lat = tags.get("GPS GPSLatitude")
    long_ref = tags.get("GPS GPSLongitudeRef")
    long = tags.get("GPS GPSLongitude")

    # Convert the GPS data to decimal degrees
    if lat and long:
        lat_degrees = float(lat.values[0].num) / float(lat.values[0].den)
        lat_minutes = float(lat.values[1].num) / float(lat.values[1].den)
        lat_seconds = float(lat.values[2].num) / float(lat.values[2].den)
        lat_decimal = lat_degrees + (lat_minutes / 60.0) + (lat_seconds / 3600.0)
        if lat_ref.values[0] == "S":
            lat_decimal = -lat_decimal

        long_degrees = float(long.values[0].num) / float(long.values[0].den)
        long_minutes = float(long.values[1].num) / float(long.values[1].den)
        long_seconds = float(long.values[2].num) / float(long.values[2].den)
        long_decimal = long_degrees + (long_minutes / 60.0) + (long_seconds / 3600.0)
        if long_ref.values[0] == "W":
            long_decimal = -long_decimal

        # Print the GPS location data
        print("Latitude: ", lat_decimal)
        print("Longitude: ", long_decimal)
    else:
        print("No GPS data found in image EXIF tags.")
