# import all modules
from tkinter import *  # gui module
from tkinter import messagebox
from tkinter import simpledialog
from osc4py3.as_eventloop import *  # osc module
from osc4py3 import oscbuildparse
import keyboard  # hotkeys
import shutil  # file manipulation
import math  # math
import os  # file manipulation

# initialize tkinter gui
root = Tk()
root.resizable(0, 0)
root.title("VroidPoser v1.0")
root.geometry("700x500+500+200")
root.iconphoto(False, PhotoImage(file="Resources/icon.png"))

# Foundation (unchanging-ish) tkinter widgets
canvas = Canvas(root, width=910, height=500)
canvas.place(relx=0, rely=0)

poseLabel = Label(root, text="Poses:", anchor="w")
poseLabel.place(x=400, y=320, width=50, height=20)
poseFrame = Frame(root, width=100, height=120)
poseFrame.pack_propagate(0)
poseFrame.place(x=400, y=340)
poseList = Listbox(poseFrame, width=13, exportselection=False)
poseList.pack(side=LEFT, fill=Y)
poseSb = Scrollbar(poseFrame, orient=VERTICAL)
poseSb.pack(side=RIGHT, fill=Y)
poseList.configure(yscrollcommand=poseSb.set, selectmode=SINGLE)
poseSb.config(command=poseList.yview)

stagingLabel = Label(root, text="Staging:", anchor="w")
stagingLabel.place(x=500, y=320, width=50, height=20)
stagingFrame = Frame(root, width=100, height=120)
stagingFrame.pack_propagate(0)
stagingFrame.place(x=500, y=340)
stagingList = Listbox(stagingFrame, width=13, exportselection=False)
stagingList.pack(side=LEFT, fill=Y)
stagingSb = Scrollbar(stagingFrame, orient=VERTICAL)
stagingSb.pack(side=RIGHT, fill=Y)
stagingList.configure(yscrollcommand=stagingSb.set, selectmode=SINGLE)
stagingSb.configure(command=stagingList.yview)

moveLabel = Label(root, text="Motions:", anchor="w")
moveLabel.place(x=600, y=320, width=50, height=20)
moveFrame = Frame(root, width=100, height=120)
moveFrame.pack_propagate(0)
moveFrame.place(x=600, y=340)
moveList = Listbox(moveFrame, width=13, exportselection=False)
moveList.pack(side=LEFT, fill=Y)
moveSb = Scrollbar(moveFrame, orient=VERTICAL)
moveSb.pack(side=RIGHT, fill=Y)
moveList.configure(yscrollcommand=moveSb.set, selectmode=SINGLE)
moveSb.configure(command=moveList.yview)

ipLabel = Label(root, text="ip:", anchor="w")
ipLabel.place(x=10, y=430, width=30, height=20)
ipEntry = Entry(root)
ipEntry.place(x=40, y=430, width=70, height=20)

portLabel = Label(root, text="Port #:")
portLabel.place(x=110, y=430, width=50, height=20)
portEntry = Entry(root)
portEntry.place(x=160, y=430, width=50, height=20)

# Global variables
ip = ""  # ip address (str)
osc = 0  # whether or not osc protocol is enabled (1 or 0)
port = 0  # port number

radius = 15  # size of the joystick BUTTON radius not the range of the joysticks
joyRange = 80  # range of motion for the joysticks
deadzone = 4
rotTarget = None  # Joint selected to rotate
target = "Placeholder"  # selected joint's joystick (str or None). Initialized as str to prevent PyCharm errors

hotkeys = {}  # Dictionary of all hotkey objects and their associated pose/motion
listen = False  # Enables/Disables key logging
pressed = []  # Array that captures keyboard inputs to turn into hotkeys later

checkVar = IntVar()  # Variable for checkbutton
staging = []  # List of poses used to create motion
travel = [0, 0, 0]  # the hip bone's x, y, z position in space
destination = [0, 0, 0]  # the desired hip bone position in space
offset = [0, 0, 0]  # required offset, if any

# List of joints and their respective joystick's coordinates on the gui (Important for calculations)
rArm = ["RightHand", "RightLowerArm", "RightUpperArm", "RightShoulder"]

lArm = ["LeftShoulder", "LeftUpperArm", "LeftLowerArm", "LeftHand"]

rHand = ["RightThumbIntermediate", "RightThumbDistal", "RightIndexProximal", "RightIndexIntermediate",
         "RightIndexDistal", "RightMiddleProximal", "RightMiddleIntermediate", "RightMiddleDistal", "RightRingProximal",
         "RightRingIntermediate", "RightRingDistal", "RightLittleProximal", "RightLittleIntermediate",
         "RightLittleDistal"]

lHand = ["LeftThumbIntermediate", "LeftThumbDistal", "LeftIndexProximal", "LeftIndexIntermediate", "LeftIndexDistal",
         "LeftMiddleProximal", "LeftMiddleIntermediate", "LeftMiddleDistal", "LeftRingProximal", "LeftRingIntermediate",
         "LeftRingDistal", "LeftLittleProximal", "LeftLittleIntermediate", "LeftLittleDistal"]

rLeg = ["RightUpperLeg", "RightLowerLeg", "RightFoot", "RightToes"]

lLeg = ["LeftUpperLeg", "LeftLowerLeg", "LeftFoot", "LeftToes"]

body = ["RightEye", "LeftEye", "Head", "Neck", "Chest", "Spine", "Hips"]

handR = [[290, 170], [290, 110], [230, 170], [230, 110], [230, 50], [170, 170], [170, 110], [170, 50], [110, 170],
         [110, 110], [110, 50], [50, 170], [50, 110], [50, 50]]
handL = [[410, 170], [410, 110], [470, 170], [470, 110], [470, 50], [530, 170], [530, 110], [530, 50], [590, 170],
         [590, 110], [590, 50], [650, 170], [650, 110], [650, 50]]

armR = [[110, 260], [170, 260], [230, 260], [290, 260]]
armL = [[410, 260], [470, 260], [530, 260], [590, 260]]

legR = [[740, 230], [740, 290], [740, 350], [740, 410]]
legL = [[860, 230], [860, 290], [860, 350], [860, 410]]
yBod = [[740, 50], [860, 50], [800, 50], [800, 110], [800, 170], [800, 230], [800, 300]]

names = [rArm, lArm, rHand, lHand, rLeg, lLeg, body]
startcoords = [armR, armL, handR, handL, legR, legL, yBod]

joints = {}
for lists in names:
    for name in lists:
        joints[name] = startcoords[names.index(lists)][lists.index(name)] + [0]
moved = joints.copy()


def create_circle(x, y, r, canvasname, **kwargs):  # function to creates circles I yoinked
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasname.create_oval(x0, y0, x1, y1, **kwargs)


def readcfg():  # reads "config.cfg" to restore previous sessions' settings
    global ip
    global port
    global osc
    global target
    global offset
    target = None  # set target to None for my own sanity
    file = open("Resources/config.cfg", "r")
    lines = file.readlines()
    for line in lines:
        split = line.rstrip("\n").split("=")
        if split[0] == "ip":
            ip = str(split[1])
            ipEntry.insert(0, ip)
        elif split[0] == "port":
            port = int(split[1])
            portEntry.insert(0, port)
        elif split[0] == "osc":
            osc = int(split[1])
        elif split[0] == "offset":
            offset = [float(split[1]), float(split[2]), float(split[3])]
        else:
            if len(split) == 3:
                if split[2] == "poseList":
                    box = poseList
                    if os.path.exists("Poses/" + split[0] + ".txt"):
                        hotkeys[split[0]] = [split[1], keyboard.add_hotkey(split[1], lambda: hotkeyactivated(split[0], box)), split[2]]
                    else:
                        print(split[0])
                else:
                    box = moveList
                    if os.path.exists("Moves/" + split[0]):
                        hotkeys[split[0]] = [split[1], keyboard.add_hotkey(split[1], lambda: hotkeyactivated(split[0], box)), split[2]]
                    else:
                        print(split[0])
    print(hotkeys)


def sendosc(bone, x, y, z):  # condensed OSC message function
    global offset
    if checkVar.get() == 1:
        if bone == "Hips":
            msg = oscbuildparse.OSCMessage("/VMC/Ext/Bone/Pos", None,
                                           [bone, float(destination[0] + offset[0]), float(destination[1] + offset[1]),
                                            float(destination[2] + offset[2]), float(x),
                                            float(y), float(z), float(1)])
        else:
            msg = oscbuildparse.OSCMessage("/VMC/Ext/Bone/Pos", None,
                                           [bone, float(0), float(0), float(0), float(x),
                                            float(y), float(z), float(1)])

        osc_send(msg, "VroidPoser")
        osc_process()


def sieve(joint, q, w, rot):
    if joint in lLeg:
        sendosc(joint, w, rot, q)
    elif joint in rLeg:
        sendosc(joint, -1 * w, rot, q)
    elif joint in body and "Eye" not in joint:
        sendosc(joint, -1 * w, -1 * rot, -1 * q)
    else:
        sendosc(joint, rot, q, w)


def rotate(bone, rot):  # takes input from slider to control limb rotation
    global joints
    global moved
    if bone is not None:
        if "Left" in bone:  # Left-side bones need to be flipped
            multiplier = -1
        else:
            multiplier = 1
        q = -4 * ((moved[bone][0] - joints[bone][0]) / joyRange)
        w = -4 * ((moved[bone][1] - joints[bone][1]) / joyRange) * multiplier
        rot = float(rot)
        moved[bone][2] = rot
        rot = (1*rot)**3

        sieve(bone, q, w, rot)


def enablecoms():  # Enables/Disables OSC protocol
    global target
    global ip
    global port
    if checkVar.get() == 1:  # Checks if the checkbutton is enabled...
        ip = str(ipEntry.get())  # ip address
        port = int(portEntry.get())  # port number

        osc_startup()  # starts osc protocol
        osc_udp_client(ip, port, "VroidPoser")  # initializes osc client
    else:
        osc_terminate()  # ...otherwise end the protocol if it's running


def draw():  # Refreshes canvas each time a change occurs and redraws it
    global joints
    global moved
    canvas.delete("all")
    for objs in joints.keys():  # for each key in the dictionary ("joints")
        if objs in names[0]:
            color = "red"
        elif objs in names[1]:
            color = "green"
        elif objs in names[2]:
            color = "blue"
        elif objs in names[3]:
            color = "indigo"
        elif objs in names[4]:
            color = "violet"
        elif objs in names[5]:
            color = "maroon"
        elif objs in names[6]:
            color = "black"
        create_circle(joints[objs][0], joints[objs][1], joyRange / 2, canvas, width=2)  # visualizes joystick range
        if objs == target:  # activates if the joint was selected
            canvas.create_line(joints[target][0], joints[target][1], moved[target][0], moved[target][1])
            create_circle(moved[target][0], moved[target][1], 5, canvas, fill=color, width=0)
            if "Left" in target:  # Left-side bones need to be flipped
                multiplier = -1
            else:
                multiplier = 1

            q = -4 * ((moved[target][0] - joints[target][0]) / joyRange)
            w = -4 * ((moved[target][1] - joints[target][1]) / joyRange) * multiplier

            rot = moved[target][2]**3

            sieve(target, q, w, rot)

        else:  # If the joint was not selected it's redrawn
            canvas.create_line(joints[objs][0], joints[objs][1], moved[objs][0], moved[objs][1])
            create_circle(moved[objs][0], moved[objs][1], radius, canvas, fill=color, width=0)


def refresh():  # Refreshes list of available poses
    poseList.delete(0, END)  # clears all listboxes
    stagingList.delete(0, END)
    moveList.delete(0, END)
    basepath = 'Poses/'
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            poseList.insert(poseList.size(), entry.split(".")[0])
    for pose in staging:
        stagingList.insert(stagingList.size(), pose)
    for x in os.walk("Moves/"):
        if x[0] != 'Moves/':
            moveList.insert(moveList.size(), x[0].split('/')[1])


def reset():  # Resets all joints
    global moved
    global joints
    global travel
    global destination
    sure = messagebox.askyesno("Resetting...", 'Are you sure you want to reset all joints?')
    if sure == 1:
        x = 0
        while x <= 1:
            destination.clear()
            a = travel[0] + (0 - travel[0]) * x
            b = travel[1] + (0 - travel[1]) * x
            c = travel[2] + (0 - travel[2]) * x
            destination = [a, b, c]
            for i in joints.keys():
                if "Left" in i:
                    multiplier = -1
                else:
                    multiplier = 1
                q = -4 * ((moved[i][0] - joints[i][0]) / joyRange)
                w = -4 * ((moved[i][1] - joints[i][1]) / joyRange) * multiplier
                e = float(moved[i][2])
                hor = q + (0 - q) * x
                ver = w + (0 - w) * x
                rot = e + (0 - e) * x

                sieve(i, hor, ver, rot)

            x += 0.01
        destination = [0, 0, 0]
        for i in joints.keys():
            sendosc(i, 0, 0, 0)
        moved = joints.copy()
        travel = [0, 0, 0]
        rotSlider.set(0)
        draw()


def posepicker(event):  # Activates a pose. Calculates poses in between initial pose "tempdict" and the loaded pose data
    global moved
    global travel
    global destination
    file = open(event, "r")
    lines = file.readlines()
    tempdict = {}  # temporary dictionary stores new pose data
    x = 0
    while x <= 1:  # ideally would be "for lines" -> "x<=1:" but the blocking provided seems to help with movement
        for line in lines:
            split = line.split(",")
            if split[0] == "speed":
                speedSlider.set(float(split[1].rstrip("\n")))
            elif split[0] == "travel":
                split[1] = travel[0] + (float(split[1]) - travel[0]) * x
                split[2] = travel[1] + (float(split[2]) - travel[1]) * x
                split[3] = travel[2] + (float(split[3]) - travel[2]) * x
                destination = [split[1], split[2], split[3]]
            else:
                # horizontal, vertical, bone, rotation. I'm too lazy to go back and fix the order
                array = [float(split[1]), float(split[2]), str(split[0]), float(split[3])]

                if "Left" in array[2]:  # converts back to positional data (x and y distance from relative origin)
                    multiplier = -1
                else:
                    multiplier = 1
                a = ((array[0] * joyRange) / (-4)) + joints[array[2]][0]
                b = ((array[1] * joyRange) / (-4 * multiplier)) + joints[array[2]][1]

                tempdict[array[2]] = [a, b, array[3]]  # Updates tempdict's data

                # start angles (calculated from relative origin)
                q = -4 * ((moved[array[2]][0] - joints[array[2]][0]) / joyRange)
                w = -4 * ((moved[array[2]][1] - joints[array[2]][1]) / joyRange) * multiplier

                # end angles (calculated from relative origin)
                e = -4 * ((a - joints[array[2]][0]) / joyRange)
                r = -4 * ((b - joints[array[2]][1]) / joyRange) * multiplier

                hor = q + (e - q) * x  # determines incremental changes to angles
                ver = w + (r - w) * x
                rot = moved[array[2]][2] + (float(array[3]) - moved[array[2]][2]) * x
                rot = (1 * rot) ** 3

                sieve(array[2], hor, ver, rot)

        x += speedSlider.get() / 100  # speed
    if len(moved) == len(tempdict):
        moved.clear()
        moved = tempdict.copy()  # sets new modified pose
    else:
        for key in moved:
            if key in tempdict:
                moved[key] = tempdict[key]
    travel = destination.copy()
    draw()


def delete():  # Removes a pose from the listbox (deletes the pose file) and refreshes it.
    global staging
    select = poseList.curselection()
    if str(select) != "()":
        sure = messagebox.askyesno("", "Are you sure you want to delete the " + str(poseList.get(select[0])) + " pose?")
        if sure is True:
            if poseList.get(select[0]) in staging:
                staging.remove(poseList.get(select[0]))
            os.remove("Poses/" + str(poseList.get(select[0])) + ".txt")
            reset()
            refresh()


def save():  # saves pose as a txt file with speed and position data
    pose = simpledialog.askstring("", 'Enter pose name:')
    if pose is not None:
        file = open("Poses/" + pose + ".txt", "w")
        file.write("speed," + str(speedSlider.get()) + "\n")
        file.write("travel," + str(travel[0]) + "," + str(travel[1]) + "," + str(travel[2]) + "\n")
        for item in moved.keys():
            if "Left" in item:
                multiplier = -1
            else:
                multiplier = 1
            q = -4 * (moved[item][0] - joints[item][0]) / joyRange  # converts positional data to angle
            w = -4 * (moved[item][1] - joints[item][1]) / joyRange * multiplier
            file.write(str(item) + "," + str(q) + "," + str(w) + "," + str(moved[item][2]) + "\n")
        file.close()
        refresh()


def clear(event):  # clears "staging" and by extension the staging listbox
    global staging
    if event is True:
        staging = []
        refresh()
    else:
        select = stagingList.curselection()[0]
        staging.pop(select)
        refresh()


def snag():  # adds pose to staging and by extension, the staging listbox
    get = poseList.curselection()
    get = str(poseList.get(get[0]))
    staging.append(get)
    refresh()


def createanimation():  # Creates a folder with all necessary pose files and an "animate.txt" with the order of poses
    motion = simpledialog.askstring("", 'Enter animation name:')
    if motion is not None:
        basepath = "Moves/"
        os.mkdir(basepath + motion)
        file = open('Moves/' + motion + '/' + "animate" + ".txt", "w")
        for pose in staging:
            if os.path.exists('Moves/' + motion + '/' + pose + '.txt') is False:
                shutil.copyfile('Poses/' + pose + '.txt', 'Moves/' + motion + '/' + pose + '.txt')
            file.write(pose + "\n")
        moveList.insert(0, motion)


def reposition(event):  # moves pose within the "staging" list which is used to make a motion
    select = stagingList.curselection()[0]
    if event is True:
        if select - 1 != -1:
            staging.insert(select - 1, staging[select])
            staging.pop(select + 1)
    else:
        if select + 1 != len(staging):
            staging.insert(select + 2, staging[select])
            staging.pop(select)
    refresh()


def deleteanim():  # deletes motion data
    select = moveList.curselection()
    if str(select) != "()":
        sure = messagebox.askyesno("", "Are you sure you want to delete the " + str(moveList.get(select[0])) +
                                   " Motion?")
        if sure is True:
            shutil.rmtree("Moves/" + str(moveList.get(select[0])))
            reset()
            refresh()


def left_click(event):  # Iterates through "moved" dictionary and checks if a joystick is close enough to be triggered
    global target
    global rotTarget
    for objs in moved.keys():
        value = math.dist([event.x, event.y], [moved[objs][0], moved[objs][1]])
        if value < radius:
            target = objs
            rotTarget = objs
            rotSlider.set(float(moved[target][2]))
            break


def release(event):  # If a joystick was selected, this unselects it.
    global target
    if target is not None:
        target = None
    draw()


def move(event):  # Fires when mouse is moved
    global moved
    if target is not None:  # If a joint is selected
        if math.dist([joints[target][0], joints[target][1]], [event.x, event.y]) > joyRange / 2:
            b = (joyRange * (event.y - joints[target][1])) / (2 * math.dist([event.x, event.y], [joints[target][0],
                                                                                                 joints[target][1]]))
            a = (joyRange * (event.x - joints[target][0])) / (2 * math.dist([event.x, event.y], [joints[target][0],
                                                                                                 joints[target][1]]))
            # If a joystick is selected but the mouse is ouside the joystick's range, the joystick still points in the
            # direction of the mouse.
            moved[target][0] = joints[target][0] + a
            moved[target][1] = joints[target][1] + b
            moved[target][2] = moved[target][2]
        elif math.dist([joints[target][0], joints[target][1]], [event.x, event.y]) <= deadzone:  # creates deazone
            moved[target] = joints[target]

        else:  # Otherwise just set the new joystick position
            moved[target] = [event.x, event.y, moved[target][2]]
        draw()


def advanced(event):  # Shows/hides advanced joysticks
    if event is True:
        root.geometry("910x500")
    else:
        root.geometry("700x500")


# More tkinter widgets
enable = Checkbutton(root, text="Send Pose Data", variable=checkVar, onvalue=1, command=enablecoms)
enable.place(x=220, y=430, width=100, height=20)

resetButton = Button(root, text="Reset Joints", command=reset)
resetButton.place(x=220, y=390, width=80, height=20)

saveButton = Button(root, text="Save Pose", command=save)
saveButton.place(x=400, y=460, width=80, height=20)

rotLabel = Label(root, text="Limb Rotation:", anchor="w")
rotLabel.place(x=10, y=340, width=100, height=20)

rotSlider = Scale(root, from_=-4, to=4, resolution=0.0001, orient=HORIZONTAL)
rotSlider.configure(command=lambda r: rotate(rotTarget, r))
rotSlider.place(x=100, y=320, width=200)

speedLabel = Label(root, text="Pose Speed", anchor="w")
speedLabel.place(x=10, y=390, width=100, height=20)

speedSlider = Scale(root, from_=0.1, to=5, resolution=0.1, orient=HORIZONTAL)
speedSlider.place(x=100, y=370, width=100)
speedSlider.set(2.5)

infoLabel = Label(root, text="| Copyleft 2021 NeilioClown | Covered by GPL-3.0 |", anchor="center")
infoLabel.place(x=10, y=460, width=300, height=20)

moveUp = Button(root, text="⬆️", command=lambda: reposition(True))
moveUp.place(x=500, y=460, width=40, height=20)
moveDown = Button(root, text="⬇️", command=lambda: reposition(False))
moveDown.place(x=540, y=460, width=40, height=20)

addAnim = Button(root, text="Save Motion", command=createanimation)
addAnim.place(x=600, y=460, width=80, height=20)

advancedButton = Button(root, text="Advanced", command=lambda: advanced(True))
advancedButton.place(x=310, y=30, width=80, height=20)

standardButton = Button(root, text="Standard", command=lambda: advanced(False))
standardButton.place(x=760, y=460, width=80, height=20)

unitEntry = Entry(root)
unitEntry.place(x=840, y=130, width=60, height=20)


def trip(direct):
    global moved
    global destination
    global travel
    if unitEntry.get() != "" and isinstance(unitEntry.get, str) is False:
        unit = float(unitEntry.get())
    else:
        unit = 0.01
    if direct == "Up":
        destination[1] += unit
    elif direct == "Down":
        destination[1] -= unit
    elif direct == "Left":
        destination[0] += unit
    elif direct == "Right":
        destination[0] -= unit
    elif direct == "Front":
        destination[2] += unit
    elif direct == "Back":
        destination[2] -= unit
    q = -4 * (moved["Hips"][0] - joints["Hips"][0]) / joyRange  # converts positional data to angle
    w = -4 * (moved["Hips"][1] - joints["Hips"][1]) / joyRange
    sendosc("Hips", -1 * w, -1 * moved["Hips"][2], -1 * q)
    travel = destination.copy()


p1 = PhotoImage(file="Resources/Up.png")
p2 = PhotoImage(file="Resources/Down.png")
p3 = PhotoImage(file="Resources/Left.png")
p4 = PhotoImage(file="Resources/Right.png")
up = Button(root, image=p1, anchor="center", repeatdelay=100, repeatinterval=100, command=lambda: trip("Up"))
up.place(x=720, y=110, width=20, height=20)
down = Button(root, image=p2, anchor="center", repeatdelay=100, repeatinterval=100, command=lambda: trip("Down"))
down.place(x=720, y=150, width=20, height=20)
left = Button(root, image=p3, anchor="center", repeatdelay=100, repeatinterval=100, command=lambda: trip("Left"))
left.place(x=700, y=130, width=20, height=20)
right = Button(root, image=p4, anchor="center", repeatdelay=100, repeatinterval=100, command=lambda: trip("Right"))
right.place(x=740, y=130, width=20, height=20)
back = Button(root, image=p1, anchor="center", repeatdelay=100, repeatinterval=100, command=lambda: trip("Back"))
back.place(x=860, y=110, width=20, height=20)
front = Button(root, image=p2, anchor="center", repeatdelay=100, repeatinterval=100, command=lambda: trip("Front"))
front.place(x=860, y=150, width=20, height=20)


def picker(event, listbox):  # Picks pose/motion and activates it
    if listbox == "test":
        for pose in staging:
            data = "Poses/" + str(pose) + ".txt"
            posepicker(data)
        posepicker(data)
    else:
        listbox.selection_clear(0, END)
        listbox.selection_set(poseList.nearest(event.y))
        listbox.activate(poseList.nearest(event.y))
        if listbox == poseList:
            select = poseList.curselection()
            if str(select) != "()":
                data = "Poses/" + str(poseList.get(select[0])) + ".txt"
                posepicker(data)
                posepicker(data)
        elif listbox == moveList:
            select = moveList.curselection()
            if str(select) != "()":
                data = "Moves/" + str(moveList.get(select[0])) + "/animate.txt"
                file = open(data, "r")
                lines = file.readlines()
                for line in lines:
                    data = "Moves/" + str(moveList.get(select[0])) + "/" + line.rstrip("\n") + ".txt"
                    posepicker(data)
                posepicker(data)


def hotkeyactivated(base, listbox):  # too lazy to integrate, so a new function for poses/motion for hotkeys
    print(base, hotkeys)
    if listbox == poseList:
        data = "Poses/" + base + ".txt"
        posepicker(data)
        posepicker(data)
    elif listbox == moveList:
        data = "Moves/" + base + "/animate.txt"
        file = open(data, "r")
        lines = file.readlines()
        for line in lines:
            data = "Moves/" + base + "/" + line.rstrip("\n") + ".txt"
            posepicker(data)
        posepicker(data)


def keylogger(event):  # Saves keyboard inputs. This is POTENTIALLY dangerous if this is a modified project
    global pressed
    global listen
    key = event.name
    if key not in pressed and listen is True:
        pressed.append(key)


def addhotkey(thing, listbox):  # allows keys to be read, then reads keys input before closing the dialog
    global pressed
    global listen
    listen = True
    messagebox.showinfo(title=None, message="Input your hotkey combo and press enter or click OK. To clear a hotkey, "
                                            "just continue.")
    listen = False
    print(pressed)
    if len(pressed) > 0:
        if pressed[len(pressed)-1] == "enter":
            pressed.pop(len(pressed)-1)
        if len(pressed) != 0:
            combo = ""
            for keys in pressed:
                combo = combo + keys + '+'
            pressed.clear()
            combo = combo.rstrip('+')
            if listbox == poseList:
                box = "poseList"
            else:
                box = "moveList"
            print(thing, combo)
            if thing not in hotkeys.keys():
                hotkeys[thing] = [combo, keyboard.add_hotkey(combo, lambda: hotkeyactivated(thing, listbox)), box]
            else:
                keyboard.clear_hotkey(hotkeys[thing][1])
                hotkeys.pop(thing)
                hotkeys[thing] = [combo, keyboard.add_hotkey(combo, lambda: hotkeyactivated(thing, listbox)), box]
        else:
            print(thing + " removed")
            keyboard.clear_hotkey(hotkeys[thing][1])
            hotkeys.pop(thing)
    elif thing in hotkeys.keys():
        print(thing + " removed")
        keyboard.clear_hotkey(hotkeys[thing][1])
        hotkeys.pop(thing)


keyboard.on_press(lambda r: keylogger(r))  # keyboard listener

# Initializes right-click menu
m = Menu(root, tearoff=0)


def do_popup(event, listbox):
    listbox.selection_clear(0, END)
    listbox.selection_set(listbox.nearest(event.y))
    listbox.activate(listbox.nearest(event.y))
    try:
        m.delete(0, END)
        if listbox == poseList:
            m.add_command(label="Delete", command=delete)
            m.add_command(label="Add to Staging", command=snag)
            select = listbox.curselection()
            if select != "()":
                motion = listbox.get(select[0])
                if motion in hotkeys.keys():
                    label = hotkeys[motion][0]
                else:
                    label = "Assign Hotkey"
                m.add_command(label=label, command=lambda: addhotkey(motion, listbox))
        elif listbox == stagingList:
            m.add_command(label="Remove", command=lambda: clear(False))
            m.add_command(label="Move Up", command=lambda: reposition(True))
            m.add_command(label="Move Down", command=lambda: reposition(False))
            m.add_command(label="Clear Staging", command=lambda: clear(True))
            m.add_command(label="Test", command=lambda: picker(None, "test"))
        elif listbox == moveList:
            m.add_command(label="Delete", command=deleteanim)
            select = listbox.curselection()
            if select != "()":
                motion = listbox.get(select[0])
                if motion in hotkeys.keys():
                    label = hotkeys[motion][0]
                else:
                    label = "Assign Hotkey"
                m.add_command(label=label, command=lambda: addhotkey(motion, listbox))
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()


# All functions that need to be called on initialization
readcfg()
refresh()
draw()
checkVar.set(osc)
enablecoms()


def terminate():  # Verifies exit and saves settings
    global ip
    global port
    global osc
    sure = messagebox.askyesno("Exiting...", 'Are you sure you want to quit?')  # Double check
    if sure == 1:
        file = open("Resources/config.cfg", "w")  # Opens and writes settings
        file.write("ip=" + str(ipEntry.get()) + "\n")
        file.write("port=" + str(portEntry.get()) + "\n")
        file.write("osc=" + str(checkVar.get()) + "\n")
        file.write("offset=" + str(offset[0]) + "=" + str(offset[1]) + "=" + str(offset[2]) + "\n")
        for hot in hotkeys.keys():
            file.write(hot + "=" + hotkeys[hot][0] + "=" + hotkeys[hot][2] + "\n")
        root.destroy()  # quits program


# Event binds
poseList.bind("<Button-3>", lambda r: do_popup(r, poseList))  # Fires when any Listbox is right-clicked
stagingList.bind("<Button-3>", lambda r: do_popup(r, stagingList))
moveList.bind("<Button-3>", lambda r: do_popup(r, moveList))

poseList.bind("<Button-1>", lambda r: picker(r, poseList))  # Fires when any Listbox is left-clicked
moveList.bind("<Button-1>", lambda r: picker(r, moveList))

canvas.bind('<Button 1>', left_click)  # Fires when the canvas is left-clicked
canvas.bind('<ButtonRelease 1>', release)  # Fires when the left mouse button is released
canvas.bind('<Motion>', move)  # Fires when the mouse moves

root.protocol("WM_DELETE_WINDOW", terminate)  # Overrules standard exit behavior with the "terminate" function.
root.mainloop()  # Run that baby!
