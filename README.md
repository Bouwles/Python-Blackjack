# Blackjack (Python + Tkinter)

A desktop Blackjack game built with Python using the Tkinter GUI toolkit.  
The project includes animated card dealing, a custom-drawn card system, and a casino-style interface.


---

## Features

- Complete Blackjack game logic
- Smooth card dealing animations
- Custom card rendering using Tkinter Canvas
- Dealer hole card with flip reveal
- Automatic Ace value handling (1 or 11)
- Real-time score display
- Dealer stands on 17
- Automatic deck reshuffle when cards run low
- Clean casino-style interface

---

## Requirements

- Python 3.8 or higher
- Tkinter (included with most Python installations)

No external dependencies are required.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/blackjack-python.git
cd blackjack-python
```

Run the program:

```bash
python blackjack.py
```

---

## Project Structure

```
blackjack/
│
├── blackjack.py
└── README.md
```

---

## Game Rules

This implementation follows standard Blackjack rules:

- Number cards are worth their face value
- Face cards (J, Q, K) are worth 10
- Aces count as 11 or 1 depending on the hand
- Dealer stands on 17
- Player may choose to Hit or Stand
- Busting (going over 21) results in an immediate loss

Possible outcomes include:

- Blackjack
- Dealer Blackjack
- Bust
- Dealer Bust
- Win
- Loss
- Push (tie)

---

## Implementation Notes

### Card System

Cards are drawn dynamically using the Tkinter Canvas rather than image assets.  
Each card is represented by a `Card` class that handles:

- rendering
- animation
- hidden state
- flipping

### Deck Handling

A standard 52-card deck is generated and shuffled.

```python
def make_deck():
    d = [(r, s) for s in SUITS for r in RANKS]
    random.shuffle(d)
    return d
```

### Score Calculation

The score function automatically adjusts Ace values to avoid unnecessary busts.

```python
while t > 21 and aces:
    t -= 10
```

### Animations

Cards slide onto the table using an easing function to create a smooth dealing animation.

---

## Running the Game

When the program launches:

1. Click **DEAL** to start a round.
2. Choose **HIT** to draw another card.
3. Choose **STAND** to end your turn and allow the dealer to play.

The result will be displayed once the round finishes.
