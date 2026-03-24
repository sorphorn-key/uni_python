import tkinter as tk

signs = ['(', ')', '%', 'AC']
ops = ['+', '-', '*', '/']
nums = ['0', '.', '=']
for i in range(9):
    nums.append(str(i + 1))

root = tk.Tk()
root.title("Calculator")
root.config(padx=20, pady=20)
root.resizable(False, False)

btn_padx = (3, 0)
btn_pady = (0, 4)

output = tk.Entry(root, bd=2, justify='right')
output.grid(columnspan=5, row=0, column=0,
            sticky='we', ipady=10, pady=(0, 7))

for i in range(len(signs)):
    btn = tk.Button(root, text=signs[i],
                    width=8, bg='#C5C6C7')
    btn.grid(row=1, column=i, ipady=1,
             padx=btn_padx, pady=btn_pady)

for i in range(len(ops)):
    btn = tk.Button(root, text=ops[i],
                    width=8, bg='#C5C6C7')
    btn.grid(row=(4 - i + 1), column=3, ipady=1,
             padx=btn_padx, pady=btn_pady)

for i in range(len(nums)):
    btn = tk.Button(root, text=nums[i],
                    width=8)
    btn.grid(row=(4 - int(i / 3) + 1), column=(i % 3), ipady=1,
             padx=btn_padx, pady=btn_pady)
    if nums[i] == '=':
        btn.config(bg='#4285F4', fg='#fff')

root.mainloop()