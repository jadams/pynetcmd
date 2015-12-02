import subprocess
import sys


# Checks to see if running on windows
def check_for_win():
	if sys.platform != 'win32':
		print 'This program is designed to run ONLY on Windows'
		sys.exit(1)


# Calculates CIDR notation from subnet mask
# Takes: xxx.xxx.xxx.xxx styled subnet mask string
# Returns: String of equivalent CIDR notation 
def calc_CIDR(subnet):
    return str(sum([bin(int(x)).count('1') for x in subnet.split('.')]))


# Get's list of IP ranges and subnetmasks
# Returns: List of IP ranges with CIDR subnets in string format
def get_IPs():
	ipconfig = subprocess.check_output("ipconfig").split('\n')
	IPs = []
	IP_list = []
	SUB_list = []
	for line in ipconfig:
		if 'IPv4 Address' in line:
			IP_list.append(line.split()[-1])
		elif 'Subnet Mask' in line:
			SUB_list.append(line.split()[-1])
	for i in range(len(IP_list)):
		temp_IP = IP_list[i].split('.')
		# Bad solution is bad
		temp_IP[-1] = '0'
		temp_IP = '.'.join(temp_IP)
		IPs.append(temp_IP+'/'+calc_CIDR(SUB_list[i]))
	return IPs


# Asks user to use or not use IP ranges found from ipconfig
# Returns: List of IP ranges selected from user input in string format
# Note: Will exit program if no IP ranges are selected
def check_IPs():
	IPs = []
	all_IPs = get_IPs()
	for ip in all_IPs:
		end_loop = False
		while(not end_loop):
			print 'Use IP range \''+ ip +'\'?'
			ans = raw_input("[Y/n] ")
			if ans.upper() == 'Y':
				IPs.append(ip)
				end_loop = True
			elif not ans:
				IPs.append(ip)
				end_loop = True
			elif ans.upper() == 'N':
				end_loop = True
			else:
				continue
	if IPs == []:
		print 'No IP ranges selected\n\nquitting...'
		sys.exit(1)
	else:
		return IPs


# Runs sl.exe (scanline) on given IP range
# Takes: String of IP range with CIDR notation ?
# Returns: List of IP addresses found in IP range in string format
# Note: Will exit program if sl.exe is not found in %PATH%
def run_SL(range):
	try:
		output = subprocess.check_output('sl.exe --help')
	except:
		print 'sl.exe not found.\n\nquitting...'
		sys.exit(1)
	return NULL


# Runs psexec to run a command on target machine
# Takes: IP address in string format, Username string, Password string
# Note: Will exit program if psexec.exe is not found in %PATH%
def run_PSE(ipaddr, username, password):
	command = 'psexec ' + '\\\\' + ipaddr + ' -u ' + username + ' -p ' + password + ' /c ' + 'command.bat'
	print command
	try:
		output = subprocess.check_output(command)
	except:
		print 'psexec.exe not found.\n\nquitting...'
		sys.exit(1)
	return

if __name__ == '__main__':
	check_for_win()

	run_PSE('192.168.1.10', 'test', 'pass')

	# clients = []
	# IPs = check_IPs()
	# for ip in IPs:
	# 	clients.append(run_SL(ip))
