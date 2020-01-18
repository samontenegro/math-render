from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc
from string import Template
from os import system
import numpy as np
import sys

from coeff import GenericCoefficientArray
from init import enum
import init

rc("text", usetex=True)                         # USE TeX FOR RENDERING TEXT
np.seterr(all='raise')                          # RAISE NUMPY WARNINGS AS ERRORS

# CONSTANTS AND KERNELS

PI              = np.pi                             # VALUE OF PI
SIN_KERNEL      = lambda x, n : np.sin(n * x)       # SINE KERNEL
COS_KERNEL      = lambda x, n : np.cos(n * x)       # COSINE KERNEL
EXP_KERNEL      = lambda x, n : np.exp(1j * n * x)  # COMPLEX EXPONENTIAL KERNEL
ONE_KERNEL      = lambda x, n : 1                   # 1-KERNEL

# LOAD COEFFS FROM CSV

COEFF_FILENAME = "data/potential.csv"
COEFF_ARRAY = GenericCoefficientArray(COEFF_FILENAME)

# AUXILIARY CONSTANTS

K = 10

# FOURIER SUMMATION

def summation(function, domain, kernel = ONE_KERNEL, N = 0, M = 0):

    # SUMMATION LIMIT MUST BE INCREASED BY 1 AS A RESULT OF CONVENTION

    S_m = np.zeros(domain.size)                                         # INITIALIZATION
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

WIDTH       = 8                                 # WIDTH OF CANVAS IN INCHES, def: 8
HEIGHT      = 8                                 # HEIGHT OF CANVAS IN INCHES def: 8
DPI         = 96                               	# DOTS PER INCH
RESOLUTION  = int(WIDTH * DPI)                  # RESOLUTION OF PLOT

# PLOT PARAMETERS

X_LIM_INF       = -2*PI                       # LOWER X BOUND
X_LIM_SUP       = 2*PI                        # UPPER X BOUND

Y_LIM_INF       = 0.0                          # LOWER Y BOUND
Y_LIM_SUP       = 3.5                           # UPPER Y BOUND

LABEL_PAD       = 12                            # SPACING BETWEEN LABELS AND AXES IN PLOT, def: 12
LABEL_FONT_SIZE = 18                            # FONT SIZE FOR LABELS, def: 18
TICK_FONT_SIZE  = 12                            # FONT SIZE FOR TICKS, def: 12

X_LABEL         = "$x$"
Y_LABEL         = lambda N : Template("$$S_ {$N} (x)$$").substitute(N = N)
COLOR           = "b"

FILENAME        = "fourier_test_potential"

# VIDEO PARAMETERS

FRAMERATE   = 10
ZERO_PAD    = 2             # DEFAULT

# COEFFICIENT FUNCTIONS

FUNCTION        = lambda x, n : COEFF_ARRAY.coeff(n)
CONSTANT        = 1.53609

# PLOT DATA

DOMAIN          = np.linspace(X_LIM_INF,X_LIM_SUP,RESOLUTION)
DATA            = lambda terms : CONSTANT + summation(FUNCTION, DOMAIN, kernel = COS_KERNEL, N=1, M=terms)

# PLOT INITIALIZATION

fig     = Figure(figsize=(WIDTH,HEIGHT), dpi=DPI)
canvas  = FigureCanvas(fig)

ax = fig.add_subplot(111)
ax.set_xlim(X_LIM_INF, X_LIM_SUP)
ax.set_ylim(Y_LIM_INF, Y_LIM_SUP)
ax.set_xlabel(X_LABEL, labelpad=LABEL_PAD, fontsize=LABEL_FONT_SIZE)

# Y LABEL IS SET WHILE PLOTTING
ax.tick_params(axis="y", direction="in", labelsize=TICK_FONT_SIZE)
ax.tick_params(axis="x", direction="in", labelsize=TICK_FONT_SIZE)

# FLAGS

TERMS   = 10        # DEFAULT
VIDEO   = False
FORMAT  = "png"
SEQ     = False
BBOX    = None 

def parse_flags(argv):

    global VIDEO
    global TERMS
    global FORMAT
    global SEQ
    global ZERO_PAD
    global BBOX
    global FRAMERATE

    for i in range(1,len(argv)):
        flag = argv[i]

        if flag == "-video":
            VIDEO = True
            FRAMERATE = int(argv[i +1]) if int(argv[i +1]) > 0 else 10
        elif flag == "-terms":
            TERMS = int(argv[i +1])
            ZERO_PAD = len(argv[i +1])
        elif flag == "-format":
            FORMAT = argv[i + 1]
        elif flag == "-seq":
            SEQ = True
        elif flag == "-tight":
            BBOX = "tight"

parse_flags(sys.argv)

# PLOTTING

PATH = "assets/img/" + FILENAME

if SEQ or VIDEO:
    for i in range(1,TERMS + 1):
        ax.set_ylabel(Y_LABEL(i), labelpad=LABEL_PAD, fontsize=LABEL_FONT_SIZE)
        _line = ax.plot(DOMAIN,DATA(i), COLOR)
        canvas.print_figure(PATH + enum(i, ZERO_PAD) + "." + FORMAT, format=FORMAT, bbox_inches=BBOX)
        _line.pop(0).remove()
    if VIDEO:
        _render_with_ffmpeg = (
            "ffmpeg -framerate " + str(FRAMERATE) + " -i " +
            PATH + "%0" + str(ZERO_PAD) + "d." + FORMAT + " "
            "assets/vid/" + FILENAME + ".mp4"
        )
        system(_render_with_ffmpeg)
else:
    ax.set_ylabel(Y_LABEL(TERMS), labelpad=LABEL_PAD, fontsize=LABEL_FONT_SIZE)
    ax.plot(DOMAIN,DATA(TERMS), COLOR)
    canvas.print_figure(PATH + "." + FORMAT, format=FORMAT, bbox_inches=BBOX)