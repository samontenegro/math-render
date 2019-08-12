from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rc
import numpy as np

rc("text", usetex=True)

# CONSTANTS

PI          = np.pi                             # VALUE OF PI
KERNEL      = lambda x, n : np.sin(n * x)                  # DEFAUT IS x, n -> 1

# CANVAS PARAMETERS

WIDTH       = 8                                 # WIDTH OF CANVAS IN INCHES
HEIGHT      = 8                                 # HEIGHT OF CANVAS IN INCHES
DPI         = 140                               # DOTS PER INCH
RESOLUTION  = int(WIDTH * DPI)

# PLOT PARAMETERS

X_LIM_INF       = -PI
X_LIM_SUP       = PI


Y_LIM_INF       = -2
Y_LIM_SUP       = 2

LABEL_PAD       = 12                            # SPACING BETWEEN LABEL AND AXIS IN PT
LABEL_FONT_SIZE = 18                            # FONT SIZE FOR LABELS
TICK_FONT_SIZE  = 12                            # FONT SIZE FOR TICKS

X_LABEL = "$z$"
Y_LABEL = "$f(z)$"

# PLOT DATA

FUNCTION        = lambda x, n : np.power(-1,n+1) / n       # FUNCTION EXPRESSIONS

def summation(function, domain, kernel = KERNEL, N = 0, M = 1):        # SUMMATION LIMIT MUST BE INCREASED BY 1 AS A RESULT OF CONVENTION

    print("//-------------------------")
    print("//   COMPUTING")
    print("//-------------------------")

    S_m = np.zeros(domain.size)                                     # INITIALIZATION
    for k in range(N,M):
        S_m = S_m + np.real(function(domain,k)*kernel(domain,k))             # SUMMATION

    print("//   PLOTTING")
    print("//-------------------------")

    return S_m

DOMAIN          = np.linspace(X_LIM_INF,X_LIM_SUP,RESOLUTION)
DATA            = summation(FUNCTION, DOMAIN, N=1, M=100+1)

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

print("//   RENDERING")
print("//-------------------------")

canvas.print_figure('test')