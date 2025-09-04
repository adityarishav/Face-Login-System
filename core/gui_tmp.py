import customtkinter
from tkinter import messagebox
import threading
import time
from core.user_system import UserSystem

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class FaceLoginGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Face Recognition Login")
        self.geometry("500x700")
        self.resizable(False, False)

        # Create a main container frame for all content
        self.main_container = customtkinter.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)

        # Create a canvas and a scrollbar
        self.canvas = customtkinter.CTkCanvas(self.main_container)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = customtkinter.CTkScrollbar(self.main_container, command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

        # Create an inner frame inside the canvas to hold all other frames
        self.inner_frame = customtkinter.CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Bind the scroll wheel to the canvas
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        self.user_system = UserSystem()

        self.create_main_frame()
        self.create_login_frame()
        self.create_admin_register_frame()
        self.create_admin_dashboard_frame()
        self.create_user_dashboard_frame()
        self.create_view_users_frame()
        self.create_loading_spinner()

        if self.user_system.is_db_empty():
            self.create_initial_register_frame()
            self.show_initial_register_frame()
        else:
            self.show_main_frame()

    def create_main_frame(self):
        self.main_frame = customtkinter.CTkFrame(self.inner_frame, width=500, height=700)
        self.main_frame.pack_propagate(False) # Prevent frame from resizing to fit children
        
        login_button = customtkinter.CTkButton(self.main_frame, text="Login", command=self.show_login_frame, width=200, height=50, font=("Segoe UI", 16, "bold"))
        login_button.place(relx=0.5, rely=0.5, anchor="center")

    def create_initial_register_frame(self):
        self.initial_register_frame = customtkinter.CTkFrame(self.inner_frame, width=500, height=700)
        self.initial_register_frame.pack_propagate(False)

        label = customtkinter.CTkLabel(self.initial_register_frame, text="Initial Admin Registration", font=("Segoe UI", 24, "bold"))
        label.pack(pady=20)

        self.initial_user_id_entry = customtkinter.CTkEntry(self.initial_register_frame, placeholder_text="User ID", width=250, height=30)
        self.initial_user_id_entry.pack(pady=10)

        self.initial_name_entry = customtkinter.CTkEntry(self.initial_register_frame, placeholder_text="Name", width=250, height=30)
        self.initial_name_entry.pack(pady=10)

        self.initial_login_key_entry = customtkinter.CTkEntry(self.initial_register_frame, placeholder_text="Login Key", show="*", width=250, height=30)
        self.initial_login_key_entry.pack(pady=10)

        register_button = customtkinter.CTkButton(self.initial_register_frame, text="Register Admin", command=self.register_initial_admin, width=200, height=50, font=("Segoe UI", 16, "bold"))
        register_button.pack(pady=20)

    def create_login_frame(self):
        self.login_frame = customtkinter.CTkFrame(self.inner_frame, width=500, height=700)
        self.login_frame.pack_propagate(False)

        label = customtkinter.CTkLabel(self.login_frame, text="Login", font=("Segoe UI", 24, "bold"))
        label.pack(pady=20)

        self.login_key_entry_login = customtkinter.CTkEntry(self.login_frame, placeholder_text="Login Key", show="*", width=250, height=30)
        self.login_key_entry_login.pack(pady=10)

        login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_user_threaded, width=200, height=50, font=("Segoe UI", 16, "bold"))
        login_button.pack(pady=20)

        back_button = customtkinter.CTkButton(self.login_frame, text="Back", command=self.show_main_frame, width=200, height=50, font=("Segoe UI", 16, "bold"))
        back_button.pack(pady=10)

    def create_admin_dashboard_frame(self):
        self.admin_dashboard_frame = customtkinter.CTkFrame(self.inner_frame, width=500, height=700)
        self.admin_dashboard_frame.pack_propagate(False)

        self.admin_name_label = customtkinter.CTkLabel(self.admin_dashboard_frame, text="", font=("Segoe UI", 16))
        self.admin_name_label.pack(pady=10)

        register_button = customtkinter.CTkButton(self.admin_dashboard_frame, text="Register New User", command=self.show_admin_register_frame, width=200, height=50, font=("Segoe UI", 16, "bold"))
        register_button.pack(pady=10)

        view_users_button = customtkinter.CTkButton(self.admin_dashboard_frame, text="View Users", command=self.show_view_users_frame, width=200, height=50, font=("Segoe UI", 16, "bold"))
        view_users_button.pack(pady=10)

        storage_info_button = customtkinter.CTkButton(self.admin_dashboard_frame, text="Get Storage Info", command=self.display_storage_info, width=200, height=50, font=("Segoe UI", 16, "bold"))
        storage_info_button.pack(pady=10)

        logout_button = customtkinter.CTkButton(self.admin_dashboard_frame, text="Logout", command=self.logout, width=200, height=50, font=("Segoe UI", 16, "bold"))
        logout_button.pack(pady=10)

    # def create_user_dashboard_frame(self):
    #     self.user_dashboard_frame = customtkinter.CTkFrame(self.inner_frame, width=500, height=700)
    #     self.user_dashboard_frame.pack_propagate(False)

    #     # Profile Card
    #     profile_card = customtkinter.CTkFrame(self.user_dashboard_frame, corner_radius=10)
    #     profile_card.pack(pady=20, padx=20, fill="x")

    #     customtkinter.CTkLabel(profile_card, text="User Profile", font=("Segoe UI", 20, "bold")).pack(pady=10)
    #     self.profile_name_label = customtkinter.CTkLabel(profile_card, text="Name: ", font=("Segoe UI", 14))
    #     self.profile_name_label.pack(anchor="w", padx=10)
    #     self.profile_id_label = customtkinter.CTkLabel(profile_card, text="User ID: ", font=("Segoe UI", 14))
    #     self.profile_id_label.pack(anchor="w", padx=10)
    #     self.profile_role_label = customtkinter.CTkLabel(profile_card, text="Role: ", font=("Segoe UI", 14))
    #     self.profile_role_label.pack(anchor="w", padx=10, pady=(0, 10))

    #     # Status Section
    #     status_section = customtkinter.CTkFrame(self.user_dashboard_frame, corner_radius=10)
    #     status_section.pack(pady=10, padx=20, fill="x")

    #     customtkinter.CTkLabel(status_section, text="Status", font=("Segoe UI", 20, "bold")).pack(pady=10)
    #     self.last_login_label = customtkinter.CTkLabel(status_section, text="Last Login: ", font=("Segoe UI", 14))
    #     self.last_login_label.pack(anchor="w", padx=10)
    #     self.face_recognition_status_label = customtkinter.CTkLabel(status_section, text="Face Recognition: ", font=("Segoe UI", 14))
    #     self.face_recognition_status_label.pack(anchor="w", padx=10, pady=(0, 10))

    #     # Security Settings Section
    #     security_section = customtkinter.CTkFrame(self.user_dashboard_frame, corner_radius=10)
    #     security_section.pack(pady=10, padx=20, fill="x")

    #     customtkinter.CTkLabel(security_section, text="Security Settings", font=("Segoe UI", 20, "bold")).pack(pady=10)
    #     change_key_button = customtkinter.CTkButton(security_section, text="Change Login Key", font=("Segoe UI", 14, "bold"), command=lambda: messagebox.showinfo("Info", "Change Login Key functionality not implemented yet."))
    #     change_key_button.pack(pady=5, padx=10, fill="x")
    #     update_face_button = customtkinter.CTkButton(security_section, text="Update Face Data", font=("Segoe UI", 14, "bold"), command=lambda: messagebox.showinfo("Info", "Update Face Data functionality not implemented yet."))
    #     update_face_button.pack(pady=5, padx=10, fill="x", expand=True)
        
    #     # Recent Activity Log
    #     activity_log_section = customtkinter.CTkFrame(self.user_dashboard_frame, corner_radius=10)
    #     activity_log_section.pack(pady=10, padx=20, fill="both", expand=True)

    #     customtkinter.CTkLabel(activity_log_section, text="Recent Activity", font=("Segoe UI", 20, "bold")).pack(pady=10)
    #     self.activity_log_textbox = customtkinter.CTkTextbox(activity_log_section, wrap="word", font=("Segoe UI", 12))
    #     self.activity_log_textbox.pack(pady=5, padx=10, fill="both", expand=True)
    #     self.activity_log_textbox.configure(state="disabled") # Make it read-only

    #     # Logout Button
    #     logout_button = customtkinter.CTkButton(self.user_dashboard_frame, text="Logout", command=self.logout, width=200, height=50, font=("Segoe UI", 16, "bold"), fg_color="red", hover_color="darkred")
    #     logout_button.pack(pady=20)
        
    def create_user_dashboard_frame(self):
        self.user_dashboard_frame = customtkinter.CTkFrame(self.inner_frame, width=500, height=700)
        self.user_dashboard_frame.pack_propagate(False)

        # Profile Card
        profile_card = customtkinter.CTkFrame(self.user_dashboard_frame, corner_radius=10)
        profile_card.pack(pady=20, padx=20, fill="x")

        customtkinter.CTkLabel(profile_card, text="User Profile", font=("Segoe UI", 20, "bold")).pack(pady=10)
        self.profile_name_label = customtkinter.CTkLabel(profile_card, text="Name: ", font=("Segoe UI", 14))
        self.profile_name_label.pack(anchor="w", padx=10)
        self.profile_id_label = customtkinter.CTkLabel(profile_card, text="User ID: ", font=("Segoe UI", 14))
        self.profile_id_label.pack(anchor="w", padx=10)
        self.profile_role_label = customtkinter.CTkLabel(profile_card, text="Role: ", font=("Segoe UI", 14))
        self.profile_role_label.pack(anchor="w", padx=10, pady=(0, 10))

        # 🔴 Logout Button INSIDE Profile Card
        logout_button = customtkinter.CTkButton(
            profile_card,
            text="Logout",
            command=self.logout,
            width=150,
            height=40,
            font=("Segoe UI", 14, "bold"),
            fg_color="red",
            hover_color="darkred"
        )
        logout_button.pack(pady=10)

        # Status Section
        status_section = customtkinter.CTkFrame(self.user_dashboard_frame, corner_radius=10)
        status_section.pack(pady=10, padx=20, fill="x")

        customtkinter.CTkLabel(status_section, text="Status", font=("Segoe UI", 20, "bold")).pack(pady=10)
        self.last_login_label = customtkinter.CTkLabel(status_section, text="Last Login: ", font=("Segoe UI", 14))
        self.last_login_label.pack(anchor="w", padx=10)
        self.face_recognition_status_label = customtkinter.CTkLabel(status_section, text="Face Recognition: ", font=("Segoe UI", 14))
        self.face_recognition_status_label.pack(anchor="w", padx=10, pady=(0, 10))

        # Security Settings Section
        security_section = customtkinter.CTkFrame(self.user_dashboard_frame, corner_radius=10)
        security_section.pack(pady=10, padx=20, fill="x")

        customtkinter.CTkLabel(security_section, text="Security Settings", font=("Segoe UI", 20, "bold")).pack(pady=10)
        change_key_button = customtkinter.CTkButton(security_section, text="Change Login Key", font=("Segoe UI", 14, "bold"), command=lambda: messagebox.showinfo("Info", "Change Login Key functionality not implemented yet."))
        change_key_button.pack(pady=5, padx=10, fill="x")
        update_face_button = customtkinter.CTkButton(security_section, text="Update Face Data", font=("Segoe UI", 14, "bold"), command=lambda: messagebox.showinfo("Info", "Update Face Data functionality not implemented yet."))
        update_face_button.pack(pady=5, padx=10, fill="x", expand=True)

        # Recent Activity Log
        activity_log_section = customtkinter.CTkFrame(self.user_dashboard_frame, corner_radius=10)
        activity_log_section.pack(pady=10, padx=20, fill="both", expand=True)

        customtkinter.CTkLabel(activity_log_section, text="Recent Activity", font=("Segoe UI", 20, "bold")).pack(pady=10)
        self.activity_log_textbox = customtkinter.CTkTextbox(activity_log_section, wrap="word", font=("Segoe UI", 12))
        self.activity_log_textbox.pack(pady=5, padx=10, fill="both", expand=True)
        self.activity_log_textbox.configure(state="disabled") # Make it read-only

    def create_view_users_frame(self):
        self.view_users_frame = customtkinter.CTkFrame(self.inner_frame, width=500, height=700)
        self.view_users_frame.pack_propagate(False)

        label = customtkinter.CTkLabel(self.view_users_frame, text="View Users", font=("Segoe UI", 24, "bold"))
        label.pack(pady=20)

        self.users_display_frame = customtkinter.CTkScrollableFrame(self.view_users_frame, width=400, height=400)
        self.users_display_frame.pack(pady=10, padx=20)

        back_button = customtkinter.CTkButton(self.view_users_frame, text="Back to Dashboard", command=self.show_admin_dashboard_frame, width=200, height=50, font=("Segoe UI", 16, "bold"))
        back_button.pack(pady=10)

    def create_admin_register_frame(self):
        self.admin_register_frame = customtkinter.CTkFrame(self.inner_frame, width=500, height=700)
        self.admin_register_frame.pack_propagate(False)

        label = customtkinter.CTkLabel(self.admin_register_frame, text="Admin Register User", font=("Segoe UI", 24, "bold"))
        label.pack(pady=20)

        self.admin_user_id_entry = customtkinter.CTkEntry(self.admin_register_frame, placeholder_text="User ID", width=250, height=30)
        self.admin_user_id_entry.pack(pady=10)

        self.admin_name_entry = customtkinter.CTkEntry(self.admin_register_frame, placeholder_text="Name", width=250, height=30)
        self.admin_name_entry.pack(pady=10)

        self.admin_login_key_entry = customtkinter.CTkEntry(self.admin_register_frame, placeholder_text="Login Key", show="*", width=250, height=30)
        self.admin_login_key_entry.pack(pady=10)

        self.role_var = customtkinter.StringVar(value="normal")
        self.role_option_menu = customtkinter.CTkOptionMenu(self.admin_register_frame, variable=self.role_var, values=["normal", "admin"], width=250, height=30, font=("Segoe UI", 14))
        self.role_option_menu.pack(pady=10)

        register_button = customtkinter.CTkButton(self.admin_register_frame, text="Register User", command=self.admin_register_user_threaded, width=200, height=50, font=("Segoe UI", 16, "bold"))
        register_button.pack(pady=20)

        back_button = customtkinter.CTkButton(self.admin_register_frame, text="Back to Dashboard", command=self.show_admin_dashboard_frame, width=200, height=50, font=("Segoe UI", 16, "bold"))
        back_button.pack(pady=10)

    def create_loading_spinner(self):
        self.loading_frame = customtkinter.CTkFrame(self.inner_frame, width=500, height=700)
        self.loading_frame.pack_propagate(False)
        self.loading_label = customtkinter.CTkLabel(self.loading_frame, text="Processing...", font=("Segoe UI", 24, "bold"))
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
        self.spinner_dots = 0

    def show_loading_spinner(self):
        self.hide_all_frames()
        self.loading_frame.pack(fill="both", expand=True)
        self.animate_loading_spinner()

    def hide_loading_spinner(self):
        self.loading_frame.pack_forget()

    def animate_loading_spinner(self):
        dots = "." * self.spinner_dots
        self.loading_label.configure(text=f"Processing{dots}")
        self.spinner_dots = (self.spinner_dots + 1) % 4
        self.after(500, self.animate_loading_spinner)

    def show_main_frame(self):
        self.hide_all_frames()
        self.main_frame.pack(fill="both", expand=True)

    def show_initial_register_frame(self):
        self.hide_all_frames()
        self.initial_register_frame.pack(fill="both", expand=True)

    def show_login_frame(self):
        self.hide_all_frames()
        self.login_frame.pack(fill="both", expand=True)

    def show_admin_dashboard_frame(self):
        user = self.user_system.get_logged_in_user()
        if not user or user['role'] != 'admin':
            messagebox.showerror("Error", "Access denied.")
            self.show_main_frame()
            return
        self.hide_all_frames()
        self.admin_name_label.configure(text=f"Welcome, {user['name']}!")
        self.admin_dashboard_frame.pack(fill="both", expand=True)

    def show_user_dashboard_frame(self):
        user = self.user_system.get_logged_in_user()
        if not user:
            messagebox.showerror("Error", "Access denied.")
            self.show_main_frame()
            return
        self.hide_all_frames()

        # Populate Profile Card
        self.profile_name_label.configure(text=f"Name: {user.get('name', 'N/A')}")
        self.profile_id_label.configure(text=f"User ID: {user.get('user_id', 'N/A')}")
        self.profile_role_label.configure(text=f"Role: {user.get('role', 'N/A')}")

        # Populate Status Section
        # NOTE: UserSystem needs to be updated to store and retrieve last login time.
        # For now, using a placeholder.
        last_login_time = "N/A (Not implemented in UserSystem)" # self.user_system.get_last_login(user['user_id'])
        self.last_login_label.configure(text=f"Last Login: {last_login_time}")

        # Determine Face Recognition Status
        # NOTE: UserSystem needs to be updated to explicitly store face recognition status.
        # Inferring from 'frames' existence for now.
        face_data_exists = False
        all_users = self.user_system.get_all_users()
        for u in all_users:
            if u.get('user_id') == user.get('user_id'):
                if u.get('frames') and len(u.get('frames')) > 0:
                    face_data_exists = True
                break
        
        face_status = "✅ Active" if face_data_exists else "❌ Inactive"
        self.face_recognition_status_label.configure(text=f"Face Recognition: {face_status}")

        # Populate Recent Activity Log
        # NOTE: UserSystem needs to be updated to store and retrieve activity logs.
        # For now, using placeholder data.
        activity_logs = [
            "2025-08-19 10:00:00 - Login successful",
            "2025-08-19 09:30:00 - Failed login attempt (incorrect key)",
            "2025-08-18 18:00:00 - Login successful"
        ] # self.user_system.get_user_activity(user['user_id'])
        self.activity_log_textbox.configure(state="normal") # Enable editing to insert text
        self.activity_log_textbox.delete("1.0", "end")
        for log in activity_logs:
            self.activity_log_textbox.insert("end", log + "\n")
        self.activity_log_textbox.configure(state="disabled") # Make it read-only again

        self.user_dashboard_frame.pack(fill="both", expand=True)
        
        logout_button = customtkinter.CTkButton(self.admin_dashboard_frame, text="Logout", command=self.logout, width=200, height=50, font=("Segoe UI", 16, "bold"))
        logout_button.pack(pady=20)
        

    def show_view_users_frame(self):
        user = self.user_system.get_logged_in_user()
        if not user or user['role'] != 'admin':
            messagebox.showerror("Error", "Access denied.")
            self.show_main_frame()
            return
        self.hide_all_frames()
        self.populate_users_list()
        self.view_users_frame.pack(fill="both", expand=True)

    def show_admin_register_frame(self):
        user = self.user_system.get_logged_in_user()
        if not user or user['role'] != 'admin':
            messagebox.showerror("Error", "Access denied.")
            self.show_main_frame()
            return
        self.hide_all_frames()
        self.admin_register_frame.pack(fill="both", expand=True)

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
        self.loading_frame.pack_forget() # Hide loading frame as well

    def create_user_card(self, parent_frame, user):
        card_frame = customtkinter.CTkFrame(parent_frame)
        card_frame.pack(pady=5, padx=10, fill="x", expand=True)

        user_id_label = customtkinter.CTkLabel(card_frame, text=f"ID: {user['user_id']}", font=("Segoe UI", 12, "bold"))
        user_id_label.pack(anchor="w", padx=10, pady=2)

        name_label = customtkinter.CTkLabel(card_frame, text=f"Name: {user['name']}", font=("Segoe UI", 12))
        name_label.pack(anchor="w", padx=10, pady=2)

        role_label = customtkinter.CTkLabel(card_frame, text=f"Role: {user['role']}", font=("Segoe UI", 12))
        role_label.pack(anchor="w", padx=10, pady=2)

        delete_button = customtkinter.CTkButton(card_frame, text="Delete", command=lambda: self.delete_user(user['user_id']), fg_color="#FF6B6B", hover_color="#FF4C4C", font=("Segoe UI", 12, "bold"))
        delete_button.pack(pady=5)

        return card_frame

    def register_initial_admin(self):
        user_id = self.initial_user_id_entry.get()
        name = self.initial_name_entry.get()
        login_key = self.initial_login_key_entry.get()

        if not user_id or not login_key or not name:
            messagebox.showerror("Error", "User ID, Name, and Login Key are required.")
            return
        
        self.show_loading_spinner()
        # Use threading to prevent GUI freeze
        threading.Thread(target=self._register_initial_admin_threaded, args=(user_id, name, login_key)).start()

    def _register_initial_admin_threaded(self, user_id, name, login_key):
        try:
            self.user_system.register_user(user_id, login_key, "admin", name)
            messagebox.showinfo("Success", "Initial admin registered successfully!")
            self.initial_register_frame.pack_forget()
            self.show_main_frame()
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
        finally:
            self.hide_loading_spinner()

    def admin_register_user_threaded(self):
        user_id = self.admin_user_id_entry.get()
        name = self.admin_name_entry.get()
        login_key = self.admin_login_key_entry.get()
        role = self.role_var.get()

        if not user_id or not login_key or not name:
            messagebox.showerror("Error", "User ID, Name, and Login Key are required.")
            return
        
        self.show_loading_spinner()
        threading.Thread(target=self._admin_register_user_threaded, args=(user_id, name, login_key, role)).start()

    def _admin_register_user_threaded(self, user_id, name, login_key, role):
        try:
            self.user_system.register_user(user_id, login_key, role, name)
            messagebox.showinfo("Success", f"User {user_id} ({role}) registered successfully!")
            self.admin_user_id_entry.delete(0, 'end')
            self.admin_name_entry.delete(0, 'end')
            self.admin_login_key_entry.delete(0, 'end')
            self.role_var.set("normal")
            self.show_admin_dashboard_frame()
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
        finally:
            self.hide_loading_spinner()

    def login_user_threaded(self):
        login_key = self.login_key_entry_login.get()

        if not login_key:
            messagebox.showerror("Error", "Login Key is required.")
            return
        
        self.show_loading_spinner()
        threading.Thread(target=self._login_user_threaded, args=(login_key,)).start()

    def _login_user_threaded(self, login_key):
        try:
            user_info = self.user_system.login_user(login_key)
            if user_info:
                messagebox.showinfo("Success", f"Login successful! Welcome {user_info['name']}!")
                if user_info['role'] == 'admin':
                    self.show_admin_dashboard_frame()
                else:
                    self.show_user_dashboard_frame()
            else:
                messagebox.showerror("Error", "Face not recognized or login key incorrect.")
                self.show_login_frame() # Add this line to return to the login frame
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {e}")
            self.show_login_frame() # Add this line to return to the login frame
        finally:
            self.hide_loading_spinner()

    def logout(self):
        self.user_system.logout_user()
        self.show_main_frame()

    def display_storage_info(self):
        stats = self.user_system.get_storage_info()
        if stats:
            messagebox.showinfo("Storage Information", 
                                f"Total Size: {stats['size'] / (1024*1024):.2f} MB\n" +
                                f"Average Object Size: {stats['avgObjSize'] / 1024:.2f} KB\n"
                                f"Number of Objects: {stats['count']}")
        else:
            messagebox.showinfo("Storage Information", "Could not retrieve storage information.")

    def populate_users_list(self):
        for widget in self.users_display_frame.winfo_children():
            widget.destroy()

        users = self.user_system.get_all_users()
        if not users:
            no_users_label = customtkinter.CTkLabel(self.users_display_frame, text="No users registered.", font=("Segoe UI", 14))
            no_users_label.pack(pady=20)
            return

        for user in users:
            self.create_user_card(self.users_display_frame, user)

    def delete_user(self, user_id):
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete user {user_id}? This action cannot be undone."):
            if self.user_system.delete_user(user_id):
                messagebox.showinfo("Success", f"User {user_id} deleted successfully.")
                self.populate_users_list()
            else:
                messagebox.showerror("Error", f"Failed to delete user {user_id}.")

if __name__ == '__main__':
    app = FaceLoginGUI()
    app.mainloop()
