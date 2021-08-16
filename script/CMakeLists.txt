
configure_file(init.sh.in init.sh)

#install the interface __init__ file
install (FILES init.sh 
		 DESTINATION script)
