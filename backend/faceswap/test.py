import os
import sys
def execfile(filename, globals=None, locals=None):
    if globals is None:
        globals = sys._getframe(1).f_globals
    if locals is None:
        locals = sys._getframe(1).f_locals
    # print(globals, locals)
    with open(filename, "r") as fh:
        exec(fh.read()+" asdf "+"\n", globals, locals)

# execute the file
# execfile("./hello.py")
path = "~/Server/DeepBackend/backend/faceswap"
os.system('python faceswap.py extract -i '+ path +'/data/src/src.mp4 -o ' + path + '/data/ext')