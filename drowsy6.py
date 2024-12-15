import streamlit as st
import cv2
from keras.models import load_model
from pygame import mixer
import numpy as np
import csv
import os
import pandas as pd
from datetime import datetime
import bcrypt  # For password hashing
import matplotlib.pyplot as plt
import seaborn as sns

# User credentials (In production, use a secure database)
#bcrypt library to hash the password "password123", storing it in a secure, non-plain-text format.
#bcrypt works with byte-encoded data rather than plain strings.
# This function(bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())) takes the byte-encoded password and salt as arguments, hashing them together to create a secure, non-reversible hashed password.
users = {
    "admin": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()),
}

# Initialize pygame mixer
#mixer module allows you to load, play, stop, and control audio files within the application.
mixer.init()#initialize mixer before loading or playing any sound files
alert_sound = "alert.mp3"  # Path to the alert sound file

# Function to play alert sound
def play_alert_sound():
    if not mixer.music.get_busy():  # Play sound only if it's not already playing, returns True if there is a sound actively playing, and False if not
        mixer.music.load(alert_sound)#Loading the sound is necessary before it can be played.
        mixer.music.play(-1)  # Play in a loop until manually stopped beacuse Continuous looping keeps the alert active and noticeable for the user until the issue (in this case, drowsiness) is resolved.

# Function to stop alert sound
def stop_alert_sound():
    if mixer.music.get_busy():  # Stop sound if it's currently playing
        mixer.music.stop()

# Log drowsy event
def log_drowsy_event(image_path, pred):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("drowsy_events_log.csv", mode="a", newline="") as file:#a-appending
        writer = csv.writer(file)
        writer.writerow([timestamp, image_path, pred])
    return timestamp

# Initialize CSV log file
if not os.path.exists("drowsy_events_log.csv"):
    with open("drowsy_events_log.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Image Path", "Prediction"])

# Function to download the report
def download_report():
    with open("drowsy_events_log.csv", "r") as file:#opens the file in read mode,with statement ensures that the file is automatically closed after reading
        st.download_button(
            label="Download Drowsiness Report",
            data=file,
            file_name="drowsy_events_log.csv",
            mime="text/csv"
        )#displays a download button

# Function to add custom styles for Streamlit's web interface
def add_custom_styles():
    st.markdown(
        """
        <style>
        /* Center the title and set font color and size */
        .title {
            text-align: center;
            font-size: 2.5em;
            color: #4B0082; /* Indigo color */
        }
        .css-1n2mz7e3 {
            width: 50px;
        }
        .css-1v0mbdj {
            margin-left: 220px;
        }
        .stApp {
            background-color: #E6E6FA; /* Light blue */
        }
        .css-1n2mz7e3 {
            background-color: #f5f5dc; /* Cream color */
        }
        section[data-testid="stSidebar"] {
            background-color: #f5f5dc;
        }
        div[data-testid="stSidebar"] .css-18e3th9 a {
            color: #4B0082; /* Indigo */
            font-weight: bold;
        }
        div[data-testid="stSidebar"] .css-18e3th9 a:hover {
            color: #FFA500; /* Orange on hover */
        }
        div[data-testid="stSidebar"] .css-1avcm0n .css-18e3th9 a {
            color: #DC143C; /* Crimson */
        }
        div[data-testid="stSelectbox"] > div {
            background-color: #FFDAB9; /* Light peach */
        }
        div[data-testid="stSelectbox"] > div select {
            color: #4B0082; /* Indigo */
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
# Function to perform data analysis on drowsy events log
def analyze_data():
    # Load the drowsy events log
    if os.path.exists("drowsy_events_log.csv"):
        df = pd.read_csv("drowsy_events_log.csv")

        # Display basic statistics
        st.subheader("Drowsiness Events Analysis")
        total_events = df.shape[0]#gives the number of rows in the DataFrame, i.e., the total number of logged drowsiness events.
        st.write(f"Total Drowsiness Events Logged: {total_events}")

        # Parse timestamp and create a date column
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])#converted from string format to a proper datetime object
        df['Date'] = df['Timestamp'].dt.date#A new column, Date, is created by extracting the date part from the Timestamp column.

        # Count events per day
        #counts how many times each date appears.
        #sort_index() ensures the dates are displayed in chronological order.
        daily_counts = df['Date'].value_counts().sort_index()
        st.write("Drowsiness Events Count by Day:")
        st.bar_chart(daily_counts)

        # Additional analysis: average drowsiness prediction value
        average_prediction = df['Prediction'].mean()
        st.write(f"Average Drowsiness Prediction Value: {average_prediction:.2f}")

        # Visualize distribution of predictions (if applicable)
        st.subheader("Distribution of Predictions")
        fig, ax = plt.subplots()
        sns.histplot(df['Prediction'], bins=10, kde=True, ax=ax)
        ax.set_title("Distribution of Drowsiness Predictions")
        ax.set_xlabel("Prediction Value")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    else:
        st.warning("No drowsiness events logged yet.")
    

# Apply custom styles
add_custom_styles()

# User Authentication
#checks if there’s already a logged_in key in st.session_state. 
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.subheader("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")#Setting type="password" masks the input, displaying dots or asterisks instead of the actual characters to keep the password hidden
    if st.button("Login"):
        if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username]):#bcrypt encodes the entered password to UTF-8 format and checks it against the stored hashed password (users[username]). 
            st.session_state.logged_in = True  # Set logged in status
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# Main app logic
if not st.session_state.logged_in:
    login()  # Show login if not logged in
else:
    # Title and sidebar setup
    st.title("DROWSINESS DETECTION SYSTEM")
    st.sidebar.image("C:/Users/sande/Desktop/ONLEI/Final_Portfolio_Projects/Drowsiness Detection System/side.jpg")
    choice = st.sidebar.selectbox("My Menu", ("HOME", "IP CAMERA", "CAMERA","dataanalysis"))

    # New feature: Sensitivity threshold slider
    # A lower threshold will detect drowsiness more readily, while a higher threshold will require stronger evidence to detect it.
    #threshold in your detection logic, for example, can be used as the cutoff for classifying a frame as "drowsy."
    threshold = st.sidebar.slider("Drowsiness Sensitivity Threshold", min_value=0.5, max_value=1.0, value=0.9, step=0.05)

    if choice == "HOME":
        st.image("C:/Users/sande/Desktop/ONLEI/Final_Portfolio_Projects/Drowsiness Detection System/Home.png",width=800)
        st.write("This Application is developed by Prasanna")
    elif choice == "IP CAMERA":
        url = st.text_input("Enter IP Camera URL")
        btn = st.button("Start Detection")
        window = st.empty()

        if btn:
            vid = cv2.VideoCapture(url)
            btn2 = st.button("Stop Detection")
            if btn2:
                vid.release()
                st.rerun()

            facemodel = cv2.CascadeClassifier("face.xml")
            maskmodel = load_model("model1.h5", compile=False)
            i = 1

            while True:
                flag, frame = vid.read()
                if flag:
                    faces = facemodel.detectMultiScale(frame)
                    for (x, y, l, w) in faces:
                        face_img = frame[y:y+w, x:x+l]#cropping the image
                        face_img = cv2.resize(face_img, (224, 224), interpolation=cv2.INTER_AREA)#resizing the image
                        face_img = np.asarray(face_img, dtype=np.float32).reshape(1, 224, 224, 3)#reshaping the image after conerting image pixel data to float
                        face_img = (face_img / 127.5) - 1#normalization for visual data(like how we do standardization for numerical data)

                        # Use adjustable threshold for drowsiness detection
                        pred = maskmodel.predict(face_img)[0][1]#here as we paased  drowsy data second,this dimensional list second value is drowsy
                        if pred < threshold:  # Adjustable threshold
                            cv2.rectangle(frame, (x, y), (x + l, y + w), (0, 255, 0), 3)#(b,g,r) full colour-255,no colour-0
                            stop_alert_sound()#stop the alert sound if its already playing
                        else:
                            path = f"data/drowsy_{i}.jpg"#save drowsy images in given location(create data folder in scripts folder )
                            cv2.imwrite(path, frame[y:y+w, x:x+l])#save the cropped images in mentioned path
                            timestamp = log_drowsy_event(path, pred)
                            i += 1
                            cv2.rectangle(frame, (x, y), (x + l, y + w), (0, 0, 255), 3)
                            play_alert_sound()#when drowsiness detected paly alert sound
                            st.write(f"Drowsiness detected at {timestamp}")

                    window.image(frame, channels="BGR")#This is the image or frame captured from the video stream, typically in BGR format since OpenCV reads images in this format.Without specifying channels="BGR", Streamlit would assume the image is in RGB format, leading to incorrect colors in the displayed image.

            # Add button to download the report
            download_report()

    elif choice == "CAMERA":
        cam = st.selectbox("Choose 0 for primary camera and 1 for secondary camera", (0, 1, 2, 3))#if a laptop/desktop has webcam then its the primary camera 
        btn = st.button("Start Detection")
        window = st.empty()

        if btn:
            vid = cv2.VideoCapture(cam)
            btn2 = st.button("Stop Detection")
            if btn2:
                vid.release()
                st.rerun()

            facemodel = cv2.CascadeClassifier("face.xml")
            maskmodel = load_model("model1.h5", compile=False)#we are telling that this model is not bundled,structured,compikled
            i = 1

            while True:
                flag, frame = vid.read()
                if flag:
                    faces = facemodel.detectMultiScale(frame)#[[1,2,3,4],[1,2,3,4]] so the current frame has two faces.if the list has 5 sublists then the current frame has 5 faces
                    for (x, y, l, w) in faces:
                        face_img = frame[y:y+w, x:x+l]#crop the image
                        face_img = cv2.resize(face_img, (224, 224), interpolation=cv2.INTER_AREA)#resize the image
                        face_img = np.asarray(face_img, dtype=np.float32).reshape(1, 224, 224, 3)#reshape the image
                        face_img = (face_img / 127.5) - 1#normalization

                        # Use adjustable threshold for drowsiness detection
                        pred = maskmodel.predict(face_img)[0][1]
                        if pred > threshold:  # Adjustable threshold
                            cv2.rectangle(frame, (x, y), (x + l, y + w), (0, 255, 0), 3)#(x,y)is start of the rectangle while (x + l, y + w) is end of the rectangle
                            stop_alert_sound()
                        else:
                            path = f"data/{i}.jpg"
                            cv2.imwrite(path, frame[y:y+w, x:x+l])
                            timestamp = log_drowsy_event(path, pred)
                            i += 1
                            cv2.rectangle(frame, (x, y), (x + l, y + w), (0, 0, 255), 3)
                            play_alert_sound()
                            st.write(f"Drowsiness detected at {timestamp}")

                    window.image(frame)
    elif choice == "dataanalysis":             
        analyze_data()  # Call the data analysis function
        
