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

        self.text_input = tk.Text(self.frame, height=3)
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

        self.textwidget_clear(self.text_error)
        self.textwidget_clear(self.text_output)

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
                    self.textwidget_insert(self.text_error, things[1])
                    return
                try:
                    stock_desired_percent = self.get_float_from_string(things[2])
                    total_stock_desired_percent += stock_desired_percent
                except ValueError as e:
                    self.textwidget_insert(self.text_error, things[2])
                    return
                stocks[stock] = [stock_value, stock_desired_percent]
            else:
                self.textwidget_insert(self.text_error, f"'{text_input_line}'")
                return
        if total_stock_desired_percent != 100.0:
            self.textwidget_insert(self.text_error, f"total_stock_desired_percent={total_stock_desired_percent} (should be 100.0)")
            return
        try:
            amount_to_invest = self.get_float_from_string(self.stringvar_amounttoinvest.get())
        except ValueError as e:
            self.textwidget_insert(self.text_error, "invalid amount_to_invest")
            return
        
        # Use the input values to calculate and display the investment split
        new_total_stock_value = total_stock_value + amount_to_invest
        for stock in stocks:
            needed_value = (stocks[stock][1] / 100.0) * new_total_stock_value
            difference = needed_value - stocks[stock][0]
            self.textwidget_insert(self.text_output, f"Put {difference} in {stock}")
    
    def textwidget_insert(self, textwidget, text):
        textwidget.configure(state=tk.NORMAL)
        textwidget.insert(tk.END, f"{text}\n")
        textwidget.configure(state=tk.DISABLED)
    
    def textwidget_clear(self, textwidget):
        textwidget.configure(state=tk.NORMAL)
        textwidget.delete("1.0", tk.END)
        textwidget.configure(state=tk.DISABLED)
    
    def get_float_from_string(self, string):
        return float("".join([char for char in string if char.isdigit() or char == "."]))


Rebalancer()