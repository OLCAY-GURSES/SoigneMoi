import requests
import tkinter as tk
import datetime


class PatientDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tableau de bord des patients")
        self.geometry("800x500")
        self.iconbitmap('C:\\Users\\SESA546828\\PycharmProjects\\SoigneMoi\\DesktopApp\\icons.ico')
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        self.menu_fichier = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="Actualiser la liste",  command=self.refresh_patient_list_immediately)
        #self.menu_fichier.add_command(label="Actualiser immédiatement", command=self.refresh_patient_list_immediately)

        self.menu_edition = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="Déconnexion", command=self.logout_with_window)

        self.incoming_frame = tk.Frame(self)
        self.incoming_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.incoming_label = tk.Label(self.incoming_frame, text="Patients entrants", font=("Arial", 16))
        self.incoming_label.pack()

        self.incoming_listbox = tk.Listbox(self.incoming_frame, height=10, font=("Arial", 12))
        self.incoming_listbox.pack(expand=True, fill=tk.BOTH)

        self.outgoing_frame = tk.Frame(self)
        self.outgoing_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.outgoing_label = tk.Label(self.outgoing_frame, text="Patients sortants", font=("Arial", 16))
        self.outgoing_label.pack()

        self.outgoing_listbox = tk.Listbox(self.outgoing_frame, height=10, font=("Arial", 12))
        self.outgoing_listbox.pack(expand=True, fill=tk.BOTH)

        self.patient_details_frame = tk.Frame(self, bg="white", width=200, height=500)
        self.patient_details_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.incoming_listbox.bind('<<ListboxSelect>>', self.show_incoming_patient_details)
        self.outgoing_listbox.bind('<<ListboxSelect>>', self.show_outgoing_patient_details)

        self.refresh_patient_list()
        self.check_inactivity()

    def show_incoming_patient_details(self, event=None):
        selected_index = self.incoming_listbox.curselection()
        if selected_index:  # Check if an item is selected
            selected_patient = self.start_patients[selected_index[0]]
            self.display_patient_details(selected_patient)

    def show_outgoing_patient_details(self, event=None):
        selected_index = self.outgoing_listbox.curselection()
        if selected_index:  # Check if an item is selected
            if selected_index[0] < len(self.end_patients):  # Check if index is valid
                selected_patient = self.end_patients[selected_index[0]]
                self.display_patient_details(selected_patient)

    def display_patient_details(self, patient):
        for widget in self.patient_details_frame.winfo_children():
            widget.destroy()

        self.patient_details_frame.configure(bg="white")

        center_frame = tk.Frame(self.patient_details_frame, bg="white", width=200, height=200, bd=2,
                                relief=tk.SOLID)
        center_frame.pack(expand=True)

        patient_details_label = tk.Label(center_frame, text="Détails du patient", font=("Arial", 12), bg="gray",
                                         fg="white", bd=2, relief=tk.SOLID)
        patient_details_label.pack(pady=10)

        first_name_label = tk.Label(center_frame, text="Prénom: " + patient['first_name'],
                                    font=("Arial", 10), bg="white")
        first_name_label.pack()

        last_name_label = tk.Label(center_frame, text="Nom: " + patient['last_name'], font=("Arial", 10),
                                   bg="white")
        last_name_label.pack()

        date_of_birth_label = tk.Label(center_frame, text="Date de naissance: " + patient['date_of_birth'],
                                       font=("Arial", 10), bg="white")
        date_of_birth_label.pack()

    def refresh_patient_list(self):
        self.last_activity_time = datetime.datetime.now()
        #response = requests.get('http://localhost:8000/api/secretary/dashboard/')
        response = requests.get('https://sgmlille.pythonanywhere.com/api/secretary/dashboard/')

        if response.status_code == 200:
            data = response.json()
            self.start_patients = data['start_patients']
            self.end_patients = data['end_patients']

            self.incoming_listbox.delete(0, tk.END)
            self.outgoing_listbox.delete(0, tk.END)

            for patient in self.start_patients:
                self.incoming_listbox.insert(tk.END, f"{patient['first_name']} {patient['last_name']}")

            for patient in self.end_patients:
                self.outgoing_listbox.insert(tk.END, f"{patient['first_name']} {patient['last_name']}")

        self.after(60000, self.check_inactivity)

    def refresh_patient_list_immediately(self):
        self.refresh_patient_list()

    def check_inactivity(self):
        current_time = datetime.datetime.now()
        inactive_time = current_time - self.last_activity_time
        if inactive_time.total_seconds() >= 300:  # 5 minutes of inactivity
            self.logout()

        self.after(60000, self.check_inactivity)  # Check inactivity every minute

    def logout(self):
        self.destroy()
        show_login_window()

    def logout_with_window(self):
        self.destroy()
        show_login_window()

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SoigneMoi")
        self.geometry("800x600")
        self.iconbitmap('C:\\Users\\SESA546828\\PycharmProjects\\SoigneMoi\\DesktopApp\\icons.ico')

        self.login_frame = tk.Frame(self)
        self.login_frame.pack(expand=True, pady=50)

        self.title_label = tk.Label(self.login_frame, text="Connectez-vous", font=("Arial", 20))
        self.title_label.pack(pady=10)

        self.username_label = tk.Label(self.login_frame, text="Identifiant", font=("Arial", 12))
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self.login_frame, font=("Arial", 12))
        self.username_entry.pack(pady=10)
        self.username_entry.bind('<KeyRelease>', self.enable_login_button)

        self.password_label = tk.Label(self.login_frame, text="Mot de passe", font=("Arial", 12))
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=10)
        self.password_entry.bind('<KeyRelease>', self.enable_login_button)

        self.login_button = tk.Button(self.login_frame, text="Connexion", background="#32DFFF",
                                      foreground="white",
                                      font=("Arial", 12), command=self.login)
        self.login_button.pack(pady=20)
        self.login_button.bind('<ButtonPress-1>', self.button_pressed)
        self.login_button.bind('<ButtonRelease-1>', self.button_released)
        self.login_button.config(state=tk.DISABLED)  # Disable the login button at startup

        self.label_error = tk.Label(self.login_frame, text="", font=("Arial", 12), fg="red")
        self.label_error.pack(pady=0)

        self.quit_button = tk.Button(self.login_frame, text="Quitter", background="#FF0000", foreground="white",
                                     font=("Arial", 12), command=self.destroy)
        self.quit_button.pack(pady=0)

        self.username_entry.focus()  # Set focus to the username entry field

        self.bind('<Return>', self.handle_enter_key)  # Bind the Enter key to the handle_enter_key method

    def enable_login_button(self, event):
        if self.username_entry.get() and self.password_entry.get():
            self.login_button.config(state=tk.NORMAL)
        else:
            self.login_button.config(state=tk.DISABLED)

    def button_pressed(self, event):
        self.login_button.config(relief=tk.SUNKEN)

    def button_released(self, event):
        self.login_button.config(relief=tk.RAISED)

    def handle_enter_key(self, event):
        self.login_button.config(relief=tk.SUNKEN)
        self.update()
        self.login()
        self.login_button.config(relief=tk.RAISED)
        self.update()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        #response = requests.post('http://localhost:8000/api/user/login/',
        #                        data={'username': username, 'password': password})
        response = requests.post('https://sgmlille.pythonanywhere.com/api/user/login/',
                                 data={'username': username, 'password': password})

        if response.status_code == 200:
            user_data = response.json()
            if user_data['role'] == 'is_secretary':
                self.destroy()
                show_patient_dashboard()
            else:
                error_message = "Erreur de connexion : Vous n'êtes pas autorisé à accéder à cette fonctionnalité"
                self.label_error.config(text=error_message)
        else:
            error_message = "Erreur de connexion : Veuillez vérifier vos identifiants ou mots de passe."
            self.label_error.config(text=error_message)
            self.after(5000, self.hide_error_message)
            self.update_idletasks()

    def hide_error_message(self):
        self.label_error.config(text="")





def show_login_window():
    login_window = LoginWindow()
    login_window.mainloop()

def show_patient_dashboard():
    patient_dashboard = PatientDashboard()
    patient_dashboard.mainloop()

if __name__ == "__main__":
    show_login_window()


