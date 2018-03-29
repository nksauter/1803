from __future__ import division
import mrcfile
import numpy as np
import sys, math
from dxtbx.format.FormatCBFMini import FormatCBFMini
from dxtbx.model.detector import DetectorFactory
from dxtbx.model.beam import BeamFactory
from scitbx.array_family import flex
from scitbx import fftpack
from numpy import fft

def load_fft():
  with mrcfile.open(sys.argv[1]) as mrc:
    # coerce to double
    realpart = flex.double(mrc.data.astype(np.float64))
    complpart = flex.double(flex.grid(realpart.focus()))
    C3D = flex.complex_double(realpart,complpart)

    print "C3Dfocus",C3D.focus()
    print C3D
    FFT = fftpack.complex_to_complex_3d((C3D.focus()[0],C3D.focus()[1],C3D.focus()[2]))
    complex_flex = FFT.forward(C3D)
    print complex_flex.focus()
    print complex_flex

  return complex_flex

def get_intensity_and_phase(complex_flex):
  real, imag = complex_flex.parts()
  intensity = real**2 + imag**2
  intensity /= 1e10
  intensity = intensity.iround()
  print "Shifting intensity..."
  intensity = flex.int(fft.fftshift(intensity.as_numpy_array()))
  print intensity.focus()

  phase = flex.atan2(imag, real)*180/math.pi
  phase = phase.iround()
  print "Shifting phases..."
  phase = flex.int(fft.fftshift(phase.as_numpy_array()))
  print phase.focus()
  return intensity, phase

def make_images(data, tag):
  pixel_size = 0.1
  detector = DetectorFactory.simple(
      'PAD', 100, (pixel_size*data.focus()[1]/2,pixel_size*data.focus()[2]/2), '+x', '-y',(pixel_size, pixel_size),
      (data.focus()[2], data.focus()[1]), (-1, 1e6-1), [],
      None)
  beam = BeamFactory.simple(1.0)

  for slice_id in [0,1,2]:
    for idx in xrange(data.focus()[slice_id]):
      if slice_id == 0: # slow
        data_slice = data[idx:idx+1,:,:]
        data_slice.reshape(flex.grid(data.focus()[1], data.focus()[2]))
        filename = "fft_frame_%s_mf_%04d.cbf"%(tag, idx)
      elif slice_id == 1: # med
        data_slice = data[:,idx:idx+1,:]
        data_slice.reshape(flex.grid(data.focus()[0], data.focus()[2]))
        filename = "fft_frame_%s_sf_%04d.cbf"%(tag, idx)
      elif slice_id == 2: # fast
        data_slice = data[:,:,idx:idx+1]
        data_slice.reshape(flex.grid(data.focus()[0], data.focus()[1]))
        filename = "fft_frame_%s_sm_%04d.cbf"%(tag, idx)
      print ['slow', 'med', 'fast'][slice_id], idx
      FormatCBFMini.as_file(detector,beam,None,None,data_slice,filename)

if __name__=="__main__":
  fft_flex = load_fft()
  for tag, dataset in zip(['I', 'phase'], get_intensity_and_phase(fft_flex)):
    make_images(dataset, tag)
  print "Done"
