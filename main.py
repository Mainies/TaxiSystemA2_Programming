"""
Final Submission
Name: Samuel Mainwood
StudentNo: s3939120
Course: Programming Principles
Assignment: 2
Highest level completed: HD (Each criteria attempted)

No major detected bugs from my own tests.
"""
# Importing the permitted modules

import os
import sys

"""
Reflection: 
When creating this program I had some challenges with understanding pointers for objects (particularly when creating 
new objects). This was very different to how I have previously managed data. For this I decided to use lists to store 
my objects as in my amateur opinion, felt more robust than a dictionary. I considered using a dictionary to match 
customer to bookings but this was tedious in the first assignment and in the second assignment.

I have demonstrated private/protected attributes in the threshold and rates classes which have appropriate getter and 
setter methods. I have also demonstrated usage of getter methods with non-protected attributes. I understand this may 
introduce more time for the program to run, but would also be less memory. Given that it is a taxi booking system, at 
an early implementation this is fine. Custom exception handling has been demonstrated with the invalid_file_error class.

Given the file description I felt there is some redundant information that meant I had to reconfigure my classes (i.e. 
each booking in the bookings file contained the flag-fall.) I have also used a mix of exception handling and while loops 
to handle errors in input. I think the latter is more robust but I was happy with my functioning programming prior to 
the week 10 content.I have demonstrated making exception classes during file-reading.

If I was to redo this, I would like to plan all of the information and make sure there is consistency within classes. 
This would help with adjusting modularity and better planning for encapsulation. If this program were more advanced, it
could save locations to co-ordinates to automatically calculate distance instead of taking user-input.
"""


class Customer:
    """Parent for Basic and Enterprise Customers"""

    def __init__(self, customer_ID: int, name: str, previous_customer=False) -> None:
        """Initialise customer class and provide framework for inheritance"""
        self.name = name
        self.customer_ID = customer_ID
        self.previous_customer = previous_customer
        Records.customer_recs.append(self)

    def get_name(self):
        return self.name

    def get_id(self):
        return self.customer_ID

    def get_previous_customer_status(self):
        """return a boolean value for a previous customer status"""
        return self.previous_customer

    def get_discount(self, distance_fee):
        """return a discount value"""
        pass

    def display_info(self):
        pass

    @staticmethod
    def get_customer_object(search_value):
        """searches for a customer object via name, and then via ID. Returns false to keep in
        a while loop"""
        for customer_obj in Records.customer_recs:
            if customer_obj.name == search_value:
                return customer_obj
        for customer_obj in Records.customer_recs:
            if customer_obj.customer_ID == search_value:
                return customer_obj

        return False


class BasicCustomer(Customer):
    """Child of Customer. Used to maintain basic customer info."""
    __discount_rate = 0.10

    def __init__(self, customer_id, name, cust_type="b"):
        super().__init__(customer_id, name)
        self.discount_rate = BasicCustomer.__discount_rate
        self.cust_type = cust_type

    def display_info(self):
        super().display_info()
        print(f'Customer ID: {self.get_id()}')
        print(f'Customer Name: {self.get_name()}')
        print(f'Previous Bookings: {self.get_previous_customer_status()}')

    def get_discount(self, distance_fee):
        """Takes a distance fee and checks for previous customer status. Returns the discount based on the
        distance fee."""
        super().get_discount(distance_fee)
        self.discount_rate = BasicCustomer.__discount_rate
        # Reset discount rate to match new discount rate.
        discount = distance_fee * self.discount_rate
        return discount

    def get_name(self):
        super().get_name()
        return self.name

    def get_id(self):
        super().get_id()
        return self.customer_ID

    @staticmethod
    def set_discount_rate():
        """Sets a new discount rate for all basic customers."""
        new_value = input("Please enter the new rate as a decimal point: ")
        new_value = new_value.strip()
        try:
            new_value = float(new_value)
            # Try except lets the simplest case to test if the number can be changed to a float.
            if new_value > 1:
                print("New value cannot be greater than 1.")
                return BasicCustomer.set_discount_rate()
            elif new_value < 0:
                print("New value must be positive.")
                return BasicCustomer.set_discount_rate()
        except:
            print("Entered rate must be numeric.")

        BasicCustomer.__discount_rate = new_value

    @staticmethod
    def get_basic_discount_rate():
        return BasicCustomer.__discount_rate


class EnterpriseCustomer(Customer):
    """Child of customer. Used to maintain enterprise customer info as well as their special discounts."""
    def __init__(self, customer_id, name, rate1=0.15, threshold=100.0, cust_type="e"):
        super().__init__(customer_id, name)
        self.__rate1 = rate1
        self.__rate2 = rate1 + 0.05
        self.__threshold = threshold
        self.cust_type = cust_type

    def display_info(self):
        super().display_info()
        base, higher = self.get_rates()
        thresh = self.get_thresh()
        print(f"Rate 1: {base * 100:.2f}%")
        print(f"Rate 2: {higher * 100:.2f}%")
        print(f"Threshold: ${thresh:.2f}")

    # Getter Methods
    def get_name(self):
        super().get_name()
        return self.name

    def get_thresh(self):
        """Return protected threshold"""
        return self.__threshold

    def get_id(self):
        super().get_id()
        return self.customer_ID

    def get_discount(self, distance_fee):
        """Calculate distance fee using threshold and rate values"""
        super().get_discount(distance_fee)
        discount = distance_fee * self.__rate1 if distance_fee > self.get_thresh() else distance_fee * self.__rate2
        return discount

    def get_rates(self):
        """Accesses protected attribute for rates"""
        return self.__rate1, self.__rate2

    # Setter Methods
    def enter_new_rate_value(self):
        """Used to ensure valid rate entering and calls the setting discount rate method"""
        new_value = input("Please enter the new rate as a decimal point: ")
        new_value = new_value.strip()
        try:
            new_value = float(new_value)
            # try except allows a simple test to see if it can be converted to float.
            if new_value > 1:
                print("New value cannot be greater than 1.")
                return self.enter_new_rate_value()
            elif new_value < 0:
                print("New value must be positive.")
                return self.enter_new_rate_value()
        except:
            print("Entered rate must be numeric.")
        self.set_discount_rate(new_value)

    def enter_new_thresh_value(self):
        """Ensures valid threshold is entered then calls the set_threshold method"""
        new_value = input("Please enter the new threshold: ")
        new_value = new_value.strip()
        try:
            new_value = float(new_value)
            if new_value < 0:
                print("New value must be positive.")
                return self.enter_new_rate_value()
        except TypeError:
            print("Entered rate must be numeric.")
        self.set_threshold(new_value)

    def set_discount_rate(self, new_rate1: float) -> None:
        """Accesses private variables to set new value"""
        self.__rate1 = new_rate1
        self.__rate2 = new_rate1 + 0.05

    def set_threshold(self, new_threshold):
        """Accesses private threshold variable to set new value"""
        self.__threshold = new_threshold


class Location:
    # assume location names are unique and do not contain digits

    def __init__(self, location_id, name: str) -> None:
        self.location_id = location_id
        self.name = name
        Records.locations_recs.append(self)

    # getters
    def get_loc_name(self):
        return self.name

    def get_loc_id(self):
        return self.location_id

    def valid_location(self):
        """Searches through the location records to make sure a location exists."""
        for valid_location in Records.locations_recs:
            if valid_location.get_loc_name() == self.get_loc_name():
                return True

        return False

    @staticmethod
    def add_location():
        """Checks if Location exists or adds it to the system."""
        new_loc = input("Please enter new location(s) separate by a comma: ")
        new_loc = new_loc.split(',')
        for loc in new_loc:
            loc = loc.strip()
            if len(loc) == 0:
                continue
            is_loc = Records.find_location(loc)
            if is_loc:
                print(f'{loc} is already available.')
            else:
                loc = loc.strip()
                new_loc_id = len(Records.locations_recs) + 1
                new_loc_id = "L" + str(new_loc_id)
                Location(new_loc_id, loc)


class Rate:
    """Maintain list of current rates."""
    def __init__(self, rate_ID, rate_name, price):
        self.ID = rate_ID
        self.rate_name = rate_name
        self.price = price

    def display_info(self):
        print(f'ID: {self.ID}')
        print(f'Name: {self.rate_name}')
        print(f'Price: ${self.price:.2f}/km')

    @staticmethod
    def new_rate():
        """Adds new rates and updates old rates. Checks that entered types are valid"""
        new_rates = input("Please enter a list of new rates separated by a comma (i.e. Holiday, Boutique): ").strip()
        new_rates = new_rates.split(',')
        for rate in new_rates:
            rate = rate.strip()
            if not rate.isalpha():
                print("Rate names cannot contain numeric characters.")
                return Rate.new_rate()

        new_rate_prices = input(
            "Please enter a corresponding list of prices for the entered rates separated by a comma: ").strip()
        new_rate_prices = new_rate_prices.split(',')
        for rate in new_rate_prices:
            rate = rate.strip()
            try:
                rate = float(rate)
            except:
                print("One or more rate types are non-numeric. Please try again.")
                return Rate.new_rate()

            if rate <= 0:
                print("Rate prices cannot be 0 or less. Please try again.")
                return Rate.new_rate()
        if len(new_rate_prices) != len(new_rates):
            print("Entered values are not the same length. Please try again.")
            return Rate.new_rate()

        for i in range(len(new_rates)):
            current_rate = new_rates[i]
            current_rate = current_rate.strip()
            is_existing = Records.find_rate(current_rate)
            if is_existing:
                is_existing.price = new_rate_prices[i]
                print(f"{is_existing.rate_name} rate type is updated.")
            else:
                added_rate_id = len(Records.rates_recs) + 1
                added_rate_id = "R" + str(added_rate_id)
                add_rate = Rate(added_rate_id, new_rates[i].strip(), new_rate_prices[i])
                Records.rates_recs.append(add_rate)
                print(f"{add_rate.rate_name} rate type added.")


class Service:
    """Maintain similar methods to allow for ease of use between classes."""
    def __init__(self, service_ID, service_name, service_price):
        self.service_ID = service_ID
        self.service_name = service_name
        self.price = float(service_price)
        Records.service_recs.append(self)

    def get_name(self):
        return self.service_name

    def get_id(self):
        return self.service_ID

    def get_price(self):
        return self.price

    def set_price(self, value):
        #ability to set new price
        self.price = value


class Package:
    """Maintain similar methods to allow for ease of use between classes."""
    def __init__(self, package_ID, package_name, package_services):
        self.service_ID = package_ID
        self.service_name = package_name
        self.contained_services = package_services
        self.price = 0
        for service in self.contained_services:
            self.price += float(service.get_price())
        self.price = self.price * 0.8
        Records.service_recs.append(self)

    def get_id(self):
        return self.service_ID

    def get_name(self):
        return self.service_name

    def get_packages(self):
        return self.contained_services

    def get_price(self):
        return self.price

    def set_price(self, value):
        #ability to set new price
        self.price = value


class Booking:
    """Main booking class to contain individual booking information. """
    base_fee = 4.2

    # Base fee is the same for all customers

    def __init__(self, booking_customer, departure, destination_list, distance_list, selected_rate, services=None,
                 discount=0.0, booking_cost=0.0):
        # Extra booking details have been added in here for use of importing/exporting for the booking file.
        if type(selected_rate) == str:
            selected_rate = Records.find_rate(selected_rate)
        self.booking_id = booking_customer.get_id()
        self.customer = booking_customer.get_name()
        self.departure = departure
        self.destination = destination_list
        self.distance_list = distance_list
        self.rate = selected_rate
        self.previous_cust = booking_customer.get_previous_customer_status()
        self.services = services
        self.discount = discount
        self.booking_cost = booking_cost
        Records.bookings_recs.append(self)

    def compute_cost(self):
        """ Calculates a fee based on distance values, discounts on customer status and base fee. Updates booking
        attributes
        """
        basic_cost = Booking.base_fee
        total_dist = 0
        for distance in self.distance_list:
            total_dist += distance

        distance_cost = total_dist * float(self.rate.price)

        if self.previous_cust:
            discount = Customer.get_customer_object(self.customer)
            discount = discount.get_discount(distance_cost)
            distance_cost -= discount
            self.discount = discount

        if self.services is not None:
            service_cost = float(self.services.get_price())
            total_cost = basic_cost + distance_cost + service_cost
            self.booking_cost = total_cost

        else:
            total_cost = basic_cost + distance_cost
            self.booking_cost = total_cost
            cust = Customer.get_customer_object(self.customer)
            cust.previous_cust = True

    @staticmethod
    def get_customer_info():
        """Used in new_booking to get customer info or create a new customer"""
        valid_name = False
        while not valid_name:
            cust_name = input("Please enter your name or ID: ")
            valid_name = cust_name.isalpha()
            cust_name = cust_name.strip()
            if not valid_name:
                ID_search = Records.find_customer(cust_name)
                if not ID_search:
                    print(
                        "Invalid entry: the entered name contains non-alphabet characters or the customer ID cannot be found.")
                if ID_search:
                    valid_name = True

        custom = Records.find_customer(cust_name)

        if custom:
            print(f"Welcome back {custom.get_name()}.")

        while not custom:
            custom = input('New customer account please select Basic (b) or Enterprise (e) account: ')

            if custom == "b":
                new_cust_id = len(Records.customer_recs) + 5
                print(f"Basic customer selected. New customer ID: {new_cust_id}.")
                custom = BasicCustomer(new_cust_id, cust_name)
            elif custom == "e":
                new_cust_id = len(Records.customer_recs) + 5
                print(f"Enterprise customer selected. New customer ID: {new_cust_id}.")
                custom = EnterpriseCustomer(new_cust_id, cust_name)
            else:
                print('Invalid selection.')
                custom = False

        return custom

    @staticmethod
    def get_departure():
        """Used in new_booking to get location info and check that the location is valid"""
        # Get Departure Location
        dept_check = False
        while not dept_check:
            departure = input("Please enter your departure location: ")
            if departure == "1":
                Records.list_locations()
                departure = input("Please enter your departure location: ")
                departure = departure.strip()
            dept_check = Records.find_location(departure)

            if not dept_check:
                print("Invalid Location. Please try again. To see a list of available locations enter 1.")

        departure = dept_check.get_loc_name()
        return departure

    @staticmethod
    def service_selector():
        """Offers a range of available services and prices and ensures selection is valid"""
        services = None
        valid_selection = False
        while not valid_selection:
            service_select = input('Would you like to add any services/packages to your booking [y/n]: ')
            service_select = service_select.strip()
            if service_select.lower() == "n":
                valid_selection = True
            elif service_select.lower() == "y":
                valid_selection = True
            else:
                print("Please enter a valid selection.")

        if service_select.lower().strip() == "n":
            valid_selection = "None"
        if service_select.lower().strip() == "y":
            print("Please select from the following services/packages:")
            print(Records.list_services())
            valid_selection = False
            while not valid_selection:
                selector = input("Please make your selection by entering service ID as shown or enter 'None' to skip: ")
                selector = selector.strip()
                if selector == "None":
                    valid_selection = "None"
                else:
                    valid_selection = Records.find_service(selector)
                    if not valid_selection:
                        print("Invalid selection. Please try again.")

        if valid_selection == "None":
            services = None
        else:
            services = valid_selection

        return services

    def print_booking(self):
        """Takes values from Booking class to print out"""
        print("\n")
        print("-".ljust(58, "-"))
        print("Taxi Receipt".center(50, " "))
        print("-".ljust(58, "-"))
        print("Name:".ljust(20, " ") + self.customer.ljust(38, " "))
        print("Departure:".ljust(20, " ") + self.departure.ljust(38, " "))
        total_dist = 0
        for i in range(len(self.distance_list)):
            fdestination = str(self.destination[i])
            fdistance = self.distance_list[i]
            total_dist += fdistance
            print("Destination:".ljust(20, " ") + fdestination.ljust(38, " "))
            print("Distance:".ljust(20, " ") + f"{fdistance:.2f} km".ljust(38, " "))
        rate_string = self.rate.price
        print("Rate:".ljust(20, " ") + f"{rate_string} (AUD per km)".ljust(38, " "))
        print("Total Distance:".ljust(20, " ") + f"{total_dist:.2f} km".ljust(38, " "))
        if self.services:
            service_item = self.services.get_name()
            print("Selected Extras: ".ljust(20, " ") + f"{service_item}")
        print("-".ljust(58, "-"))
        print("Basic fee".ljust(20, " ") + f"{Booking.base_fee:.2f} (AUD)".ljust(38, " "))
        if self.previous_cust:
            discount = Customer.get_customer_object(self.customer)
            discount = discount.get_discount(total_dist)
            print("Discount:".ljust(20, " ") + f"{discount:.2f} (AUD)".ljust(38, " "))
        else:
            print("Discount:".ljust(20, " ") + f"{0.00:.2f} (AUD)".ljust(38, " "))
        if self.services:
            serv_price = float(self.services.get_price())
            print("Services/Extras: ".ljust(20, " ") + f"{serv_price:.2f} (AUD)")
        print("-".ljust(58, "-"))
        total = float(self.booking_cost)
        print("Total Cost:".ljust(20, " ") + f"{total:.2f} (AUD)".ljust(38, " "))
        print("-".ljust(58, "-"))

    @staticmethod
    def new_booking():
        """Calls appropriate methods to get details and creates a new booking at the end of the method."""
        custom = Booking.get_customer_info()
        departure = Booking.get_departure()
        # Destination and Distance Cycle
        both = False
        dest_list = []
        dist_list = []
        while not both:
            # while loops allow for a recursive input until the input is valid.
            dest_check = False
            while not dest_check:
                destination = input("Please enter your destination: ")
                destination = destination.strip()
                if destination == "1":
                    Records.list_locations()
                    destination = input("Please enter your destination location: ")
                    destination = destination.strip()
                dest_check = Records.find_location(destination)
                if not dest_check:
                    print("Invalid Location. Please try again. To see a list of available locations enter 1.")
                    dest_check = False
                if destination.strip() == departure:
                    print('Destination cannot be the same as departure. Please try again.')
                    dest_check = False

            dest_list.append(dest_check.get_loc_name())

            valid_dist = False
            while not valid_dist:
                dist = input("Please enter the distance to this destination in km: ")
                dist = dist.strip()
                try:
                    dist = float(dist)
                    valid_dist = True
                except:
                    print("Entered distance contains non-numeric values. Please try again.")

                if valid_dist and dist <= 0:
                    print("Distance cannot be 0 or less. PLease try again")
                    valid_dist = False

            dist_list.append(dist)

            extra_check = False
            while not extra_check:
                extra = input("Would you like to add another location [y/n]: ")
                extra = extra.strip()
                if extra.strip() == "y":
                    extra_check = True
                    both = False
                elif extra.strip() == "n":
                    extra_check = True
                    both = True
                else:
                    print("Invalid Input. Please try again.")

        rate_check = False
        while not rate_check:
            select_rate = input("Please enter the rate category: ")
            select_rate = select_rate.strip()
            if select_rate == "1":
                Records.list_rates()
                select_rate = input("Please enter the rate category: ")
                select_rate = select_rate.strip()
            rate_check = Records.find_rate(select_rate)
            if not rate_check:
                print("Invalid Rate. Please try again. To see a list of available rates enter 1.")

        services = Booking.service_selector()
        current_booking = Booking(custom, departure, dest_list, dist_list, rate_check, services)
        current_booking.compute_cost()
        current_booking.print_booking()
        customer_pointer = Records.find_customer(current_booking.customer)
        customer_pointer.previous_customer = True


class invalid_file_error(Exception):
    """Sample usage of custom exception handling."""
    # this is used to demonstrate the ability/knowledge for customer exception handling.
    pass


class Records:
    """Main data manager for within the program. Reads from Filemanager class to update within program classes."""
    customer_recs = []
    locations_recs = []
    bookings_recs = []
    rates_recs = []
    service_recs = []

    @staticmethod
    # Can assume customers always in format ID, name, type, rate
    # Assumes no error in customer file, discount and threshold values always valid
    def read_customers():
        """Reads through customer file to input new customer object as per specifications"""
        try:
            cust_file = open(file_manager.customer_file, 'r')
            for cust in cust_file:
                cust = cust.strip().split(',')
                if len(cust) == 4:
                    BasicCustomer(cust[0].strip(), cust[1].strip())
                elif len(cust) == 5:
                    EnterpriseCustomer(cust[0].strip(), cust[1].strip(), float(cust[3].strip()),
                                       float(cust[4].strip()))
                else:
                    print('Invalid Data Line')
                    raise invalid_file_error

        except invalid_file_error:
            print("Invalid Data In Customer File.")

    @staticmethod
    def read_rates():
        rates_file = open(file_manager.rate_file, 'r')
        for old_rate in rates_file:
            old_rate = old_rate.strip().split(',')
            new_rate = Rate(old_rate[0].strip(), old_rate[1].strip(), old_rate[2].strip())
            Records.rates_recs.append(new_rate)

    @staticmethod
    def read_locations():
        location_file = open(file_manager.location_file, 'r')
        for exist_loc in location_file:
            exist_loc = exist_loc.strip().split(',')
            new_location = Location(exist_loc[0].strip(), exist_loc[1].strip())

    @staticmethod
    def read_services():
        service_file = open(file_manager.service_file, 'r')
        for service in service_file:
            service = service.strip().split(',')
            if service[0][0] == "S":
                Service(service[0].strip(), service[1].strip(), float(service[2].strip()))
            else:
                service_list = []
                for i in range(len(service)):
                    if i >= 2:
                        serv_id = Records.find_service(service[i].strip())
                        service_list.append(serv_id)
                Package(service[0].strip(), service[1].strip(), service_list)

    @staticmethod
    def read_bookings():
        if not FileManager.bookings_available:
            print('No current bookings in the system.')
            return
        booking_file = open(file_manager.booking_file, 'r')
        try:
            for booking in booking_file:
                booking = booking.strip().split(',')
                cust = booking[0]
                departure = booking[1]
                destination_list = []
                distance_list = []
                service = booking[-5]
                service = service.strip()
                if len(service) == 0:
                    service = None
                else:
                    service = Records.find_service(service)
                    if service == False:
                        service = None
                rate = booking[-6].strip()
                distance_fee = float(booking[-3])
                book_discount = float(booking[-2])
                total_cost = float(booking[-1])
                travel_chunk = booking[2:-6]
                for i in range(0, len(travel_chunk), 2):
                    destination_list.append(travel_chunk[i])
                    distance_list.append(travel_chunk[(i + 1)])

                cust = Records.find_customer(cust)
                Booking(cust, departure, destination_list, distance_list, rate, service, discount=book_discount,
                        booking_cost=total_cost)
        except invalid_file_error:
            print("Invalid Data In Bookings File... Closing App.")
            exit()

    @staticmethod
    def find_customer(cust_value) -> object:
        for cust_obj in Records.customer_recs:
            if cust_value == cust_obj.get_name():
                return cust_obj
        for cust_obj in Records.customer_recs:
            if cust_value == cust_obj.get_id():
                return cust_obj
        return False

    @staticmethod
    def find_location(new_loc):
        """Searches for location via ID or name"""
        for loc_obj in Records.locations_recs:
            if new_loc == loc_obj.get_loc_name():
                return loc_obj
        for loc_obj in Records.locations_recs:
            if new_loc == loc_obj.get_loc_id():
                return loc_obj
        return False

    @staticmethod
    def find_rate(rate):
        """Searches through rate via ID or name"""
        for rate_obj in Records.rates_recs:
            if rate == rate_obj.rate_name:
                return rate_obj
        for rate_obj in Records.rates_recs:
            if rate == rate_obj.ID:
                return rate_obj
        else:
            return False

    @staticmethod
    def find_service(serv_value):
        """Searches through services and packages via ID or name"""
        for serv_object in Records.service_recs:
            if serv_value == serv_object.get_id():
                return serv_object
        for serv_object in Records.service_recs:
            if serv_value == serv_object.get_name():
                return serv_object
        return False

    @staticmethod
    def list_customers():
        """Prints list of customer objects."""
        print("Customer ID | Customer Name | Customer Type")
        print("_".ljust(30, "_"))
        for customer_object in Records.customer_recs:
            cust_type = None
            if customer_object.cust_type == "e":
                cust_type = "Enterprise"
            elif customer_object.cust_type == "b":
                cust_type = "Basic"
            else:
                cust_type = None
            print(f"{customer_object.get_id():<12}" + f"| {customer_object.get_name():<}".ljust(16, " ") +
                  f"| {cust_type}")

    @staticmethod
    def list_locations():
        """Prints list of locations"""
        print("Location ID | Customer Name")
        print("_".ljust(30, "_"))
        for location_object in Records.locations_recs:
            print(f"{location_object.get_loc_id():<12}" + f"| {location_object.get_loc_name():<}")

    @staticmethod
    def list_rates():
        """Prints list of available rates"""
        print("Rate Name".ljust(12, " ") + "| Rate Price")
        print("_".ljust(30, "_"))
        for rate_object in Records.rates_recs:
            price = float(rate_object.price)
            print(f"{rate_object.rate_name:<12}" + f"| {price:.2f}")

    @staticmethod
    def list_services():
        """Prints list of available services."""
        print("ID".ljust(5, " ") + "ServiceName".ljust(15, " ") + "Cost (AUD)")
        for ser_obj in Records.service_recs:
            if ser_obj.service_ID[0] == "S":
                print(f"{ser_obj.service_ID}".ljust(5, " "), f"{ser_obj.service_name}".ljust(15, " ") +
                      f"{ser_obj.price:.2f}")
            else:
                print(f"{ser_obj.service_ID}".ljust(5, " "), f"{ser_obj.service_name}".ljust(15, " ") +
                      f"{ser_obj.price:.2f}")

    most_val_customer = None
    most_val_spend = 0

    @staticmethod
    def val_customer():
        """Compares a current 'champion' customer against each other customer's booking to return the most valuable
        customer."""
        for customer in Records.customer_recs:
            total_spend = 0
            for booking in Records.bookings_recs:
                if customer.get_name() == booking.customer:
                    total_spend += booking.booking_cost
            if total_spend > Records.most_val_spend:
                Records.most_val_customer = customer
                Records.most_val_spend = total_spend
        if Records.most_val_customer is None:
            print("There have been no bookings.")
        else:
            print(f"The most valuable customer is {Records.most_val_customer.get_name()}"
                  f" who has spent ${Records.most_val_spend}.")

    @staticmethod
    def all_previous_bookings():
        print("All Previous Bookings")
        print("\n")
        print("Customer".ljust(15, " ") + "Departure".ljust(15, " ") + "Destination".ljust(15, " ") + "Total Cost")
        print("_".ljust(55, "_"))
        print()
        for booking in Records.bookings_recs:
            print(f"{booking.customer}".ljust(15, " ") + f"{booking.departure}".ljust(15, " ") +
                  f"{booking.destination[-1]}".ljust(15, " ") + f"{booking.booking_cost:.2f}")

    @staticmethod
    def customer_previous_bookings(cust_value):
        """Finds a customer object, then returns each booking using the customer object to loop through all bookings."""
        customer = Records.find_customer(cust_value)
        if not customer:
            try:
                cust_value = int(customer)
                customer = Records.find_customer(cust_value)
            except:
                print("The customer is entered incorrectly or is not in the system.")
                return
        cust_bookings = []
        for booking in Records.bookings_recs:
            if customer.get_name() == booking.customer:
                cust_bookings.append(booking)
        if len(cust_bookings) == 0:
            print("This customer has no previous bookings.")
            return

        print("-".ljust(30, '-'))
        booking_number = 1
        top_string = " ".ljust(20, " ")
        departure_string = "Departure".ljust(20, " ")
        destination_string = "Destination".ljust(20, " ")
        total_string = "Total Cost".ljust(20, " ")
        for booking in cust_bookings:
            # go through each booking
            num = str(booking_number)
            booking_number += 1
            top_string_chunk = ("Booking " + num).ljust(30, " ")
            depart = booking.departure.strip()
            departure_string += depart.ljust(30, " ")
            destination1_string = booking.destination[0].strip()
            for dest in booking.destination:
                if dest.strip() == destination1_string:
                    continue
                # go through each destination after the first
                destination1_string += (", " + dest.strip())
            destinations_chunk = destination1_string.ljust(30, " ")
            cost_chunk = f"{booking.booking_cost:.2f}".ljust(30, " ")
            top_string += top_string_chunk
            destination_string += destinations_chunk
            total_string += cost_chunk
        print(top_string)
        print(departure_string)
        print(destination_string)
        print(total_string)


class FileManager:
    """Class created to have file management in one object. Used to interact with CLI and maintain required files."""
    arguments = sys.argv
    bookings_available = True

    # Indicator to reference if the bookings file is available.

    def __init__(self):
        self.customer_file = "customers.txt"
        self.location_file = "locations.txt"
        self.rate_file = "rates.txt"
        self.service_file = "services.txt"
        self.booking_file = "bookings.txt"

    def num_arguments(self):
        if len(FileManager.arguments) == 1:
            # No command-line arguments provided, use default file names
            print("Using default values: <customers.txt> <locations.txt> <rates.txt> <services.txt> <bookings.txt>")
            FileManager.check_files_existence()
            return
        if len(FileManager.arguments) == 5:
            _, self.customer_file, self.location_file, self.rate_file, self.service_file = sys.argv
            print('Customer, Location, Rates, Services files provided. Bookings unavailable.')
            FileManager.bookings_available = False
        elif len(FileManager.arguments) == 6:
            _, self.customer_file, self.location_file, self.rate_file, self.service_file, self.booking_file = sys.argv
        else:
            print("Incorrect number of arguments entered, closing file")
            print("Usage: python script.py <customer_file> <location_file> <rate_file> <service_file> [booking_file]")

            sys.exit(1)

    @staticmethod
    def check_files_existence():
        required_files = ['customers.txt', 'locations.txt', 'rates.txt', 'services.txt', 'bookings.txt']

        for file_name in required_files:
            if os.path.exists(file_name):
                print(f"File '{file_name}' found.")
                if file_name == "bookings.txt":
                    FileManager.bookings_available = True
            else:
                if file_name == 'bookings.txt':
                    print(f"Notification: File '{file_name}' is not available.")
                    FileManager.bookings_available = False
                else:
                    print(
                        f"Error: File '{file_name}' is not available. Please check that files are in correct directory.")
                    print("Closing app")
                    exit()

    @staticmethod
    def write_cust_on_close():
        with open(file_manager.customer_file, 'w') as cust_file:
            for customer_obj in Records.customer_recs:
                if customer_obj.cust_type == "b":
                    line = f"{customer_obj.get_id()},"
                    line += f"{customer_obj.get_name()},"
                    line += f"{customer_obj.cust_type},"
                    line += f"{BasicCustomer.get_basic_discount_rate()}\n"  # Add a newline character at the end
                    cust_file.write(line)
                else:
                    line = f"{customer_obj.get_id()},"
                    line += f"{customer_obj.get_name()},"
                    line += f"{customer_obj.cust_type},"
                    rate1, rate2 = customer_obj.get_rates()
                    line += f"{rate1},"
                    line += f"{customer_obj.get_thresh()}\n"  # Add a newline character at the end
                    cust_file.write(line)

    @staticmethod
    def write_loc_file_on_close():
        location_file = open(file_manager.location_file, 'w')
        for loc_obj in Records.locations_recs:
            line = ""
            line += f"{loc_obj.get_loc_id()},"
            line += f"{loc_obj.get_loc_name()}\n"
            location_file.write(line)
        location_file.close()

    @staticmethod
    def write_rates_file_on_close():
        rate_file = open(file_manager.rate_file, 'w')
        for rate in Records.rates_recs:
            line = ""
            line += f"{rate.ID},"
            line += f"{rate.rate_name},"
            line += f"{rate.price}\n"
            rate_file.write(line)
        rate_file.close()

    @staticmethod
    def write_bookings():
        booking_file = open(file_manager.booking_file, 'w')
        for booking in Records.bookings_recs:
            new_line = ""
            cust = booking.customer
            new_line += f"{cust},"
            departure = booking.departure
            new_line += f"{departure},"

            for i in range(len(booking.destination)):
                new_line += f'{booking.destination[i]},'
                new_line += f'{booking.distance_list[i]},'
            rate = booking.rate
            rate = rate.rate_name
            new_line += f"{rate},"
            if booking.services is None:
                new_line += ","
            else:
                new_line += f"{booking.services.service_name.strip()},"
            base_fee = Booking.base_fee
            total_dist = 0
            for i in booking.distance_list:
                total_dist += float(i)
            distance_fee = total_dist * float(booking.rate.price)
            book_discount = booking.discount
            total_cost = booking.booking_cost
            new_line += f"{base_fee},"
            new_line += f"{distance_fee},"
            new_line += f"{book_discount},"
            new_line += f"{total_cost}\n"
            booking_file.write(new_line)
        booking_file.close()


class Operations:

    @staticmethod
    def menu_printer():
        sys.stdout.write("""\nPlease select from the following by inputting the corresponding number:\n
        1  - Book a trip.\n
        2  - Add/update rate types and prices.\n
        3  - Display existing customers.\n
        4  - Display existing locations.\n
        5  - Add new locations.\n
        6  - Display existing rate types. \n
        7  - Update Basic Customer Discount Rate. \n
        8  - Update Enterprise Customer Discount Rate.\n
        9  - Update Enterprise Customer Discount Threshold.\n
        10 - See the most valuable customer.\n
        11 - See a previous customer's bookings. \n
        12 - Display all previous bookings. \n
        0 - Exit the program.\n
        \n
        Please enter your selection: """)

    @staticmethod
    def option_select():
        """Menu input that returns the corresponding function and calls itself."""
        selection = sys.stdin.readline().strip()
        sys.stdout.write("\n")

        if selection == "1":
            Operations.book_trip()
            sys.stdout.write("\n")
            Operations.menu_printer()
            Operations.option_select()

        elif selection == "2":
            Rate.new_rate()
            Operations.menu_printer()
            Operations.option_select()

        elif selection == "3":
            Records.list_customers()
            sys.stdout.write("\n")
            Operations.menu_printer()
            Operations.option_select()

        elif selection == "4":
            Records.list_locations()
            sys.stdout.write("\n")
            Operations.menu_printer()
            Operations.option_select()

        elif selection == "5":
            Location.add_location()
            sys.stdout.write("\n")
            Operations.menu_printer()
            Operations.option_select()

        elif selection == "6":
            Records.list_rates()
            sys.stdout.write("\n")
            Operations.menu_printer()
            Operations.option_select()

        elif selection == "7":
            BasicCustomer.set_discount_rate()
            sys.stdout.write("\n")
            Operations.menu_printer()
            Operations.option_select()

        elif selection == "8":
            # Need to fix to filter out basic customers
            valid_cust = False
            while not valid_cust:
                cust_obj = input("Please enter the customer name or ID you wish to alter: ")
                cust_obj = cust_obj.strip()
                valid_cust = Customer.get_customer_object(cust_obj)
                print(valid_cust)
                if not valid_cust:
                    print("The entered customer does not exist. Please try again.")
            try:
                valid_cust.enter_new_rate_value()
            except:
                print("That customer is not an enterprise customer.")

            Operations.menu_printer()
            Operations.option_select()

        elif selection == "9":
            valid_cust = False
            while not valid_cust:
                cust_obj = input("Please enter the customer name or ID you wish to alter: ")
                cust_obj = cust_obj.strip()
                valid_cust = Customer.get_customer_object(cust_obj)
                if not valid_cust:
                    print("The entered customer does not exist. Please try again.")
            try:
                valid_cust.enter_new_thresh_value()

            except:
                print("That customer is not an enterprise customer.")
            Operations.menu_printer()
            Operations.option_select()

        elif selection == "10":
            Records.val_customer()
            Operations.menu_printer()
            Operations.option_select()

        elif selection == "11":
            selection = input('For which customer would you like to see bookings: ')
            selection = selection.strip()
            Records.customer_previous_bookings(selection)
            Operations.menu_printer()
            Operations.option_select()

        elif selection == "12":
            Records.all_previous_bookings()
            Operations.menu_printer()
            Operations.option_select()

        elif selection == "0":
            sys.stdout.write("Thank you for using RMIT Taxi Service.")
            file_manager.write_cust_on_close()
            file_manager.write_loc_file_on_close()
            file_manager.write_rates_file_on_close()
            file_manager.write_bookings()
            sys.exit()

        else:
            sys.stdout.write("Please enter a valid number.\n")
            Operations.menu_printer()
            Operations.option_select()

    @staticmethod
    def book_trip():
        Booking.new_booking()

    @staticmethod
    def display_existing_customers():
        Records.list_customers()

    @staticmethod
    def display_existing_locations():
        Records.list_locations()

    @staticmethod
    def display_existing_rates():
        Records.list_rates()


if __name__ == "__main__":
    file_manager = FileManager()
    file_manager.num_arguments()
    Records.read_customers()
    Records.read_locations()
    Records.read_rates()
    Records.read_services()
    try:
        Records.read_bookings()
    except:
        print('No previous bookings in system.')
    New_op = Operations()
    New_op.menu_printer()
    New_op.option_select()
