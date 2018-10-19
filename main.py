import markov
import tkinter.ttk as ttk
import tkinter as tk
class CompleteText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs, undo=True)
        self.bind('<Control-Key-a>', self.event_select_all)
        self.bind('<Control-Key-A>', self.event_select_all)
    def event_select_all(self, event):
        self.tag_add(tk.SEL, "1.0", tk.END)
        self.mark_set(tk.INSERT, "1.0")
        self.see(tk.INSERT)
        return 'break'
class GUI(ttk.Frame):
    def __init__(self,master=None):
        ttk.Frame.__init__(self)
        self.me = markov.MarkovEncode(markov.shakespeare())
        ttk.Label(self, text='Plaintext:').grid(row=0, column=0)
        self.plain_in = CompleteText(self, width=80, height=8)
        self.plain_in.grid(row=1, column=0)
        self.encoded_out = CompleteText(self)
        self.encoded_out.grid(row=2, column=0)
        ttk.Label(self, text='Encoded:').grid(row=0, column=1)
        self.encoded_in = CompleteText(self, width=80, height=8)
        self.encoded_in.grid(row=1, column=1)
        self.plain_out = CompleteText(self)
        self.plain_out.grid(row=2, column=1)
        self.plain_in.bind('<Key>', self.delayed)
        self.encoded_in.bind('<Key>', self.delayed)
    def delayed(self, _=None):
        self.after(10, self.manage_encryption)
    def manage_encryption(self, _=None):
        encoded_out = ''.join(self.me.encode(self.plain_in.get('1.0', 'end-1c').encode()))
        self.encoded_out.replace('1.0', 'end-1c', encoded_out)
        encoded_in = self.encoded_in.get('1.0', 'end-1c').strip()
        plain_out = self.me.decode(encoded_in)
        self.plain_out.replace('1.0', 'end-1c', plain_out)
        

gui = GUI()
gui.grid()
gui.focus_set()
gui.mainloop()
