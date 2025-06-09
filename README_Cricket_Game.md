# Mini Cricket Head-Tail Game

A complete cricket simulation game built with Python's tkinter library.

## Features

### Game Modes
- **vs Computer**: Play against AI opponent
- **vs Player**: Play against another human player

### Team Selection
- Choose from 4 international teams:
  - India
  - Australia  
  - England
  - Pakistan
- Each team has 11 realistic player names

### Game Flow
1. **Main Menu**: Choose game mode (vs Computer or vs Player)
2. **Team Selection**: Select your team and opponent team
3. **Toss**: Head/Tail selection determines who wins the toss
4. **Choice**: Toss winner chooses to bat or bowl first
5. **First Innings**: Team bats while other bowls
6. **Second Innings**: Teams switch roles, chasing target
7. **Game Over**: Results and statistics displayed

### Gameplay Mechanics
- **Batting**: Click numbers 1-6 to choose your shot
- **Bowling**: Click numbers 1-6 to choose your bowling delivery
- **Getting Out**: If batting and bowling numbers match, batsman is OUT
- **Scoring**: If numbers don't match, batsman scores runs equal to chosen number
- **Innings**: Each team gets 10 wickets (players can get out)

### Visual Effects
- **Four (4 runs)**: Greenish-yellow glowing effect with "+4 FOUR!" text
- **Six (6 runs)**: Green glowing effect with "+6 SIX!" text  
- **Other runs**: White text showing "+X" runs
- **Wickets**: Red "OUT!" or "WICKET!" text

### Score Display
- Current player name and individual score
- Team total score and wickets lost
- Target information during chase
- Real-time score updates

### Game States
- Professional UI with cricket-themed colors
- Responsive layout that works on different screen sizes
- Clear navigation between game phases
- Comprehensive game statistics

## How to Run

1. Make sure you have Python installed with tkinter (usually included)
2. Run the game:
   ```bash
   python cricket_game.py
   ```
3. Follow the on-screen instructions to play

## Game Rules

1. **Toss**: Choose Head or Tail, winner decides to bat or bowl first
2. **Batting**: Select a number 1-6 for your shot
3. **Bowling**: Opponent/Computer selects a number 1-6 
4. **Out Condition**: If both numbers match, batsman is OUT
5. **Scoring**: If numbers don't match, batsman scores the chosen number
6. **Innings End**: When 10 players are out or all players have batted
7. **Winning**: Team with higher total score wins
8. **Chase**: Second batting team needs to score more than target

## Code Structure

The game is built with object-oriented design:

- **CricketGame**: Main game controller and UI manager
- **Team**: Represents a cricket team with players and score
- **Player**: Individual player with name and personal score  
- **GameState**: Enum for different game phases
- **Modular Functions**: Separate methods for each game phase

## Technical Features

- Clean, commented code for easy understanding
- Error handling for invalid inputs
- Proper game state management
- Visual feedback with animations
- Responsive UI design
- Professional color scheme
