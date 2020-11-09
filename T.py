from MCP23S17 import MCP23S17
from modules.Database import Database
from modules.Database import Executor
import time


class Worker:

    def __init__(self):
        self.mcp = MCP23S17(0x20, 0, 0)

    def run(self):
        self.mcp.write_config("B", 0b10000000)
        self.mcp.write_config("A", 0b00000000)
        try:
            self.db = Database("admin", "password", "highscores")
            self.exec = Executor(self.db)
            self.exec.saveScore("natalie", 20)

            print("id, name, highscore")
            for col in self.exec.getScores():
                print(str(col[0]) + ", " + col[1] + ", " + str(col[2]))
            
        except KeyboardInterrupt:
            self.cleanup()
            print("\nProgramm beendet")

    def cleanup(self):
        self.mcp.write_config("A", 0)
        self.mcp.write_output("A", 0)

def main():
    w = Worker()
    w.run()

if __name__ == "__main__":
    main()