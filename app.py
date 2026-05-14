import tkinter as tk
root = tk.Tk()
root.title("Basic Grid Example")
root.geometry("400x300")

# Create labels for the 3x3 grid
for row in range(3):
    for col in range(3):
        label = tk.Label(root, text=f"Row {row}, Col {col}", 
   borderwidth=1, relief="solid", width=10, height=3)
        label.grid(row=row, column=col, padx=2, pady=2)

root.mainloop()