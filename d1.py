# loader our newly minted testbed file
from pyats.topology import loader
testbed = loader.load('ios_testbed.yaml')

# access the devices
testbed.devices
# AttrDict({'ios-1': <Device ott-tb1-n7k4 at 0xf77190cc>,
#           'ios-2': <Device ott-tb1-n7k5 at 0xf744e16c>})
ios_1 = testbed.devices['ios-1']
ios_2 = testbed.devices['ios-2']

# find links from one device to another
for link in ios_1.find_links(ios_2):
    print(repr(link))
# <Link link-1 at 0xf744ef8c>

# establish basic connectivity
ios_1.connect()

# issue commands
print(ios_1.execute('show version'))
ios_1.configure('''
    interface GigabitEthernet0/0
        ip address 10.10.10.1 255.255.255.0
''')

# establish multiple, simultaneous connections
ios_2.connect(alias = 'console', via = 'a')
ios_2.connect(alias = 'vty_1', via = 'vty')

# issue commands through each connection separately
ios_2.vty_1.execute('show running')
ios_2.console.execute('reload')

# creating connection pools
ios_2.start_pool(alias = 'pool', size = 2)

# use connection pool in multiprocessing paradigms
# each process will be allocated a connection - whenever one is available
def sleep(seconds):
    ios_2.pool.execute('sleep %s' % seconds)
import multiprocessing
p1 = multiprocessing.Process(target=sleep, args = (10, ))
p2 = multiprocessing.Process(target=sleep, args = (10, ))
p3 = multiprocessing.Process(target=sleep, args = (10, ))
p1.start(); p2.start(); p3.start()
p1.join(); p2.join(); p3.join()