import tensorflow as tf
import random
import time
import numpy as np

import led 
import camera


# model = tf.keras.models.load_model('whack_a_mole_model.h5')
model = tf.keras.models.load_model('finetunedmodelnew2.h5')
class_labels = ['00-wack', '01-wack', '02-wack', '10-wack', '11-wack', '12-wack', 'nowack']

led_control = led.led()
camera_control = camera.camera()



def make_prediction(img_array):
    prediction = model.predict(img_array, verbose=0).flatten()
    predicted_index = np.argmax(prediction)
    predicted_label = class_labels[predicted_index]
    confidence = prediction[predicted_index] * 100

    print(f"Predicted class: {predicted_label}")
    print(f"Model is {confidence:.2f}% sure about this prediction.")

    return predicted_label, confidence

    

def capture_player_movement():
    start_time = time.time()
    frames = []
    frame_count = 0  

    while time.time() - start_time < 0.8:
        frame = camera_control.capture_frame()
        if frame is not None:
            frame_count += 1  

            if frame_count > 15:
                frames.append(frame)

    return frames



def check_whack(predicted_label, confidence, random_led, whack_count):
    required_confidence = 60
    no_whack_weight = 0.5


    if confidence < required_confidence:
        return whack_count

    if predicted_label == class_labels[random_led]:
        whack_count += 1

    elif predicted_label == 'nowack':
        whack_count -= no_whack_weight

    return whack_count     



def game_loop():

    score = 0
    max_rounds = 5  
    round_count = 0

    try:
        while round_count < max_rounds:
            random_led = random.randint(0, len(class_labels) - 2)
            led_control.turn_on_random_led(random_led)
            time.sleep(0.3)

            frames = capture_player_movement()
            led_control.turn_off_random_led(random_led)

            whack_count = 0

            print("capturing frames...")
            print(f"random led is: {random_led}")
            print(f"Mole is on {class_labels[random_led]}")
            print(f"amount of frames is {len(frames)}")

            for frame in frames:
                img_array = camera_control.process_frame(frame)
                predicted_label, confidence = make_prediction(img_array)
                whack_count = check_whack(predicted_label, confidence, random_led, whack_count)

            if whack_count > 0:
                score += 1
                print("Correct whack!\n\n")

            else:
                print("Miss!\n\n")

            round_count += 1  
            print(f"score is: {score}, round count is {round_count}")  

    except KeyboardInterrupt:
        print("Game interrupted. Exiting...")
        print(f"score is: {score}, round count is {round_count}")
        led_control.turn_off_led()

            

print("starting the game")
game_loop()