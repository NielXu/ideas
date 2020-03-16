# Some Hello-World examples

# Comment
=begin
    Multiple lines of comments
=end

# puts - Print string on console with new line
# print - Print string on console without new line
puts "Hello World"

# Run before the program is run
BEGIN {
    puts "Initialization in BEGIN"
}
# Run after the program is finish
END {
    puts "Termination in END"
}

# Here document - Multiple lines of strings
print <<EOF
   This is the first way of creating
   here document ie. multiple line string.
EOF

# Same as above
print <<"EOF"
   This is the second way of creating
   here document ie. multiple line string.
EOF

# Surrounded by `` - Execute commands
print <<`EOC`
    ls
EOC

# Stack multiple identifiers
print <<"foo", <<"bar"
	I said foo.
foo
	I said bar.
bar
