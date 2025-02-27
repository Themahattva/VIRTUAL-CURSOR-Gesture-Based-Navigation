import cv2
import mediapipe as mp
import pyautogui

# Initialize Webcam
cap = cv2.VideoCapture(0)

# Hand Tracking
hand_detector = mp.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

# Variables for smoother movement
prev_x, prev_y = 0, 0
index_y = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                # Index Finger (Cursor Movement)
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=20, color=(0, 255, 255), thickness=-1)
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                    # Smooth movement
                    index_x = prev_x + (index_x - prev_x) * 0.5
                    index_y = prev_y + (index_y - prev_y) * 0.5
                    pyautogui.moveTo(index_x, index_y)
                    
                    prev_x, prev_y = index_x, index_y

                # Thumb (Click Detection)
                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=20, color=(230, 230, 250), thickness=-1)
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    # Click when thumb and index finger are close
                    if abs(index_y - thumb_y) < 30:
                        pyautogui.click()
                        pyautogui.sleep(0.1)  # Reduce delay for better performance

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
