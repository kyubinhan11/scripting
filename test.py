y = u'Mo:L\u00e9 Restaurant'
r = y.encode('utf-8').decode('utf-8')
print r
print 'Rank {0}, '.format('1') + r
print 'Rank %s, %s' % ('1', r)

# print "Hello %s. Your score is % d" % (name, score)