# Import required libraries
import boto3            # AWS SDK for Python (to connect with Rekognition & DynamoDB)
import io               # For handling byte streams
from PIL import Image, ImageTk   # Pillow library to work with images
import tkinter as tk    # GUI toolkit for Python
from tkinter import Label, StringVar, Frame   # Specific Tkinter widgets
from time import sleep  # To pause execution for animations/effects
import random           # To generate random colors for effects

# ---------------- AWS CLIENT SETUP ----------------
# Create Rekognition client (for face matching)
rekognition = boto3.client('rekognition', region_name='us-east-1')
# Create DynamoDB client (for fetching criminal details)
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# ---------------- LOAD SUSPECT IMAGE ----------------
image_path = "criminal.jpg"   # Path to the suspect/criminal image
image = Image.open(image_path)   # Open the image
stream = io.BytesIO()            # Create a byte stream
image.save(stream, format="JPEG")   # Save the image in JPEG format to stream
image_binary = stream.getvalue()   # Get binary representation of the image (needed by Rekognition)

# ---------------- GUI SETUP ----------------
window = tk.Tk()  # Create the GUI window
window.title("Criminal Identification System")  # Title of the window
window.geometry("650x550")   # Window size
window.configure(bg="black") # Background color

# ---------------- DYNAMIC MESSAGE LABEL ----------------
message = StringVar()   # Variable to hold text dynamically
message.set("Starting face recognition...")  # Initial text
label = Label(window, textvariable=message, font=("Helvetica", 14, "bold"),
              fg="white", bg="black", wraplength=600, justify="center")
label.pack(pady=20)   # Place label on window

# ---------------- IMAGE DISPLAY AREA ----------------
img_label = Label(window, bg="black")  # Will be used later to show criminal image

# ---------------- COLORS FOR FLASH EFFECT ----------------
background_colors = ["#ff4d4d", "#3399ff", "#33cc33", "#ff9933", "#9966ff", "#ff66b3"]
text_colors = ["white", "black"]

# Function to randomly select a background & text color
def random_color():
    return random.choice(background_colors), random.choice(text_colors)

# ---------------- MAIN FACE SEARCH FUNCTION ----------------
def search_faces():
    try:
        # Send suspect image to Rekognition collection for face search
        response = rekognition.search_faces_by_image(
            CollectionId='facial_collection',   # Pre-created Rekognition collection
            Image={'Bytes': image_binary}       # Image bytes for comparison
        )

        # If matches are found in collection
        if response['FaceMatches']:
            for match in response['FaceMatches']:
                face_id = match['Face']['FaceId']        # Unique Rekognition face ID
                confidence = match['Face']['Confidence'] # Match confidence %

                # ---------------- FLASH EFFECT ----------------
                bg_color, text_color = random_color()
                frame = Frame(window, width=500, height=50, bg=bg_color)
                frame.pack(pady=10)

                # Update message with match details
                message.set(f"Match found! FaceId: {face_id}\nConfidence: {confidence:.2f}%")
                label.config(fg=text_color, bg=bg_color)
                window.update()
                sleep(1.5)

                # ---------------- FETCH DETAILS FROM DYNAMODB ----------------
                face = dynamodb.get_item(
                    TableName='faceimage',
                    Key={'RekognitionId': {'S': face_id}}  # Search by RekognitionId
                )

                if 'Item' in face:
                    # Extract stored attributes from DynamoDB record
                    person_name = face['Item']['FullName']['S']
                    crime_type = face['Item'].get('CrimeType', {}).get('S', 'Unknown')
                    wanted_status = face['Item'].get('WantedStatus', {}).get('S', 'Unknown')

                    # Show criminal details in GUI
                    message.set(f"IDENTIFIED CRIMINAL:\n\n"
                                f"Name: {person_name}\n"
                                f"Crime: {crime_type}\n"
                                f"Wanted Status: {wanted_status}")

                    # Display the suspect image in GUI
                    img_for_display = image.resize((250, 250))
                    photo = ImageTk.PhotoImage(img_for_display)
                    img_label.config(image=photo)
                    img_label.image = photo  # Store reference to avoid garbage collection
                    img_label.pack(pady=10)

                    # Reset label color
                    label.config(fg="white", bg="black")
                    window.update()
                    sleep(2)
                else:
                    # Case: Face matched but no record in DB
                    message.set("Face found, but no record in database.")
                    label.config(fg="red", bg="black")
                    window.update()
                    sleep(1.5)

                # ---------------- FADE-OUT EFFECT ----------------
                for i in range(20, 255, 15):
                    fade_color = f'#{i:02x}{i:02x}{i:02x}'  # Gradually changing grey shades
                    frame.config(bg=fade_color)
                    window.update()
                    sleep(0.1)
                frame.destroy()  # Remove flash frame

        else:
            # If no faces matched
            message.set("No faces matched in the collection.")
            label.config(fg="red", bg="black")
            window.update()

    except Exception as e:
        # Error handling
        message.set(f"Error: {str(e)}")
        label.config(fg="red", bg="black")
        window.update()

# ---------------- RUN THE FACE SEARCH AFTER GUI LOADS ----------------
window.after(1000, search_faces)  # Call search_faces after 1 second
window.mainloop()  # Keep the GUI running
