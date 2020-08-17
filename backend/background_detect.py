import os
import sys
from keras import backend as K
import shutil
import operator
import cv2
import tempfile

# from ..wsgi import bucket, nude_classifier
from NudeNet.nudenet import NudeClassifier


def main(argv):

    file_name = argv[0]
    path = argv[1]
    name = argv[2]
    path_name = path + name
    # path = 'storage/91dbc50e37edac95729d7bca31bd07/src/src.mp4'
    print(path_name)
    
    K.clear_session()
    
    nude_classifier = NudeClassifier()

    dic_result = nude_classifier.classify_video(path_name)
    # print(dic_result)

    fps = dic_result['metadata']['fps']
    spf = 1 / fps
    print("fps: ", fps, "len: ", dic_result['metadata']['video_length'])
    count = 0
    num_frames = 0

    pred_list = []
    pred_dict = {}

    # print(path, "got result")
    for key, value in dic_result['preds'].items():
        if float(value['unsafe']) > 0.6:
            time = int(key) * spf
            prob = value['unsafe']
            # pred_list.append("time: {} porn: {}".format(str(time), prob))
            pred_dict[int(key)] = float(prob)
            count += 1
        num_frames += 1

    pred = count / num_frames

    pred = "Porn" if pred > 0.7 else "Safe"
    
    if pred == "Porn":
        pred_sdict = sorted(pred_dict.items(), key=lambda x: x[1], reverse=True)[:3]
        
        vidcap = cv2.VideoCapture(path_name)
        detected_frame = pred_sdict[0][0]
        print('frame: ', detected_frame)
        success, image = vidcap.read()
        count = 0
        success = True

        while success:
            success, image = vidcap.read()
            if count == detected_frame:
                cv2.imwrite('/home/ubuntu/Server/DeepBackend/' + path + 'nsfw.jpg', image)
                break
            count += 1
    
    if os.path.isfile(path + 'out.txt'):
        os.remove(path + 'out.txt')

    with open(path + 'out.txt', 'w') as out:
        out.write(pred)

    print(pred)
    

if __name__ == "__main__":
    main(sys.argv)