import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

class CricketGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mini Cricket Head-Tail Game")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e3a8a")
        
        # Game state variables
        self.game_mode = None  # "computer" or "player"
        self.teams = {
            "India": ["Rohit", "Virat", "Dhoni", "Hardik", "Jadeja", "Bumrah", "Shami", "Kuldeep", "Rahul", "Pant", "Iyer"],
            "Australia": ["Warner", "Smith", "Finch", "Maxwell", "Stoinis", "Starc", "Hazlewood", "Lyon", "Carey", "Labuschagne", "Zampa"],
            "England": ["Root", "Stokes", "Butler", "Morgan", "Bairstow", "Archer", "Broad", "Anderson", "Woakes", "Rashid", "Moeen"],
            "Pakistan": ["Babar", "Rizwan", "Fakhar", "Hafeez", "Shadab", "Shaheen", "Hasan", "Wasim", "Haris", "Azam", "Nawaz"]
        }
        
        self.player1_team = None
        self.player2_team = None
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        
        # Game variables
        self.toss_winner = None
        self.batting_first = None
        self.current_innings = 1
        self.current_batsman_index = 0
        self.player1_score = 0
        self.player2_score = 0
        self.player1_wickets = 0
        self.player2_wickets = 0
        self.current_player_score = 0
        self.target = 0
        self.is_batting = True
        
        # Player scores tracking
        self.player1_individual_scores = [0] * 11
        self.player2_individual_scores = [0] * 11
        
        self.setup_main_menu()
        
    def setup_main_menu(self):
        """Setup the main menu interface"""
        self.clear_screen()
        
        # Title
        title_label = tk.Label(self.root, text="Mini Cricket Head-Tail Game", 
                              font=("Arial", 24, "bold"), fg="white", bg="#1e3a8a")
        title_label.pack(pady=50)
        
        # Game mode selection
        mode_frame = tk.Frame(self.root, bg="#1e3a8a")
        mode_frame.pack(pady=30)
        
        tk.Label(mode_frame, text="Select Game Mode:", 
                font=("Arial", 16), fg="white", bg="#1e3a8a").pack(pady=10)
        
        computer_btn = tk.Button(mode_frame, text="VS Computer", 
                                font=("Arial", 14), bg="#22c55e", fg="white",
                                command=lambda: self.set_game_mode("computer"),
                                width=15, height=2)
        computer_btn.pack(pady=10)
        
        player_btn = tk.Button(mode_frame, text="VS Player", 
                              font=("Arial", 14), bg="#3b82f6", fg="white",
                              command=lambda: self.set_game_mode("player"),
                              width=15, height=2)
        player_btn.pack(pady=10)
        
    def set_game_mode(self, mode):
        """Set the game mode and proceed to team selection"""
        self.game_mode = mode
        if mode == "computer":
            self.player2_name = "Computer"
        self.setup_team_selection()
        
    def setup_team_selection(self):
        """Setup team selection interface"""
        self.clear_screen()
        
        # Title
        title_label = tk.Label(self.root, text="Select Teams", 
                              font=("Arial", 20, "bold"), fg="white", bg="#1e3a8a")
        title_label.pack(pady=30)
        
        # Team selection frame
        selection_frame = tk.Frame(self.root, bg="#1e3a8a")
        selection_frame.pack(pady=20)
        
        # Player 1 team selection
        p1_frame = tk.Frame(selection_frame, bg="#1e3a8a")
        p1_frame.pack(side=tk.LEFT, padx=50)
        
        tk.Label(p1_frame, text=f"{self.player1_name} - Select Team:", 
                font=("Arial", 14), fg="white", bg="#1e3a8a").pack(pady=10)
        
        self.p1_team_var = tk.StringVar()
        for team in self.teams.keys():
            tk.Radiobutton(p1_frame, text=team, variable=self.p1_team_var, value=team,
                          font=("Arial", 12), fg="white", bg="#1e3a8a",
                          selectcolor="#3b82f6").pack(anchor=tk.W)
        
        # Player 2 team selection
        p2_frame = tk.Frame(selection_frame, bg="#1e3a8a")
        p2_frame.pack(side=tk.RIGHT, padx=50)
        
        tk.Label(p2_frame, text=f"{self.player2_name} - Select Team:", 
                font=("Arial", 14), fg="white", bg="#1e3a8a").pack(pady=10)
        
        self.p2_team_var = tk.StringVar()
        for team in self.teams.keys():
            tk.Radiobutton(p2_frame, text=team, variable=self.p2_team_var, value=team,
                          font=("Arial", 12), fg="white", bg="#1e3a8a",
                          selectcolor="#3b82f6").pack(anchor=tk.W)
        
        # Continue button
        continue_btn = tk.Button(self.root, text="Continue to Toss", 
                                font=("Arial", 14), bg="#22c55e", fg="white",
                                command=self.validate_teams, width=20, height=2)
        continue_btn.pack(pady=30)
        
    def validate_teams(self):
        """Validate team selection and proceed to toss"""
        self.player1_team = self.p1_team_var.get()
        self.player2_team = self.p2_team_var.get()
        
        if not self.player1_team or not self.player2_team:
            messagebox.showerror("Error", "Please select teams for both players!")
            return
            
        if self.player1_team == self.player2_team:
            messagebox.showerror("Error", "Please select different teams!")
            return
            
        self.setup_toss()
        
    def setup_toss(self):
        """Setup toss interface"""
        self.clear_screen()
        
        # Title
        title_label = tk.Label(self.root, text="Toss Time!", 
                              font=("Arial", 20, "bold"), fg="white", bg="#1e3a8a")
        title_label.pack(pady=30)
        
        # Teams display
        teams_label = tk.Label(self.root, text=f"{self.player1_team} vs {self.player2_team}", 
                              font=("Arial", 16), fg="yellow", bg="#1e3a8a")
        teams_label.pack(pady=20)
        
        # Toss instruction
        instruction_label = tk.Label(self.root, text=f"{self.player1_name}, call Heads or Tails:", 
                                    font=("Arial", 14), fg="white", bg="#1e3a8a")
        instruction_label.pack(pady=20)
        
        # Toss buttons
        toss_frame = tk.Frame(self.root, bg="#1e3a8a")
        toss_frame.pack(pady=20)
        
        heads_btn = tk.Button(toss_frame, text="HEADS", 
                             font=("Arial", 14), bg="#fbbf24", fg="black",
                             command=lambda: self.perform_toss("heads"),
                             width=10, height=2)
        heads_btn.pack(side=tk.LEFT, padx=20)
        
        tails_btn = tk.Button(toss_frame, text="TAILS", 
                             font=("Arial", 14), bg="#f87171", fg="white",
                             command=lambda: self.perform_toss("tails"),
                             width=10, height=2)
        tails_btn.pack(side=tk.RIGHT, padx=20)
        
    def perform_toss(self, call):
        """Perform the toss and determine winner"""
        coin_result = random.choice(["heads", "tails"])
        
        if call == coin_result:
            self.toss_winner = "player1"
            winner_text = f"{self.player1_name} wins the toss!"
        else:
            self.toss_winner = "player2"
            winner_text = f"{self.player2_name} wins the toss!"
        
        # Show toss result
        messagebox.showinfo("Toss Result", f"Coin shows: {coin_result.upper()}\n{winner_text}")
        self.setup_batting_choice()
        
    def setup_batting_choice(self):
        """Setup batting choice for toss winner"""
        self.clear_screen()
        
        winner_name = self.player1_name if self.toss_winner == "player1" else self.player2_name
        
        # Title
        title_label = tk.Label(self.root, text=f"{winner_name} won the toss!", 
                              font=("Arial", 18, "bold"), fg="yellow", bg="#1e3a8a")
        title_label.pack(pady=30)
        
        # Choice instruction
        choice_label = tk.Label(self.root, text="Choose to Bat or Bowl first:", 
                               font=("Arial", 14), fg="white", bg="#1e3a8a")
        choice_label.pack(pady=20)
        
        # Choice buttons
        choice_frame = tk.Frame(self.root, bg="#1e3a8a")
        choice_frame.pack(pady=30)
        
        bat_btn = tk.Button(choice_frame, text="BAT FIRST", 
                           font=("Arial", 14), bg="#22c55e", fg="white",
                           command=lambda: self.set_batting_order("bat"),
                           width=12, height=2)
        bat_btn.pack(side=tk.LEFT, padx=20)
        
        bowl_btn = tk.Button(choice_frame, text="BOWL FIRST", 
                            font=("Arial", 14), bg="#ef4444", fg="white",
                            command=lambda: self.set_batting_order("bowl"),
                            width=12, height=2)
        bowl_btn.pack(side=tk.RIGHT, padx=20)
        
    def set_batting_order(self, choice):
        """Set who bats first based on toss winner's choice"""
        if choice == "bat":
            self.batting_first = self.toss_winner
        else:
            self.batting_first = "player2" if self.toss_winner == "player1" else "player1"
        
        self.setup_game_interface()
        
    def setup_game_interface(self):
        """Setup the main game interface"""
        self.clear_screen()
        
        # Determine current batting team
        if self.current_innings == 1:
            current_batting = self.batting_first
        else:
            current_batting = "player2" if self.batting_first == "player1" else "player1"
        
        # Score display frame
        score_frame = tk.Frame(self.root, bg="#1e3a8a")
        score_frame.pack(pady=10, fill=tk.X)
        
        # Team scores
        p1_score_text = f"{self.player1_team}: {self.player1_score}/{self.player1_wickets}"
        p2_score_text = f"{self.player2_team}: {self.player2_score}/{self.player2_wickets}"
        
        tk.Label(score_frame, text=p1_score_text, font=("Arial", 14, "bold"), 
                fg="white", bg="#1e3a8a").pack(side=tk.LEFT, padx=20)
        
        tk.Label(score_frame, text=p2_score_text, font=("Arial", 14, "bold"), 
                fg="white", bg="#1e3a8a").pack(side=tk.RIGHT, padx=20)
        
        # Current innings info
        innings_text = f"Innings {self.current_innings}"
        if self.current_innings == 2:
            innings_text += f" - Target: {self.target + 1}"
        
        tk.Label(self.root, text=innings_text, font=("Arial", 12), 
                fg="yellow", bg="#1e3a8a").pack(pady=5)
        
        # Current batsman info
        if current_batting == "player1":
            current_team = self.teams[self.player1_team]
            batsman_name = current_team[self.current_batsman_index]
            current_score = self.player1_individual_scores[self.current_batsman_index]
        else:
            current_team = self.teams[self.player2_team]
            batsman_name = current_team[self.current_batsman_index]
            current_score = self.player2_individual_scores[self.current_batsman_index]
        
        batsman_info = f"Current Batsman: {batsman_name} - {current_score} runs"
        self.batsman_label = tk.Label(self.root, text=batsman_info, font=("Arial", 14, "bold"), 
                                     fg="lime", bg="#1e3a8a")
        self.batsman_label.pack(pady=10)
        
        # Game action area
        self.setup_game_actions(current_batting)
        
    def setup_game_actions(self, batting_team):
        """Setup game action buttons based on current situation"""
        # Clear previous action frame if exists
        if hasattr(self, 'action_frame'):
            self.action_frame.destroy()
        
        self.action_frame = tk.Frame(self.root, bg="#1e3a8a")
        self.action_frame.pack(pady=20)
        
        # Determine if human player is batting
        if (batting_team == "player1") or (batting_team == "player2" and self.game_mode == "player"):
            self.setup_batting_interface()
        else:
            # Computer is batting
            self.setup_bowling_interface()
        
    def setup_batting_interface(self):
        """Setup interface when human player is batting"""
        tk.Label(self.action_frame, text="Select your shot (1-6):", 
                font=("Arial", 14), fg="white", bg="#1e3a8a").pack(pady=10)
        
        # Batting buttons
        buttons_frame = tk.Frame(self.action_frame, bg="#1e3a8a")
        buttons_frame.pack(pady=10)
        
        for i in range(1, 7):
            btn = tk.Button(buttons_frame, text=str(i), font=("Arial", 16, "bold"),
                           width=3, height=2, bg="#3b82f6", fg="white",
                           command=lambda run=i: self.player_bats(run))
            btn.pack(side=tk.LEFT, padx=5)
    
    def setup_bowling_interface(self):
        """Setup interface when human player is bowling"""
        tk.Label(self.action_frame, text="Select your bowl (1-6):", 
                font=("Arial", 14), fg="white", bg="#1e3a8a").pack(pady=10)
        
        # Bowling buttons
        buttons_frame = tk.Frame(self.action_frame, bg="#1e3a8a")
        buttons_frame.pack(pady=10)
        
        for i in range(1, 7):
            btn = tk.Button(buttons_frame, text=str(i), font=("Arial", 16, "bold"),
                           width=3, height=2, bg="#ef4444", fg="white",
                           command=lambda bowl=i: self.player_bowls(bowl))
            btn.pack(side=tk.LEFT, padx=5)
    
    def player_bats(self, run):
        """Handle when player bats"""
        # Generate opponent's bowling number
        if self.game_mode == "computer":
            bowl_number = random.randint(1, 6)
        else:
            # In player vs player, generate random for opponent
            bowl_number = random.randint(1, 6)
        
        self.process_batting_result(run, bowl_number)
    
    def player_bowls(self, bowl):
        """Handle when player bowls (computer is batting)"""
        # Computer selects batting number
        bat_number = random.randint(1, 6)
        self.process_batting_result(bat_number, bowl)
    
    def process_batting_result(self, bat_number, bowl_number):
        """Process the result of batting vs bowling"""
        # Determine current batting team
        if self.current_innings == 1:
            current_batting = self.batting_first
        else:
            current_batting = "player2" if self.batting_first == "player1" else "player1"
        
        result_text = f"Bat: {bat_number}, Bowl: {bowl_number}\n"
        
        if bat_number == bowl_number:
            # OUT!
            result_text += "OUT!"
            self.show_result_effect(result_text, "#ef4444")  # Red for out
            
            if current_batting == "player1":
                self.player1_wickets += 1
            else:
                self.player2_wickets += 1
            
            self.current_batsman_index += 1
            self.current_player_score = 0
            
        else:
            # Runs scored
            result_text += f"+{bat_number} runs"
            
            if current_batting == "player1":
                self.player1_score += bat_number
                self.player1_individual_scores[self.current_batsman_index] += bat_number
            else:
                self.player2_score += bat_number
                self.player2_individual_scores[self.current_batsman_index] += bat_number
            
            # Show effect based on runs
            if bat_number == 4:
                self.show_result_effect(result_text, "#84cc16")  # Green-yellow for 4
            elif bat_number == 6:
                self.show_result_effect(result_text, "#22c55e")  # Green for 6
            else:
                self.show_result_effect(result_text, "#3b82f6")  # Blue for other runs
        
        # Check game conditions
        self.check_game_status()
    
    def show_result_effect(self, text, color):
        """Show result with color effect"""
        # Create overlay for effect
        overlay = tk.Toplevel(self.root)
        overlay.geometry("300x150")
        overlay.configure(bg=color)
        overlay.overrideredirect(True)
        
        # Center the overlay
        x = self.root.winfo_x() + self.root.winfo_width()//2 - 150
        y = self.root.winfo_y() + self.root.winfo_height()//2 - 75
        overlay.geometry(f"300x150+{x}+{y}")
        
        # Result text
        tk.Label(overlay, text=text, font=("Arial", 16, "bold"), 
                fg="white", bg=color).pack(expand=True)
        
        # Auto-close after 1.5 seconds
        self.root.after(1500, overlay.destroy)
        self.root.after(1600, self.update_game_display)
    
    def update_game_display(self):
        """Update the game display after each ball"""
        # Check if innings should end
        if self.should_end_innings():
            self.end_innings()
        else:
            self.setup_game_interface()
    
    def should_end_innings(self):
        """Check if current innings should end"""
        if self.current_innings == 1:
            current_batting = self.batting_first
        else:
            current_batting = "player2" if self.batting_first == "player1" else "player1"
        
        # Check wickets
        if current_batting == "player1":
            if self.player1_wickets >= 10:
                return True
        else:
            if self.player2_wickets >= 10:
                return True
        
        # Check if target is chased in second innings
        if self.current_innings == 2:
            if current_batting == "player1":
                if self.player1_score > self.target:
                    return True
            else:
                if self.player2_score > self.target:
                    return True
        
        return False
    
    def end_innings(self):
        """End current innings and proceed"""
        if self.current_innings == 1:
            # Set target for second innings
            if self.batting_first == "player1":
                self.target = self.player1_score
            else:
                self.target = self.player2_score
            
            self.current_innings = 2
            self.current_batsman_index = 0
            self.current_player_score = 0
            
            # Show innings break
            messagebox.showinfo("Innings Break", 
                              f"First innings complete!\nTarget: {self.target + 1} runs")
            
            self.setup_game_interface()
        else:
            # Game over
            self.show_game_result()
    
    def check_game_status(self):
        """Check if game should end"""
        # This is called after each ball, but actual checking is done in should_end_innings
        pass
    
    def show_game_result(self):
        """Show final game result"""
        self.clear_screen()
        
        # Title
        tk.Label(self.root, text="GAME OVER!", font=("Arial", 24, "bold"), 
                fg="yellow", bg="#1e3a8a").pack(pady=30)
        
        # Final scores
        score_frame = tk.Frame(self.root, bg="#1e3a8a")
        score_frame.pack(pady=20)
        
        p1_final = f"{self.player1_team}: {self.player1_score}/{self.player1_wickets}"
        p2_final = f"{self.player2_team}: {self.player2_score}/{self.player2_wickets}"
        
        tk.Label(score_frame, text=p1_final, font=("Arial", 16, "bold"), 
                fg="white", bg="#1e3a8a").pack(pady=5)
        tk.Label(score_frame, text=p2_final, font=("Arial", 16, "bold"), 
                fg="white", bg="#1e3a8a").pack(pady=5)
        
        # Winner announcement
        if self.player1_score > self.player2_score:
            winner_text = f"{self.player1_team} WINS!"
            winner_color = "#22c55e"
        elif self.player2_score > self.player1_score:
            winner_text = f"{self.player2_team} WINS!"
            winner_color = "#22c55e"
        else:
            winner_text = "IT'S A TIE!"
            winner_color = "#fbbf24"
        
        tk.Label(self.root, text=winner_text, font=("Arial", 20, "bold"), 
                fg=winner_color, bg="#1e3a8a").pack(pady=30)
        
        # Play again button
        play_again_btn = tk.Button(self.root, text="PLAY AGAIN", 
                                  font=("Arial", 16), bg="#3b82f6", fg="white",
                                  command=self.restart_game, width=15, height=2)
        play_again_btn.pack(pady=20)
        
        # Exit button
        exit_btn = tk.Button(self.root, text="EXIT", 
                            font=("Arial", 16), bg="#ef4444", fg="white",
                            command=self.root.quit, width=15, height=2)
        exit_btn.pack(pady=10)
    
    def restart_game(self):
        """Restart the game"""
        # Reset all game variables
        self.game_mode = None
        self.player1_team = None
        self.player2_team = None
        self.toss_winner = None
        self.batting_first = None
        self.current_innings = 1
        self.current_batsman_index = 0
        self.player1_score = 0
        self.player2_score = 0
        self.player1_wickets = 0
        self.player2_wickets = 0
        self.current_player_score = 0
        self.target = 0
        self.player1_individual_scores = [0] * 11
        self.player2_individual_scores = [0] * 11
        
        # Return to main menu
        self.setup_main_menu()
    
    def clear_screen(self):
        """Clear all widgets from the screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def run(self):
        """Start the game"""
        self.root.mainloop()

# Create and run the game
if __name__ == "__main__":
    game = CricketGame()
    game.run()
