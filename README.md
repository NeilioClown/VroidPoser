# VroidPoser - a pose creator/animator for VSeeFace

<img src="https://raw.githubusercontent.com/NeilioClown/VroidPoser/v1.0/Guide/icon.png" width="200" />


![Basic](https://raw.githubusercontent.com/NeilioClown/VroidPoser/v1.0/Guide/Base.PNG)

> Written with [StackEdit](https://stackedit.io/).

**Note**: Vroid is the intellectual property of pixiv. I do not claim any ownership of any Vroid related software or licenses except for the software I provide. All other Vroid related licenses and software are the property of their respective holders.

About:
-
VroidPoser is an admittedly shoddy but fully featured python application designed for creating and sending motion data to VSeeFace. It utilizes the OSC protocol, of which the VMC ([Virtual Motion Capture](https://protocol.vmc.info/)) protocol is derived from. 

This project came about because despite my limited usage of [Vroids](https://vroid.com/en), I still wanted to give them more interesting movements without having to shell out for hand tracking.

Why Python? It's the only language I'm semi-fluent in and I like torturing myself (/s, I think). In the (far) future I'll definitely do a rewrite with a 3d engine for more ease of use, if one doesn't exist by then.

This application is not necessarily meant to be for daily use, however it can be if you are willing to put up with it. 
*It's meant to be more of a baseline which can hopefully influence more refined derivatives.*

Features:
 - 
 - Fluid motion between poses.
 - Motion (animation) creation based on poses.
 - Ability to trigger poses/motions with hotkeys.
 - Compatibility with most programs utilizing the VMC protocol (?)


Known limitations:
 - 
 - The entire UI.
 - No full 360 degree rotation, only -180 to 180 degree.
 - More-than-I-care-for CPU usage.


Usage:
 - 
 VroidPoser is covered by GPL-3.0. All I ask is that I be credited in any derivitive projects, if any.


Setup:
-
**VSeeFace:**

 - Download [VSeeFace](https://www.vseeface.icu/) and install it to your computer following the instructions provided. 
 - Launch VSeeFace.exe and complete the first-time setup.
 - Load a Vroid model of your choice.
 - Open Settings > General Settings. Scroll down to "OSC/VMC reciever" and enable it. If you want partial tracking, enable "Apply VSeeFace tracking" and enable it, then enable the features that you want. 
Recommended setting are:
	 - Apply expressions
	 - Track face features
		   - Track blendshapes
		   - Track jawbone 
	- Track head and neck
	- Track spine and chest
- Note the ip address and the port number.

**VroidPoser:**

- Download VroidPoser and extract it to a directory of your choice.
- Launch VroidPoser.exe.
- At the bottom, leave the ip address as 127.0.0.1 unless you know how to use computer connections over a network. Make sure the port number is the same as in VSeeFace.
- Under "Motions" click "Wave" to test if your program is configured correctly.

How To:
-
**Make a Pose:**

The best way to look at the joysticks in VroidPoser is to imagine them as pins that poke lengthwise straight into each limb. By manipulating the joysticks you alter the angle the limb is pointing in. 
If you want to alter a limb's rotation, click on its joystick, then use the "Limb Rotation" slider.
If you want to alter the time it takes for the Vroid to switch to a new pose, use the "Pose Speed" slider. This value is pose specific and is saved.

Move each joystick around until you've made a pose that you want. Then select "Save Pose."

*Warning:* Saving a Pose with the same name as another Pose will overwrite the original Pose. This is half by design and half a result of laziness.



https://user-images.githubusercontent.com/84215966/118752905-c643f380-b818-11eb-98c0-a3751e945305.mp4



**Make a Motion:**

Create a series of Poses that you'd like your Vroid to make. 

Right-click the first pose and select "Add to Staging." 

Repeat with all Poses you want to add. If you want to change their order in the "Staging" menu, simply right click the Pose you want to reorder and select "Move Up" or "Move Down," or Left click the pose and hit one of the buttons. 

To remove a Pose from the "Staging" menu, right click it and select "Remove"

To test the Motion, right click anywhere in the "Staging" menu and select "Test." When you are happy with your Motion, click "Save Motion."



https://user-images.githubusercontent.com/84215966/118753220-597d2900-b819-11eb-93f3-e5c4772212e6.mp4




*Warning:* You can't edit a Motion after you save it (It's not impossible, it's just not worth my time) . However, with the way that Motions are formatted, you can simply open the folder the Motion's Poses are stored in and copy them to the "Poses" folder. Load and edit them in-program, then copy them back.

*Warning:* Unlike Poses, trying to overwrite a Motion with another Motion of the same name will fail.

**Delete a Pose/Motion:**

Right Click on any Pose/Motion and select "Delete." A pop-up will ask you to verify your choice, as this is irreversible.

**Use Hotkeys:**

Right click on any Pose or Motion and select "Assign Hotkey." 

A popup will come up telling you to input a key combo and press ENTER or OK. 

Right click on the Pose/Motion and it should show the assigned hotkey combo where "Assign Hotkey" used to be.

To clear a hotkey, right click and select the hotkey from the menu. When it asks you to input a key combo, simply press ENTER or hit OK.



https://user-images.githubusercontent.com/84215966/118752944-d8259680-b818-11eb-8ca0-efe7b7794579.mp4




**Standard Mode:**

Standard Mode is meant for people who aren't going to be showing more than the upper part of their Vroid avatar. This limits you to only arm/finger manipulation in tandem with VSeeFace's native tracking. However, you can still play back Poses and Motions made in Advanced Mode in Standard Mode. 

**Advanced Mode:**

Advanced Mode allows a higher range of customization, with the caveat that it opens up the potential for more errors.

Advanced Mode expands the amount of joints that you can manipulate from the arms and hands to essentially all joints in the body, as well as rotating the body itself and moving it in space.

Click on the "Advanced" Button to enter  Advanced Mode. The window will expand to reveal more options.

![Advanced](https://raw.githubusercontent.com/NeilioClown/VroidPoser/v1.0/Guide/Advanced.png)

Go to Vseeface and open Settings > General and scroll down to "OSC/VMC Protocol." Either deselect "Apply VSeeFace tracking" or deselect the options of your choice. Remember that VSeeFace overrides motion data from VroidPoser.

Use Advanced Mode as you would Standard Mode.

Use the arrow buttons to change your avatar's position in space. The default speed is 0.001 units, but entering a number into the entry box will override it.


Click on the "Standard" Button exit Advanced Mode.

Wrapping
-
If you want to try to understand my sloppy coding, simply download the source code provided and place it in a development environment utilizing Python 3.9.
It requires 2 external modules: [osc4py3](https://pypi.org/project/osc4py3/) and [keyboard](https://pypi.org/project/keyboard/).
Install them to your development environment and open `VroidPoser.py`.

**Windows:**

VroidPoser was tested in a PyCharm virtual environment, after which I moved it to a global environment and wrapped it with [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/). Make sure to include the Moves, Poses, and Resources folders.

**Linux:**

Untested. Windows binary can probably run through WINE.
*Note:* If you run from source, keep in mind that the keyboard module requires root access on Linux.

**MacOS:**

Untested. Probably works but there is little support for Vroid on Mac regardless.



