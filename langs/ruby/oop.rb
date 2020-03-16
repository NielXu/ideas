# Ruby OOP

# $variable - Global variable
$TEST = "YES";

class Customer
    # @@variable - Class Variable, share among all instances
    @@no_of_customers = 0;

    # Constant
    CONST = -1;

    # attr_reader :instance_variable - Allow access to instance variable
    # cust_id is read-only
    attr_reader :cust_id
    
    # attr_writer :instance_variable - Allow modification to instance variable
    # cust_addr is write-only
    attr_writer :cust_addr

    # attr_accessor :instance_variable - Allow both read and write to instance variable
    # cust_name has both getter and setter
    attr_accessor :cust_name

    # initialize - Consturctor
    def initialize(id, name, addr)
        # @variable - Instance variable, every instance has its own instance variables
        @cust_id = id;
        @cust_name = name;
        @cust_addr = addr;
        # Increment no_of_customers, shared between instances
        @@no_of_customers += 1;
    end

    def test
        # #variable - access variable or constant
        puts "The test result is #$TEST";
        puts "The const is #{CONST}"
    end

    def display_info
        puts "Customer ID: #@cust_id"
        puts "Customer Name: #@cust_name"
        puts "Customer Address: #@cust_addr"
    end

    def cust_count
        # Return something
        return @@no_of_customers
    end

    def log(msg)
        puts msg
    end

    def create_appointment(time)
        # Calling another method in the same class
        log("Confirmed appointment at: #{time}")
    end
end

# Create instances
# .new(...) - Calling constructor
cust1 = Customer.new('0', 'Daniel', '123 Foo Street');
cust2 = Customer.new('1', 'Alex', '456 Bar Ave');

# instance_name.method_name - Calling method
cust1.test;
cust2.test;

puts
# calling method
cust1.display_info
cust2.display_info

puts
# calling method with argument
cust1.create_appointment("2020-02-02")

puts
# #{code}, executing the code inside the block and concat it with the string 
puts "Numeber of customers in cust1: #{cust1.cust_count}"
puts "Numeber of customers in cust2: #{cust2.cust_count}"

puts
# Read the instance variable
puts cust1.cust_id

puts
# Write the instance variable
cust1.cust_addr = "999 Local Street"
cust1.display_info

puts
# Read then write the instance variable
puts cust1.cust_name
cust1.cust_name = "Zero"
cust1.display_info