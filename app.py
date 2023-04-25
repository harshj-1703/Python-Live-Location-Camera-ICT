import cv2
import tkinter as tk
from PIL import Image, ImageTk

# Function to capture photo
def capture_photo():
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Check if frame was captured successfully
    if not ret:
        print("Failed to capture frame")
        return

    # Specify the path and filename to save the photo
    save_path = './photos/photo.jpg'

    # Save the captured frame as an image
    cv2.imwrite(save_path, frame)

    # Print success message
    print(f"Photo saved as {save_path}")

    # Open the saved photo using Pillow
    img = Image.open(save_path)
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
