from __future__ import division
import mrcfile
import numpy as np

def get_3D_transform():
  #with mrcfile.open("cropout_bin4.mrc") as mrc: # small example
  with mrcfile.open("cropout.mrc") as mrc:
    imax=512 #take small subset, optimized for prime factorization

    # coerce to double
    from scitbx.array_family import flex
    realpart = flex.double(mrc.data.astype(np.float64))
    # in-place resize to a good multiple of 2
    realpart.resize(flex.grid(imax,imax,imax))
    complpart = flex.double(flex.grid(imax,imax,imax))
    #from IPython import embed; embed()
    C3D = flex.complex_double(realpart,complpart)

    from matplotlib import pyplot as plt
    from scitbx import fftpack
    #plt.imshow(S2D)
    #plt.show()
    #from IPython import embed; embed()
    print "C3Dfocus",C3D.focus()
    print C3D
    FFT = fftpack.complex_to_complex_3d((C3D.focus()[0],C3D.focus()[1],C3D.focus()[2]))
    c = FFT.forward(C3D)
    print c.focus()
    print c
    return c

if __name__=="__main__":
  c = get_3D_transform()
  #f = get_unit_points_on_hemisphere()
  print c[(0,0,0)]
