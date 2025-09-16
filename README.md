# Intelligent Cloud-Based Criminal Identification System


🕵️‍♂️ Intelligent Cloud-Based Criminal Identification System

 

📌 Overview

The Intelligent Cloud-Based Criminal Identification System leverages AWS Rekognition, S3, DynamoDB, and Lambda to automatically detect, store, and identify criminals from uploaded images.

With a Tkinter-based GUI, this system provides real-time criminal identification with details like Name, Crime Type, and Wanted Status.

✨ Features

✅ Automatic Face Detection & Indexing using AWS Rekognition
✅ Metadata Storage (Name, Crime Type, Wanted Status) in S3 + DynamoDB
✅ Lambda Automation on image upload
✅ Tkinter GUI for live face matching and visualization
✅ Flash & Fade Effects for real-time results
✅ Scalable & Cloud-Native architecture

🏗️ System Architecture
flowchart TD
    A[Upload Criminal Image] -->|Stored with Metadata| B[S3 Bucket]
    B -->|Trigger Event| C[Lambda Function]
    C -->|Face Detection| D[AWS Rekognition Collection]
    C -->|Store FaceId + Metadata| E[DynamoDB Criminal Records]
    F[Run GUI - Tkinter] -->|Upload Suspect Image| D
    D -->|Face Match Results| F
    F -->|Display Details| G[Identified Criminal Info]

📂 Project Structure
📁 Intelligent-Criminal-ID
│── BulkFacePictureUploadToS3_with_Metadata.py   # Upload images + metadata to S3
│── Lambda_FaceRekognitionCode.py                # Lambda for Rekognition + DynamoDB
│── RunTest_FaceDetect.py                        # GUI for live criminal identification
│── diagram.png                                  # System architecture diagram
│── README.md                                    # Project documentation

⚙️ Workflow

Upload Images

Use BulkFacePictureUploadToS3_with_Metadata.py to upload criminal images with metadata (Name, Crime, Status) to S3.

Face Indexing

AWS Lambda is triggered on upload → Rekognition indexes the face.

Metadata stored in DynamoDB (criminal_records).

Identification

Run RunTest_FaceDetect.py to launch GUI.

Upload a suspect image.

Rekognition matches face from collection.

System displays criminal details with effects.

🖼️ GUI Preview


(Replace with actual screenshot)

🚀 Tech Stack

Cloud: AWS Rekognition, S3, DynamoDB, Lambda

Frontend: Python Tkinter GUI

Backend: Python (Boto3 SDK)

Database: DynamoDB (NoSQL)

▶️ How to Run
🔹 Step 1: Setup AWS Resources

Create S3 bucket (criminal-images-bucket)

Create Rekognition Collection (criminal_collection)

Create DynamoDB table (criminal_records)

Deploy Lambda function (Lambda_FaceRekognitionCode.py)

🔹 Step 2: Upload Criminal Images
python BulkFacePictureUploadToS3_with_Metadata.py

🔹 Step 3: Run GUI for Detection
python RunTest_FaceDetect.py

📊 Example Output
Uploaded 1.jpg with metadata -> Name: John Doe, Crime: Robbery, Status: Wanted
Face indexed successfully: abcd1234 (John Doe)
Match found! FaceId: abcd1234
Confidence: 98.75%
IDENTIFIED CRIMINAL:
Name: John Doe
Crime: Robbery
Wanted Status: Wanted

🌟 Future Enhancements

🔐 Add role-based authentication (Police access only)

📹 Support for CCTV live video feeds

📊 Dashboard with criminal statistics & heatmaps

📡 Multi-cloud support (Azure Face API, GCP Vision AI)
