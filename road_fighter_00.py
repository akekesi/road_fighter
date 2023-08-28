import copy
import time
import random
import customtkinter


class RoadFighter(customtkinter.CTk):
    speed = 1
    time = time.time()
    score = 0
    score_pos = "+"
    score_neg = "-"

    after_id_game = None
    after_id_time = None

    road_l = list("XX|")
    road_r = copy.deepcopy(road_l)
    road_r.reverse()
    road_m = list("  |  ")
    road_line = road_l + road_m + road_r

    road = []
    for i in range(10):
        road.append(copy.deepcopy(road_line))

    car_idx = len(road_l) + len(road_m) - 1
    car = "↑"

    padx_grid = 10
    pady_grid = 10

    def __init__(self):
        super().__init__()

        # attributes
        self.title("Road Fighter")
        self.resizable(0,0)

        # frame - textbox
        self.frame_textbox = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_textbox.grid(row=0, column=0, padx=self.padx_grid, pady=(self.pady_grid, 0))

        self.textbox = customtkinter.CTkTextbox(self.frame_textbox, width=105, height=190, activate_scrollbars=False, autoseparators=True, font=("Courier", 14), state="disabled", border_width=2, border_color="#565B5E")
        self.textbox.grid(row=0, column=0, sticky="nsew")

        # frame - info
        self.frame_info = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_info.grid(row=1, column=0, padx=self.padx_grid, pady=(self.pady_grid, 0))

        self.entry_speed = customtkinter.CTkEntry(self.frame_info, width=105, state="disabled", justify="right")
        self.entry_speed.grid(row=0, column=0, padx=0, pady=0)
        self.entry_time = customtkinter.CTkEntry(self.frame_info, width=105, state="disabled", justify="right")
        self.entry_time.grid(row=1, column=0, padx=0, pady=1)
        self.entry_score = customtkinter.CTkEntry(self.frame_info, width=105, state="disabled", justify="right")
        self.entry_score.grid(row=2, column=0, padx=0, pady=0)

        # frame - buttons
        self.frame_buttons = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_buttons.grid(row=2, column=0, padx=self.padx_grid, pady=self.pady_grid)

        self.button_up = customtkinter.CTkButton(self.frame_buttons, text="↑", width=35, command=lambda event=None: self.up(event))
        self.button_up.grid(row=0, column=1, sticky="ew")
        self.button_left = customtkinter.CTkButton(self.frame_buttons, text="←", width=35, command=lambda event=None: self.left(event))
        self.button_left.grid(row=1, column=0, sticky="ew")
        self.button_right = customtkinter.CTkButton(self.frame_buttons, text="→", width=35, command=lambda event=None: self.right(event))
        self.button_right.grid(row=1, column=2, sticky="ew")
        self.button_down = customtkinter.CTkButton(self.frame_buttons, text="↓", width=35, command=lambda event=None: self.down(event))
        self.button_down.grid(row=2, column=1, sticky="ew")

        # click
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.bind("<Left>", self.left)
        self.bind("<Right>", self.right)

        # init functions
        self.show()
        self.set_speed()
        self.set_time()
        self.set_score()

    def game(self):
        self.move()
        self.show()
        delay = int(1000 / self.speed)
        self.after_id_game = self.after(delay, self.game)
        print("game")

    def up(self, event):
        self.speed = min(10, self.speed + 0.5)
        self.set_speed()
        print(f"up")

    def down(self, event):
        self.speed = max(1, self.speed - 0.5)
        self.set_speed()
        print(f"down")

    def left(self, event):
        car_pre = self.car_idx
        self.car_idx = max(len(self.road_l), self.car_idx - 1)
        if self.road[8][self.car_idx] == self.score_pos:
            self.score += 1
            self.set_score()
        if self.road[8][self.car_idx] == self.score_neg:
            self.score -= 1
            self.set_score()
        self.road[8][car_pre] = self.road_line[car_pre]
        self.road[8][self.car_idx] = self.car
        self.show()
        print("left")

    def right(self, event):
        car_pre = self.car_idx
        self.car_idx = min(len(self.road_l) + len(self.road_m) - 1, self.car_idx + 1)
        if self.road[8][self.car_idx] == self.score_pos:
            self.score += 1
            self.set_score()
        if self.road[8][self.car_idx] == self.score_neg:
            self.score -= 1
            self.set_score()
        self.road[8][car_pre] = self.road_line[car_pre]
        self.road[8][self.car_idx] = self.car
        self.show()
        print("right")

    def set_speed(self):
        self.entry_speed.configure(state="normal")
        self.entry_speed.delete(0, "end")
        self.entry_speed.insert(0, f"{int(20*self.speed)} km/h")
        self.entry_speed.configure(state="disabled")

    def set_time(self):
        self.entry_time.configure(state="normal")
        self.entry_time.delete(0, "end")
        self.entry_time.insert(0, f"{(time.time() - self.time):.1f} sec")
        self.after_id_time = self.after(100, self.set_time)
        self.entry_time.configure(state="disabled")

    def set_score(self):
        # if self.score > 1:
        #     self.after_cancel(self.after_id_game) # <-- does not work ?!?!?
        #     self.after_cancel(self.after_id_time)
        #     return
        self.entry_score.configure(state="normal")
        self.entry_score.delete(0, "end")
        self.entry_score.insert(0, f"{100*self.score} $")
        self.entry_score.configure(state="disabled")

    def show(self):
        self.textbox.configure(state="normal")
        self.textbox.delete(0.0,"end")
        for r in self.road:
            self.textbox.insert("end", "".join(r))
        self.textbox.configure(state="disabled")
        print("show")

    def move(self):
        if self.road[7][self.car_idx] == self.score_pos:
            self.score += 1
            self.set_score()
        if self.road[7][self.car_idx] == self.score_neg:
            self.score -= 1
            self.set_score()
        new = copy.deepcopy(self.road_line)
        if not (random.randint(1, 4) % 4):
            if not (random.randint(1, 2) % 2):
                new[random.randint(len(self.road_l), len(self.road_l) + len(self.road_m) - 1)] = self.score_pos
            else:
                new[random.randint(len(self.road_l), len(self.road_l) + len(self.road_m) - 1)] = self.score_neg
        self.road.insert(0, new)
        self.road[8][self.car_idx] = self.car
        self.road[9][self.car_idx] = self.road_line[self.car_idx]
        self.road.pop()
        print("move")


if __name__ == "__main__":
    # RoadFighter()
    customtkinter.set_appearance_mode("dark")
    app = RoadFighter()
    app.game()
    app.mainloop()
