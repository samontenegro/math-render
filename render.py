from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc
from os import system
import numpy as np
import sys

from coeff import GenericCoefficientArray
from init import enum
import init

rc("text", usetex=True)                         # USE TeX FOR RENDERING TEXT
np.seterr(all='raise')                          # RAISE WARNINGS AS ERRORS

# FLAGS

TERMS = int(sys.argv[1]) > 0 and int(sys.argv[1]) or 0
VIDEO = len(sys.argv) == 3 and sys.argv[2] or ""

# CONSTANTS AND KERNELS

PI              = np.pi                             # VALUE OF PI
SIN_KERNEL      = lambda x, n : np.sin(n * x)       # SINE KERNEL
COS_KERNEL      = lambda x, n : np.cos(n * x)       # COSINE KERNEL
EXP_KERNEL      = lambda x, n : np.exp(1j * n * x)  # COMPLEX EXPONENTIAL KERNEL
ONE_KERNEL      = lambda x, n : 1                   # 1-KERNEL

# AUXILIARY FUNCTIONS

COEFF_FILENAME = "coeffs.csv"
COEFF_ARRAY = GenericCoefficientArray(COEFF_FILENAME)

# AUXILIARY CONSTANTS

K = 10

# HELPER FUNCTIONS

def summation(function, domain, kernel = ONE_KERNEL, N = 0, M = 0):

    # SUMMATION LIMIT MUST BE INCREASED BY 1 AS A RESULT OF CONVENTION

    S_m = np.zeros(domain.size)                                             # INITIALIZATION
    for k in range(N,M+1):
        try:
            _term = function(domain,k)*kernel(domain,k)
        except FloatingPointError:                                      # CATCH PRECISION ERRORS
            print("Warning: Floating Point Error")
            return S_m
        except ZeroDivisionError:                                       # CATCH DIVISION BY ZERO
            print("Warning: Zero Division Error")
            return S_m

        S_m = S_m + _term                                               # SUMMATION
    return S_m
    
# CANVAS PARAMETERS

WIDTH       = 8                                 # WIDTH OF CANVAS IN INCHES
HEIGHT      = 8                                 # HEIGHT OF CANVAS IN INCHES
DPI         = 140                               # DOTS PER INCH
RESOLUTION  = int(WIDTH * DPI)                  # RESOLUTION OF PLOT

# PLOT PARAMETERS

X_LIM_INF       = -1*PI                       # LOWER X BOUND
X_LIM_SUP       = 1*PI                        # UPPER X BOUND

Y_LIM_INF       = -0.1                          # LOWER Y BOUND
Y_LIM_SUP       = 1.0                           # UPPER Y BOUND

LABEL_PAD       = 12                            # SPACING BETWEEN LABELS AND AXES IN PT
LABEL_FONT_SIZE = 18                            # FONT SIZE FOR LABELS
TICK_FONT_SIZE  = 12                            # FONT SIZE FOR TICKS

X_LABEL         = "$z$"
Y_LABEL         = "$f(z)$"
COLOR           = "b"

FILENAME        = "fourier_test_spike"

# VIDEO PARAMETERS

FRAMERATE   = 5
ZERO_PAD    = 3

# COEFFICIENT FUNCTIONS

FUNCTION        = lambda x, n : (1/PI) * COEFF_ARRAY.coeff(n)
CONSTANT        = (1/ (2*PI)) * 2 * np.arctan(K*PI) / K

# PLOT DATA

DOMAIN          = np.linspace(X_LIM_INF,X_LIM_SUP,RESOLUTION)
DATA            = lambda terms : CONSTANT + summation(FUNCTION, DOMAIN, kernel = COS_KERNEL, N=1, M=terms)

# PLOT INITIALIZATION

fig = Figure(figsize=(WIDTH,HEIGHT), dpi=DPI)
canvas = FigureCanvas(fig)

ax = fig.add_subplot(111)
ax.set_xlim(X_LIM_INF, X_LIM_SUP)
ax.set_ylim(Y_LIM_INF, Y_LIM_SUP)
ax.set_xlabel(X_LABEL, labelpad=LABEL_PAD, fontsize=LABEL_FONT_SIZE)
ax.set_ylabel(Y_LABEL, labelpad=LABEL_PAD, fontsize=LABEL_FONT_SIZE)
ax.tick_params(axis="y", direction="in", labelsize=TICK_FONT_SIZE)
ax.tick_params(axis="x", direction="in", labelsize=TICK_FONT_SIZE)

# PLOTTING

PATH = "assets/img/" + FILENAME

if VIDEO == "-v":
    for i in range(1,TERMS + 1):
        
        _line = ax.plot(DOMAIN,DATA(i), COLOR)
        canvas.print_figure(PATH + enum(i, ZERO_PAD))
        _line.pop(0).remove()
    
    _render_with_ffmpeg = (
        "ffmpeg -framerate " + str(FRAMERATE) + " -i " +
        PATH + "%0" + str(ZERO_PAD) + "d.png " +
        "assets/vid/" + FILENAME + ".mp4"
    )

    system(_render_with_ffmpeg)
else:
    ax.plot(DOMAIN,DATA(TERMS), COLOR)
    canvas.print_figure(PATH)


