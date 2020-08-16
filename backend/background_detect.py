import os
import sys
from keras import backend as K
import shutil

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
    print(dic_result)

    count = 0
    num_frames = 0
    # print(path, "got result")
    for key, value in dic_result['preds'].items():
        if float(value['unsafe']) > 0.6:
            count += 1
        num_frames += 1
        # print(count)

    pred = count / num_frames

    pred = "Porn" if pred > 0.5 else "Safe"
    
    print(pred)
    
    if os.path.isfile('backend/out.txt'):
        os.remove('backend/out.txt')

    with open('backend/out.txt', 'w') as out:
        out.write(pred)
    

if __name__ == "__main__":
    main(sys.argv)