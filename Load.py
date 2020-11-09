from MCP23S17 import MCP23S17
from modules.Led import Led
from modules.Taster import Taster
from modules.Database import Database
from modules.Database import Executor
import time
import math


class Worker:

    def __init__(self, blink_ms):
        self.player_name = input("Please enter player name: ")
        self.blink_ms = blink_ms
        self.chip = MCP23S17(0x20, 0, 0)
        self.taster = Taster(self.chip, "B", 0)
        self.leds = []
        for i in range(0, 8): self.leds.append(Led(self.chip, "A", i)); i += 1
        self.game_state = 0
        self.db = Database("admin", "password", "highscores")
        self.exec = Executor(self.db)

    def run(self):
        try:
            self.chip.write_config("A", 0b00000000)
            self.chip.write_config("B", 0b00000001)
            
            while self.game_state < 8:
                ### start ###
                playing = True
                lost = False
                while playing:
                    self.leds[self.game_state].switch(True)
                    passed = time.time() + self.blink_ms
                    while time.time() < passed:
                        if self.taster.state():
                            playing = False
                    if playing:
                        self.leds[self.game_state].switch(False)
                        passed = time.time() + self.blink_ms
                        while time.time() < passed:
                            if self.taster.state():
                                playing = False
                                lost = True
                ### End ###
                if not lost:
                    for index in range(self.game_state+1):
                        if not self.leds[index].state():
                            self.leds[index].switch(True)
                            print(index)
                    time.sleep(1)
                    self.game_state += 1
                else:
                    print("You have Lost!")
                    for led in self.leds:
                        led.switch(True)
                    time.sleep(.4)
                    for led in self.leds:
                        led.switch(False)
                    time.sleep(.4)
                    for led in self.leds:
                        led.switch(True)
                    time.sleep(.4)
                    for led in self.leds:
                        led.switch(False)
                    time.sleep(.4)
                    for led in self.leds:
                        led.switch(True)
                    time.sleep(.5)
                    break
            self.exec.saveScore(self.player_name, self.game_state)
            print("Your highscore is: " + str(self.game_state))

            for col in self.exec.getScores():
                print(str(col[0]) + ", " + col[1] + ", " + str(col[2]))
                
            self.cleanup()

        except KeyboardInterrupt:
            self.cleanup()
            self.db.close()
            print("\nProgramm beendet")

    def cleanup(self):
        self.chip.write_config("A", 0)
        self.chip.write_output("A", 0)
        self.chip.write_config("B", 0)
        self.chip.write_output("B", 0)

def main():
    w = Worker(.5)
    w.run()

if __name__ == "__main__":
    main()