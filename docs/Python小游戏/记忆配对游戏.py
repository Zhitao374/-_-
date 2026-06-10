import tkinter as tk
import random

class MemoryGame:
    def __init__(self, root, rows=4, cols=8, fruits=None):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.fruits = fruits or ['🍎', '🍌', '🍒', '🍇', '🥝', '🍊', '🍉', '🍓']
        self.root.title("记忆配对 · 优化版")
        
        self.buttons = [[None] * cols for _ in range(rows)]
        self.data = [[0] * cols for _ in range(rows)]
        self.state = [[False] * cols for _ in range(rows)]
        self.first = None
        self.waiting = False
        self.paired_count = 0   # 已配对的对数，用于快速胜利检测
        
        self.create_board()
        self.new_game()
    
    def create_board(self):
        frame = tk.Frame(self.root)
        frame.pack()
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(frame, text='?', width=4, height=2,
                                font=('Arial', 20),
                                command=lambda r=r, c=c: self.on_click(r, c))
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[r][c] = btn
        
        reset_btn = tk.Button(self.root, text="新游戏", command=self.new_game)
        reset_btn.pack()
    
    def new_game(self):
        total = self.rows * self.cols
        pairs = total // 2
        
        # 生成成对卡片列表（简化写法）
        # 重复水果列表足够多次后切片，再复制一份成对
        icon_list = (self.fruits * (pairs // len(self.fruits) + 1))[:pairs]
        cards = icon_list + icon_list
        random.shuffle(cards)
        
        for r in range(self.rows):
            for c in range(self.cols):
                self.data[r][c] = cards[r * self.cols + c]
                self.state[r][c] = False
                self.buttons[r][c].config(text='?', state=tk.NORMAL)  # 不指定bg
        self.first = None
        self.waiting = False
        self.paired_count = 0
    
    def on_click(self, r, c):
        if self.waiting or self.state[r][c]:
            return
        if self.first is None:
            self._reveal_card(r, c)
            self.first = (r, c)
        else:
            r1, c1 = self.first
            if (r1, c1) == (r, c):
                return
            self._reveal_card(r, c)
            if self.data[r1][c1] == self.data[r][c]:
                # 配对成功
                self.state[r1][c1] = True
                self.state[r][c] = True
                self.buttons[r1][c1].config(state=tk.DISABLED)
                self.buttons[r][c].config(state=tk.DISABLED)
                self.paired_count += 1
                self.first = None
                if self.paired_count == (self.rows * self.cols // 2):
                    tk.messagebox.showinfo("胜利", "恭喜你完成了所有配对！")
                    self.root.destroy()
            else:
                # 配对失败，延迟翻回
                self.waiting = True
                self.root.after(1000, self._reset_cards, r1, c1, r, c)
                self.first = None
    
    def _reveal_card(self, r, c):
        """翻开一张卡片（显示图标并禁用按钮）"""
        self.buttons[r][c].config(text=self.data[r][c], state=tk.DISABLED)
    
    def _reset_cards(self, r1, c1, r2, c2):
        """将两张卡片翻回背面"""
        self.buttons[r1][c1].config(text='?', state=tk.NORMAL)
        self.buttons[r2][c2].config(text='?', state=tk.NORMAL)
        self.waiting = False

if __name__ == '__main__':
    root = tk.Tk()
    game = MemoryGame(root, rows=4, cols=8)
    root.mainloop()