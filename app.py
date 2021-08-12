from typing import Counter
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server

# create requirements doc: pip freeze > requirements.txt
app = Flask(__name__)

def reasonableNumberOfGrades(num):
    if num < 0 or num > 40:
        return 'Invalid'

def goodInput(userInput):
    for k,v in userInput.items():
        if not v.isnumeric():
            return False
    return True

def reasonableUCHonorsCount(num,grades):
    if num > grades['gradeA_count10']+grades['gradeB_count10']+grades['gradeC_count10']+grades['gradeD_count10']+grades['gradeF_count10']+grades['gradeA_count11']+grades['gradeB_count11']+grades['gradeC_count11']+grades['gradeD_count11']+grades['gradeF_count11']:
        return 'Invalid number of UC Honors courses'
    if num < 0:
        return 'Invalid number of UC Honors courses'

def validateTermCount(count):
    if count <= 0 or count > 4:
        return 'Invalid number of terms'

def getgpa(info,uchonorcount,gradeCounts):
    if uchonorcount > 4*info['termCount']:
        uchonorcount = 4*info['termCount']

    sumPoint = 0
    sumPoint += 4*(info['gradeA_count10']+info['gradeA_count11'])
    sumPoint += 3*(info['gradeB_count10']+info['gradeB_count11'])
    sumPoint += 2*(info['gradeC_count10']+info['gradeC_count11'])
    sumPoint += 1*(info['gradeD_count10']+info['gradeD_count11'])
    sumPoint += uchonorcount
    return sumPoint / gradeCounts
    
def run():
    put_markdown('# ***UC Match: GPA Calculator***')
    put_text('Calculate the various GPAs UCs could potentially view in your applications to assess your chances at admission! Put in grades that are a-g approved. Use this link to see what courses at your high school are a-g and UC Honors approved: https://hs-articulation.ucop.edu/agcourselist')
    info = input_group("User info",[
        input('Enter number of terms per school year', name='termCount', type=NUMBER, validate=validateTermCount),
        input('Enter number of a-g As in the summer before 10th grade, 10th grade, and summer after 10th grade', name='gradeA_count10', type=NUMBER, validate=reasonableNumberOfGrades),
        input('Enter number of a-g Bs in the summer before 10th grade, 10th grade, and summer after 10th grade', name='gradeB_count10', type=NUMBER, validate=reasonableNumberOfGrades),
        input('Enter number of a-g Cs in the summer before 10th grade, 10th grade, and summer after 10th grade', name='gradeC_count10', type=NUMBER, validate=reasonableNumberOfGrades),
        input('Enter number of a-g Ds in the summer before 10th grade, 10th grade, and summer after 10th grade', name='gradeD_count10', type=NUMBER, validate=reasonableNumberOfGrades),
        input('Enter number of a-g Fs in the summer before 10th grade, 10th grade, and summer after 10th grade', name='gradeF_count10', type=NUMBER, validate=reasonableNumberOfGrades),

        input('Enter number of a-g As in 11th grade and summer after 11th grade', name='gradeA_count11', type=NUMBER, validate=reasonableNumberOfGrades),
        input('Enter number of a-g Bs in 11th grade and summer after 11th grade', name='gradeB_count11', type=NUMBER, validate=reasonableNumberOfGrades),
        input('Enter number of a-g Cs in 11th grade and summer after 11th grade', name='gradeC_count11', type=NUMBER, validate=reasonableNumberOfGrades),
        input('Enter number of a-g Ds in 11th grade and summer after 11th grade', name='gradeD_count11', type=NUMBER, validate=reasonableNumberOfGrades),
        input('Enter number of a-g Fs in 11th grade and summer after 11th grade', name='gradeF_count11', type=NUMBER, validate=reasonableNumberOfGrades)
    ])

    clear()
    put_markdown('# ***UC Match: GPA Calculator***')
    uchonorcount = 1000
    while reasonableUCHonorsCount(uchonorcount,info) == 'Invalid number of UC Honors courses':
        uchonorcount = input('Enter number of UC Honors courses taken between the summer of 9th grade and summer of 11th grade inclusively. Only give yourself an extra point if you got a grade of C or higher in the UC Honor class',type=NUMBER)
    
    gradeCounts = 0
    for k,v in info.items():
        if k != 'termCount':
            gradeCounts += v
    ucgpa = getgpa(info,uchonorcount,gradeCounts)
    popup('Your UC GPA: '+str(ucgpa))
    put_text('Reload to try again.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(run, port=args.port)
