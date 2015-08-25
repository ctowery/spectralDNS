__author__ = "Mikael Mortensen <mikaem@math.uio.no>"
__date__ = "2015-04-09"
__copyright__ = "Copyright (C) 2015 " + __author__
__license__  = "GNU Lesser GPL version 3 or any later version"

#from utilities.MPI_knee import mpi_import
#with mpi_import():
from mpi4py import MPI
comm = MPI.COMM_WORLD
from cbcdns import config

def get_solver(update=None, regression_test=None):
    #args = None
    #try:
        #if comm.Get_rank() == 0:
            #args = config.parser.parse_args()
    #finally:
        #args = comm.bcast(args, root=0)
        
    args = config.parser.parse_args()
    if args.solver in ('NS2D', 'Bq2D'):
        args.decomposition = 'line'
    vars(config).update(vars(args))
        
    #with mpi_import():
    
    if config.solver == 'NS':
        import cbcdns.solvers.spectralDNS as solver
        
    elif config.solver == 'VV':
        import cbcdns.solvers.spectralDNSVV as solver
        
    elif config.solver == 'NS2D':
        config.L = [config.L[0], config.L[1]]
        config.M = [config.M[0], config.M[1]]    
        import cbcdns.solvers.spectralDNS2D as solver
        
    elif config.solver == 'MHD':
        import cbcdns.solvers.spectralMHD3D as solver

    elif config.solver == 'Bq2D':
        config.L = [config.L[0], config.L[1]]
        config.M = [config.M[0], config.M[1]]    
        import cbcdns.solvers.spectralDNS2D_Boussinesq as solver
        
    else:
        raise AttributeError("Wrong solver!")
            
    if update: solver.update = update
    if regression_test: solver.regression_test = regression_test
    return solver