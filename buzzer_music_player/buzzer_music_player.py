from machine import Pin, PWM
import utime

tones = {
    'C0':16,
    'C#0':17,
    'D0':18,
    'D#0':19,
    'E0':21,
    'F0':22,
    'F#0':23,
    'G0':24,
    'G#0':26,
    'A0':28,
    'A#0':29,
    'B0':31,
    'C1':33,
    'C#1':35,
    'D1':37,
    'D#1':39,
    'E1':41,
    'F1':44,
    'F#1':46,
    'G1':49,
    'G#1':52,
    'A1':55,
    'A#1':58,
    'B1':62,
    'C2':65,
    'C#2':69,
    'D2':73,
    'D#2':78,
    'E2':82,
    'F2':87,
    'F#2':92,
    'G2':98,
    'G#2':104,
    'A2':110,
    'A#2':117,
    'B2':123,
    'C3':131,
    'C#3':139,
    'D3':147,
    'D#3':156,
    'E3':165,
    'F3':175,
    'F#3':185,
    'G3':196,
    'G#3':208,
    'A3':220,
    'A#3':233,
    'B3':247,
    'C4':262,
    'C#4':277,
    'D4':294,
    'D#4':311,
    'E4':330,
    'F4':349,
    'F#4':370,
    'G4':392,
    'G#4':415,
    'A4':440,
    'A#4':466,
    'B4':494,
    'C5':523,
    'C#5':554,
    'D5':587,
    'D#5':622,
    'E5':659,
    'F5':698,
    'F#5':740,
    'G5':784,
    'G#5':831,
    'A5':880,
    'A#5':932,
    'B5':988,
    'C6':1047,
    'C#6':1109,
    'D6':1175,
    'D#6':1245,
    'E6':1319,
    'F6':1397,
    'F#6':1480,
    'G6':1568,
    'G#6':1661,
    'A6':1760,
    'A#6':1865,
    'B6':1976,
    'C7':2093,
    'C#7':2217,
    'D7':2349,
    'D#7':2489,
    'E7':2637,
    'F7':2794,
    'F#7':2960,
    'G7':3136,
    'G#7':3322,
    'A7':3520,
    'A#7':3729,
    'B7':3951,
    'C8':4186,
    'C#8':4435,
    'D8':4699,
    'D#8':4978,
    'E8':5274,
    'F8':5588,
    'F#8':5920,
    'G8':6272,
    'G#8':6645,
    'A8':7040,
    'A#8':7459,
    'B8':7902,
    'C9':8372,
    'C#9':8870,
    'D9':9397,
    'D#9':9956,
    'E9':10548,
    'F9':11175,
    'F#9':11840,
    'G9':12544,
    'G#9':13290,
    'A9':14080,
    'A#9':14917,
    'B9':15804
}

# Define buzzer pin
buzzer_pin = 18
button1ID = 20
button2ID = 21
button3ID = 22

# Initialize buzzer with PWM on pin 18
buzzer = PWM(Pin(buzzer_pin))

# Define a function to play a single note
def play_note(frequency, duration_ms, song_chosen):
    if (current_song != song_chosen):
        return
    duration = 2
    duration /= int (duration_ms)
    buzzer.duty_u16(1000)  # Adjust duty cycle for volume (optional)
    buzzer.freq(frequency)
    utime.sleep(duration)
    buzzer.duty_u16(0)
    utime.sleep(0.05)
    silient()

def silient():
    buzzer.duty_u16(0)

# Define a simple song (replace with your desired melody)
# the digit is the length of each note, as the divisor to 1
song1 = ['E5', 8,'D5',8,'C5',8,'D5',8,'E5',8, 'E5',8,'E5',4, 'D5',8, 'D5',8, 'D5',4,'E5',8, 'G5',8, 'G5',4,
         'E5', 8,'D5',8,'C5',8,'D5',8,'E5',8, 'E5',8,'E5',4, 'D5',8, 'D5',8,'E5',8, 'D5',8,   'C5',8]
song2 = ['G#4', 8,'D#5', 8,'D#5', 8,'D#5', 8,'F5', 8,'G#4', 8,'A#4', 8,'C5', 2,'C5', 2,'C5', 2,'C5', 8,'A#4',
          8,'G#4', 8,'C5', 2,'C5', 2,'C5', 2 ,'G#4', 8,'A#4', 8,'C5',8 ,'C#5',4, 'C#5',8, 'C5',4,'A#4', 8, 'A#4', 8,
            'G#4', 4, 'G#4', 8, 'A#4', 8 , 'C5', 8, 'A#4', 4 ]
song3 = ['G4', 8, 'F4', 8, 'G4', 8, 'A#3', 4, 'A#4', 8, 'F4', 8, 'G#4', 8,'G4', 4,'F4', 4 , 'D#4', 2,
         'G#4', 8,'G4', 8,'G#4', 8, 'C4', 4,  'A#4', 8, 'G#4', 8, 'G4',8, 'G4',4, 'G#4', 4,'G4',16, 'D#4', 16 ,
         'G4',4, 'F4',4  ]

def playsong(notes, length,song_chosen):
    for i in range(len(notes)):
        if (notes[i] == "P"):
            silient()
        else:
            play_note(notes[i],length[i], song_chosen)
    silient()

def chooseSong(song_chosen):
    note = []
    length = []
    for i in range(len(song_chosen)):
        if i == 0 or i % 2 == 0:
            note.append(song_chosen[i])
        else:
            length.append( song_chosen[i])
    newTone = []
    for i in note:
        newTone.append(tones[i])

    playsong(newTone, length,song_chosen)
    silient()
    utime.sleep(0.5)

button1 = Pin(button1ID, Pin.IN)
button2 = Pin(button2ID, Pin.IN)
button3 = Pin(button3ID, Pin.IN)

def setSong(pin):
    global current_song
    if (button1() == 0):
        current_song = song1
    if (button2() == 0):
        current_song = song2
    if (button3() == 0):
        current_song = song3
button1.irq(setSong,trigger= Pin.IRQ_FALLING)
button2.irq(setSong,trigger= Pin.IRQ_FALLING)
button3.irq(setSong,trigger= Pin.IRQ_FALLING)
    

current_song = []
while (1):
    chooseSong(current_song)




