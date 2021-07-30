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

        self.stringvar_amount_to_invest = tk.StringVar(value="amount to invest")
        self.entry_amount_to_invest = ttk.Entry(self.frame, textvariable=self.stringvar_amount_to_invest)
        self.entry_amount_to_invest.grid()

        self.button_calculate = ttk.Button(self.frame, text="Calculate", command=self.__calculate)
        self.button_calculate.grid()

        self.text_output = tk.Text(self.frame, height=3, state=tk.DISABLED)
        self.text_output.grid()

        # Tkinter mainloop
        self.root.mainloop()
    
    def __calculate(self):
        
        self.__textwidget_clear(self.text_error)
        self.__textwidget_clear(self.text_output)

        stocks = {}
        total_stock_value = 0.0
        total_stock_desired_percent = 0.0

        for line in self.text_input.get("1.0", f"{tk.END}-1c").split("\n"):

            things = line.split(";")

            if len(things) != 3:
                self.__textwidget_insert(self.text_error, f"'{line}'")
                return
            
            # stock
            stock = things[0]
            # stock_value
            try:
                stock_value = self.__get_float_from_string(things[1])
                total_stock_value += stock_value
            except ValueError as e:
                self.__textwidget_insert(self.text_error, things[1])
                return
            # stock_desired_percent
            try:
                stock_desired_percent = self.__get_float_from_string(things[2])
                total_stock_desired_percent += stock_desired_percent
            except ValueError as e:
                self.__textwidget_insert(self.text_error, things[2])
                return
            
            stocks[stock] = [stock_value, stock_desired_percent]
            
        if total_stock_desired_percent != 100.0:
            self.__textwidget_insert(self.text_error, f"total_stock_desired_percent={total_stock_desired_percent} (should be 100.0)")
            return

        try:
            amount_to_invest = self.__get_float_from_string(self.stringvar_amount_to_invest.get())
        except ValueError as e:
            self.__textwidget_insert(self.text_error, "invalid amount_to_invest")
            return
            
        new_total_stock_value = total_stock_value + amount_to_invest

        for stock in stocks:
            needed_value = (stocks[stock][1] / 100.0) * new_total_stock_value # stock_desired_percent * new_total_stock_value
            difference = needed_value - stocks[stock][0] # needed_value - stock_value
            self.__textwidget_insert(self.text_output, f"Put {round(difference, 2)} in {stock}")

    def __textwidget_insert(self, textwidget, text):
        textwidget.configure(state=tk.NORMAL)
        textwidget.insert(tk.END, f"{text}\n")
        textwidget.configure(state=tk.DISABLED)

    def __textwidget_clear(self, textwidget):
        textwidget.configure(state=tk.NORMAL)
        textwidget.delete("1.0", tk.END)
        textwidget.configure(state=tk.DISABLED)
    
    def __get_float_from_string(self, string):
        return float("".join([char for char in string if char.isdigit() or char == "."]))


if __name__ == "__main__":
    Rebalancer()

