import sqlite3

con = sqlite3.connect("Rolsa_Technologies.db")
cur = con.cursor()
# cur.execute("PRAGMA foreign_keys = OFF")

# This used to create user table

cur.execute("""Create Table If Not Exists users_table
            (UserId Integer Primary Key Autoincrement, Name Text Not Null,  
            Company Boolean, Email Text Not Null, Password Text Not Null)
            """)

#This used to create bookings table

cur.execute("""Create Table If Not Exists bookings_table
            (BookingId Integer Primary Key Autoincrement, Name Text Not Null,
            Email Text Not Null, Option Text Not Null, Date Text Not Null, Start_Time Text Not Null, End_Time Not Null, Message Text, 
            UserId Integer Not Null, FOREIGN KEY(UserId) REFERENCES users_table(UserId))
            """)

#This used to create products table

cur.execute("""Create Table If Not Exists products_table
            (ProductsId Integer Primary Key Autoincrement, Name Text Not Null,
            Description Text Not Null, Price Integer Not Null, Image Text Not Null)
            """)

#This used to create cart table

cur.execute("""Create Table If Not Exists cart_table
            (UserId Integer Not Null, ProductsId Integer Not Null, Quantities Integer Not Null,
            FOREIGN KEY(UserId) REFERENCES users_table(UserId), 
            FOREIGN KEY(ProductsId) REFERENCES products_table(ProductsId))
            """)

#This used to create carbon footprint table


cur.execute("""Create Table If Not Exists carbon_footprint_table
             ( 
            Carbon_Footprint_By_Electricity Integer Not Null, 
            Carbon_Footprint_By_Gas Integer Not Null, 
            Carbon_Footprint_By_Water Integer Not Null, 
            Carbon_Footprint_By_Car Integer Not Null, 
            Carbon_Footprint_By_Air_Travel Integer Not Null,
            Total_Carbon_Footprint_On_Monday Integer Not Null,
            Total_Carbon_Footprint_On_Tuesday Integer Not Null,
            Total_Carbon_Footprint_On_Wednesday Integer Not Null,
            Total_Carbon_Footprint_On_Thursday Integer Not Null,
            Total_Carbon_Footprint_On_Friday Integer Not Null,
            Total_Carbon_Footprint_On_Saturday Integer Not Null,
            Total_Carbon_Footprint_On_Sunday Integer Not Null,
            Week_Number Integer Not Null,
            UserId Integer Not Null,
             FOREIGN KEY(UserId) REFERENCES users_table(UserId)
            )
             """)





#These are values that are inserted into the product page


cur.execute ("""INSERT INTO products_table (Name, Description, Price, Image)
              
VALUES              
("SunVolt X5",
"A premium solar panel with 22% efficiency and sleek black framing. Ideal for rooftops, it performs well in all climates and comes with a 25-year performance warranty for peace of mind.",
549,"/static/images/solar-panels/solar-panels_1.jpg"),

("HelioEdge Pro",
"Built for modern solar systems, this panel features high-output cells and advanced coating. Engineered for durability and smart integration, it's perfect for off-grid living or high-efficiency residential installs.",
699, "/static/images/solar-panels/solar-panels_2.jpg"),

("Solarion One",
"An affordable yet reliable panel for small-scale solar setups. Offers 19% efficiency and weather-resistant build, making it great for beginners, cabins, or budget-conscious homeowners getting into solar energy.",
389, "/static/images/solar-panels/solar-panels_3.jpg"),

("LumaRay 360",
"Combining performance and aesthetics, this panel suits homes or businesses. It features anti-glare glass, a lightweight frame, and strong energy output in both sunny and partly cloudy conditions year-round.",
629, "/static/images/solar-panels/solar-panels_4.jpg"),

             
("VoltMate Home 40",
"This compact Level 2 charger delivers up to 40 amps for efficient overnight charging. With a 25-foot cable and universal EV compatibility, it’s ideal for garages, driveways, or wall mounting",
649, "/static/images/EV-charger-station/EV-charger-station_1.jpg"),

("ChargeNova Pro",
"High-speed charging meets smart tech. Features include dual charging modes, real-time app monitoring, and built-in safety protections. Built for tech-savvy EV owners who want control and convenience at home.",
829, "/static/images/EV-charger-station/EV-charger-station_2.jpg"),

("EcoWatt Flex",
"Eco-friendly, affordable, and easy to install. This Level 2 charger offers weather-resistant housing, a flexible cable, and plug-and-play setup. Perfect for daily use by drivers looking for simple functionality.",
459, "/static/images/EV-charger-station/EV-charger-station_3.jpg"),

("PowerLane Ultra",
"A commercial-grade charger for apartments or workplaces. Supports RFID access, payment integration, and 11 kW output. Built tough for public use with smart load balancing and secure access control features.",
1099, "/static/images/EV-charger-station/EV-charger-station_4.jpg"),

             
("GridSync Core",
"A smart hybrid inverter system that connects solar panels, the grid, and battery storage. Offers seamless power switching, app control, and backup capabilities during outages or peak rate hours",
1799, "/static/images/Smart-home-device/Smart-home-device_1.jpg"),

("EcoStore 10X",
"This compact home battery stores up to 10 kWh of solar energy. With built-in temperature control and Wi-Fi monitoring, it ensures reliable backup power for evenings or unexpected grid failures.",
2299, "/static/images/Smart-home-device/Smart-home-device_2.jpg"),

("PowerNest Hub",
"A complete energy management system that includes inverter, battery, and load balancing. Optimizes your home’s power flow automatically, lowering utility costs and enabling smart home energy independence.",
3499, "/static/images/Smart-home-device/Smart-home-device_3.jpg"),

("Lumina SmartVault",
"Stylish and stackable, this modular battery system scales with your needs. Ideal for large homes or growing solar setups, it offers smart charging, mobile alerts, and long-term durability.",
2899, "/static/images/Smart-home-device/Smart-home-device_4.jpg")

""")

con.commit()
con.close()