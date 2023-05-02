import os
import glob
import shutil
import exifread
from PIL import Image, ImageDraw, ImageFont

# Open the camera app on Windows
os.system("start microsoft.windows.camera:")

# Wait for the user to capture an image and save it
input("Press Enter to save the captured image...")

# Find the latest image in the Camera Roll directory
file_list = glob.glob('C:/Users/kinjal jadav/Pictures/Camera Roll/*.jpg')

if not file_list:
    print("No JPG files found in Camera Roll directory")
else:
    latest_file = max(file_list, key=os.path.getctime)
    # Specify the desired file path to save the captured image
    save_path = "C:/Degree/Kinjal/Filtering and Geotagging/myphoto.jpg"

    # # Move the latest image to the desired file path
    shutil.move(latest_file, save_path)

def get_gps(gps_tag):
    degrees = float(gps_tag.values[0].num) / float(gps_tag.values[0].den)
    minutes = float(gps_tag.values[1].num) / float(gps_tag.values[1].den)
    seconds = float(gps_tag.values[2].num) / float(gps_tag.values[2].den)
    return degrees + (minutes / 60.0) + (seconds / 3600.0)

def get_date_time(date_tag, time_tag):
    date_str = date_tag.printable
    time_str = time_tag.printable
    return date_str, time_str

# Open the image file in binary mode
image_file = open("myphoto.jpg", "rb")

# Read the image file using exifread
tags = exifread.process_file(image_file)

# Extract the GPS information from the image if available
if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
    gps_latitude = tags['GPS GPSLatitude']
    gps_longitude = tags['GPS GPSLongitude']

    # Convert the GPS coordinates to degrees
    latitude = get_gps(gps_latitude)
    longitude = get_gps(gps_longitude)

    # Extract the date and time information from the image if available
    if 'EXIF DateTimeOriginal' in tags:
        date_time_original = tags['EXIF DateTimeOriginal']
        date, time = get_date_time(date_time_original, date_time_original)
    else:
        date, time = "N/A", "N/A"

    # Close the image file
    image_file.close()

    # Load the image
    image = Image.open("myphoto.jpg")

    # Create an ImageDraw object
    draw = ImageDraw.Draw(image)

    # Define the font and size for the text
    font = ImageFont.truetype("OpenSans-Regular.ttf", size=50)

    # Define the text you want to add
    text = "Location: ({:.6f}, {:.6f})\nDateTime: {}".format(latitude, longitude, date)

    # Define the position of the text
    position = (10, 10)

    # Add the text to the image
    draw.text(position, text, font=font, fill=(255, 255, 255))

    # Save the tagged image
    image.save("geotagimg.jpg")
else:
    print("GPS metadata not found in image file.")

    # Close the image file
    image_file.close()
