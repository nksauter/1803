from __future__ import division
import mrcfile
#with mrcfile.open("cropout_bin4.mrc") as mrc:
with mrcfile.open("cropout.mrc") as mrc:
 mrc.print_header()
 for sec in xrange(200,300):
  S2D = mrc.data[0:512,0:512,sec]
  from matplotlib import pyplot as plt
  #plt.imshow(S2D)
  #plt.show()
  print S2D.shape

  import numpy.fft
  C = numpy.fft.fft2(S2D)
  import numpy as np
  D = numpy.fft.fftshift(C)
  plt.imshow(np.abs(D))
  plt.show()
  #from IPython import embed; embed()
