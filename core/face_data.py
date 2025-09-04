import cv2
from deepface import DeepFace
import numpy as np
import os
import time
import dlib
from scipy.spatial import distance as dist

class FaceData:
    def __init__(self):
        print("[DEBUG] Initializing FaceData...")
        print("[INFO] Initializing facial recognition system...")
        dummy_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        try:
            DeepFace.represent(img_path=dummy_frame, model_name='VGG-Face', enforce_detection=False)
            print("[INFO] Facial recognition system initialized.")
        except Exception as e:
            print(f"[ERROR] Failed to initialize facial recognition system: {e}")

        # Initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        print("[INFO] loading facial landmark predictor...")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("D:\\tmp\\prototype1_v2\\prototype1_v2\\model\\shape_predictor_68_face_landmarks.dat")

        # Grab the indexes of the facial landmarks for the left and
        # right eye, respectively
        (self.lStart, self.lEnd) = (42, 48)
        (self.rStart, self.rEnd) = (36, 42)

        # Define constants for eye aspect ratio
        self.EYE_AR_THRESH = 0.25
        self.EYE_AR_CONSEC_FRAMES = 3
        self.BLINK_COUNT_REQUIRED = 2

        # Initialize blink counter and total blinks
        self.COUNTER = 0
        self.TOTAL_BLINKS = 0

    def _eye_aspect_ratio(self, eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear

    def capture_multiple_faces(self, num_images=5, require_liveness=True):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            print("[ERROR] Could not open video stream.")
            return []

        print(f"[INFO] Capturing {num_images} facial images...")
        captured_frames = []
        
        # Reset blink counters for each capture session
        self.TOTAL_BLINKS = 0
        self.COUNTER = 0
        blink_liveness_met = False # Flag to track if blink liveness is met for the session

        while len(captured_frames) < num_images:
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = self.detector(gray, 0)

            face_detected = False

            if len(rects) > 0:
                face_detected = True
                for rect in rects:
                    shape = self.predictor(gray, rect)
                    shape = np.array([(shape.part(i).x, shape.part(i).y) for i in range(68)])

                    leftEye = shape[self.lStart:self.lEnd]
                    rightEye = shape[self.rStart:self.rEnd]
                    leftEAR = self._eye_aspect_ratio(leftEye)
                    rightEAR = self._eye_aspect_ratio(rightEye)

                    ear = (leftEAR + rightEAR) / 2.0

                    if require_liveness:
                        if not blink_liveness_met: # Only check for blinks if liveness not yet met
                            if ear < self.EYE_AR_THRESH:
                                self.COUNTER += 1
                            else:
                                if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                                    self.TOTAL_BLINKS += 1
                                    print(f"[DEBUG] Blink detected! Total blinks: {self.TOTAL_BLINKS}")
                                self.COUNTER = 0

                            if self.TOTAL_BLINKS >= self.BLINK_COUNT_REQUIRED:
                                blink_liveness_met = True
                                cv2.putText(frame, "Liveness: PASSED", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            else:
                                cv2.putText(frame, f"Please blink {self.BLINK_COUNT_REQUIRED - self.TOTAL_BLINKS} more times.", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        else: # Liveness already met
                            cv2.putText(frame, "Liveness: PASSED", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        # If liveness is met (either now or previously), capture the frame
                        if blink_liveness_met:
                            captured_frames.append(frame)
                            print(f"[INFO] Captured image {len(captured_frames)}/{num_images}")
                            cv2.imshow("Capturing...", frame)
                            cv2.waitKey(1000) # Pause after capture
                    else: # No liveness required
                        captured_frames.append(frame)
                        print(f"[INFO] Captured image {len(captured_frames)}/{num_images}")
                        cv2.imshow("Capturing...", frame)
                        cv2.waitKey(1000)

                    cv2.putText(frame, f"EAR: {ear:.2f}", (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(frame, f"COUNTER: {self.COUNTER}", (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(frame, f"Blinks: {self.TOTAL_BLINKS}", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            if not face_detected:
                cv2.putText(frame, "No Face Detected", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.imshow("Face Capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        if len(captured_frames) < num_images:
            return []
        return captured_frames

