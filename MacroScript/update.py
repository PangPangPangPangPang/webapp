import os

os.chdir('../../webapp')
print 'current path' + ' ' + os.getcwd()
print '...........'
print 'updating git'
os.system('git pull')
