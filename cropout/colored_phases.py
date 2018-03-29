from __future__ import division
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
import dxtbx, sys
from scitbx.array_family import flex
from scitbx.math import five_number_summary

""" Usage: libtbx.python colored_phases.py mf_0602 """

def followup_brightness_scale(data):
  """ histogramming ported from iotbx/detectors/display.h """
  #first pass through data calculate average
  data = data.as_double()
  qave = flex.mean(data)

  #second pass calculate histogram
  hsize=100

  histogram = flex.double(hsize, 0)
  for i in xrange(data.size()):
    temp = int((hsize/2)*data[i]/qave);
    if temp<0: histogram[0]+=1
    elif temp>=hsize: histogram[hsize-1]+=1
    else: histogram[temp]+=1

  #third pass calculate 90%
  percentile=0
  accum=0
  for i in xrange(hsize):
    accum+=histogram[i]
    if (accum > 0.9*data.size()):
      percentile=i*qave/(hsize/2)
      break

  adjlevel = 0.4
  brightness = 0.4
  if percentile > 0.:
    correction = brightness * adjlevel/percentile
  else:
    correction = brightness / 5.0

  outscale = 256
  corrected = data*correction
  outvalue  = outscale * ( 1.0 - corrected )
  sel1 = outvalue < 0
  sel2 = outvalue >= outscale
  outvalue.set_selected(sel1, 0)
  outvalue.set_selected(sel2, outscale-1)

  return outvalue

# frame 602
min_fast = 525
min_slow = 540
delta = 100

frame = sys.argv[1]
intensity = dxtbx.load("fft_frame_I_%s.cbf"%frame).get_raw_data()
intensity_adjust = followup_brightness_scale(intensity)
intensity = intensity[min_slow:min_slow+delta,min_fast:min_fast+delta]
intensity_adjust = intensity_adjust[min_slow:min_slow+delta,min_fast:min_fast+delta]

phases = dxtbx.load("fft_frame_phase_%s.cbf"%frame).get_raw_data()
phases = phases[min_slow:min_slow+delta,min_fast:min_fast+delta]

fast, slow = intensity.focus()

min_i, q1_i, med_i, q3_i, max_i = five_number_summary(intensity.as_1d())
iqr = (q3_i-q1_i)*10
max_value = med_i + (iqr/2)
print "Cutting I at", max_value
i = intensity.as_numpy_array()
i[i<0] = 0
i[i>max_value] = max_value
i = i * (1/max_value)

p = phases.as_numpy_array()
p = p % 180

ones = np.zeros(i.shape) + 1

plt.imshow(intensity_adjust.as_numpy_array(), cmap='gray')
plt.title("Intensities")

plt.figure()
plt.imshow(p, cmap='hsv')
plt.colorbar()
plt.title("Phases")

plt.figure()
p = p.reshape(fast*slow) / 180
i = i.reshape(fast*slow)
ones = ones.reshape(fast*slow)
c = colors.hsv_to_rgb(np.array(zip(p, i, ones)))
c = c.reshape(slow,fast,3)
plt.imshow(c)
plt.title("HSV (hue: phase, saturation: intensity, brightness: 100%)")

plt.show()
