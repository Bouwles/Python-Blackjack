import tkinter as tk
import random
import math

# Made by Paul Nercessian

BG        = "#0a0f1e"
FELT      = "#0d1f12"
FELT2     = "#112918"
GOLD      = "#d4a94a"
GOLD2     = "#f0c060"
WHITE     = "#f0ede6"
RED       = "#c0392b"
BLACK_C   = "#1a1a1a"
SOFT_WHT  = "#e8e4db"
SHADOW    = "#050a10"
GREEN_BTN = "#1a6b34"
BLUE_BTN  = "#1a3a6b"
TEXT_DIM  = "#6a8f6a"
LOSE_RED  = "#e05555"
WIN_GRN   = "#55e07a"

CW, CH = 80, 115   # card size

SUITS  = ["♠", "♥", "♦", "♣"]
RANKS  = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
VALS   = {r: (int(r) if r.isdigit() else (11 if r == "A" else 10)) for r in RANKS}


def make_deck():
    d = [(r, s) for s in SUITS for r in RANKS]
    random.shuffle(d)
    return d


def total(hand):
    t, aces = 0, 0
    for r, _ in hand:
        t += VALS[r]
        if r == "A":
            aces += 1
    while t > 21 and aces:
        t -= 10
        aces -= 1
    return t


class Card:
    """Animated card that slides in from a position."""
    def __init__(self, canvas, rank, suit, target_x, target_y, hidden=False):
        self.canvas   = canvas
        self.rank     = rank
        self.suit     = suit
        self.target_x = target_x
        self.target_y = target_y
        self.hidden   = hidden
        self.x        = target_x
        self.y        = -CH - 20   # start off screen top
        self.ids      = []
        self._draw()

    def _draw(self):
        for i in self.ids:
            try:
                self.canvas.delete(i)
            except Exception:
                pass
        self.ids = []
        x, y = self.x, self.y
        color = RED if self.suit in ("♥", "♦") else BLACK_C

        if self.hidden:
            s = self.canvas.create_rectangle(x+4, y+4, x+CW+4, y+CH+4,
                                              fill=SHADOW, outline="")
            b = self.canvas.create_rectangle(x, y, x+CW, y+CH,
                                              fill="#1c2a5e", outline="#3a4a8e", width=2)
            lines = []
            for off in range(-CH, CW + CH, 16):
                # clip line to card bounds so it never bleeds outside during animation
                lx1, ly1 = x + off,      y
                lx2, ly2 = x + off + CH, y + CH
                if lx1 < x:
                    t   = (x - lx1) / CH
                    ly1 = int(ly1 + t * CH)
                    lx1 = x
                if lx2 > x + CW:
                    t   = (lx2 - (x + CW)) / CH
                    ly2 = int(ly2 - t * CH)
                    lx2 = x + CW
                if lx1 >= lx2:
                    continue
                ln = self.canvas.create_line(lx1, ly1, lx2, ly2,
                                             fill="#223070", width=1)
                lines.append(ln)
            inner = self.canvas.create_rectangle(x+8, y+8, x+CW-8, y+CH-8,
                                                  outline="#2a3a7e", fill="", width=1)
            self.ids = [s, b] + lines + [inner]
            return

        s  = self.canvas.create_rectangle(x+4, y+4, x+CW+4, y+CH+4,
                                           fill=SHADOW, outline="")
        bg = self.canvas.create_rectangle(x, y, x+CW, y+CH,
                                          fill=SOFT_WHT, outline="#cccccc", width=1)
        tl_r = self.canvas.create_text(x+9,  y+13, text=self.rank,
                                        font=("Helvetica", 12, "bold"), fill=color, anchor="w")
        tl_s = self.canvas.create_text(x+9,  y+28, text=self.suit,
                                        font=("Helvetica", 12),          fill=color, anchor="w")
        ctr  = self.canvas.create_text(x+CW//2, y+CH//2, text=self.suit,
                                        font=("Helvetica", 32),           fill=color)
        br_r = self.canvas.create_text(x+CW-9, y+CH-13, text=self.rank,
                                        font=("Helvetica", 12, "bold"), fill=color, anchor="e")
        br_s = self.canvas.create_text(x+CW-9, y+CH-28, text=self.suit,
                                        font=("Helvetica", 12),          fill=color, anchor="e")
        self.ids = [s, bg, tl_r, tl_s, ctr, br_r, br_s]

    def move_to(self, progress):
        # easeOutQuint
        p = 1 - math.pow(1 - progress, 4)
        self.y = int(-CH - 20 + (self.target_y - (-CH - 20)) * p)
        self._draw()

    def flip(self):
        self.hidden = False
        self._draw()

    def delete(self):
        for i in self.ids:
            try:
                self.canvas.delete(i)
            except Exception:
                pass
        self.ids = []


class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack  •  Made by Paul Nercessian")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.deck         = make_deck()
        self.player_hand  = []   # list of (rank, suit)
        self.dealer_hand  = []
        self.card_objs    = []   # Card instances on canvas
        self.game_active  = False
        self.animating    = False

        self._build_ui()

    #UI

    def _build_ui(self):
        W = 860

        # header
        hdr = tk.Frame(self.root, bg=BG, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="♠   B L A C K J A C K   ♥",
                 font=("Georgia", 22, "bold"), fg=GOLD, bg=BG).pack(side="left", padx=28)
        tk.Label(hdr, text="Made by Paul Nercessian",
                 font=("Georgia", 9, "italic"), fg=TEXT_DIM, bg=BG).pack(side="right", padx=24)

        # thin gold divider
        tk.Frame(self.root, bg=GOLD, height=1).pack(fill="x")

        # main canvas (the table)
        self.cv = tk.Canvas(self.root, width=W, height=400,
                            bg=FELT, highlightthickness=0)
        self.cv.pack()

        # felt oval decoration
        self.cv.create_oval(80, 20, W-80, 380, outline=FELT2, width=3, fill="")
        self.cv.create_oval(90, 28, W-90, 372, outline="#0f2216", width=1, fill="")

        # zone labels (center)
        self.cv.create_text(W//2, 48, text="D E A L E R",
                             font=("Georgia", 11, "italic"), fill=TEXT_DIM)
        self.cv.create_text(W//2, 350, text="P L A Y E R",
                             font=("Georgia", 11, "italic"), fill=TEXT_DIM)

        # side score readouts — left-aligned so they're always visible
        self.cv.create_text(22, 100, text="Dealer\nhas:",
                             font=("Georgia", 9, "italic"), fill=TEXT_DIM, anchor="w")
        self.dealer_score_id = self.cv.create_text(22, 128, text="",
                                                    font=("Georgia", 20, "bold"), fill=GOLD, anchor="w")

        self.cv.create_text(22, 272, text="You\nhave:",
                             font=("Georgia", 9, "italic"), fill=TEXT_DIM, anchor="w")
        self.player_score_id = self.cv.create_text(22, 300, text="",
                                                    font=("Georgia", 20, "bold"), fill=GOLD, anchor="w")

        # thin gold divider
        tk.Frame(self.root, bg=GOLD, height=1).pack(fill="x")

        # result message — lives outside the canvas so cards never overlap it
        self.msg_lbl = tk.Label(self.root, text="Place your bet and hit DEAL",
                                font=("Georgia", 17, "bold"), fg=GOLD2,
                                bg=BG, pady=8)
        self.msg_lbl.pack()

        tk.Frame(self.root, bg=GOLD, height=1).pack(fill="x")

        # button row
        btn_row = tk.Frame(self.root, bg=BG, pady=18)
        btn_row.pack()

        bkw = dict(font=("Georgia", 14, "bold"), relief="flat",
                   padx=30, pady=11, cursor="hand2", bd=0)

        self.deal_btn = tk.Button(btn_row, text="DEAL", bg=GOLD, fg=BG,
                                   activebackground=GOLD2, activeforeground=BG,
                                   command=self.deal, **bkw)
        self.deal_btn.pack(side="left", padx=10)

        self.hit_btn = tk.Button(btn_row, text="HIT", bg=GREEN_BTN, fg=WHITE,
                                  activebackground="#22883f", activeforeground=WHITE,
                                  state="disabled", command=self.hit, **bkw)
        self.hit_btn.pack(side="left", padx=10)

        self.stand_btn = tk.Button(btn_row, text="STAND", bg=BLUE_BTN, fg=WHITE,
                                    activebackground="#224d8f", activeforeground=WHITE,
                                    state="disabled", command=self.stand, **bkw)
        self.stand_btn.pack(side="left", padx=10)

        # footer
        ft = tk.Frame(self.root, bg=BG, pady=6)
        ft.pack(fill="x")
        self.status_lbl = tk.Label(ft, text="Dealer stands on 17",
                                    font=("Courier", 9), fg=TEXT_DIM, bg=BG)
        self.status_lbl.pack()

    #helpers

    def _clear_table(self):
        for c in self.card_objs:
            c.delete()
        self.card_objs = []
        self.msg_lbl.config(text="")
        self.cv.itemconfig(self.dealer_score_id, text="")
        self.cv.itemconfig(self.player_score_id, text="")

    def _card_x(self, index, count):
        # center cards in the zone
        total_w = count * CW + (count - 1) * 14
        start_x = (860 - total_w) // 2
        return start_x + index * (CW + 14)

    def _update_scores(self, hide_dealer=True):
        p = total(self.player_hand)
        self.cv.itemconfig(self.player_score_id, text=str(p))
        if hide_dealer and self.dealer_hand:
            d = total([self.dealer_hand[0]])
            self.cv.itemconfig(self.dealer_score_id, text=str(d))
        elif self.dealer_hand:
            d = total(self.dealer_hand)
            self.cv.itemconfig(self.dealer_score_id, text=str(d))

    def _set_buttons(self, deal=False, hit=False, stand=False):
        self.deal_btn.config( state="normal"   if deal  else "disabled")
        self.hit_btn.config(  state="normal"   if hit   else "disabled")
        self.stand_btn.config(state="normal"   if stand else "disabled")

    def _msg(self, text, color=GOLD2):
        self.msg_lbl.config(text=text, fg=color)

    #animation

    def _animate_cards(self, cards_to_animate, step=0, total_steps=18, on_done=None):
        """Animate a list of Card objects sliding in simultaneously."""
        progress = step / total_steps
        for card in cards_to_animate:
            card.move_to(progress)
        if step < total_steps:
            self.root.after(16, self._animate_cards, cards_to_animate,
                            step + 1, total_steps, on_done)
        else:
            # snap to final
            for card in cards_to_animate:
                card.move_to(1.0)
            if on_done:
                on_done()

    def _deal_one_card(self, rank, suit, target_x, target_y,
                       hidden=False, on_done=None):
        card = Card(self.cv, rank, suit, target_x, target_y, hidden=hidden)
        self.card_objs.append(card)
        self._animate_cards([card], on_done=on_done)
        return card

    #game logic

    def deal(self):
        if self.animating:
            return

        if len(self.deck) < 15:
            self.deck = make_deck()

        self.player_hand = []
        self.dealer_hand = []
        self._clear_table()
        self.game_active = True
        self.animating   = True
        self._set_buttons()

        # sequence: deal p1 -> d1 -> p2 -> d2 (hidden)
        cards_to_deal = [
            ("player", self.deck.pop(), False),
            ("dealer", self.deck.pop(), False),
            ("player", self.deck.pop(), False),
            ("dealer", self.deck.pop(), True),   # hole card
        ]
        self._deal_sequence(cards_to_deal, 0)

    def _deal_sequence(self, sequence, idx):
        if idx >= len(sequence):
            self.animating = False
            self._after_deal()
            return

        who, (rank, suit), hidden = sequence[idx]

        if who == "player":
            self.player_hand.append((rank, suit))
            hand   = self.player_hand
            zone_y = 240
        else:
            self.dealer_hand.append((rank, suit))
            hand   = self.dealer_hand
            zone_y = 88

        # recalculate x positions for all cards in this zone
        count = len(hand)
        x = self._card_x(count - 1, count)

        # set correct x for already-placed cards in this zone
        zone_cards = [c for c in self.card_objs if c.target_y == zone_y]
        for i, zc in enumerate(zone_cards):
            new_x = self._card_x(i, count)
            zc.target_x = new_x

        card = Card(self.cv, rank, suit, x, zone_y, hidden=hidden)
        self.card_objs.append(card)

        self._update_scores(hide_dealer=True)

        self._animate_cards([card], total_steps=14,
                             on_done=lambda: self.root.after(
                                 80, self._deal_sequence, sequence, idx + 1))

    def _after_deal(self):
        p = total(self.player_hand)
        d = total(self.dealer_hand)

        if p == 21 and d == 21:
            self._flip_hole(lambda: self._finish("push_bj"))
        elif p == 21:
            self._flip_hole(lambda: self._finish("blackjack"))
        elif d == 21:
            self._flip_hole(lambda: self._finish("dealer_bj"))
        else:
            self._set_buttons(hit=True, stand=True)
            self._msg("Hit or Stand?", GOLD)

    def hit(self):
        if not self.game_active or self.animating:
            return
        self.animating = True
        self._set_buttons()

        rank, suit = self.deck.pop()
        self.player_hand.append((rank, suit))

        count = len(self.player_hand)
        x     = self._card_x(count - 1, count)
        card  = Card(self.cv, rank, suit, x, 240)
        self.card_objs.append(card)

        self._update_scores(hide_dealer=True)

        def after_hit():
            self.animating = False
            p = total(self.player_hand)
            if p > 21:
                self._flip_hole(lambda: self._finish("bust"))
            elif p == 21:
                self.stand()
            else:
                self._set_buttons(hit=True, stand=True)
                self._msg("Hit or Stand?", GOLD)

        self._animate_cards([card], total_steps=14, on_done=after_hit)

    def stand(self):
        if not self.game_active or self.animating:
            return
        self._set_buttons()
        self._flip_hole(self._dealer_draw_loop)

    def _flip_hole(self, on_done=None):
        # find hole card (hidden dealer card, index 1)
        dealer_zone = [c for c in self.card_objs if c.target_y == 88]
        if len(dealer_zone) >= 2:
            hole = dealer_zone[1]
            hole.flip()
        self._update_scores(hide_dealer=False)
        if on_done:
            self.root.after(300, on_done)

    def _dealer_draw_loop(self):
        d = total(self.dealer_hand)
        if d < 17:
            self.animating = True
            rank, suit = self.deck.pop()
            self.dealer_hand.append((rank, suit))

            count = len(self.dealer_hand)
            x     = self._card_x(count - 1, count)
            card  = Card(self.cv, rank, suit, x, 88)
            self.card_objs.append(card)
            self._update_scores(hide_dealer=False)

            def after_dealer():
                self.animating = False
                self.root.after(400, self._dealer_draw_loop)

            self._animate_cards([card], total_steps=14, on_done=after_dealer)
        else:
            self.root.after(200, self._resolve)

    def _resolve(self):
        p = total(self.player_hand)
        d = total(self.dealer_hand)
        if d > 21:
            self._finish("dealer_bust")
        elif p > d:
            self._finish("win")
        elif d > p:
            self._finish("lose")
        else:
            self._finish("push")

    def _finish(self, result):
        self.game_active = False
        self.animating   = False

        msgs = {
            "blackjack":   ("★  BLACKJACK!  ★",           GOLD2),
            "push_bj":     ("Both Blackjack — Push",       WHITE),
            "dealer_bj":   ("Dealer Blackjack",            LOSE_RED),
            "bust":        ("Bust!",                       LOSE_RED),
            "dealer_bust": ("Dealer Busts — You Win!",     WIN_GRN),
            "win":         ("You Win!",                    WIN_GRN),
            "lose":        ("Dealer Wins",                 LOSE_RED),
            "push":        ("Push",                        WHITE),
        }
        text, color = msgs.get(result, ("", WHITE))
        self._msg(text, color)
        self._set_buttons(deal=True)


def main():
    root = tk.Tk()
    root.geometry("860x670")
    BlackjackApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
