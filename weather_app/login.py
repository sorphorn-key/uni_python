import tkinter as tk

def loged_in(l):
    if btn.cget("text") == "Login":
        btn.config(text="Logout")
        l.config(text="You are logged in.", fg="green")
    else:
        btn.config(text="Login")
        l.config(text="You are logged out.", fg="red")

root = tk.Tk()
root.title("Title")
root.geometry("300x260")
# root.iconbitmap("image.ico")
root.configure(padx=20, pady=20)

label_font = ("arial", 12)
label_entry = ("arial", 11)
label_btn = ("arial", 11)

label = tk.Label(root, text="Username", font=label_font)
label.pack(pady=(0, 5))
username = tk.Entry(root, font=label_entry, width=25)
username.pack(pady=(0, 5), ipady=3)

label2 = tk.Label(root, text="Password", font=label_font)
label2.pack(pady=(0, 5))
password = tk.Entry(root, show="*", font=label_entry, width=25)
password.pack(pady=(0, 5), ipady=3)

label3 = tk.Label(root, text="", font=label_entry, fg="red")

btn = tk.Button(root, text="Login", font=label_btn, width=10, command=lambda: loged_in(label3))
btn.pack(pady=(15, 5))

label3.pack(pady=(15, 5))

root.mainloop()