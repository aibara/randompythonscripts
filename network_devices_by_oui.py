#!/usr/bin/env

import netaddr
import re
import subprocess
import matplotlib

matplotlib.use('macosx')

import pylab

# get the text output of arp -an
txt = subprocess.Popen(["arp", "-an"], stdout=subprocess.PIPE).communicate()[0]

# compile a regex for mac addrs
addr_re = re.compile("\w+:\w+:\w+:\w+:\w+:\w+")

# get a list of mac addrs
ouis = addr_re.findall(txt)

# build a dictionary of orgs and count
orgmap = {}
for oui in ouis:
	if oui == 'ff:ff:ff:ff:ff:ff':
		continue

	mac = netaddr.EUI(oui)

	org = str(mac)
	try:
		org = mac.oui.registration().org
	except Exception:
		pass
	if orgmap.has_key(org):
		orgmap[org] += 1
	else:
		orgmap[org] = 1

# build another dictionary based only on first word (Apple, Inc vs Apple vs Apple Computer vs Apple Inc.)
# they key is first word, value is tuple of full org name, count
# org name gets reset each time to the current one
first_word_re = re.compile("\w+")
orgmap2 = {}
for org in orgmap.keys():
	start = first_word_re.match(org).group(0)
	if orgmap2.has_key(start):
		orgmap2[start] = (org, orgmap2[start][1] + orgmap[org])
	else:
		orgmap2[start] = (org, orgmap[org])

# sort the list in descending order
sorted_list = sorted(orgmap2.items(), key=lambda x: x[1][1], reverse = True)

# list of just the fullname, total count
sorted_list = map(lambda x: x[1], sorted_list)

# print the list out
for name, count in sorted_list:
	print "%3d %5.1f%%" % (count, 100 * count/(len(ouis)- 1)), name

# plot a pie chart
pylab.figure(1, figsize=(15,15))
ax = pylab.axes([0.1, 0.1, 0.8, 0.8])

labels = map(lambda x: x[0], sorted_list)
fracs = map(lambda x: x[1], sorted_list)

pylab.pie(fracs, labels=labels, autopct='%1.1f%%')
pylab.title('Network Devices by Type', bbox={'facecolor':'0.8', 'pad':5})

pylab.show()
