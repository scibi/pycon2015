from PIL import Image
im = Image.open("/tmp/caterpillar-home.png") #Can be many different formats.
pix = im.load()
print(im.format, im.size, im.mode)
print pix
print im.getbands()
(a,b,maxx,maxy)=im.getbbox()
print maxx

for y in xrange(2):
    l=[]
    for x in xrange(maxx/20):
        (r,g,b,a)=pix[x,y]
#        l.append(r%2)
#        l.append(r)
        l.append((r%2,g%2,b%2))
#        l.append(4*(r%2)+2*(g%2)+b%2)
#        l.append(g%2)
#        l.append(b%2)
    print l
print "=========================="
print set(l)

#for x in xrange(len(l)):
#    print l[x],
#    if x%8==0:
#        print

def frombits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append((int(''.join([str(bit) for bit in byte]), 2)))
    return chars
    return ''.join(chars)

#print frombits(l)
#for x in xrange(8):
#    print int(''.join([str(pix[x*8+x2,0][0]%2) for x2 in xrange(8)]),2)
#    print ' ',int(''.join([str(pix[x*8+x2,0][1]%2) for x2 in xrange(8)]),2)
#    print '  ',int(''.join([str(pix[x*8+x2,0][2]%2) for x2 in xrange(8)]),2)
#    print '   ',int(''.join([str(pix[x*8+x2,0][3]%2) for x2 in xrange(8)]),2)

