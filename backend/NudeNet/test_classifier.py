import os
import cv2
from nudenet import NudeClassifier, NudeDetector

video_path = 'porn.mp4'

classifier = NudeClassifier()
dic = classifier.classify_video(video_path, batch_size=4)
# dic = classifier.classify('example.jpg')


# detector = NudeDetector()
# dic = detector.detect('example.jpg')



print(dic)


video = cv2.VideoCapture(video_path)
print(video.isOpened())
fps = video.get(cv2.CAP_PROP_FPS)
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
print("fps:", fps, "length", length)

# print(os.getcwd())