import cv2
import tkinter as tk
from PIL import Image, ImageTk
from PIL import Image, ImageDraw, ImageFont
import geocoder
import requests

def get_location_info(lat, lng):
    api_key = '3d95a7ba9fe8491586f4668a1a3a3783'
    url = f'https://api.opencagedata.com/geocode/v1/json?q={lat}+{lng}&key={api_key}'
    response = requests.get(url).json()
    if response['total_results'] > 0:
        location = response['results'][0]['formatted']
        components = response['results'][0]['components']
        city = components.get('city', '')
        state = components.get('state', '')
        country = components.get('country', '')
        address = components.get('road', '') + ' ' + components.get('house_number', '')
        return f"{location}, \n{city}, \n{state}, \n{country}, \n{address}"
    else:
        return 'location not loaded perfectly'

def capture_photo():
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Check if frame was captured successfully
    if not ret:
        print("Failed to capture frame")
        return

    # Get the current location
    g = geocoder.ip('me')
    location_info = get_location_info(g.lat, g.lng)

    # Specify the path and filename to save the photo
    save_path = './photos/photo.jpg'

    # Open the watermark image
    watermark = Image.open('watermark.png')

    # Resize the watermark to 25% of the size of the captured image
    width, height = frame.shape[1], frame.shape[0]
    watermark_width = int(width * 0.25)
    watermark_height = int(watermark_width * watermark.size[1] / watermark.size[0])
    watermark = watermark.resize((watermark_width, watermark_height), resample=Image.LANCZOS)

    watermark1 = Image.open('watermark1.png')

    # Resize the watermark to 25% of the size of the captured image
    width1, height1 = frame.shape[1], frame.shape[0]
    watermark_width1 = int(width1 * 0.15)
    watermark_height1 = int(watermark_width1 * watermark1.size[1] / watermark1.size[0])
    watermark1 = watermark1.resize((watermark_width1, watermark_height1), resample=Image.LANCZOS)

    # Convert the captured frame to PIL Image
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Blend the watermark with the captured image
    x = img.width - watermark.width - 10
    y = 10
    img.paste(watermark, (x, y), mask=watermark)

    # Blend the watermark with the captured image
    x = 10
    y = 10
    img.paste(watermark1, (x, y), mask=watermark1)

    # Add location overlay
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 12)
    text_width, text_height = draw.textsize(location_info, font=font)
    x = int(width * 0.02)
    y = int(height * 0.824)
    draw.rectangle((x, y, x + text_width + 8, y + text_height + 8), fill=(255, 255, 255, 80))
    draw.text((x + 5, y + 5), location_info, fill=(0, 0, 0), font=font)

    # Save the image with watermark and location overlay
    img.save(save_path)

    # Print success message
    print(f"Photo saved as {save_path}")

    # Open the saved photo using Pillow
    img.show()


# Function to create the GUI window
def create_window():
    window = tk.Tk()
    window.title("Capture Photo")

    # Create a label to display camera feed
    label = tk.Label(window)
    label.pack()

    # Function to update the camera feed
    def update_feed():
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Convert the frame to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to PIL Image
        img = Image.fromarray(frame)

        # Convert the PIL Image to PhotoImage
        img = ImageTk.PhotoImage(img)

        # Update the label with the new image
        label.config(image=img)
        label.image = img

        # Call this function again after a delay of 10 milliseconds
        label.after(10, update_feed)

    # Create a button in the window
    button = tk.Button(window, text="Capture Photo", command=capture_photo)
    button.pack()

    # Call the function to start updating the camera feed
    update_feed()

    window.mainloop()

# Open the default camera
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Failed to open camera")
    exit()

# Create the window
create_window()

# Release the camera
cap.release()
