# Imports that will be used for running the prototype 
from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
import sqlite3
from datetime import datetime
import requests
# Here we are defining the imports
app = Flask(__name__) # This will be defined as app and will be used through-out the program

# Stored the libraries into variables
bcrypt = Bcrypt(app) 
login_manager = LoginManager(app)

app.secret_key = "255sues!" # The reason for defining is to able to use flash messages
login_manager.login_view = "login" # The reason for defining is to able search for the function route login
DATABASE = "Rolsa_Technologies.db"

labels_1 = ["Electricity", "Gas", "Water", "Car Travel", "Air Travel"]

################################################################### Functions

def check_if_user_exists(email):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT Email FROM users_table WHERE Email=(?)", (email,))
    row = cur.fetchone()
    con.commit()
    con.close()

    if row == None:
        return False
    else:
        return True

def inserting_users_details_in_user_table(name, company, email, password):
    """ Inserts the users details in the database """
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("Insert Into users_table (Name, Company, Email, Password) Values (?, ?, ?, ?)", (name, company, email, password))
    con.commit()
    con.close()

def inserting_bookings_in_bookings_table(name, email, option, date, time, message, user):
    """ Inserts the booking information in the database """
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("Insert Into bookings_table (Name, Email, Option, Date, Time, Message, UserId) Values (?, ?, ?, ?, ?, ?, ?)", 
                (name, email, option, date, time, message, user))
    con.commit()
    con.close()

def displaying_all_booked_time():
    """ Displays all the booked timing """
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("Select Time From bookings_table")
    record = cur.fetchall()
    con.commit()
    con.close()
    return record

def avaliablity_slotes(start_time, end_time, current_time, date):
    """ This function takes in timing and date the user has chosen and 
    checks if booking is valid and makes sure that it doesn't book the 
    time which is already taken by someone """
    avaliablity = True
    con = sqlite3.connect(DATABASE)
    cur = con. cursor()
    cur.execute("Select End_Time From bookings_table Where Date=(?)", (date,))
    times = cur.fetchall()
    con.commit()
    con.close()
    
    # This checks if any book are not colliding 
    for time in times:
        if start_time > datetime.strptime(time[0][:-3], "%H:%M").time():
            print("good go")
            pass
        else:
            avaliablity = False

    # This part checks if the timing is greating than current_time and end_time
    if start_time >= current_time:
        if end_time >= current_time:
            if start_time < end_time: 
                pass
            else:
                avaliablity = False  
        else:
            avaliablity = False        
    else:
        avaliablity = False
        
    return avaliablity

def get_product(id):
    """ Returns the product details """
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("Select * From products_table Where ProductsId=(?)", (id,))
    row = cur.fetchone()
    con.commit()
    con.close()
    return row

def add_to_cart(user_id, product_id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("Insert Into cart_table (UserId, ProductsId, Quantities) Values (?, ?, ?)", (user_id, product_id, 1))
    con.commit()
    con.close()

def Increase_the_quantity_of_the_product(product_id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("Update cart_table Set Quantities = Quantities + 1 Where ProductsId=(?)", (product_id,))
    con.commit()
    con.close()

def check_if_user_id_exist_in_carbon_footprint_table(user_id):
    """ Takes the user id and checks if its their if not then returns search as False. if not, then True """
    search = True
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("""Select * From carbon_footprint_table Where UserId=(?)""", (user_id,))
    row = cur.fetchone()
    con.commit()
    con.close()

    if row is None:
        search = False
        return search
    else:
        return search
    
def create_new_row_for_user_in_carbon_footprint_table(user_id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(""" Insert Into carbon_footprint_table (
                Carbon_Footprint_By_Electricity,
                Carbon_Footprint_By_Gas,
                Carbon_Footprint_By_Water ,
                Carbon_Footprint_By_Car,
                Carbon_Footprint_By_Air_Travel ,
                Total_Carbon_Footprint_On_Monday,
                Total_Carbon_Footprint_On_Tuesday ,
                Total_Carbon_Footprint_On_Wednesday,
                Total_Carbon_Footprint_On_Thursday,
                Total_Carbon_Footprint_On_Friday,
                Total_Carbon_Footprint_On_Saturday,
                Total_Carbon_Footprint_On_Sunday,
                Week_Number,
                UserId) Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                (0,0,0,0,0,0,0,0,0,0,0,0,0,user_id))
    con.commit()
    con.close()


def check_week_number(user_id, week_number):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("""Select Week_Number From carbon_footprint_table Where UserId=(?)""", (user_id,))
    row = cur.fetchone()[0]
    con.commit()
    con.close()
    
    if row == int(week_number):
        return True
    else:
        return False

def reset_weekly_carbon_footprint(current_week):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(f"""UPDATE carbon_footprint_table
                    SET 
                    Total_Carbon_Footprint_On_Monday = 0,
                    Total_Carbon_Footprint_On_Tuesday  = 0,
                    Total_Carbon_Footprint_On_Wednesday = 0,
                    Total_Carbon_Footprint_On_Thursday = 0,
                    Total_Carbon_Footprint_On_Friday = 0,
                    Total_Carbon_Footprint_On_Saturday = 0,
                    Total_Carbon_Footprint_On_Sunday = 0,
                    Week_Number = {current_week}
                    Where UserId = {current_user.id}""")
    con.commit()
    con.close()


def display_the_todays_carbon_footprint(user_id):
    """ This displays todays Carbon footprint the user has generated """
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(""" Select Carbon_Footprint_By_Electricity, 
                Carbon_Footprint_By_Gas, 
                Carbon_Footprint_By_Water, 
                Carbon_Footprint_By_Car, 
                Carbon_Footprint_By_Air_Travel From carbon_footprint_table Where UserId=(?)""", (user_id,))
    row = cur.fetchone()
    con.commit()
    con.close()
    return row

def display_the_week_carbon_footprint(user_id):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(""" Select 
                Total_Carbon_Footprint_On_Monday,
                Total_Carbon_Footprint_On_Tuesday,
                Total_Carbon_Footprint_On_Wednesday,
                Total_Carbon_Footprint_On_Thursday ,
                Total_Carbon_Footprint_On_Friday,
                Total_Carbon_Footprint_On_Saturday,
                Total_Carbon_Footprint_On_Sunday 
                From carbon_footprint_table Where UserId=(?)""", (user_id,))
    row = cur.fetchone()
    con.commit()
    con.close()
    return row


def check_both_password(password, confirm_password):
    """ If both passwords are identical then gives a Pass. If not then displays a messages and returns back to sign in page """
    if password == confirm_password:
        return True
    else:
        flash("Passwords do not match. Please ensure both fields are identical.")
        return redirect(url_for("sign_in"))

def search_user_details_for_login(email):
    """ Searches for the user details based on the email and return it returns the row """    
    import sqlite3
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("Select * From users_table Where Email=(?)", (email,))
    row = cur.fetchone()
    con.commit()
    con.close()
    
    if row == None:
        return None
    else:
        return row


def verify_password(password, email):
    """ Checks if the password matches the password which is stored in the database and returns True or False"""

    row = search_user_details_for_login(email)
    if row is not None:
        access = bcrypt.check_password_hash(row[-1], password)
        if access is False:
            return access
        else:
            return access
    else:
        return False
    


################################################################### Classes

class User(UserMixin):
    """ This class is used to store the user details"""
    def __init__(self, id, name, company, email, password):
        super().__init__()
        self.id = id
        self.name = name
        self.company = company
        self.email = email
        self.password = password
    def get_id(self):
        return self.id
    

@login_manager.user_loader
def load_user(id):
    """ This function is used for automatically logging in the system"""
    import sqlite3
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("Select * From users_table Where UserId=(?)", (id,))
    row = cur.fetchone()
    con.commit()
    con.close()

    if row is None:
        flash("Email not found. Please check your email or sign up for an account.")
        return redirect(url_for('login'))
    else:
        return User(row[0], row[1], row[2], row[3], row[4])
    


################################################################### Routes 


@app.route("/")
def home():
    """ Displays the home page template """
    return render_template("home.html")

@app.route("/Products")
def products():
    """ Displays the products and loads the product template """
    con = sqlite3.connect("Rolsa_Technologies.db")
    cur = con.cursor()
    cur.execute("Select * From products_table")
    rows = cur.fetchall()
    con.commit()
    con.close()
    return render_template("products.html", rows=rows)

@app.route("/products/<int:id>", methods=['GET', 'POST'])
@login_required
def add_products_to_cart(id):
    """ Checks if product exists in the user's cart then it increments
      the quantity of the product by 1. If it doesn't exists then it adds the product"""
    # when user press the add cart button it will send the id
    # of the card that is being pressed using that we will 
    # find the product and add its id with the user_id in the cart tabel
    if request.method == "POST":
        # This part search for the user's basket if nots there then it creates
        # otherwise it adds the product to the user's basket
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("Select * From cart_table Where UserId=(?) And ProductsId=(?)", (current_user.id, id))
        row = cur.fetchone()
        con.commit()
        con.close()

        
        if row is None:
            add_to_cart(current_user.id, id)
        else:
            Increase_the_quantity_of_the_product(id)

    flash("The product is added to the cart.")       
    return redirect(url_for("products"))

@app.route("/Cart")
@login_required
def cart():
    """ Displays the cart page template and displays the products the user has added to the cart"""
    # This part searches for user's basket
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("Select * From cart_table Where UserId=(?)", (current_user.id,))
    rows = cur.fetchall()
    con.commit()
    con.close()

    # We define the list. And store product's information in product info
    # then we store the amount of quantity he bought in the quantity list
    product_info = []
    quantity = []
    for row in rows:
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("Select Name, Price, Image From products_table Where ProductsId=(?)", (row[1],))
        product = cur.fetchall()[0]
        con.commit()
        con.close()
        product_info.append(product)
        quantity.append(row[-1])
    
    # We calculate the total price that is being made
    total_price = 0
    for i in range(len(quantity)):
        total_price = total_price + (product_info[i][1] * quantity[i])
    
    
    return render_template('cart.html', quantity=quantity, product_info=product_info, total_price=total_price)

@app.route("/Educate")
def educate():
    """ This diplays educate template """
    return render_template("educate.html")

@app.route("/Calculate-Carbon-Footprint", methods=['GET', 'POST'])
def calculate_carbon_footprint():
    # Since the values aren't send we make them 0 and false
    labels = 0
    data = 0
    values_sent = False
    if request.method == "POST":
        # These are the calculation used for calculating the carbon footprint
        # electricity – 0.233 kg of CO2e per kWh
        # gas – 0.184kg of CO2e per kWh
        # water – 0.149 kg of CO2e per cubic metre
        # car travel – 0.16843 of CO2e per KM
        # air travel – 0.18362 of CO2e per pkm
        # We get values from the form
        electricity = request.form.get("electricity")
        gas = request.form.get("gas")
        water = request.form.get("water")
        car_travel = request.form.get("car-travel")
        air_travel = request.form.get("air-travel")
        
        # Here we Calculate the carbon for each item separately
        carbon_footprint_by_electricity = int(int(electricity) * 0.233)
        carbon_footprint_by_gas = int(int(gas) * 0.184)
        carbon_footprint_by_water = int(int(water) *  0.149)
        carbon_footprint_by_car_travel = int(int(car_travel) *  0.16843)
        carbon_footprint_by_air_travel = int(int(air_travel) * 0.18362)

        # Then make them into list so we can use to plot the graph
        labels = labels_1
        data = [
            carbon_footprint_by_electricity,
            carbon_footprint_by_gas,
            carbon_footprint_by_water,
            carbon_footprint_by_car_travel,
            carbon_footprint_by_air_travel
        ]
        # Now we have the values we make it True so the save button can appear
        values_sent = True
        # We are using session so we can use the values in the function save_calculations()
        session["todays_carbon_footprint"] = data
        
        return render_template("calculate_carbon_footprint.html", labels=labels, data=data, values_sent=values_sent)
    
    return render_template("calculate_carbon_footprint.html", labels=labels, data=data, values_sent=values_sent)

@app.route("/Save-Calculations", methods=['GET', 'POST'])
@login_required
def save_calculations():
    """ This function allows to save the users Carbon footprint Calcutations"""

    if request.method == "POST":
        # Once the user clicks the button the function it will try to find the user
        search = check_if_user_id_exist_in_carbon_footprint_table(current_user.id)
        # if the search fails then it creates the row for the user
        if search == False:
            create_new_row_for_user_in_carbon_footprint_table(current_user.id)    
        # If the search is True then it tries to only update the columns

        # Here we calculate the total amount of carbon generated
        total_carbon_footprint = 0
        for carbon_footprint in session["todays_carbon_footprint"]:
            total_carbon_footprint = total_carbon_footprint + carbon_footprint
        
        # Here we check the if it is the same week. if not then resets the week
        # which also updates the graph in the account page
        current_week = datetime.today().strftime("%W")
        search = check_week_number(current_user.id, current_week)
        if search == False:
            reset_weekly_carbon_footprint(current_week)

        # using datatime we check todays day name and use it to combine
        # string which will then create the column_day_name
        # making it easier for us to update the day column
        current_day = datetime.today().strftime("%A")
        column_day_name = "Total_Carbon_Footprint_On_" + current_day
        
        # In lines above we find the total carbon footprint then it takes the current day 
        # which allows us to update the column on specific days
        # Here we are updating the row
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute(f"""UPDATE carbon_footprint_table
                    SET Carbon_Footprint_By_Electricity = {session["todays_carbon_footprint"][0]},
                    Carbon_Footprint_By_Gas = {session["todays_carbon_footprint"][1]},
                    Carbon_Footprint_By_Water  = {session["todays_carbon_footprint"][2]},
                    Carbon_Footprint_By_Car = {session["todays_carbon_footprint"][3]},
                    Carbon_Footprint_By_Air_Travel = {session["todays_carbon_footprint"][4]},
                    {column_day_name} = {total_carbon_footprint}
                    Where UserId = {current_user.id}""")
        con.commit()
        con.close()
    return redirect(url_for("calculate_carbon_footprint"))


@app.route("/Book", methods=['GET', 'POST'])
@login_required
def book():
    """ This function allows the users to create their account and insert it in the database. """
    # Once the user sends form, stores details in the variables so they can be
    # sent to the function
    if request.method == "POST":
        # we get inputs from the booking page
        option = request.form.get('option')
        date = request.form.get('date')
        start_time = request.form.get('start-time')
        end_time = request.form.get('end-time')
        message = request.form.get('message')
        
        # convert start time and end time into datetime to do calculations
        start_time = datetime.strptime(start_time, "%H:%M").time()
        end_time = datetime.strptime(end_time, "%H:%M").time()
        current_time = datetime.today().time()
        
        # This function returns True or False depending slotes avaliablity
        avaliablity = avaliablity_slotes(start_time, end_time, current_time, date)
        if avaliablity is True:
            # if the avaliablity is True then it inserts booking_table
            con = sqlite3.connect(DATABASE)
            cur = con.cursor()
            cur.execute("""Insert Into bookings_table 
                        (Name, Email, Option, Date, Start_Time, End_Time, Message, UserId) 
                        Values (?, ?, ?, ?, ?, ?, ?, ?)""", (current_user.name, current_user.email, option, date, str(start_time), str(end_time), message, current_user.id))
            con.commit()
            con.close()
            flash(f"Your {option} is booked.")

        else:
            flash("The slot you were booking isn't avaiable. Please choose a different slot.")
        
    return render_template('book.html')


@app.route("/Sign-In", methods=['GET', 'POST'])
def sign_in():
    """ This function allows the users to create their account and insert it in the database. """
    # Once the user sends form, stores details in the variables so they can be
    # sent to the function
    if request.method == "POST":
        # get the inputs from sign-in page
        name = request.form.get('name')
        company = bool(request.form.get('company'))
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # check if the user already exists if not then it creates an account
        # otherwise it won't allow the person to create a second account
        search = check_if_user_exists(email)
        
        if search == False:
            # check if the there is empty space
            if name == " ":
                flash("Please make sure that you fill out all details correctly.")
                return redirect(url_for("sign_in"))
            # checks if passwords entered are both the same
            if check_both_password(password, confirm_password):
                encrypted_password = bcrypt.generate_password_hash(password).decode("utf-8") 
            # then we insert the user_detials
            inserting_users_details_in_user_table(name, company, email, encrypted_password)
            flash("Account created successfully! Before you procced use the account to login")
            return redirect(url_for('login'))
        else:
            flash("Sorry, this account is already taken")
    return render_template('sign_in.html')


@app.route("/Login", methods=['GET', 'POST'])
def login():
    """ This function allows the users to login to the website using their account. """
    # Once the user sends form it check whether is authenticated to use their account
    if request.method == "POST":
        if current_user.is_authenticated:
            flash('Welcome back!')
            return redirect(url_for('home'))
        
        # if not, then it goes through series of checks 
        else:
            # Retieves the values from the form
            email = request.form.get('email')
            password = request.form.get('password')
            remember = bool(request.form.get('remember'))  
            row = search_user_details_for_login(email)# Searches for the email
            if row is not None:
                access = verify_password(password, email) # checks if the password matches
                if access is True:
                    user_details = User(row[0], row[1], row[2], row[3], row[4]) # Store the users details in the User class            
                    login_user(user_details, remember)
                    flash("You have successfully logged in.")
                    return redirect(url_for('home'))
                else:
                    flash("Incorrect email or password. Please try again.")
                    return redirect(url_for('login'))
            else:
                flash("Email not found. Please check your email or sign up for an account.")
                return redirect(url_for('login'))
    return render_template("login.html")    
    

@app.route("/logout")
def logout():
    """ This function is used logout the perently from the website"""
    logout_user()
    return redirect(url_for('home'))


@app.route("/Account")
def account():
    """ This the account page which displays the API of the weather
    current day graph and weekly graph"""
    url = "https://api.openweathermap.org/data/2.5/weather?"
    params = {
        "lat":52.408871,
        "lon":-1.7907919999999997,
        "appid":"cf14aad0e340a8586dd31f96d2d38e13"
    }
    weather_api = requests.get(url,params).json()
    description = weather_api["weather"][0]["description"]
    icon = weather_api["weather"][0]["icon"]
    temperature = weather_api["main"]["temp"]
    
    data = display_the_todays_carbon_footprint(current_user.id)
    labels = labels_1

    data_2 = display_the_week_carbon_footprint(current_user.id)
    labels_2 = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    return render_template("account.html", data=data, labels=labels, 
                           data_2=data_2, labels_2= labels_2, 
                           temperature=int(temperature),description=description, 
                           icon=icon)
    pass
#@app.route("/About-Us")
#def about_us():
#@app.route("/Contact-Us")
#def contact_us():



# Design the website 5th day


# This is the part where it runs the script 


if __name__ == "__main__":
    app.run(debug=True)
