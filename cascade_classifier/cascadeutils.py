import os

#to use standalone:
#Open terminal, cd to cascade_classifier directory, type:
#python
#from cascadeutils import generate_negative_description_file
#generate_negative_description_file()

#path for opencv:
#C:\Users\ZelPC\opencv\build\x64\vc15\bin

#first we run opencv_annotation
#C:\Users\ZelPC\opencv\build\x64\vc15\bin\opencv_annotation.exe --annotations=cascade_classifier\pos.txt --images=cascade_classifier\positive\
#create boxes around positive objects, 'c' to confirm. 'd' to undo prev confirm 'n' to move to next img
# esc to exit

#step2: create vector file
#cd into cascade_classifier folder
#C:\Users\ZelPC\opencv\build\x64\vc15\bin\opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec

#Step3: train model:
#C:\Users\ZelPC\opencv\build\x64\vc15\bin\opencv_traincascade.exe -data cascade\ -vec pos.vec -bg neg.txt -w 24 -h 24 -precalcValBufSize 6000 -precalcIdxBuffSize 6000 -numPos 40 -numNeg 1000 -numStages 12 -maxFalseAlarmRate 0.4 -minHitRate 0.999

#C:\Users\ZelPC\opencv\build\x64\vc15\bin\opencv_traincascade.exe -data cascade\ -vec pos.vec -bg neg.txt -w 24 -h 24 -precalcValBufSize 8000 -precalcIdxBuffSize 8000 -numPos 700 -numNeg 1400 -numStages 12 -maxFalseAlarmRate 0.3 -minHitRate 0.995
def generate_negative_description_file():
    #open the output file for writing: Will overwrite all existing data in there
    with open('neg.txt', 'w') as f:
        #loop over all filenames
        for filename in os.listdir('negative'):
            f.write('negative/' + filename + '\n')

#340 pos images dataset [786 samples]
#239 Neg images dataset