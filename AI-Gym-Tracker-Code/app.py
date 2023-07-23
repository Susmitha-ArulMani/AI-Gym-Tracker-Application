
from flask import *
import cv2
import mediapipe as mp
import numpy as np
import pygame
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget


app = Flask(__name__)

counter = 0
stage = None
set_count = 0

@app.route('/')
def home():
      return render_template('index.html')


@app.route('/gym_tracker')
def gym_tracker():
    return render_template('gym_tracker.html')
      
@app.route('/start_exercise', methods=['POST'])
def start_exercise():
    exercise_type = request.form['exercise_type']
    target_count = int(request.form['target_count'])
    threshold_angle = 160
    global counter, stage, set_count
    counter = 0 
    stage = None
    set_count = 0
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    pygame.mixer.init()
    alarm_sound = pygame.mixer.Sound('audio/alarm.wav')

    def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
    
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
    
        if angle >180.0:
            angle = 360-angle
        
        return angle 

    cap = cv2.VideoCapture(0)
   

    frame_width = 800
    frame_height = 600
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    # counter = 0 
    # stage = None
    # set_count = 0

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
      
            # Make detection
            results = pose.process(image)
    
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                if exercise_type == "bicep":
                # Get coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
                    # Calculate angle
                    angle = calculate_angle(shoulder, elbow, wrist)
            
                    # Visualize angle
                    cv2.putText(image, str(angle), 
                                tuple(np.multiply(elbow, [800, 600]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    
                    # Curl counter logic
                    if angle > 160:
                        stage = "down"
                    if angle < 30 and stage =='down':
                        stage="up"
                        counter +=1
                        print(counter)

                        if counter == target_count:
                            set_count += 1
                            pygame.mixer.Sound.play(alarm_sound)

                            counter = 0
                            # stage = None

                elif exercise_type == "squat":
                    hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                    # Calculate angle
                    angle = calculate_angle(hip, knee, ankle)
            
                    # Visualize angle
                    cv2.putText(image, str(angle), 
                                tuple(np.multiply(knee, [500, 600]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    
                    # Curl counter logic
                    if angle > 120:
                        stage = "up"
                    if angle < 90 and stage =='up':
                        stage="down"
                        counter +=1
                        print(counter)

                        if counter == target_count:
                            set_count += 1
                            pygame.mixer.Sound.play(alarm_sound)
                            counter = 0
                            
                            # stage = None

                elif exercise_type == "pushup":
                    shoulders = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbows = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrists = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    angle = calculate_angle(shoulders, elbows, wrists)
            
                    # Visualize angle
                    cv2.putText(image, str(angle), 
                                tuple(np.multiply(elbows, [800, 600]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                    
                    if angle > 160:
                        stage = "up"
                    if angle < 30 and stage =='up':
                        stage="down"
                        counter +=1
                        print(counter)

                        if counter == target_count:
                            set_count += 1
                            pygame.mixer.Sound.play(alarm_sound)
                            counter = 0
                            # stage = None

                elif exercise_type == "shoulder Press":
                    sshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    selbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    swrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    angle = calculate_angle(sshoulder, selbow, swrist)
            
                    # Visualize angle
                    cv2.putText(image, str(angle), 
                                tuple(np.multiply(selbow, [800, 600]).astype(int)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
            
                    if angle > 160:
                        stage = "up"
                    if angle < 30 and stage =='up':
                        stage="down"
                        counter +=1
                        print(counter)

                        if counter == target_count:
                            set_count += 1
                            pygame.mixer.Sound.play(alarm_sound)
                            counter = 0
                            # stage = None
                       
            except:
                pass
        
        
            cv2.putText(image, f'Exercise:{exercise_type}', (10,30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (137,17,17), 2, cv2.LINE_AA)
            cv2.putText(image, f'Set:{set_count}/{target_count}', (10,70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (137,17,17), 2, cv2.LINE_AA)
            cv2.putText(image, f'Reps:{counter}', (10,110), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (137,17,17), 2, cv2.LINE_AA)
            cv2.putText(image, f'Stage:{stage}', (10,150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (137,17,17), 2, cv2.LINE_AA)
            cv2.putText(image, 'Click q to quit this window', (200,580), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
        
        
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
        
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    
        cap.release()
        cv2.destroyAllWindows()
        return render_template('gym_tracker.html')    
      
@app.route('/nutrition_suggestion')
def nutrition_suggestion():
    return render_template('nutrition_suggestion.html')

@app.route('/calculate', methods=['GET','POST'])
def calculate_bmi():
    bmi=None
    result = None
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        
        bmi = weight / (height/100)**2
        
        if bmi < 18.5:
            result = "Underweight"
        elif bmi >= 18.5 and bmi < 24.9:
            result = "Normal weight"
        elif bmi >= 25.0 and bmi < 30.0:
            result = "Overweight"
        else:
            result = "Obese"
        
        # return render_template('result.html', bmi=bmi, result=result)
    
    return render_template('nutrition_suggestion.html',bmi=bmi,result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

