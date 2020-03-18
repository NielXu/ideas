# Basics about Ruby, inlucding data types, if else and loop

# Array, [a, b, c, ...] does not necessary to have a same type
ary = ["fred", 10, 3.14, "This is a string", "last element"]
# loop through the array, |i| specifies that the element in the array will be used as i
ary.each do |i|
   puts i
end

puts
# HashMap, {key => value, key => value, ...} does not necessary to have a same type
hsh = { "red" => 0xf00, "green" => 0x0f0, "blue" => 0x00f, 999 => -1 }
# loop through the map, |k, v| -> k = the key, v = the value
hsh.each do |k, v|
    puts "Key is: #{k}, value is: #{v}"
end

puts
# (a..b) range from a to b, inclusive, the result will be an array
(10..15).each do |i|
    print i, " "
end
puts

puts
# Condition block
# if, elsif, else
# and(&&), or(||)
x = 1010
if x % 20 == 0 or x % 13 == 0
    puts "1010 % 20 = 0"
elsif x % 2 == 0 and x/2 >= x-x/2
    puts "1010 % 12 = 0 and x/2=x-x/2"
else
    puts "Ops"
end

puts
# code if cond, execute code if the condition is true
puts "One line" if true

puts
# cond? if_true : if_false, conditional assignment
a = 10 == 11 - 1? "Yes" : "No"
puts a