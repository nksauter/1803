from __future__ import division
import mrcfile
with mrcfile.open("cropout_bin4.mrc") as mrc:
#with mrcfile.open("cropout.mrc") as mrc:
  imax=128
  import numpy as np

  # coerce to double
  from scitbx.array_family import flex
  C3D = flex.double(mrc.data.astype(np.float64))
  # in-place resize to a good multiple of 2
  C3D.resize(flex.grid(imax,imax,imax))


  from matplotlib import pyplot as plt
  from scitbx import fftpack
  #plt.imshow(S2D)
  #plt.show()
  #from IPython import embed; embed()
  print C3D.focus()
  print C3D
  import copy
  FFT = fftpack.real_to_complex_3d((C3D.focus()[0],C3D.focus()[1],C3D.focus()[2]-2))
  c = FFT.forward(C3D)
  print c.focus()
  print c

  cum = None
  for sec in xrange((imax//4)-25,(imax//4)+25):
    print sec

    D = c[:,:,sec:sec+1]
    #D = C[:,:,sec]
    parts = D.parts()
    magnitude = flex.sqrt(parts[0]*parts[0] + parts[1]*parts[1])
    mag2d = magnitude.reshape(flex.grid(128,128))
    n = magnitude.as_numpy_array()
    n.reshape(128,128)
    #plt.imshow(n)
    #plt.show()

    if cum is None:
      cum = copy.deepcopy(n)
    else:
      #from IPython import embed; embed()
      for x in xrange(imax):
        for y in xrange(imax):
          cum[x,y] = max(cum[x,y],n[x,y])


    ##plt.imshow(np.abs(D))
    #p
  #from IPython import embed; embed()
  plt.imshow(cum)
  plt.show()
