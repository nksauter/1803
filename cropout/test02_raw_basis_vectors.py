from __future__ import division
import mrcfile
import numpy as np
from scitbx.matrix import col
from scitbx.array_family import flex
imax=512 #take small subset, optimized for prime factorization

def get_3D_transform():
  #with mrcfile.open("cropout_bin4.mrc") as mrc: # small example
  with mrcfile.open("cropout.mrc") as mrc:

    # coerce to double
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
def get_unit_points_on_hemisphere():
  mersenne_twister = flex.mersenne_twister(seed=0)
  sphere_points = []
  for m in xrange(20000):
    sphere_pt = col(mersenne_twister.random_double_point_on_sphere())
    sphere_points.append(sphere_pt)
  return sphere_points

def coord_list(unitvec):
  def coerce(coord):
    # translate a floating value index into an array index.  Units are pixels.
    int_coord = int(round(coord,0))
    if int_coord<0: return int_coord+imax
    else: return int_coord
  coord_list = []
  # given a unit vector, find a list of fast,med,slow on that candidate axis.
  for x in xrange(-100,100):
    arrayvec = x*unitvec
    A = (coerce(arrayvec[0]),coerce(arrayvec[1]),coerce(arrayvec[2]))
    coord_list.append(A)
  return coord_list

if __name__=="__main__":
  c = get_3D_transform()
  f = get_unit_points_on_hemisphere()
  idx_summ_fom = flex.double()
  idx_projections = []
  for vec in f:
    CL = coord_list(vec)
    projection = flex.double()
    summ = 0.0
    i = -101
    for cdl in CL:
      i+=1
      if -10 < i < 10:
        projection.append(0)
        continue
      value = abs(c[cdl])
      projection.append(value)
      summ += value
    print summ
    idx_projections.append(projection)
    idx_summ_fom.append(summ)
    print
  #good start here.  Record the projections.  Graph the 10 best, see if they are periodic.  Try to select the basis
  order = flex.sort_permutation(idx_summ_fom,reverse=True)
  print list(idx_summ_fom.select(order))[:100]

  for x in range(20):
    from matplotlib import pyplot as plt
    plt.plot(range(-100,100),idx_projections[order[x]],"r-")
    plt.show()
