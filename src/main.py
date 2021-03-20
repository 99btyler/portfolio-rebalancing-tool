import tkinter as tk
from tkinter import ttk


class Rebalancer():

    def __init__(self):

        # Tkinter root
        self.root = tk.Tk()
        self.root.title("portfolio-rebalancing-tool")
        self.root.resizable(False, False)

        # Tkinter frame
        self.frame = ttk.Frame(self.root, padding=25)
        self.frame.grid()

        # Tkinter widgets
        self.text_hint = tk.Text(self.frame, height=1)
        self.text_hint.insert(tk.END, "stock ; stock_value ; stock_desired_percent")
        self.text_hint.configure(state=tk.DISABLED)
        self.text_hint.grid()

        self.text_input = tk.Text(self.frame, height = 3)
        self.text_input.grid()

        self.text_error = tk.Text(self.frame, height=1, state=tk.DISABLED)
        self.text_error.grid()

        self.stringvar_amounttoinvest = tk.StringVar(value="amount to invest")
        self.entry_amounttoinvest = ttk.Entry(self.frame, textvariable=self.stringvar_amounttoinvest)
        self.entry_amounttoinvest.grid()

        self.button_calculate = ttk.Button(self.frame, text="Calculate", command=self.calculate)
        self.button_calculate.grid()

        self.text_output = tk.Text(self.frame, height=3, state=tk.DISABLED)
        self.text_output.grid()

        # Tkinter mainloop
        self.root.mainloop()
    
    def calculate(self):

        self.clear_texterror()

        # Get all input values and verify them
        stocks = {}
        total_stock_value = 0.0
        total_stock_desired_percent = 0.0
        text_input_lines = self.text_input.get("1.0", tk.END).split("\n")
        for i in range(0, len(text_input_lines) - 1):
            text_input_line = text_input_lines[i]
            things = text_input_line.split(";")
            if len(things) == 3:
                stock = things[0]
                try:
                    stock_value = self.get_float_from_string(things[1])
                    total_stock_value += stock_value
                except ValueError as e:
                    self.insert_texterror(things[1])
                    return
                try:
                    stock_desired_percent = self.get_float_from_string(things[2])
                    total_stock_desired_percent += stock_desired_percent
                except ValueError as e:
                    self.insert_texterror(things[2])
                    return
                stocks[stock] = [stock_value, stock_desired_percent]
            else:
                self.insert_texterror(f"'{text_input_line}'")
                return
        if total_stock_desired_percent != 100.0:
            self.insert_texterror(f"total_stock_desired_percent={total_stock_desired_percent} (should be 100.0)")
            return
        try:
            amount_to_invest = self.get_float_from_string(self.stringvar_amounttoinvest.get())
        except ValueError as e:
            self.insert_texterror("invalid amount_to_invest")
            return
        
        # Use the input values to calculate and display the investment split
        new_total_stock_value = total_stock_value + amount_to_invest
        self.text_output.configure(state=tk.NORMAL)
        for stock in stocks:
            needed_value = (stocks[stock][1] / 100.0) * new_total_stock_value
            difference = needed_value - stocks[stock][0]
            self.text_output.insert(tk.END, f"Put {difference} in {stock}\n")
        self.text_output.configure(state=tk.DISABLED)
    
    def get_float_from_string(self, string):
        return float("".join([char for char in string if char.isdigit() or char == "."]))
    
    def insert_texterror(self, error):
        self.clear_texterror()
        self.text_error.configure(state=tk.NORMAL)
        self.text_error.insert(tk.END, f"ERROR: {error}")
        self.text_error.configure(state=tk.DISABLED)
    
    def clear_texterror(self):
        self.text_error.configure(state=tk.NORMAL)
        self.text_error.delete("1.0", tk.END)
        self.text_error.configure(state=tk.DISABLED)


Rebalancer()