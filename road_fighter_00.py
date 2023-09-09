import copy
import time
import random
import customtkinter


class RoadFighter(customtkinter.CTk):
    win = 0
    first = 1
    speed = 1
    time = time.time()
    score = 0
    distance = 0
    score_max = 10

    after_id_time = None

    road_l = list("XX|")
    road_r = copy.deepcopy(road_l)
    road_r.reverse()
    road_m = list("  |  ")
    road_line = road_l + road_m + road_r
    road = []
    for i in range(10):
        road.append(copy.deepcopy(road_line))

    car_x = len(road_l) + len(road_m) - 1
    car_y = 8
    car = "↑"
    score_p = "+"
    score_n = "-"
    score_o = "X"
    score_w = "W"

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

        self.textbox = customtkinter.CTkTextbox(self.frame_textbox, width=160, height=250, activate_scrollbars=False, autoseparators=True, font=("Courier", 21), state="disabled", border_width=2, border_color="#565B5E")
        self.textbox.grid(row=0, column=0, sticky="nsew")

        # frame - info
        self.frame_info = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_info.grid(row=1, column=0, padx=self.padx_grid, pady=(self.pady_grid, 0))
        self.frame_info.grid_columnconfigure(1, weight=1)


        self.entry_speed = customtkinter.CTkLabel(self.frame_info, text="Speed:")
        self.entry_speed.grid(row=0, column=0, padx=(self.padx_grid, 0), pady=0, sticky="w")
        self.entry_time = customtkinter.CTkLabel(self.frame_info, text="Time:")
        self.entry_time.grid(row=1, column=0, padx=(self.padx_grid, 0), pady=0, sticky="w")
        self.entry_distance = customtkinter.CTkLabel(self.frame_info, text="Distance:")
        self.entry_distance.grid(row=2, column=0, padx=(self.padx_grid, 0), pady=0, sticky="w")
        self.entry_score = customtkinter.CTkLabel(self.frame_info, text="Score:")
        self.entry_score.grid(row=3, column=0, padx=(self.padx_grid, 0), pady=0, sticky="w")

        self.entry_speed = customtkinter.CTkEntry(self.frame_info, width=93, state="disabled", justify="right")
        self.entry_speed.grid(row=0, column=1, padx=self.padx_grid, pady=0, sticky="e")
        self.entry_time = customtkinter.CTkEntry(self.frame_info, width=93, state="disabled", justify="right")
        self.entry_time.grid(row=1, column=1, padx=self.padx_grid, pady=1)
        self.entry_distance = customtkinter.CTkEntry(self.frame_info, width=93, state="disabled", justify="right")
        self.entry_distance.grid(row=2, column=1, padx=self.padx_grid, pady=1)
        self.entry_score = customtkinter.CTkEntry(self.frame_info, width=93, state="disabled", justify="right")
        self.entry_score.grid(row=3, column=1, padx=self.padx_grid, pady=0)

        # frame - buttons
        self.frame_buttons = customtkinter.CTkFrame(self, fg_color="transparent")
        self.frame_buttons.grid(row=2, column=0, padx=self.padx_grid, pady=self.pady_grid)

        self.button_up = customtkinter.CTkButton(self.frame_buttons, text="↑", width=53, command=lambda event=None: self.up(event))
        self.button_up.grid(row=0, column=1, sticky="ew")
        self.button_left = customtkinter.CTkButton(self.frame_buttons, text="←", width=53, command=lambda event=None: self.left(event))
        self.button_left.grid(row=1, column=0, sticky="ew")
        self.button_right = customtkinter.CTkButton(self.frame_buttons, text="→", width=53, command=lambda event=None: self.right(event))
        self.button_right.grid(row=1, column=2, sticky="ew")
        self.button_down = customtkinter.CTkButton(self.frame_buttons, text="↓", width=53, command=lambda event=None: self.down(event))
        self.button_down.grid(row=2, column=1, sticky="ew")

        # click
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.bind("<Left>", self.left)
        self.bind("<Right>", self.right)
        self.bind("<Escape>", self.close)

        # init
        self.set_speed()
        self.set_time()
        self.set_distance()
        self.set_score()

    def game(self):
        if self.car_y < 0 or self.win < 0:
            return
        if self.win:
            self.move_win()
        else:
            self.move()
        self.show()
        delay = int(1000 / self.speed)
        self.after_id_game = self.after(delay, self.game)

        print("game")

    def show(self):
        self.textbox.configure(state="normal")
        self.textbox.delete(0.0,"end")
        for r in self.road:
            self.textbox.insert("end", "".join(r))
        self.textbox.configure(state="disabled")
        print("show")

    def up(self, event):
        self.speed = min(20, self.speed + 1)
        self.set_speed()
        print(f"up")

    def down(self, event):
        self.speed = max(1, self.speed - 1)
        self.set_speed()
        print(f"down")

    def left(self, event):
        if self.win:
            return
        car_pre = self.car_x
        self.car_x = max(len(self.road_l), self.car_x - 1)
        if self.road[self.car_y][self.car_x] == self.score_p:
            self.score += 1
            self.set_score()
        if self.road[self.car_y][self.car_x] == self.score_n:
            self.score -= 1
            self.set_score()
        if self.road[self.car_y][self.car_x] == self.score_o:
            self.win = -1
            self.road[self.car_y][self.car_x + 1] = "#"
            self.after_cancel(self.after_id_time)
            self.show()
            return
        self.road[self.car_y][car_pre] = self.road_line[car_pre]
        self.road[self.car_y][self.car_x] = self.car
        self.show()
        print("left")

    def right(self, event):
        if self.win:
            return
        car_pre = self.car_x
        self.car_x = min(len(self.road_l) + len(self.road_m) - 1, self.car_x + 1)
        if self.road[self.car_y][self.car_x] == self.score_p:
            self.score += 1
            self.set_score()
        if self.road[self.car_y][self.car_x] == self.score_n:
            self.score -= 1
            self.set_score()
        if self.road[self.car_y][self.car_x] == self.score_o:
            self.win = -1
            self.road[self.car_y][self.car_x - 1] = "#"
            self.after_cancel(self.after_id_time)
            self.show()
            return
        self.road[self.car_y][car_pre] = self.road_line[car_pre]
        self.road[self.car_y][self.car_x] = self.car
        self.show()
        print("right")

    def set_speed(self):
        if self.win:
            return
        self.entry_speed.configure(state="normal")
        self.entry_speed.delete(0, "end")
        self.entry_speed.insert(0, f"{self.speed} km/h")
        self.entry_speed.configure(state="disabled")

    def set_time(self):
        self.entry_time.configure(state="normal")
        self.entry_time.delete(0, "end")
        self.entry_time.insert(0, f"{(time.time() - self.time):.1f} sec")
        self.after_id_time = self.after(100, self.set_time)
        self.entry_time.configure(state="disabled")

    def set_distance(self):
        self.entry_distance.configure(state="normal")
        self.entry_distance.delete(0, "end")
        self.entry_distance.insert(0, f"{self.distance} m")
        self.entry_distance.configure(state="disabled")

    def set_score(self):
        self.entry_score.configure(state="normal")
        self.entry_score.delete(0, "end")
        self.entry_score.insert(0, f"{self.score} $")
        self.entry_score.configure(state="disabled")

    def move(self):
        self.distance += 1
        self.set_distance()
        if self.road[7][self.car_x] == self.score_w:
            self.score += 3
            self.set_score()
            self.after_cancel(self.after_id_time)
            self.win = 1
        if self.road[7][self.car_x] == self.score_p:
            self.score += 1
            self.set_score()
        if self.road[7][self.car_x] == self.score_n:
            self.score -= 1
            self.set_score()
        if self.road[7][self.car_x] == self.score_o:
            self.win = -1
            self.road[self.car_y][self.car_x] = "#"
            self.after_cancel(self.after_id_time)
            return
        new = copy.deepcopy(self.road_line)
        if self.score < self.score_max:
            if not (random.randint(1, 4) % 4):
                r = random.randint(1, 3) % 3
                if r == 0:
                    new[random.randint(len(self.road_l), len(self.road_l) + len(self.road_m) - 1)] = self.score_p
                if r == 1:
                    new[random.randint(len(self.road_l), len(self.road_l) + len(self.road_m) - 1)] = self.score_n
                if r == 2:
                    new[random.randint(len(self.road_l), len(self.road_l) + len(self.road_m) - 1)] = self.score_o
        if self.first and self.score == self.score_max:
            self.first = 0
            new[len(self.road_l):len(self.road_l) + len(self.road_m)] = len(self.road_m) * [self.score_o]
            new[random.randint(len(self.road_l), len(self.road_l) + len(self.road_m) - 1)] = self.score_w
        self.road.insert(0, new)
        self.road[self.car_y][self.car_x] = self.car
        self.road[9][self.car_x] = self.road_line[self.car_x]
        self.road.pop()
        print("move_game")

    def move_win(self):
        new = copy.deepcopy(self.road_line)
        self.road.insert(0, new)
        self.road[self.car_y + 1][self.car_x] = self.road_line[self.car_x]
        self.car_y -= 1
        self.road[self.car_y][self.car_x] = self.car
        self.road.pop()
        print("move_win")

    def close(self, event):
        self.destroy()
        print("close")


if __name__ == "__main__":
    # RoadFighter()
    customtkinter.set_appearance_mode("dark")
    app = RoadFighter()
    app.game()
    app.mainloop()
