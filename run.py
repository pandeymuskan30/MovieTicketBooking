#Python_Project_sem2
#Muskan Rambachan Pandey   #F098  #First Year Computer Science
import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime

# Create a connection to the SQLite database
conn = sqlite3.connect('movietickets.db')
c = conn.cursor()


# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS userss
             (firstname TEXT, lastname TEXT, age INTEGER, gender TEXT, show TEXT,
             time TEXT, date TEXT, num_tickets INTEGER, totalbill REAL, username TEXT, password TEXT, selected_seats TEXT)''')

movie_time_details = [
        ("12th Fail", "11:00 AM"), ("Hi Nanna", "11:00 AM"), ("Jawan", "11:00 AM"), ("Fighter", "11:00 AM"),
        ("12th Fail", "4:00 PM"), ("Hi Nanna", "4:00 PM"), ("Jawan", "4:00 PM"),
        ("12th Fail", "8:00 PM"), ("Hi Nanna", "8:00 PM"), ("Jawan", "8:00 PM"), ("Fighter", "8:00 PM")
        ]

        # Insert values into the 'details' table
c.execute('''CREATE TABLE IF NOT EXISTS details
             (show TEXT, time TEXT)''')
c.executemany("INSERT INTO details (show, time) VALUES (?, ?)", movie_time_details)
conn.commit()

username = ""
password = ""
payment_amount = None  # Global variable to store payment amount

class PreBookingWindow:
    def __init__(self, parent):
        self.parent = parent
        self.pre_booking_window = tk.Toplevel(parent)
        self.pre_booking_window.title("Pre Booking")
        self.pre_booking_window.geometry("1200x790+50+0")
        self.pre_booking_window.config(bg="pink")

        self.label = tk.Label(self.pre_booking_window, text="Pre Booking Window", font=("Arial", 16))
        self.label.pack(pady=20)

        self.fname_label = tk.Label(self.pre_booking_window, text="First Name:", font=("Arial", 12))
        self.fname_label.pack(pady=5)
        self.fname_entry = tk.Entry(self.pre_booking_window, font=("Arial", 12))
        self.fname_entry.pack(pady=5)

        self.lname_label = tk.Label(self.pre_booking_window, text="Last Name:", font=("Arial", 12))
        self.lname_label.pack(pady=5)
        self.lname_entry = tk.Entry(self.pre_booking_window, font=("Arial", 12))
        self.lname_entry.pack(pady=5)

        self.age_label = tk.Label(self.pre_booking_window, text="Age:", font=("Arial", 12))
        self.age_label.pack(pady=5)
        self.age_entry = tk.Entry(self.pre_booking_window, font=("Arial", 12))
        self.age_entry.pack(pady=5)
 
        self.num_tickets_label = tk.Label(self.pre_booking_window, text="Number of Tickets:", font=("Arial", 12))
        self.num_tickets_label.pack(pady=10)

        # Option menu for selecting number of tickets USING 
        self.num_tickets_var = tk.IntVar()
        self.num_tickets_var.set(1)
        num_tickets_options = list(range(1, 26))
        self.num_tickets_option_menu = tk.OptionMenu(self.pre_booking_window, self.num_tickets_var, *num_tickets_options)
        self.num_tickets_option_menu.pack(pady=5)

        self.movie_label = tk.Label(self.pre_booking_window, text="Select Movie:", font=("Arial", 12))
        self.movie_label.pack(pady=10)

        self.selected_movie = tk.StringVar()
        self.selected_movie.set([0])

        # Radio buttons for movie selection
        self.movies = [("Housefull 5  (June 24)", 550), ("Stree 2 (August 24)", 500), ("Bhool bhulaiyaa 3 (Novemeber 24)", 600)]
        self.movie_buttons = []
        for movie, price in self.movies:
            tk.Radiobutton(self.pre_booking_window, text=movie + " - Rs." + str(price), variable=self.selected_movie, value=movie).pack()

        self.num_tickets_label = tk.Label(self.pre_booking_window, text="Number of Tickets:", font=("Arial", 12))
        self.num_tickets_label.pack(pady=10)

        #pay
        self.pay_button = tk.Button(self.pre_booking_window, text="Pay", command=self.open_payment_window)
        self.pay_button.pack(pady=10)
        #process
        self.process_button = tk.Button(self.pre_booking_window, text="Process", command=lambda: self.process_show_details(payment_amount))
        self.process_button.pack(pady=10)

        self.close_button = tk.Button(self.pre_booking_window, text="Close", command=self.pre_booking_window.destroy)
        self.close_button.pack(pady=10)
        

    def process_show_details(self,payment_amount):
        firstname = self.fname_entry.get().strip()
        lastname = self.lname_entry.get().strip()
        num_tickets = self.num_tickets_var.get()
        selected_movie = self.selected_movie.get()
        age = self.age_entry.get().strip()

        if not firstname or not lastname or not age or not num_tickets or not selected_movie or not payment_amount:
            messagebox.showerror("Error", "Please fill in all details.")
            return

        if payment_amount is None:
           messagebox.showerror("Error", "Please enter the payment amount.")
           return

        # Check if first name contains only alphabetic characters
        if not firstname.isalpha():
            messagebox.showerror("Error", "First name should contain only alphabetic characters.")
            return

        # Check if last name contains only alphabetic characters
        if not lastname.isalpha():
            messagebox.showerror("Error", "Last name should contain only alphabetic characters.")
            return

        # Validate age input
        try:
            age = int(age)
            if age <= 0:
                raise ValueError("Age must be a positive integer")
        except ValueError:
            messagebox.showerror("Error", "Invalid age. Please enter a valid number.")
            return

        c.execute('''CREATE TABLE IF NOT EXISTS prebooking
                 (firstname TEXT, lastname TEXT, age INTEGER, num_tickets INTEGER,
                 selected_movie TEXT, payment REAL)''')
        c.execute("INSERT INTO prebooking (firstname, lastname, age, num_tickets, selected_movie, payment) VALUES (?, ?, ?, ?, ?, ?)",
              (firstname, lastname, age, num_tickets, selected_movie,payment_amount))
        conn.commit()

        messagebox.showinfo("Success", "Booking details saved successfully!")

        details_window = tk.Toplevel(self.pre_booking_window)
        details_window.title("Show Details")
        details_window.geometry("800x500+350+150")
        confirmation_time = datetime.datetime.now().strftime("%H:%M:%S on %Y-%m-%d")
        details_label = tk.Label(details_window, text=f"Congratulation you have sucessfuly booked you Pre-Booking\nName: {firstname} {lastname}\nNumber of Tickets: {num_tickets}\nAge: {age}\nSelected Movie: {selected_movie}\nPayment: {payment_amount}\nYour booking has been confirmed at {confirmation_time}", font=("Arial", 12))
        details_label.pack(pady=20)


    def open_payment_window(self):
        selected_movie = self.selected_movie.get()
        num_tickets = self.num_tickets_var.get()
        if selected_movie:
            movie_price = 550 if selected_movie.startswith("Housefull 5") else (500 if selected_movie.startswith("Stree2 ") else 600)
            total_amount = movie_price * num_tickets
            payment_window = tk.Toplevel(self.pre_booking_window)
            payment_window.title("Pre Payment Window")  # Change title here
            payment_window.geometry("500x400")

            tk.Label(payment_window, text="Total Amount: Rs.{}".format(total_amount), font=("Arial", 12)).pack(pady=10)

            # Add payment fields here
            tk.Label(payment_window, text="Cardholder Name:", font=("Arial", 12)).pack()
            cardholder_entry = tk.Entry(payment_window, font=("Arial", 12))
            cardholder_entry.pack()

            tk.Label(payment_window, text="Card Number:", font=("Arial", 12)).pack()
            card_number_entry = tk.Entry(payment_window, font=("Arial", 12))
            card_number_entry.pack()

            tk.Label(payment_window, text="Expiry Date (MM/YY):", font=("Arial", 12)).pack()
            expiry_date_entry = tk.Entry(payment_window, font=("Arial", 12))
            expiry_date_entry.pack()

            tk.Label(payment_window, text="CVV:", font=("Arial", 12)).pack()
            cvv_entry = tk.Entry(payment_window, font=("Arial", 12))
            cvv_entry.pack()

            tk.Label(payment_window, text="Payment Amount:", font=("Arial", 12)).pack()
            payment_entry = tk.Entry(payment_window, font=("Arial", 12))
            payment_entry.pack()

            pay_button = tk.Button(payment_window, text="Pay", command=lambda: self.check_payment(payment_window, total_amount, cardholder_entry, card_number_entry, expiry_date_entry, cvv_entry, payment_entry))
            pay_button.pack(pady=10)

            self.process_button.config(command=lambda: self.process_show_details(total_amount))

            

    def check_payment(self, payment_window, total_amount, cardholder_entry, card_number_entry, expiry_date_entry, cvv_entry, payment_entry):
        cardholder_name = cardholder_entry.get().strip()
        card_number = card_number_entry.get().strip()
        expiry_date = expiry_date_entry.get().strip()
        cvv = cvv_entry.get().strip()
        payment_amount = payment_entry.get().strip()

        try:
            # Check if cardholder name contains only alphabetic characters
            if not cardholder_name.isalpha():
                messagebox.showerror("Payment Error", "Cardholder name should contain only alphabetic characters.")
                return

            # Check if card number has 16 digits
            if not (len(card_number) == 16 and card_number.isdigit()):
                messagebox.showerror("Payment Error", "Card number should be a 16-digit numeric value.")
                return

            # Check if CVV has 3 digits
            if not (len(cvv) == 3 and cvv.isdigit()):
                messagebox.showerror("Payment Error", "CVV should be a 3-digit numeric value.")
                return

            # Check if expiry date is in MM/YY format
            if not (len(expiry_date) == 5 and expiry_date[2] == '/' and expiry_date[:2].isdigit() and expiry_date[3:].isdigit()):
                messagebox.showerror("Payment Error", "Expiry date should be in MM/YY format.")
                return

            payment_amount = float(payment_amount)
            if payment_amount == total_amount:
                messagebox.showinfo("Payment Successful", "Payment successful!")
                payment_window.destroy()
                self.pre_booking_window.lift()
            else:
                messagebox.showerror("Payment Error", "Payment amount does not match the total amount.")
        except ValueError:
            messagebox.showerror("Payment Error", "Invalid payment amount. Please enter a valid number.")

        

# login window details
def show_login_window():  
    global username_entry, password_entry, login_window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("800x500+350+150")
    login_window.config(bg="lightgreen")

    username_label = tk.Label(login_window, text="Username:", bg="#7CFC00")           #username_label
    username_label.place(x=150, y=130)
    username_entry = tk.Entry(login_window, bg="#EEE0E5")                             #username_entry
    username_entry.place(x=250, y=130)

    password_label = tk.Label(login_window, text="Password:", bg="#7CFC00")            #password_label
    password_label.place(x=150, y=180)
    password_entry = tk.Entry(login_window, show="*", bg="#EEE0E5")                    #pass_entry
    password_entry.place(x=250, y=180)

    login_button = tk.Button(login_window, text="Login", bg="#98FB98", command=login)  #login_button
    login_button.place(x=350, y=230)
    login_window.mainloop()
# Function to check login
def login():
    global username, password
    username = username_entry.get()
    password = password_entry.get()
    c.execute("SELECT * FROM userss WHERE username = ? AND password = ?", (username, password))
    if username=="muskan" or username=="98765":
        login_window.destroy()
        show_main_window()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def calculate_bill(num_tickets):            #Total_Bill
    ticket_price = 500                      #Price of ticket
    totalbill = ticket_price * num_tickets
    return totalbill

# Function to open the main application window
def show_main_window():
    def open_pre_booking_window():
        pre_booking = PreBookingWindow(main_window)
                                       
    def open_small_window():    #View Details of The Show
        small_window = tk.Toplevel(main_window)
        small_window.title("View Details Window")
        small_window.geometry("800x500+350+150")
        small_window.config(bg="lightgray")
        movie_label = tk.Label(small_window, text="BUY ANY MOVIE TICKET AT 500/-", font=("Arial", 14), bg="lightpink")
        movie_label.place(x=250, y=1)

        label = tk.Label(small_window, text="Available Movies at specific time:\nAt 11:00 AM  \n1) 12th Fail\n2) Hi Nanna\n 3) Jawan\n4) Fighter\n----- \nAt 4:00 PM\n1) 12th Fail\n2) Hi Nanna\n 3) Jawan\n"
        "\n-----\nAt 8:00 PM  \n1) 12th Fail\n2) Hi Nanna\n 3) Jawan\n4) Fighter", font=("Arial", 14), bg="#856ff8", width=25, height=20)
        label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        close_button = tk.Button(small_window, text="Close", command=small_window.destroy, width=10, height=1)
        close_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)


    def open_payment_window():
        global payment_amount_entry,card_holder_entry, card_number_entry, expiry_date_entry, cvv_entry, payment_amount_window
        payment_amount_window = tk.Toplevel()           #Payment_window
        payment_amount_window.title("Enter Payment Details")
        payment_amount_window.geometry("400x300+500+200")

        payment_amount_label = tk.Label(payment_amount_window, text="Payment Amount:", font=("Arial", 12))#payment_labrl
        payment_amount_label.grid(row=0, column=0, padx=10, pady=10)
        payment_amount_entry = tk.Entry(payment_amount_window, font=("Arial", 12))#payment_entry
        payment_amount_entry.grid(row=0, column=1, padx=10, pady=10)

        card_number_label = tk.Label(payment_amount_window, text="Card Number:", font=("Arial", 12))#card_number_labrl
        card_number_label.grid(row=2, column=0, padx=10, pady=10)
        card_number_entry = tk.Entry(payment_amount_window, font=("Arial", 12)) #card_number_entry
        card_number_entry.grid(row=2, column=1, padx=10, pady=10)

        expiry_date_label = tk.Label(payment_amount_window, text="Expiry Date (MM/YY):", font=("Arial", 12))#expiry_date_labrl
        expiry_date_label.grid(row=3, column=0, padx=10, pady=10)
        expiry_date_entry = tk.Entry(payment_amount_window, font=("Arial", 12))             #expiry_date_entry
        expiry_date_entry.grid(row=3, column=1, padx=10, pady=10)

        cvv_label = tk.Label(payment_amount_window, text="CVV:", font=("Arial", 12))#cvv_labrl
        cvv_label.grid(row=4, column=0, padx=10, pady=10)
        cvv_entry = tk.Entry(payment_amount_window, font=("Arial", 12))                     #cvv_entry
        cvv_entry.grid(row=4, column=1, padx=10, pady=10)

        card_holder_label = tk.Label(payment_amount_window, text="Card Holder Name:", font=("Arial", 12))#cardholder_label
        card_holder_label.grid(row=1, column=0, padx=10, pady=10)
        card_holder_entry = tk.Entry(payment_amount_window, font=("Arial", 12))             #cardholder_name                          
        card_holder_entry.grid(row=1, column=1, padx=10, pady=10)

        save_button = tk.Button(payment_amount_window, text="Save", command=save_payment)       
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def save_payment():    #exception_handlings_of_payment
        global payment_amount,card_holder_name, card_number, expiry_date, cvv
        payment_amount = payment_amount_entry.get()
        card_holder_name = card_holder_entry.get()
        card_number = card_number_entry.get()
        expiry_date = expiry_date_entry.get()
        cvv = cvv_entry.get()
        
        # Validate inputs
        try:
            payment_amount = float(payment_amount)
            if payment_amount <= 0:
                raise ValueError("Payment amount must be a positive number")
        except ValueError:
            messagebox.showerror("Error", "Invalid payment amount")
            return

        if not card_holder_name.isalpha():
            try:
                raise ValueError("Name must contain only alphabetic characters")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            return

        if not card_number.isdigit() or len(card_number) != 16:
            try:
                raise ValueError("Invalid card number. It should be a 16-digit number.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            return

        if len(expiry_date) != 5 or expiry_date[2] != '/':
            try:
                raise ValueError("Invalid expiry date format. Use MM/YY format.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            return

        if not cvv.isdigit() or len(cvv) != 3:
            try:
                raise ValueError("Invalid CVV. It should be a 3-digit number.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            return


        # Insert payment details into a new table
        c.execute('''CREATE TABLE IF NOT EXISTS payments (
                     payment_amount REAL,card_holder_name TEXT, card_number TEXT, expiry_date TEXT, cvv TEXT)''')
        c.execute("INSERT INTO payments (payment_amount,card_holder_name, card_number, expiry_date, cvv) VALUES (?,?, ?, ?, ?)",
                  (payment_amount,card_holder_name, card_number, expiry_date, cvv))
        conn.commit()

        payment_amount_window.destroy()

    def submit_booking():
        global username, password
        firstname = firstname_entry.get().strip()
        lastname = lastname_entry.get().strip()
        age = age_entry.get().strip()
        gender = gender_var.get()
        show = show_var.get()
        time = time_var.get()
        num_tickets_str = num_tickets_entry.get().strip()
        date = date_entry.get().strip()

        try:
            if not firstname or not lastname or not age or not num_tickets_str:
                raise ValueError("All fields are required")

            if not firstname.isalpha():
                raise ValueError("Firstname must contain only alphabetic characters")

            if not lastname.isalpha():
                raise ValueError("Lastname must contain only alphabetic characters")

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return


        try:
            age = int(age)
            num_tickets = int(num_tickets_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for Age and Number of Tickets")
            return

        if age <= 0:
            messagebox.showerror("Error", "Age must be a positive integer")
            return

        if num_tickets <= 0 or num_tickets > 25:
            messagebox.showerror("Error", "Number of Tickets must be a positive integer")
            return

        try:
            date_str = date_entry.get().strip()
            if len(date_str) != 8 or date_str[2] != '/' or date_str[5] != '/':
                raise ValueError("Invalid date format. Please use DD/MM/YY format.")
            day = int(date_str[:2])
            month = int(date_str[3:5])
            year = int(date_str[6:])
            if not (1 <= day <= 31 and 1 <= month <= 12 and 0 <= year <= 99):
                raise ValueError("Invalid date values.")
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return
        
        selected_seats = [value for var, value in checkboxes if var.get()]
        if not selected_seats:
            messagebox.showerror("Error", "Please select at least one seat")
            return

        if num_tickets != len(selected_seats):
            messagebox.showerror("Error", "Number of tickets must match the number of selected seats")
            return

        if (show, time) not in movie_time_details:
            messagebox.showerror("Error", "Selected show is not available at the chosen time")
            return

        if payment_amount is None:
            messagebox.showerror("Error", "Please enter the payment amount")
            return

        totalbill = calculate_bill(num_tickets)
        if float(payment_amount) < totalbill:
            messagebox.showerror("Error", "Payment amount should be equal to or greater than the total amount of tickets")
            return

        if float(payment_amount) != totalbill:
            messagebox.showerror("Error", "Payment amount should be equal to the total bill")
            return

        # Insert booking details into the database
        c.execute("INSERT INTO userss (firstname, lastname, age, gender, show, time, date, num_tickets, totalbill, username, password, selected_seats) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (firstname, lastname, age, gender, show, time, date, num_tickets, totalbill, username, password, ','.join(map(str, selected_seats))))
        conn.commit()
        messagebox.showinfo("Success", "Booking submitted successfully!")
        show_billing_window(firstname, lastname, age, gender, show, time, date, num_tickets, totalbill, selected_seats)

    def show_billing_window(firstname, lastname, age, gender, show, time, date, num_tickets, totalbill, selected_seats):

        billing_window = tk.Toplevel()
        billing_window.title("TICKET DETAILS")
        billing_window.geometry("800x500+350+150")
        billing_window.config(bg="pink")
        save_time = datetime.datetime.now().strftime("%H:%M:%S on %Y-%m-%d")

        details_label = tk.Label(billing_window, text="Congratulation you have successful booked your ticket", font=("Arial", 20))
        details_label.pack(pady=10)

        detail_text = f"Name: {firstname} {lastname}\nAge: {age}\nGender: {gender}\nShow: {show}\nTime: {time}\nDate: {date}\nNumber of Tickets: {num_tickets}\nTotal Bill: Rs.{totalbill}\nSelected Seats: {', '.join(map(str, selected_seats))}\nBooking details saved at {save_time}"
        detail_label = tk.Label(billing_window, text=detail_text, justify="left", font=("Arial", 14))
        detail_label.pack(pady=10)

        billing_window.mainloop()

    main_window = tk.Tk()  # MAIN_WINDOW AFTER LOGIN
    main_window.title("Main Application")
    main_window.geometry("1500x800+0+0")  # width*hieght+x_offset+y_offset
    main_window.config(bg="#90EE90")

    def exit_application():
        main_window.destroy()

    def logout():
        main_window.destroy()
        show_login_window()

    def show_about_us():
        about_us_window = tk.Toplevel(main_window)
        about_us_window.title("About Us")
        about_us_window.geometry("500x300")
        about_us_window.resizable(False, False)

        about_us_label = tk.Label(about_us_window, text="This application is created by Muskan Rambachan Pandey\nThe use of this application to book online movie tickets ", font=("Arial", 14))
        about_us_label.pack(pady=20)

    def show_help():
        help_window = tk.Toplevel(main_window)
        help_window.title("Help")
        help_window.geometry("500x300")
        help_window.resizable(False, False)

        help_label = tk.Label(help_window, text="Need any help? \nContact support at support@mymovieshow1388.com", font=("Arial", 14))
        help_label.pack(pady=20)

    menubar = tk.Menu(main_window)

    pre_booking_menu = tk.Menu(menubar, tearoff=0)
    pre_booking_menu.add_command(label="Pre Booking Window", command=open_pre_booking_window)
    menubar.add_cascade(label="Pre Booking", menu=pre_booking_menu)

    # settings menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Logout", command=logout, font=("Arial", 12))  
    file_menu.add_command(label="Exit", command=exit_application, font=("Arial", 12))  
    menubar.add_cascade(label="Settings", menu=file_menu, font=("Arial", 12))  

    # About menu
    about_menu = tk.Menu(menubar, tearoff=0)
    about_menu.add_command(label="About Us", command=show_about_us, font=("Arial", 12))  
    menubar.add_cascade(label="About", menu=about_menu, font=("Arial", 12))  

    # Help menu
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="Help", command=show_help, font=("Arial", 12))  
    menubar.add_cascade(label="Help", menu=help_menu, font=("Arial", 12))  

    main_window.config(menu=menubar)

    label = tk.Label(main_window, text="Welcome BookMyMovie Application!", font=("Arial", 22), bg="#8B7D7B")
    label.place(x=500, y=50)

    entry_width = 40  # NOT FOR ALL LABEL AND ENTRY BUT IT APPLIED SOME OF THEM
    entry_height = 1
    label_width = 10
    label_height = 1

    firstname_label = tk.Label(main_window, text="First Name:", font=("Arial", 14), bg="#FFA07A", width=label_width, height=label_height)  # firstname
    firstname_label.place(x=50, y=130)
    firstname_entry = tk.Entry(main_window, width=entry_width, font=("Arial", 14), bg="#EEAEEE")
    firstname_entry.place(x=180, y=130)

    lastname_label = tk.Label(main_window, text="Last Name:", font=("Arial", 14), bg="#FFA07A", width=label_width, height=label_height)  # lastname
    lastname_label.place(x=50, y=180)
    lastname_entry = tk.Entry(main_window, width=entry_width, font=("Arial", 14), bg="#EEAEEE")
    lastname_entry.place(x=180, y=180)

    age_label = tk.Label(main_window, text="Age:", font=("Arial", 14), bg="#FFA07A", width=label_width, height=label_height)  # age
    age_label.place(x=50, y=230)
    age_entry = tk.Entry(main_window, width=entry_width, font=("Arial", 14), bg="#EEAEEE")
    age_entry.place(x=180, y=230)

    gender_label = tk.Label(main_window, text="Gender:", font=("Arial", 14), bg="#FFA07A", width=label_width, height=label_height)  # gender
    gender_label.place(x=50, y=280)
    gender_var = tk.StringVar(main_window)
    gender_var.set("Male")
    gender_menu = tk.OptionMenu(main_window, gender_var, "Male", "Female", "Other")
    gender_menu.place(x=180, y=280)

    open_small_window_button = tk.Button(main_window, text="VIEW SHOW DETAILS", bg="green", command=open_small_window)  # VIEW SHOW DETAILS
    open_small_window_button.place(x=50, y=330)

    show_label = tk.Label(main_window, text="Show:", font=("Arial", 14), bg="#FFA07A", width=label_width, height=label_height)  # select show
    show_label.place(x=50, y=370)
    show_var = tk.StringVar(main_window)
    show_var.set("Show")
    show_menu = tk.OptionMenu(main_window, show_var, "12th Fail", "Hi Nanna", "Jawan", "Fighter")
    show_menu.place(x=180, y=370)

    time_label = tk.Label(main_window, text="Time:", font=("Arial", 14), bg="#FFA07A", width=label_width, height=label_height)  # select time
    time_label.place(x=50, y=410)
    time_var = tk.StringVar(main_window)
    time_var.set("TIME")
    time_menu = tk.OptionMenu(main_window, time_var, "11:00 AM", "4:00 PM", "8:00 PM")
    time_menu.place(x=180, y=410)

    num_tickets_label = tk.Label(main_window, text="Number of Tickets:", font=("Arial", 14), bg="#FFA07A", width=14, height=label_height)  # Number of Tickets
    num_tickets_label.place(x=50, y=460)
    num_tickets_entry = tk.Entry(main_window, width=42, font=("Arial", 14), bg="#EEAEEE")
    num_tickets_entry.place(x=220, y=460)

    date_label = tk.Label(main_window, text="Date:", font=("Arial", 14), bg="#FFA07A", width=label_width, height=label_height)
    date_label.place(x=50, y=500)
    date_entry = tk.Entry(main_window, width=entry_width, font=("Arial", 14), bg="#EEAEEE")
    date_entry.place(x=180, y=500)

    payment_amount_label = tk.Label(main_window, text="Payment :", font=("Arial", 14), bg="#FFA07A", width=label_width, height=label_height)  # payment
    payment_amount_label.place(x=50, y=550)
    payment_amount_button = tk.Button(main_window, text="Add Card Payment ", command=open_payment_window)
    payment_amount_button.place(x=180, y=550)

    seats_label = tk.Label(main_window, text="Select Seat:", font=("Arial", 14), bg="#FFA07A", width=14, height=label_height)  # select seat
    seats_label.place(x=50, y=600)

    # Checkboxes
    checkbox_values = list(range(1, 26))
    checkboxes = []
    for i, value in enumerate(checkbox_values):
        row = i // 5
        column = i % 5
        var = tk.BooleanVar(main_window)
        checkbox = tk.Checkbutton(main_window, text=str(value), font=("Arial", 12), variable=var, onvalue=True, offvalue=False)
        checkbox.place(x=300 + (column * 80), y=600 + (row * 30))
        checkboxes.append((var, value))

    submit_button = tk.Button(main_window, text="Submit Booking", bg="#8B636C", command=submit_booking)
    submit_button.place(x=680, y=740)

    main_window.mainloop()
show_login_window()
# Close the connection to the database when the application is closed
conn.close()
if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("Main Application")
    main_window.geometry("800x500+350+150")
    main_window.config(bg="#90EE90")

    show_login_window()
