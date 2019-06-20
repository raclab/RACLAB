import cv2
import imutils
import time
import numpy as np

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
gender_list = ['Erkek', 'Kadin']


def initialize_caffe_models():
    age_net = cv2.dnn.readNetFromCaffe(
        'data/deploy_age.prototxt',
        'data/age_net.caffemodel')

    gender_net = cv2.dnn.readNetFromCaffe(
        'data/deploy_gender.prototxt',
        'data/gender_net.caffemodel')

    return (age_net, gender_net)

face_Cascade = (r'C:\Users\Sony\PycharmProjects\untitled6\haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier(face_Cascade)


img = cv2.imread ('Semih.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(gray,1.1,5)

def read_from_camera(age_net, gender_net):
    font = cv2.FONT_HERSHEY_SIMPLEX

    if (len(faces) > 0):
        print("Found {} faces".format(str(len(faces))))

    for(x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w , y + h), (255, 255, 0), 2)

            face_img = img[y:y + h, h:h + w].copy()
            blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

            # Predict Gender
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = gender_list[gender_preds[0].argmax()]
            print("Gender : " + gender)

            # Predict Age
            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = age_list[age_preds[0].argmax()]
            print("Age Range: " + age)

            overlay_text = "%s %s" % (gender, age)
            cv2.putText(img, overlay_text, (x, y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('faces',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    age_net, gender_net = initialize_caffe_models()

    read_from_camera(age_net, gender_net)