import subprocess
import sys


# Checks to see if running on windows
def check_for_win():
	if sys.platform != 'win32':
		print 'This program is designed to run ONLY on Windows'
		sys.exit(1)


### Dead code follows ###
# Calculates CIDR notation from subnet mask
# Takes: xxx.xxx.xxx.xxx styled subnet mask string
# Returns: String of equivalent CIDR notation 
def calc_CIDR(subnet):
    return str(sum([bin(int(x)).count('1') for x in subnet.split('.')]))
### End dead code ###


# Get's list of IP ranges and subnetmasks
# Returns: List of IP ranges with subnets in string format
def get_subnet():
	# Gets the output from ipconfig and splits on newlines
	ipconfig = subprocess.check_output("ipconfig").split('\n')
	IPs = []
	IP_list = []
	SUB_list = []
	# Read through output line by line
	for line in ipconfig:
		# Important line if contains IPv4 Address
		if 'IPv4 Address' in line:
			# Get the last part (seperated by spaces)
			IP_list.append(line.split()[-1])
		# Important line if contains Subnet Mask
		elif 'Subnet Mask' in line:
			# Get the last part (seperated by spaces)
			SUB_list.append(line.split()[-1])
	# Go through list of IP addresses (if more than one NIC)
	for i in range(len(IP_list)):
		# Split on periods
		temp_IP = IP_list[i].split('.')
		# Bad solution is bad (just assume Subnet ID is 0)
		temp_IP[-1] = '0'
		# Replace last octect with a 0 and reassemble into a string
		temp_IP = '.'.join(temp_IP)
		# IPs.append(temp_IP+'/'+calc_CIDR(SUB_list[i]))
		# Change format into IP/SubnetMask format
		IPs.append(temp_IP+'/'+SUB_list[i])
	return IPs


# Asks user to use or not use IP ranges found from ipconfig
# Returns: List of IP ranges selected from user input in string format
# Note: Will exit program if no IP ranges are selected
def ip_prompt(all_IPs):
	IPs = []
	# all_IPs = get_subnet()
	# Loop through IP addresses from IP config
	for ip in all_IPs:
		end_loop = False
		# Start input loop
		while(not end_loop):
			# Ask question
			print 'Use IP range \"'+ ip +'\"?'
			ans = raw_input("[Y/n] ")
			# Add IP if y or Y
			if ans.upper() == 'Y':
				IPs.append(ip)
				end_loop = True
			# Default answer counts as Y (no keyboard input)
			elif not ans:
				IPs.append(ip)
				end_loop = True
			# Don't add if n or N entered
			elif ans.upper() == 'N':
				end_loop = True
			# Didn't input N/n/Y/y or nothing try again
			else:
				continue
	# If you don't add any IP ranges then there's nothing to do
	if IPs == []:
		print 'No IP ranges selected\n\nquitting...'
		sys.exit(1)
	else:
		return IPs


# Runs sl.exe (scanline) on given IP range
# Takes: String of IP range with subnet notation
# Returns: List of IP addresses found in IP range in string format
# Note: Will exit program if sl.exe is not found in %PATH%
def run_SL(ip_range):
	# Split IP from netmask
	ip = ip_range.split('/')
	# Split IP octets
	split_ip = ip[0].split('.')
	# Change last octet to 1-254 if /24
	if ip[-1] == '255.255.255.0':
		split_ip[-1] = '1-254'
	# Input loop if not /24
	else:
		end_loop = False
		while(not end_loop):
			# Ask for IP range
			ans = raw_input("Enter IP range: ")
			# Some input validation
			if '-' in ans:
				nums = ans.split('-')
				if len(nums) == 2:
					try:
						# Make sure start is less than end
						if (int(nums[0]) < int(nums[1])) and (int(nums[1]) < 255):
							split_ip[-1] = ans
							end_loop = True
							break
					except:
						pass
			print '\nEnter range in format: 1-254'
	c_ip = '.'.join(split_ip)
	command = 'sl.exe -ht 445 ' + c_ip
	try:
		print 'running \"' + command + '\"'
		output = subprocess.check_output(command)
	except:
		print 'sl.exe not found.\n\nquitting...'
		# sys.exit(1)
	with open('sl_test_output.txt') as f:
		output = f.readlines()
	ip_list = []
	for line in output:
		if '.' in line and 'ms' not in line:
			ip_list.append(line.strip('\n'))
	return ip_list


# Runs psexec to run a command on target machine
# Takes: IP address in string format, Username string, Password string
# Note: Will exit program if psexec.exe is not found in %PATH%
def run_PSE(ipaddr, username, password, runfile):
	command = 'psexec ' + '\\\\' + ipaddr + ' -u ' + username + ' -p ' + password + ' /c ' + runfile
	try:
		print 'running \"' + command + '\"'
		output = subprocess.check_output(command)
	except:
		print 'psexec.exe not found.\n\nquitting...'
		# sys.exit(1)
	return


def main():
	try:
		username = sys.argv[1]
		password = sys.argv[2]
		runfile  = sys.argv[3]
	except:
		print 'Usage: ' + sys.argv[0] + ' <username> <password> <file to run>'
		sys.exit(1)
	try:
		open(runfile)
	except:
		print runfile + ' not found'
		sys.exit(1)
	clients = []
	# Get subnet and prompt for use
	IPs = ip_prompt(get_subnet())
	# Run sl on subnets (1 loop for 1 nic)
	for ip in IPs:
		clients.append(run_SL(ip))
	# Run psexec on subnets (1 loop for 1 nic)
	for slist in clients:
		for ip in slist:
			run_PSE(ip, username, password, runfile)


if __name__ == '__main__':
	check_for_win()
	main()