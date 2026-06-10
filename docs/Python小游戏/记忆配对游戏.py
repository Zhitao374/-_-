import tkinter as tk # 1 导入tkinter库
import random # 3 导入随机库

class MemoryGame:    # 1 定义记忆配对游戏类
    def __init__(self, root, rows=4, cols=8, fruits=None): # 1 初始化游戏对象
        self.root = root # 1 初始化主窗口对象
        self.rows = rows # 2 初始化行数
        self.cols = cols # 2 初始化列数
        self.fruits = fruits or ['🍎', '🍌', '🍒', '🍇', '🥝', '🍊', '🍉', '🍓'] # 3 初始化水果列表
        self.root.title("记忆配对游戏") # 2 设置窗口标题

        self.buttons = [[None] * cols for _ in range(rows)] # 3 初始化游戏板按钮列表
        self.data = [[0] * cols for _ in range(rows)] # 3 初始化游戏板数据
        self.first = None # 4 初始化第一次点击的按钮
        self.paired_count = 0 # 5 初始化成功配对数
        self.total_pairs = rows * cols // 2 # 5 初始化总配对数
        self.pending = None          # 5 存储待翻回的卡片对 (r1,c1,r2,c2)
        self.pending_id = None       # 5 存储 after 任务的 id，用于取消

        self.create_board() # 2 创建游戏板
        self.new_game() # 3 游戏渲染

    def create_board(self): # 2 创建游戏板
        frame = tk.Frame(self.root) # 2 创建游戏板框架
        frame.pack() # 2 放置游戏板框架
        for row in range(self.rows): # 2 创建游戏板行
            for col in range(self.cols): # 2 创建游戏板列
                btn = tk.Button(frame, text="？", width=4, height=2, font=("微软雅黑", 24) # 2 创建游戏板按钮
                                , command=lambda r=row, c=col: self.on_click(r, c)) # 4 游戏板按钮点击事件
                btn.grid(row=row, column=col, padx=2, pady=2) # 2 放置游戏板按钮
                self.buttons[row][col] = btn # 3 初始化游戏板按钮列表
        
        reset_btn = tk.Button(self.root, text="新游戏", command=self.new_game) # 6 创建新游戏按钮
        reset_btn.pack(side=tk.RIGHT, padx=10) # 6 放置新游戏按钮

    def new_game(self): # 3 游戏渲染
        # 6 取消任何未完成的延迟任务，避免干扰新游戏
        if self.pending_id:
            self.root.after_cancel(self.pending_id)
            self.pending_id = None
        self.pending = None

        total = self.rows * self.cols # 3 计算游戏板总按钮数
        pairs = total // 2 # 3 计算游戏板配对数
        icon_list = (self.fruits * (pairs // len(self.fruits) + 1))[:pairs] # 3 生成游戏板配对
        cards = icon_list*2 # 3 生成游戏板配对
        random.shuffle(cards) # 3 随机选择游戏板配对

        for row in range(self.rows): # 3 游戏板行
            for col in range(self.cols): # 3 游戏板列
                self.data[row][col] = cards[row*self.cols+col] # 3 设置游戏板数据
                self.buttons[row][col].config(text='？', state=tk.NORMAL) # 3 设置游戏板按钮文本
        self.first = None # 6 初始化第一次点击的按钮
        self.paired_count = 0 # 6 初始化成功配对数

    def on_click(self, r, c): # 4 游戏板按钮点击事件
        # 5 如果存在等待翻回的卡片对，立即取消并翻回
        if self.pending:
            # 5 取消延迟任务
            if self.pending_id:
                self.root.after_cancel(self.pending_id)
                self.pending_id = None
            # 5 立即翻回 pending 的卡片
            r1, c1, r2, c2 = self.pending
            self._reset_cards(r1, c1, r2, c2)   # 这个方法会设置 self.pending = None
            
        if self.first is None: # 4 如果是第一次点击
            self._reveal_card(r, c) # 4 揭示游戏板按钮
            self.first = (r, c) # 4 设置第一次点击的按钮
        else: # 4 如果是第二次点击
            r1, c1 = self.first # 4 获取第一次点击的按钮
            if (r1, c1) == (r, c): # 4 如果是第一次点击的按钮
                return
            self._reveal_card(r, c) # 4 揭示游戏板按钮
            if self.data[r1][c1] == self.data[r][c]: # 4 如果是配对
                self.buttons[r1][c1].config(state=tk.DISABLED) # 4 禁用游戏板按钮
                self.buttons[r][c].config(state=tk.DISABLED) # 4 禁用游戏板按钮
                self.first = None   # 4 重置第一次点击的按钮
                self.paired_count += 1 # 5 增加成功配对数
                # 5 如果全部配对成功
                if self.paired_count == self.total_pairs:   # 5 如果全部配对成功
                    tk.messagebox.showinfo("胜利", "恭喜你完成了所有配对！") # 5 显示胜利消息
                    self.root.destroy() # 5 销毁主窗口对象 
            else:
                # 4 配对失败，延迟翻回
                self.pending = (r1, c1, r, c) # 5 存储待翻回的卡片对
                # 5 延迟翻回游戏板按钮
                self.pending_id = self.root.after(800, self._reset_cards, r1, c1, r, c) # 4 延迟翻回游戏板按钮
                self.first = None # 4 重置第一次点击的按钮

    def _reveal_card(self, r, c): # 4 揭示游戏板按钮
        self.buttons[r][c].config(text=self.data[r][c], state=tk.DISABLED) # 4 揭示游戏板按钮

    def _reset_cards(self, r1, c1, r2, c2): # 4 重置游戏板按钮
        """将两张卡片翻回背面"""
        self.buttons[r1][c1].config(text='?', state=tk.NORMAL) # 4 重置游戏板按钮
        self.buttons[r2][c2].config(text='?', state=tk.NORMAL) # 4 重置游戏板按钮
        self.pending = None # 5 重置待翻回的卡片对
        self.pending_id = None # 5 重置 after 任务的 id，用于取消延迟任务

if __name__ == "__main__":  # 1 主函数入口
    root = tk.Tk()  # 1 创建主窗口对象
    game = MemoryGame(root) # 1 创建游戏对象
    root.mainloop() # 1 进入主事件循环
