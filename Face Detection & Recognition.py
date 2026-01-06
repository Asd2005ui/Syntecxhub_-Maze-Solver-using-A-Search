import cv2
import face_recognition
import pickle
import numpy as np
import os

# Function to register a new face (now uses face_recognition for detection too, for consistency)
def register_face(name, num_samples=10):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam. Check camera permissions or index.")
        return

    encodings = []
    count = 0
    print(f"Capturing {num_samples} samples for {name}. Position your face in the camera. Press 'q' to quit early.")

    while count < num_samples:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame from camera.")
            break

        # Convert to RGB for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces and get encodings using face_recognition (consistent with recognition function)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            encodings.append(face_encoding)
            count += 1
            # Draw bounding box for feedback
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, f"Sample {count}/{num_samples}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            break  # Process one face per frame

        cv2.imshow('Register Face', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if encodings:
        # Load existing data or create new
        if os.path.exists('known_faces.pkl'):
            with open('known_faces.pkl', 'rb') as f:
                known_data = pickle.load(f)
        else:
            known_data = {'encodings': [], 'names': []}

        known_data['encodings'].extend(encodings)
        known_data['names'].extend([name] * len(encodings))

        with open('known_faces.pkl', 'wb') as f:
            pickle.dump(known_data, f)
        print(f"Registered {len(encodings)} encodings for {name}.")
    else:
        print("No faces captured. Ensure your face is visible, well-lit, and centered in the camera.")

# Function for real-time face recognition (unchanged, but now consistent)
def recognize_faces():
    # Load known faces
    try:
        with open('known_faces.pkl', 'rb') as f:
            known_data = pickle.load(f)
        known_encodings = known_data['encodings']
        known_names = known_data['names']
    except FileNotFoundError:
        print("No known faces found. Run registration first.")
        return

    # Start webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to RGB for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces and get encodings
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Process each face
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare to known faces
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"

            # Find best match
            if known_encodings:  # Avoid error if no known faces
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

            # Draw bounding box and label
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Main menu (unchanged)
if __name__ == "__main__":
    while True:
        print("\nFace Detection & Recognition System")
        print("1. Register a new face")
        print("2. Start face recognition")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")

        if choice == '1':
            name = input("Enter name to register: ")
            register_face(name)
        elif choice == '2':
            recognize_faces()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Try again.")