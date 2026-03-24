import tkinter as tk

root = tk.Tk()
root.title("Title")
root.geometry("300x260")
root.configure(padx=30, pady=30)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

label_font = ("arial", 12)
link_font = ("arial", 8)

label1 = tk.Label(root,
                  text="Username:",
                  font=label_font)
label1.grid(row=0, column=0, pady=(0, 10), sticky="w")
username = tk.Entry(root,
                    width=25)
username.grid(columnspan=2, row=0, column=1, ipady=3, pady=(0, 10),sticky="e")

label2 = tk.Label(root,
                  text="Password:",
                  font=label_font)
label2.grid(row=1, column=0, pady=(0, 10), sticky="w")
password = tk.Entry(root,
                    width=25,
                    show='*')
password.grid(columnspan=2, row=1, column=1, ipady=3, pady=(0, 10), sticky="e")

label3 = tk.Label(root,
                  text="Forgot password?",
                  font=link_font,
                  fg="blue")
label3.grid(row=2, column=0, sticky="w")
label4 = tk.Label(root,
                  text="Sign up",
                  font=link_font,
                  fg="blue")
label4.grid(row=2, column=2, sticky="e")

btn = tk.Button(root,
                text="Login",
                font=("arial", 12),
                width=10)
btn.grid(columnspan=3, row=3, column=0, pady=(20, 0))

root.mainloop()



