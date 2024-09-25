from .drop import prediction
from .discrep import discrep
from .shell import shell

from ._parser import Args

args = Args.get()

prediction(args, do_ticks=True, show_title=True, do_contours=True, do_stable=True)
discrep(args)
shell(args)
