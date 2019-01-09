# Transform-Motion-into-Sound-Effects
By using IMU sensors we collect the movements of a juggling club in real time and interpret them as sound effect signals to an on playing song.

## Things you will learn
* Pyaudio sound effect processing
* Reading IMU data via UDP in Python
* Plotting in Real-Time in Matlab for exactring feature movements
* Create a keyboard interface through Pygame

## Overview
The overall structure of the Python code involves collecting data coming from the sensors by the HyperIMU app via UDP, determining which conditions the data satisfies as it is being processed in real time, and based on the threshold condition, passing the condition to a specific function, with each function corresponding to a different audio effect. 

.- Function for amplitude modulation is called func_duck() 
.- Function for the vibrato effect is called func_vibrato.
.- Function for the robotization effect is called func_robotization.
.- Function for echo is called func_echo.
.- Function for the reverberation effect is called func_reverberation.

This project had two input methods: the incoming data from sensors & keyboard inputs. We developed different ways of reproducing the audio files to implement more than three audio effects at the same time. One was through threading and the other was by adding the outputs of each audio effect. Adding the output effects gave better results in terms of the final audio output.

DEMO for Keyboard

We eventually want to develop juggling kits for street performers to create their own
audio processing effects according to their own juggling routine. Some additional
implementations we are considering in the future involve switching to bluetooth (we tried to do
this earlier on for this project, but decided to switch to Wi-Fi due to time constraints), utilizing
swarm robotics and researching more juggling patterns and juggling theory for a better
understanding of the different motions that take place in juggling. Swarm robotics involves
utilizing collective behavior that the robot will pick up from its interactions with the
5environment, such as juggling patterns. This can be used to practice and enhance juggling
performance, as well as to teach beginners how to juggle.
The following is the DEMO code to read incoming data via UDP in Python.
#

Using an android application called HyperIMU (Inertial Measurement Unit), we managed to gain access to Micro-Electro-Mechanical System (MEMS) sensors straight from our cell phones. HyperIMU allowed us to select the different sensors that exist in smartphones and collect the motion data. The physical sensors used were the accelerometer, gyro, and magnetometer. Through these sensors we implement sensor fusion to take advantage of virtual sensors, such as the linear accelerometer, gravity, rotation vector and compass. Another great feature of the application was the network protocols that were available. We used User Datagram Protocol (UDP) to transmit the sensor data in real time from the phone to a computer, and then read it in Python and Matlab. By activating HyperIMU on our phones and securing the phones in
juggling clubs, we were able to juggle and perform real time plotting in Matlab. The motion data was transmitted every 20ms as a CSV file. This data was used to create threshold conditions, which when satisfied, would give us a desired audio effect. The initial idea was to figure out whether the incoming data from the app was useful or not. We also needed to know if it needed some kind of filtering to make it usable. To achieve this, we decided to plot in real time the incoming data from all the sensors that we had decided to incorporate and observe them while performing various juggling patterns to get different conditions. We developed a code in MATLAB using the UDP library to get the sensor data being transmitted by the android application via UDP. We then plotted all the 3 axis data of each sensor in real-time. Figure 1 shows a real time plot of the data collected from the rotational vector.


As it turned out, all the plots were smooth enough and needed no filtering. Afterwards, we observed all twelve plots and constructed five different conditions based on the behavior of the plots. Each condition was used to implement a different audio effect. The five audio effects we decided to implement were amplitude modulation, vibrato, robotization, reverberation and echo, which were all implemented (in real time) on a wave file. Our wave file was Charlie Puth’s hit song, “We Don’t Talk Anymore,” featuring Selena Gomez. A vibrato is a musical effect that involves a slight variation in pitch to produce a richer tone and a reverb is the persistence of a sound after it has been produced, caused by reflections which build up, only to decay once the sound waves are absorbed by objects in the environment. We asked Selena Gomez for permission and she said it was okay to use her song (we actually didn’t, but for now, let us assume copyright is not an issue...we will eventually address this issue if we take this project any further). 

We knew that we could get good conditions by observing the gyroscope data for the normal juggling throw. In a similar way, we observed different sensor data for different motions until we filtered out five robust conditions. We decided that the amplitude modulation would be a result of the faceup toss, as shown in Figure 2, and the robotization effect would take place when the juggling pins were upright, as shown in Figure 3. The reverberation effect would take place when a circular motion occurred, as shown in Figure 4, and the echo effect would take place whenever the jugglers performed a weave with the pin, as shown in Figure 5. We went with these specific motions because these are the most common types of movements in juggling.

Although real time plotting could be done in Python, we decided to use Matlab because Matlab plots are visually more friendly than Python plots. In our Python code, we decided that the amplitude modulation (duck sound) would take place whenever the Z-Gravity Sensor was greater than 7 and the robotization effect would take place whenever the Y-Gravity Sensor was greater than 7. The vibrato would take place whenever the Z-Gyroscope was above .5 and the reverberation effect (feedback) would take place whenever √(X − Linear acceleration)2 + (Z − Linear Acceleration)2 was greater than 3. The echo effect would take place whenever |X − Rotational V ector| + |Z − rotational vector| was greater than 2 

These thresholds and audio effects were implemented in Python using if statements to correspond with a different audio processing effect. In order to implement multiple conditions at once, we placed flags in the Python code (the variable is called noCondition). Figure 6 shows a fragment of the Python code with two of the conditions and audio effects (echo and reverberation). Gff refers to the feed forward gain, Gdp refers to the direct path gain and Gfb refers to the feedback gain. These are just parameters that are needed to implement echo and reverberation in Python. 

We also implemented PyGame to incorporate keyboard control, providing users with two methods of input (real time motion or pressing a button on the keyboard). We initially came up with this method because we just wanted to make sure that the audio effect was programmed correctly, regardless of the juggling motion. This is why the “condition3True” and “condition4True” variables are in the if statements. For amplitude modulation (condition1True), 4we press the “a” key. For the vibrato effect (condition2True), we press the “v” key. For the echo effect (condition3True), we press the “e” key. For the reverberation effect (condition4True), we press the “f” key. For the robotization effect (condition5True), we press the “r” key. These keyboard inputs can be considered another set of threshold conditions, as an alternative to juggling motion. Figure 7 shows the Pygame implementation for keyboard control


