from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc
import numpy as np

rc("text", usetex=True)                         # USE TEX FOR RENDERING TEXT

# CONSTANTS AND KERNELS

PI              = np.pi                             # VALUE OF PI
SIN_KERNEL      = lambda x, n : np.sin(n * x)       # SINE KERNEL
COS_KERNEL      = lambda x, n : np.cos(n * x)       # COSINE KERNEL
EXP_KERNEL      = lambda x, n : np.exp(1j * n * x)  # COMPLEX EXPONENTIAL KERNEL
ONE_KERNEL      = lambda x, n : 1                   # 1-KERNEL

# HELPER FUNCTIONS

def summation(function, domain, kernel = ONE_KERNEL, N = 0, M = 1):

    # SUMMATION LIMIT MUST BE INCREASED BY 1 AS A RESULT OF CONVENTION

    S_m = np.zeros(domain.size)                                             # INITIALIZATION
    for k in range(N,M):
        S_m = S_m + function(domain,k)*kernel(domain,k)                     # SUMMATION

    return S_m

# CANVAS PARAMETERS

WIDTH       = 8                                 # WIDTH OF CANVAS IN INCHES
HEIGHT      = 8                                 # HEIGHT OF CANVAS IN INCHES
DPI         = 140                               # DOTS PER INCH
RESOLUTION  = int(WIDTH * DPI)                  # RESOLUTION OF PLOT

# PLOT PARAMETERS

X_LIM_INF       = -PI                       # LOWER X BOUND
X_LIM_SUP       = PI                        # UPPER X BOUND

Y_LIM_INF       = -1.25                          # LOWER Y BOUND
Y_LIM_SUP       = 1.25                           # UPPER Y BOUND

LABEL_PAD       = 12                            # SPACING BETWEEN LABELS AND AXES IN PT
LABEL_FONT_SIZE = 18                            # FONT SIZE FOR LABELS
TICK_FONT_SIZE  = 12                            # FONT SIZE FOR TICKS

X_LABEL         = "$z$"
Y_LABEL         = "$f(z)$"

FILENAME        = "fourier_test"

# COEFFICIENT FUNCTIONS

FUNCTION        = lambda x, n : (2/(PI * n)) * (np.cos(n * PI / 2) - np.cos(n * PI))
CONSTANT        = 0

# PLOT DATA

DOMAIN          = np.linspace(X_LIM_INF,X_LIM_SUP,RESOLUTION)
DATA            = (CONSTANT * np.ones(DOMAIN.size)) + summation(FUNCTION, DOMAIN, kernel = SIN_KERNEL, N=1, M=30+1)

# PLOT INITIALIZATION

fig = Figure(figsize=(WIDTH,HEIGHT), dpi=DPI)
canvas = FigureCanvas(fig)

ax = fig.add_subplot(111)
ax.plot(DOMAIN,DATA)
ax.set_xlim(X_LIM_INF, X_LIM_SUP)
ax.set_ylim(Y_LIM_INF, Y_LIM_SUP)
ax.set_xlabel(X_LABEL, labelpad=LABEL_PAD, fontsize=LABEL_FONT_SIZE)
ax.set_ylabel(Y_LABEL, labelpad=LABEL_PAD, fontsize=LABEL_FONT_SIZE)
ax.tick_params(axis="y", direction="in", labelsize=TICK_FONT_SIZE)
ax.tick_params(axis="x", direction="in", labelsize=TICK_FONT_SIZE)

# ax.set_title('hi mom')
# ax.grid(True)

canvas.print_figure('assets/' + FILENAME)