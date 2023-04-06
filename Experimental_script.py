from experiment import Experiment
from psychopy import visual, core, event, gui, event
from collections import defaultdict
from pandas import DataFrame
import glob, os
import numpy as np
import random, string
import prep, ltpFR2, pickle
import config
import serial

#serial port settings - Begin Experiment tab in a code component
# s_port = serial.Serial('COM3', baudrate=115200)         #serial port name
# s_port.port = 'COM3'             # chosen serial port
# s_port.timeout = 1               # timeout 1 second (give 1 second to the board to initialize port)
# s_port.close()
# s_port.open()                    #open serial port to start routine
# s_port.write(1)

###### Event trigger codes ######
#0 - Distractor word presentation
#1- Target word presentation
#2- Target button press
#3- Start of presentation block
#4- Start of the math period
#5- Start of the recall period
#6- recalled word
#7- Practice Distractor Word Presentation
#8- Practice Target Word Presentation
#global variables presented here

colorRed = 'red'
colorGrn = 'green'

def make_wordlists(SubNum):
    #Create directory for subject
    #os.mkdir('Subject_Word_Lists/Subject_'+str(SubNum))
    #Generate word lists
    config.listLength = config.listLength + 2
    (wp, subjItems, pairDicts, semMat) = prep.subjWordOrder(config)
    pairDicts = ltpFR2.fixPairDicts(pairDicts, wp, semMat)
    config.listLength = config.listLength - 4
    #shorten wordlists to 18 items
    wordlists = subjItems[0]
    for i in list(range(0, len(wordlists))):
            wordlists[i] = wordlists[i][0:16]

    targnum = [[]]*config.nLists
    for i in np.multiply(list(range(0, (int(config.nLists / 4)))), 4):
        a = [1]
        ab = [1,0]
        aab = [1,0,0]
        dd = [1,2,3, 1,2,3, 1,3];
        random.shuffle(dd)
        for j in list(range(0, len(dd))):
            if dd[j] == 1:
                targnum[i] = targnum[i] + a
            elif dd[j] == 2:
                targnum[i] = targnum[i] + ab
            elif dd[j] == 3:
                targnum[i] = targnum[i] + aab

        targnum[i+1] = targnum[i][::-1]
        targnum[i+2] = np.add(targnum[i], 1)
        targnum[i+2][targnum[i+2] == 2] = 0
        targnum[i+3] = np.add(targnum[i+1], 1)
        targnum[i+3][targnum[i+3] == 2] = 0


    return wordlists, targnum


def gen_square(win, color):
    '''
    gen_square(win, color) - generates a psychopy visual 10x10 square of the
    specified color
        Inputs: [win] is the active window. [color] is an RGB list.
        Returns: A psychopy visual stim rectangle
    '''


    sq1 = visual.Rect(win=win, units="deg", width=(2, 2)[0],
        height=(1.5, 1.5)[1], ori=0, pos=(0, 3), lineWidth=1, lineColor=color,
        fillColor=color, opacity=1, depth=-1.0, interpolate=True)
    sq2 = visual.Rect(win=win, units="deg", width=(2, 2)[0],
        height=(1.5, 1.5)[1], ori=0, pos=(0, -3), lineWidth=1, lineColor=color,
        fillColor=color, opacity=1, depth=-1.0, interpolate=True)
    return sq1, sq2

def math_distractor(exp, math_sofar):
    '''
    Conduct math distractor task for 30s following list presentation
    '''

    math_data = []
    math_correct = 0
    stim_timer = core.Clock()

    # exp.win.callOnFlip(s_port.write, str.encode('4'))  #code start of math block
    time = 30
    Timer = core.CountdownTimer(time)
    while stim_timer.getTime() <= time:
        keys = event.getKeys()
        if 'escape' in keys:
            core.quit()
        Int1 = random.randrange(-2, 3)
        Int2 = random.randrange(1, 3)
        Int3 = random.randrange(1, 3)
        text = visual.TextStim(win=exp.win, name='text',
            text= str(Int1)+" + "+str(Int2)+" + "+str(Int3)+" = ?\
            \n\
            \n\
            \nTime Left: "+str(int(Timer.getTime()))+"s",
            font='Arial',
            pos=(0, 0), height=2, wrapWidth=None, ori=0,
            color='black', colorSpace='rgb', opacity=1,
            languageStyle='LTR',
            depth=0.0);
        text.draw()
        exp.win.flip()

        while not event.getKeys() and Timer.getTime() >= 0:
                text = visual.TextStim(win=exp.win, name='text',
                    text= str(Int1)+" + "+str(Int2)+" + "+str(Int3)+" = ?\
                    \n\
                    \n\
                    \nTime Left: "+str(int(Timer.getTime()))+"s",
                    font='Arial',
                    pos=(0, 0), height=2, wrapWidth=None, ori=0,
                    color='black', colorSpace='rgb', opacity=1,
                    languageStyle='LTR',
                    depth=0.0);
                text.draw()
                exp.win.flip()

        if Timer.getTime() <= 0:
            exp.win.flip
            break

        resp_key = event.waitKeys(keyList = ['0', '1','2','3','4','5','6','7', '8', '9'], timeStamped=stim_timer)
        resp_time = stim_timer.getTime()


        if int(resp_key[0][0]) == Int1 + Int2 + Int3:
            math_correct = math_correct + 1
            while resp_time <= stim_timer.getTime() < resp_time + .500:
                text = visual.TextStim(win=exp.win, name='text',
                text='+',
                font='Arial',
                pos=(0, 0), height=5, wrapWidth=None, ori=0,
                color='green', colorSpace='rgb', opacity=1,
                languageStyle='LTR',
                depth=0.0);
                text.draw()
                exp.win.flip()
        else:
            while resp_time <= stim_timer.getTime() < resp_time + .500:
                text = visual.TextStim(win=exp.win, name='text',
                text='x',
                font='Arial',
                pos=(0, 0), height=4, wrapWidth=None, ori=0,
                color='red', colorSpace='rgb', opacity=1,
                languageStyle='LTR',
                depth=0.0);
                text.draw()
                exp.win.flip()

        math_data.append([math_correct])
        exp.data_write(math_data, './Data/', 'Math_task')
        #exp.win.flip()

    return (math_correct+math_sofar)

def free_recall(exp, block, wordlist, targcycle):
    '''
    Conduct math distractor task for 30s following list presentation
    '''

    allLetters = list(string.ascii_lowercase)
    stim_timer = core.Clock()
    textFill = ''
    recall_resp = []
    time = 75
    Timer = core.CountdownTimer(time)
    # exp.win.callOnFlip(s_port.write, str.encode('5')) #code start of recall block
    exp.text_box.text = "\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \nPlease type in as many words from the\
        \nprevious list as you can remember.\
        \nPress 'return' after entering each word.\
        \n\
        \nTime Left: "+str(int(Timer.getTime()))+"s"
    exp.text_box.draw()
    exp.win.flip()

    while stim_timer.getTime() <= 75.0:
        keys = event.getKeys()
        if 'escape' in keys:
            if block == -1:
                exp.data_write(recall_resp, './Data/', 'Practice_recall')
            else:
                exp.data_write(recall_resp, './Data/', 'free_recall_list_'+str(block+1))
            core.quit()  # So you can quit
        elif keys:
            if keys[0] == 'space':
                textFill += ' '  # Adds a space instead of 'space'
            elif keys[0] == 'backspace':
                textFill = textFill[:-1]  # Deletes
            elif keys[0] in allLetters:
                textFill+=keys[0]  # Adds character to text if in alphabet.
            if 'return' in keys:
                # exp.win.callOnFlip(s_port.write, str.encode('6')) #record word recall
                if textFill.upper() in wordlist: #check if correct recall
                    correct_recall = 1
                    serial_pos = wordlist.index(textFill.upper()) + 1
                    if targcycle[wordlist.index(textFill.upper())] == 1: #check if target or distractor recall
                        targ_word = 1
                    else:
                        targ_word = 0
                else:
                    correct_recall = 0
                    targ_word = -1
                    serial_pos = -1

                recall_resp.append((block+1, textFill.upper(), stim_timer.getTime(), correct_recall, serial_pos, targ_word))
                textFill = ''
            exp.text_box.text = "\
                \n\
                \n\
                \n\
                \n\
                \n\
                \n\
                \nPlease type in as many words from the\
                \nprevious list as you can remember.\
                \nPress 'return' after entering each word.\
                \n\
                \nTime Left: "+str(int(Timer.getTime()))+"s"
            text = visual.TextStim(win=exp.win, name='text',
                text= str(textFill.upper()),
                font='Arial',
                pos=(0, 0), height=2.5, wrapWidth=None, ori=0,
                color='black', colorSpace='rgb', opacity=1,
                languageStyle='LTR',
                depth=0.0);
            exp.text_box.draw()
            text.draw()
            exp.win.flip()  # Set new text on screen

            if Timer.getTime() <= 0:
                exp.win.flip
                break
        else:
            exp.text_box.text = "\
                \n\
                \n\
                \n\
                \n\
                \n\
                \n\
                \nPlease type in as many words from the\
                \nprevious list as you can remember.\
                \nPress 'return' after entering each word.\
                \n\
                \nTime Left: "+str(int(Timer.getTime()))+"s"
            text = visual.TextStim(win=exp.win, name='text',
                text= str(textFill.upper()),
                font='Arial',
                pos=(0, 0), height=2.5, wrapWidth=None, ori=0,
                color='black', colorSpace='rgb', opacity=1,
                languageStyle='LTR',
                depth=0.0);
            exp.text_box.draw()
            text.draw()
            exp.win.flip()  # Set new text on screen

    if block == -1:
        exp.data_write(recall_resp, './Data/', 'Practice_recall')
    else:
        exp.data_write(recall_resp, './Data/', 'free_recall_list_'+str(block+1))


def practice_task(exp, red_target, ISI):
    '''
    practice_task(exp, red_target) - Runs
    the practice encoding and detection task, math distractor task, and free recall and saves the data
    Inputs: [exp] is an Experiment class. [red_target] is a boolean value indicating whether or
    not red is the target color.
    '''

    wordlist = ['HAPPY', 'COLD','HEAVY', 'FUNNY', 'SCARY', 'PEACEFUL',
    'TIRED', 'ENTERTAINING', 'GRATEFUL', 'LOUD', 'SMART', 'SMOOTH', 'DISHONEST', 'WEALTHY', 'DREARY', 'PLAYFUL']

    targcycle = [0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0 ,1, 1]
    exp.text_box.text = "\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \nWe will begin with a brief\
        \npractice session.\
        \nYou will see a list of words\
        \nand colored squares in the following task.\
        \n\
        \nPress the spacebar whenever you see\
        \na " + ("RED" if red_target else "GREEN") + " square. \
        \n\
        \n\
        \nPress the spacebar to continue."
    exp.text_box.draw()
    exp.win.flip()
    event.waitKeys(keyList = ["space"])

    exp.text_box.text = "\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \nPlease try to remember as many of the words\
        \nas you can, and try to think about the meaning\
        \nof each word as it appears.\
        \n\
        \nAfter the detection and encoding task you\
        \nwill be asked to briefly solve some\
        \nmath problems. Please solve as many\
        \nproblems as you can in the time given.\
        \n\
        \nPress the spacebar to continue."
    exp.text_box.draw()
    exp.win.flip()
    event.waitKeys(keyList = ["space"])

    exp.text_box.text = "\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \nAfter solving the math problems,\
        \nyou will be asked to type in as many words\
        \nfrom the previous list as you can remember for 75 seconds.\
        \n\
        \nIf you finish recalling before the 75 seconds are up,\
        \njust sit tight and try to think of\
        \nany more words you could have missed.\
        \n\
        \nWe will begin with a brief practice session.\
        \n\
        \nPress the spacebar to continue."
    exp.text_box.draw()
    exp.win.flip()
    event.waitKeys(keyList = ["space"])

    [redSq1, redSq2] = gen_square(exp.win, colorRed) #generates a red square
    [greenSq1, greenSq2] = gen_square(exp.win, colorGrn) #generates a green square

    detection_data = []

    clock = core.Clock()

    fixation_timer = core.Clock()
    while fixation_timer.getTime() <= 2:
        text = visual.TextStim(win=exp.win, name='text',
            text="+",
            font='Arial',
            pos=(0, 0), height=2.5, wrapWidth=None, ori=0,
            color='black', colorSpace='rgb', opacity=1,
            languageStyle='LTR',
            depth=0.0);
        text.draw()
        exp.win.flip()
    #loop runs through each image in shuffled_images argument for procedure
    targets_responded = 0
    non_targets_responded = 0
    #response_times used to calculate median response time
    response_times = []
    math_correct = 0
    for index in list(range(16)):
        #text on screen
        text = visual.TextStim(win=exp.win, name='text',
            text=str(wordlist[index]),
            font='Arial',
            pos=(0, 0), height=2.5, wrapWidth=None, ori=0,
            color='black', colorSpace='rgb', opacity=1,
            languageStyle='LTR',
            depth=0.0);

        reaction_times = [] #times when user reacted to the stim

        text.draw()
        exp.win.flip() #immediately presents stim and records time

        # if targcycle[index] == 1:
        #     exp.win.callOnFlip(s_port.write, str.encode('7'))# where '1' is the start value
        # else:
        #     exp.win.callOnFlip(s_port.write,  str.encode('8'))# where '0' is the start value


        stim_presentation = clock.getTime()
        stim_exit = 0.0
        space_pressed = False
        ISI = random.choice(list(range(1250, 1750)))/1000
        stim_timer = core.Clock()
        while stim_timer.getTime() <= ISI:
            key = exp.get_keypress()
            if key == 'escape':
                exp.data_write(detection_data, './Data/', 'Encoding')
                # s_port.close()
                exp.shutdown()

            elif key == 'space':
                reaction_times.append(stim_timer.getTime())
                # exp.win.callOnFlip(s_port.write, str.encode('2'))# record buttonpress
                if (not space_pressed) and targcycle[index] == 1:
                    space_pressed = True
                    targets_responded += 1
                    response_times.append(stim_timer.getTime())
                elif (not space_pressed) and not targcycle[index] == 1:
                    space_pressed = True
                    non_targets_responded += 1
                    response_times.append(stim_timer.getTime())


            if 0.0 <= stim_timer.getTime() < 0.100:
                text.draw()
                if((targcycle[index] == 1 and red_target) or
                    (not targcycle[index] == 1 and not red_target)):
                    redSq1.draw()
                    redSq2.draw()
                else:
                    greenSq1.draw()
                    greenSq2.draw()
                exp.win.flip()
            elif 0.10 <= stim_timer.getTime() < 0.5:
                text.draw()
                exp.win.flip()
            elif 0.5 <= stim_timer.getTime() < ISI:
                exp.win.flip()
                stim_exit = clock.getTime()

        #attach results of experiment to dataset
        detection_data.append(
            [
                exp.subject_data['subject_num'],
                len(detection_data)+1,
                wordlist[index],
                targcycle[index],
                red_target,
                stim_presentation,
                stim_exit
            ])
        detection_data[len(detection_data)-1].extend(reaction_times)
        exp.data_write(detection_data, './Data/', 'Encoding')

    math_correct = 0
    math_correct = math_distractor(exp, math_correct)
    free_recall(exp, -1,  wordlist, targcycle)
    math_correct = int(math_correct)
    exp.text_box.text = "\n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \nPractice Block complete. Here are your results:\
        \n\
        \nMath problems solved: "+str(math_correct)+" \
        \nPercentage of targets you responded to: "+str(int(targets_responded)/(.5*(config.listLength+2))*100.0)+"\
        \nPercentage of NON-targets you responded to: "+str(int(non_targets_responded)/(.5*(config.listLength+2))*100.0)+"\
        \n\
        \nThe experiment will start now.\
        \nPress the spacebar to continue."

    exp.text_box.draw()
    exp.win.flip()
    event.waitKeys(keyList = ["space"])

    exp.data_write(detection_data, './Data/', 'Practice_detection')

def run_experiment(exp, wordlist, targcycle, red_target):
    '''
    run_experiment(exp, wordlist, targcycle, red_target) - Runs
    the encoding and detection task, math distractor task, and free recalland saves the data
    Inputs: [exp] is an Experiment class. [stim_images] is a pandas
    dataframe with columns indicating image name, target, and race of
    individual's face. [red_target] is a boolean value indicating whether or
    not red is the target color.
    Requires:
    '''

    exp.text_box.text = "\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        \nWe will now begin the experiment!\
        \n\
        \nPlease try to remember all words from each list.\
        \nPress the spacebar whenever you see a " + ("red" if red_target
        else "green") + " square.\
        \n\
        \nPress the spacebar to continue."

    exp.text_box.draw()
    exp.win.flip()
    event.waitKeys(keyList = ["space"])

    [redSq1, redSq2] = gen_square(exp.win, colorRed) #generates a red square
    [greenSq1, greenSq2] = gen_square(exp.win, colorGrn) #generates a green square

    detection_data = []

    exp.text_box.text = "\
            \n\
            \n\
            \n\
            \nBlock 1 will start now.\
            \nPress the spacebar to continue."
    exp.text_box.draw()
    exp.win.flip()
    event.waitKeys(keyList = ["space"])

    clock = core.Clock()
    math_correct = 0

    for i in range(config.nLists):

        #Add fixation at start of list
        fixation_timer = core.Clock()
        # exp.win.callOnFlip(s_port.write,  str.encode('3'))# coding start of block
        while fixation_timer.getTime() <= 2:
            text = visual.TextStim(win=exp.win, name='text',
                text="+",
                font='Arial',
                pos=(0, 0), height=2.5, wrapWidth=None, ori=0,
                color='black', colorSpace='rgb', opacity=1,
                languageStyle='LTR',
                depth=0.0);
            text.draw()
            exp.win.flip()

        #loop runs through each image in shuffled_images argument for procedure
        targets_responded = 0
        non_targets_responded = 0
        #response_times used to calculate median response time
        response_times = []
        for index in list(range(config.listLength)):
            #creates image and scramble for procedure
            text = visual.TextStim(win=exp.win, name='text',
                text=str(wordlist[i][index]),
                font='Arial',
                pos=(0, 0), height=2.5, wrapWidth=None, ori=0,
                color='black', colorSpace='rgb', opacity=1,
                languageStyle='LTR',
                depth=0.0);

            RT = float('NaN')#times when user reacted to the stim

            text.draw()
            exp.win.flip() #immediately presents stim and records time

            # if targcycle[i][index] == 1:
            #     exp.win.callOnFlip(s_port.write, str.encode('1'))# where '1' is the start value
            # else:
            #     exp.win.callOnFlip(s_port.write,  str.encode('0'))# where '0' is the start value

            stim_presentation = clock.getTime()
            stim_exit = 0.0
            space_pressed = False

            stim_timer = core.Clock()
            ISI = random.choice(list(range(1250, 1750)))/1000
            while stim_timer.getTime() <= ISI:
                key = exp.get_keypress()
                if key == 'escape':
                    exp.data_write(detection_data, './Data/', 'Encoding')
                    # s_port.close()
                    exp.shutdown()

                elif key == 'space':
                    RT = stim_timer.getTime()
                    # exp.win.callOnFlip(s_port.write,  str.encode('2'))# where '0' is the start value
                    #Check to make sure this is the first time  the spacebar
                    #has been pressed and depending on whether the image
                    #is a target or not, add up the appropriate statistic
                    if (not space_pressed) and targcycle[i][index] == 1:
                        space_pressed = True
                        targets_responded += 1
                        response_times.append(stim_timer.getTime())
                    elif (not space_pressed) and not targcycle[i][index] == 1:
                        space_pressed = True
                        non_targets_responded += 1
                        response_times.append(stim_timer.getTime())


                if 0.0 <= stim_timer.getTime() < 0.100:
                    text.draw()
                    if((targcycle[i][index] == 1 and red_target) or
                        (not targcycle[i][index] == 1 and not red_target)):
                        redSq1.draw()
                        redSq2.draw()
                    else:
                        greenSq1.draw()
                        greenSq2.draw()
                    exp.win.flip()
                elif 0.10 <= stim_timer.getTime() < 0.5:
                    text.draw()
                    exp.win.flip()
                elif 0.5 <= stim_timer.getTime() < ISI:
                    exp.win.flip()
                    stim_exit = clock.getTime()

            #attach results of experiment to dataset
            detection_data.append(
                [
                    exp.subject_data['subject_num'],
                    i,
                    index,
                    len(detection_data)+1,
                    wordlist[i][index],
                    targcycle[i][index],
                    stim_presentation,
                    stim_exit,
                    RT
                ])
            exp.data_write(detection_data, './Data/', 'Encoding')

        math_correct = math_distractor(exp, math_correct)
        free_recall(exp, i, wordlist[i], targcycle[i])
        math_correct = int(math_correct)
        median_response = np.median([i for i in response_times if i >= 0.050])
        if (i+1) < 10:
            exp.text_box.text = "\n\
                \n\
                \n\
                \n\
                \n\
                \n\
                \n\
                \nBlock "+str(i+1)+" complete. Here are your results:\
                \n\
                \nMath problems solved: "+str(math_correct)+" \
                \nPercentage of targets you responded to: "+str(int(targets_responded)/(.5*config.listLength)*100.0)+"\
                \nPercentage of NON-targets you responded to: "+str(int(non_targets_responded)/(.5*config.listLength)*100.0)+"\
                \n\
                \nBlock "+str(i+2)+" will start now.\
                \nPress the spacebar to continue."
        else:
            exp.text_box.text = "\n\
                \n\
                \n\
                \n\
                \n\
                \n\
                \n\
                \nBlock "+str(i+1)+" complete. Here are your results:\
                \n\
                \nMath problems solved so far: "+str(math_correct)+" \
                \nPercentage of targets you responded to: "+str(int(targets_responded)/(.5*config.listLength)*100.0)+"\
                \nPercentage of NON-targets you responded to: "+str(int(non_targets_responded)/(.5*config.listLength)*100.0)+"\
                \n\
                \nBlock "+str(i+2)+" will start now.\
                \nPress the spacebar to continue."
        exp.text_box.draw()
        exp.win.flip()
        event.waitKeys(keyList = ["space"])

    exp.data_write(detection_data, './Data/', 'Encoding')



if __name__ == "__main__":
    exp = Experiment([1400, 800], True, {}, 'ABE_FR2', 'testMonitor')

    exp.win.flip()
    # s_port.write(1)

    [wordlist, targcycle] = make_wordlists(exp.subject_data['subject_num'])

    ISI = random.choice(list(range(1250, 1750)))/1000
    if exp.subject_data['subject_num'] % 2 == 1:
        red_target = True

    else:
        red_target = False



    skip_prac = 0


    if skip_prac == 0:
        practice_task(exp, red_target, ISI)

    run_experiment(exp, wordlist, targcycle, red_target)
    exp.text_box.text = "\
    \n\
    \n\
    \n\
    \n\
    \n\
    \nThank you for participating in this experiment.\
    \nYour responses have been recorded"
    exp.text_box.draw()
    event.waitKeys(keyList=["space"])
    exp.win.flip()
    # s_port.close()
