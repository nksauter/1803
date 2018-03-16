from __future__ import division
import mrcfile
with mrcfile.open("cropout_bin4.mrc") as mrc:
#with mrcfile.open("cropout.mrc") as mrc:
  imax=128
  S3D = mrc.data[0:imax,0:imax,0:imax]
  from matplotlib import pyplot as plt
  #plt.imshow(S2D)
  #plt.show()
  print S3D.shape
  import copy
  import numpy.fft
  C = numpy.fft.fftn(a=S3D,s=(imax,imax,imax),axes=(0,1,2))
  print C.shape
  import numpy as np
  cum = None
  for sec in xrange((imax//2)-25,(imax//2)+25):
    D = numpy.fft.fftshift(C[:,sec,:])
    #D = C[:,:,sec]
    Dabs = np.abs(D)
    if cum is None:
      cum = copy.deepcopy(np.abs(D))
    else:
      #from IPython import embed; embed()
      for x in xrange(imax):
        for y in xrange(imax):
          cum[x,y] = max(cum[x,y],Dabs[x,y])


    ##plt.imshow(np.abs(D))
    #plt.show()
  #from IPython import embed; embed()
  plt.imshow(cum)
  plt.show()
