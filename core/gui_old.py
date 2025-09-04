import tkinter as tk
from tkinter import font, messagebox
from PIL import Image, ImageTk, ImageDraw
from core.user_system import UserSystem

class FaceLoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Login")
        self.root.geometry("500x700")
        self.root.resizable(False, False)

        self.user_system = UserSystem()

        self.create_main_frame()
        self.create_login_frame()
        self.create_admin_register_frame()
        self.create_admin_dashboard_frame()
        self.create_user_dashboard_frame()
        self.create_view_users_frame()

        if self.user_system.is_db_empty():
            self.create_initial_register_frame()
            self.show_initial_register_frame()
        else:
            self.show_main_frame()

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, width=500, height=700)
        self.main_canvas = tk.Canvas(self.main_frame, width=500, height=700)
        self.main_canvas.pack()

        self.draw_gradient(self.main_canvas)
        self.create_glass_button(self.main_canvas, 150, 300, "Login", self.show_login_frame)

    def create_initial_register_frame(self):
        self.initial_register_frame = tk.Frame(self.root, width=500, height=700)
        self.initial_register_canvas = tk.Canvas(self.initial_register_frame, width=500, height=700)
        self.initial_register_canvas.pack()

        self.draw_gradient(self.initial_register_canvas)

        self.initial_register_canvas.create_text(250, 100, text="Initial Admin Registration", fill="white", font=font.Font(family="Helvetica", size=24, weight="bold"))

        self.initial_register_canvas.create_text(100, 200, text="User ID:", fill="white", font=font.Font(family="Helvetica", size=16))
        self.initial_user_id_entry = tk.Entry(self.initial_register_canvas, width=30)
        self.initial_register_canvas.create_window(300, 200, window=self.initial_user_id_entry)

        self.initial_register_canvas.create_text(100, 250, text="Name:", fill="white", font=font.Font(family="Helvetica", size=16))
        self.initial_name_entry = tk.Entry(self.initial_register_canvas, width=30)
        self.initial_register_canvas.create_window(300, 250, window=self.initial_name_entry)

        self.initial_register_canvas.create_text(100, 300, text="Login Key:", fill="white", font=font.Font(family="Helvetica", size=16))
        self.initial_login_key_entry = tk.Entry(self.initial_register_canvas, width=30, show="*")
        self.initial_register_canvas.create_window(300, 300, window=self.initial_login_key_entry)

        self.create_glass_button(self.initial_register_canvas, 150, 450, "Register Admin", self.register_initial_admin)

    def create_login_frame(self):
        self.login_frame = tk.Frame(self.root, width=500, height=700)
        self.login_canvas = tk.Canvas(self.login_frame, width=500, height=700)
        self.login_canvas.pack()

        self.draw_gradient(self.login_canvas)

        self.login_canvas.create_text(250, 100, text="Login", fill="white", font=font.Font(family="Helvetica", size=24, weight="bold"))

        self.login_canvas.create_text(100, 250, text="Login Key:", fill="white", font=font.Font(family="Helvetica", size=16))
        self.login_key_entry_login = tk.Entry(self.login_canvas, width=30, show="*")
        self.login_canvas.create_window(300, 250, window=self.login_key_entry_login)

        self.create_glass_button(self.login_canvas, 150, 400, "Login", self.login_user)
        self.create_glass_button(self.login_canvas, 150, 500, "Back", self.show_main_frame)

    def create_admin_dashboard_frame(self):
        self.admin_dashboard_frame = tk.Frame(self.root, width=500, height=700)
        self.admin_dashboard_canvas = tk.Canvas(self.admin_dashboard_frame, width=500, height=700)
        self.admin_dashboard_canvas.pack()

        self.draw_gradient(self.admin_dashboard_canvas)

        self.admin_dashboard_canvas.create_text(250, 100, text="Admin Dashboard", fill="white", font=font.Font(family="Helvetica", size=24, weight="bold"))

        self.admin_name_label = self.admin_dashboard_canvas.create_text(250, 150, text="", fill="white", font=font.Font(family="Helvetica", size=16))

        self.create_glass_button(self.admin_dashboard_canvas, 150, 250, "Register New User", self.show_admin_register_frame)
        self.create_glass_button(self.admin_dashboard_canvas, 150, 350, "View Users", self.show_view_users_frame)
        self.create_glass_button(self.admin_dashboard_canvas, 150, 450, "Get Storage Info", self.display_storage_info)
        self.create_glass_button(self.admin_dashboard_canvas, 150, 550, "Logout", self.logout)

    def create_user_dashboard_frame(self):
        self.user_dashboard_frame = tk.Frame(self.root, width=500, height=700)
        self.user_dashboard_canvas = tk.Canvas(self.user_dashboard_frame, width=500, height=700)
        self.user_dashboard_canvas.pack()

        self.draw_gradient(self.user_dashboard_canvas)

        self.user_dashboard_canvas.create_text(250, 100, text="User Dashboard", fill="white", font=font.Font(family="Helvetica", size=24, weight="bold"))

        self.user_name_label = self.user_dashboard_canvas.create_text(250, 150, text="", fill="white", font=font.Font(family="Helvetica", size=16))

        self.create_glass_button(self.user_dashboard_canvas, 150, 300, "Logout", self.logout)

    def create_view_users_frame(self):
        self.view_users_frame = tk.Frame(self.root, width=500, height=700)
        self.view_users_canvas = tk.Canvas(self.view_users_frame, width=500, height=700)
        self.view_users_canvas.pack()

        self.draw_gradient(self.view_users_canvas)

        self.view_users_canvas.create_text(250, 50, text="View Users", fill="white", font=font.Font(family="Helvetica", size=24, weight="bold"))

        self.users_display_frame = tk.Frame(self.view_users_canvas, bg="#ADD8E6", bd=2, relief="groove") # Light blue background for user cards
        self.users_display_frame.place(x=50, y=100, width=400, height=400)

        self.users_canvas = tk.Canvas(self.users_display_frame, bg="#ADD8E6")
        self.users_canvas.pack(side="left", fill="both", expand=True)

        self.users_scrollbar = tk.Scrollbar(self.users_display_frame, orient="vertical", command=self.users_canvas.yview)
        self.users_scrollbar.pack(side="right", fill="y")

        self.users_canvas.configure(yscrollcommand=self.users_scrollbar.set)
        self.users_canvas.bind('<Configure>', lambda e: self.users_canvas.configure(scrollregion = self.users_canvas.bbox("all")))

        self.users_inner_frame = tk.Frame(self.users_canvas, bg="#ADD8E6")
        self.users_canvas.create_window((0, 0), window=self.users_inner_frame, anchor="nw")

        # Bind the scroll wheel to the canvas
        self.users_canvas.bind_all("<MouseWheel>", lambda event: self.users_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        self.create_glass_button(self.view_users_canvas, 250, 550, "Back to Dashboard", self.show_admin_dashboard_frame)

    def create_admin_register_frame(self):
        self.admin_register_frame = tk.Frame(self.root, width=500, height=700)
        self.admin_register_canvas = tk.Canvas(self.admin_register_frame, width=500, height=700)
        self.admin_register_canvas.pack()

        self.draw_gradient(self.admin_register_canvas)

        self.admin_register_canvas.create_text(250, 100, text="Admin Register User", fill="white", font=font.Font(family="Helvetica", size=24, weight="bold"))

        self.admin_register_canvas.create_text(100, 200, text="User ID:", fill="white", font=font.Font(family="Helvetica", size=16))
        self.admin_user_id_entry = tk.Entry(self.admin_register_canvas, width=30)
        self.admin_register_canvas.create_window(300, 200, window=self.admin_user_id_entry)

        self.admin_register_canvas.create_text(100, 250, text="Name:", fill="white", font=font.Font(family="Helvetica", size=16))
        self.admin_name_entry = tk.Entry(self.admin_register_canvas, width=30)
        self.admin_register_canvas.create_window(300, 250, window=self.admin_name_entry)

        self.admin_register_canvas.create_text(100, 300, text="Login Key:", fill="white", font=font.Font(family="Helvetica", size=16))
        self.admin_login_key_entry = tk.Entry(self.admin_register_canvas, width=30, show="*")
        self.admin_register_canvas.create_window(300, 300, window=self.admin_login_key_entry)

        self.admin_register_canvas.create_text(100, 350, text="Role:", fill="white", font=font.Font(family="Helvetica", size=16))
        self.role_var = tk.StringVar(self.admin_register_canvas)
        self.role_var.set("normal") # default value
        self.role_option_menu = tk.OptionMenu(self.admin_register_canvas, self.role_var, "normal", "admin")
        self.admin_register_canvas.create_window(300, 350, window=self.role_option_menu)

        self.create_glass_button(self.admin_register_canvas, 150, 450, "Register User", self.admin_register_user)
        self.create_glass_button(self.admin_register_canvas, 150, 550, "Back to Dashboard", self.show_admin_dashboard_frame)

    def show_main_frame(self):
        self.hide_all_frames()
        self.main_frame.pack()

    def show_initial_register_frame(self):
        self.hide_all_frames()
        self.initial_register_frame.pack()

    def show_login_frame(self):
        self.hide_all_frames()
        self.login_frame.pack()

    def show_admin_dashboard_frame(self):
        user = self.user_system.get_logged_in_user()
        if not user or user['role'] != 'admin':
            messagebox.showerror("Error", "Access denied.")
            self.show_main_frame()
            return
        self.hide_all_frames()
        self.admin_dashboard_canvas.itemconfig(self.admin_name_label, text=f"Welcome, {user['name']}!")
        self.admin_dashboard_frame.pack()

    def show_user_dashboard_frame(self):
        user = self.user_system.get_logged_in_user()
        if not user:
            messagebox.showerror("Error", "Access denied.")
            self.show_main_frame()
            return
        self.hide_all_frames()
        self.user_dashboard_canvas.itemconfig(self.user_name_label, text=f"Welcome, {user['name']}!")
        self.user_dashboard_frame.pack()

    def show_view_users_frame(self):
        user = self.user_system.get_logged_in_user()
        if not user or user['role'] != 'admin':
            messagebox.showerror("Error", "Access denied.")
            self.show_main_frame()
            return
        self.hide_all_frames()
        self.populate_users_list()
        self.view_users_frame.pack()

    def show_admin_register_frame(self):
        user = self.user_system.get_logged_in_user()
        if not user or user['role'] != 'admin':
            messagebox.showerror("Error", "Access denied.")
            self.show_main_frame()
            return
        self.hide_all_frames()
        self.admin_register_frame.pack()

    def hide_all_frames(self):
        self.main_frame.pack_forget()
        if hasattr(self, 'initial_register_frame'):
            self.initial_register_frame.pack_forget()
        self.login_frame.pack_forget()
        self.admin_register_frame.pack_forget()
        self.admin_dashboard_frame.pack_forget()
        self.user_dashboard_frame.pack_forget()
        if hasattr(self, 'view_users_frame'):
            self.view_users_frame.pack_forget()

    def draw_gradient(self, canvas):
        for i in range(700):
            r = 25 + int((100 - 25) * (i / 700))
            g = 100 + int((200 - 100) * (i / 700))
            b = 200 + int((255 - 200) * (i / 700))
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, 500, i, fill=color)

    def create_glass_button(self, canvas, x, y, text, command):
        button_width = 200
        button_height = 50

        # Create a semi-transparent rounded rectangle
        canvas.create_rectangle(x, y, x + button_width, y + button_height, 
                                 fill="#FFFFFF", outline="", 
                                 stipple="gray50")

        # Add a white border
        canvas.create_rectangle(x, y, x + button_width, y + button_height, outline="#FFFFFF", width=2)

        # Add a reflection
        canvas.create_line(x + 10, y + 10, x + button_width - 10, y + 10, fill="#FFFFFF", width=2)

        # Add the text
        canvas.create_text(x + button_width / 2, y + button_height / 2, text=text, 
                           fill="#FFFFFF", font=font.Font(family="Helvetica", size=16, weight="bold"))

        # Bind the click event
        canvas.tag_bind(canvas.create_rectangle(x, y, x + button_width, y + button_height, fill="", outline=""), 
                        "<Button-1>", lambda e: command())

    def create_user_card(self, parent_frame, user):
        card_frame = tk.Frame(parent_frame, bg="#FFFFFF", bd=2, relief="raised")
        card_frame.pack(pady=5, padx=10, fill="x", expand=True)

        user_id_label = tk.Label(card_frame, text=f"ID: {user['user_id']}", font=font.Font(family="Helvetica", size=12, weight="bold"), bg="#FFFFFF")
        user_id_label.pack(anchor="w", padx=10, pady=2)

        name_label = tk.Label(card_frame, text=f"Name: {user['name']}", font=font.Font(family="Helvetica", size=12), bg="#FFFFFF")
        name_label.pack(anchor="w", padx=10, pady=2)

        role_label = tk.Label(card_frame, text=f"Role: {user['role']}", font=font.Font(family="Helvetica", size=12), bg="#FFFFFF")
        role_label.pack(anchor="w", padx=10, pady=2)

        delete_button = tk.Button(card_frame, text="Delete", command=lambda: self.delete_user(user['user_id']), bg="#FF6B6B", fg="white", font=font.Font(family="Helvetica", size=10, weight="bold"))
        delete_button.pack(pady=5)

        return card_frame

    def register_initial_admin(self):
        user_id = self.initial_user_id_entry.get()
        name = self.initial_name_entry.get()
        login_key = self.initial_login_key_entry.get()

        if not user_id or not login_key or not name:
            messagebox.showerror("Error", "User ID, Name, and Login Key are required.")
            return

        self.user_system.register_user(user_id, login_key, "admin", name)
        messagebox.showinfo("Success", "Initial admin registered successfully!")
        self.initial_register_frame.pack_forget()
        self.show_main_frame()

    def admin_register_user(self):
        user_id = self.admin_user_id_entry.get()
        name = self.admin_name_entry.get()
        login_key = self.admin_login_key_entry.get()
        role = self.role_var.get()

        if not user_id or not login_key or not name:
            messagebox.showerror("Error", "User ID, Name, and Login Key are required.")
            return

        self.user_system.register_user(user_id, login_key, role, name)
        messagebox.showinfo("Success", f"User {user_id} ({role}) registered successfully!")
        self.admin_user_id_entry.delete(0, tk.END)
        self.admin_name_entry.delete(0, tk.END)
        self.admin_login_key_entry.delete(0, tk.END)
        self.role_var.set("normal")
        self.show_admin_dashboard_frame()

    def login_user(self):
        login_key = self.login_key_entry_login.get()

        if not login_key:
            messagebox.showerror("Error", "Login Key is required.")
            return

        user_info = self.user_system.login_user(login_key)
        if user_info:
            messagebox.showinfo("Success", f"Login successful! Welcome {user_info['name']}!")
            if user_info['role'] == 'admin':
                self.show_admin_dashboard_frame()
            else:
                self.show_user_dashboard_frame()
        else:
            messagebox.showerror("Error", "Face not recognized or login key incorrect.")

    def logout(self):
        self.user_system.logout_user()
        self.show_main_frame()

    def display_storage_info(self):
        stats = self.user_system.get_storage_info()
        if stats:
            messagebox.showinfo("Storage Information", 
                                f"Total Size: {stats['size'] / (1024*1024):.2f} MB\n" +
                                f"Average Object Size: {stats['avgObjSize'] / 1024:.2f} KB\n" +
                                f"Number of Objects: {stats['count']}")
        else:
            messagebox.showinfo("Storage Information", "Could not retrieve storage information.")

    def populate_users_list(self):
        # Clear existing cards
        for widget in self.users_inner_frame.winfo_children():
            widget.destroy()

        users = self.user_system.get_all_users()
        if not users:
            no_users_label = tk.Label(self.users_inner_frame, text="No users registered.", bg="#ADD8E6", font=font.Font(family="Helvetica", size=14))
            no_users_label.pack(pady=20)
            return

        for user in users:
            self.create_user_card(self.users_inner_frame, user)
        
        self.users_inner_frame.update_idletasks()
        self.users_canvas.config(scrollregion=self.users_canvas.bbox("all"))

    def delete_user(self, user_id):
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete user {user_id}? This action cannot be undone."):
            if self.user_system.delete_user(user_id):
                messagebox.showinfo("Success", f"User {user_id} deleted successfully.")
                self.populate_users_list() # Refresh the list after deletion
            else:
                messagebox.showerror("Error", f"Failed to delete user {user_id}.")

if __name__ == '__main__':
    root = tk.Tk()
    app = FaceLoginGUI(root)
    root.mainloop()