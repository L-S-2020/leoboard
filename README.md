# Leoboard
<img src="https://github.com/L-S-2020/leoboard/blob/main/pictures_readme/overview.jpg?raw=true" alt="the console" width="600"/>

A makroboard I designed as a christmas present and my first project using 3d printing / cad design.
You can find the case design on onshape under: 
https://cad.onshape.com/documents/f016138659585157d187dc39/w/5da7c9f47346b58de636040e/e/736dc8079a6dc26abaf89305?renderMode=0&uiState=69bc84548cc73f69bd25787e

## Features
- 6 MX Style switches
- buzzer (for sound)
- rotary encoder
- rgb leds 
- rp2040 based

Note: The code folder also includes kmk and the necessary addons, so it can be directly flashed to the rp2040.

## Standard key binds
The board has 3 switchable layers:
|Layer| Rotary button | Rotary encoder | Button 1 | Button 2 | Button 3 | Button 4 | Button 5 | Button 6 |
|--|--|--|--|--|--|--|--|--|
| 1 (normal) | Mute | Volume | Play/ Pause | Next song | Previous song | Win+Shift+S | Task manager | Lock pc |
|2 (gaming) |Discord mute| Volume | Mute | Discord audio off | Medal save clip | Screenshot | M | I |
|3 (premiere pro) | \ | Seek through frames | Add cut | Delete clip | Zoom in | Zoom out | Undo | Redo |
|Setings| must be hold down | -- | Layer 1 | Layer 2 | Layer 3 | LED on/off | LED breathe animation |LED rainbow animation |

## The story
One day as I was editing a video for the video club at my school (check out the [yt channel](https://www.youtube.com/@gsgwaldkirch4155)), I was annoyed by the standard key assignments of Premiere Pro. Especially using the arrow keys to seek through frames manually (i.e. for finding the excact startframe of a clip) is a really slow process, so I thought, wouldn't it be cool to have a rotary knob for that and then also to have a special key set for directly placing cuts and zooming in the timeline? 

So I the idea to design my own macroboard was born. I found a nice starting tutorial on [the hackclub blueprint website](https://blueprint.hackclub.com/), which showed the ground ideas of macroboard design.
As it was just two weeks before christmas back then, I thought it would also be cool to use the board as a christmas present.

So I got started with the pcb design using kicad. The design itself is based on the seed xiao rp2040 devboard, as it is the perfect size and also quite cheap. Additionally to my initial requirements (switches and rotary encoder), I came up with the idea to also add leds for light and a buzzer for playing startup sounds.

<img src="https://github.com/L-S-2020/leoboard/blob/main/pictures_readme/wiring.png?raw=true" alt="the console" width="500"/>

Then I designed the pcb board and searched in the jlcpcb parts library for suiting (and cheap) parts. 

<img src="https://github.com/L-S-2020/leoboard/blob/main/pictures_readme/pcb-design.png?raw=true" alt="the console" width="400"/>
<img src="https://github.com/L-S-2020/leoboard/blob/main/pictures_readme/pcb.png?raw=true" alt="the console" width="500"/>

As the order was on its way, I started designing the case using onshape.

<img src="https://github.com/L-S-2020/leoboard/blob/main/pictures_readme/case-cad.png?raw=true" alt="the console" width="600"/>

I also created an assembled model in onshape, to test the dimensions.

<img src="https://github.com/L-S-2020/leoboard/blob/main/pictures_readme/cad-assembly.png?raw=true" alt="the console" width="500"/>

After printing and assembling the final macropads, I learned that, it's not good to make the inner dimensions of your case exactly like the dimensions of your board ;) , but fortunately, I printed everything in pla, so after some heating using a hair dryer, I could fit the pcb inside.

<img src="https://github.com/L-S-2020/leoboard/blob/main/pictures_readme/assembly.jpg?raw=true" alt="the console" width="500"/>

I then wrote a script for it, using kmk, as I liked the idea of being able to quickly change some configurations, without having to recompile. 
[@SillyGoose123](https://github.com/SillyGoose123) is also currently working on a more powerful, rust-based firmware for the board with a web based settings interface, check it out [here](https://github.com/SillyGoose123/MacroBoard).

##
A big thanks to my cs teacher for letting me print out the cases using the 3dprinter in his office and to [@SillyGoose123](https://github.com/SillyGoose123) for printing out the keycaps.
