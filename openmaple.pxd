cdef extern from "maplec.h":
    #--------------------------------------------------------------------------
    #
    # Basic Types
    #
    # 64-bit architectures
    ctypedef long M_INT
    
    # 32-bit architectures
    ctypedef int M_INT
  
    # Maple Internal Types
    ctypedef M_INT ***ALGEB
    ctypedef M_INT M_BOOL
    ctypedef int INTEGER32
    
   # ctypedef unsigned M_INT M_UINT
    
    # Numeric types
    #ctypedef signed char INTEGER8
    ctypedef short INTEGER16
    ctypedef int INTEGER32
    #ctypedef unsigned INTEGER32 UINTEGER32
    #ctypedef __int64 INTEGER64 #if defined _MSC_VER
    #ctypedef long INTEGER64 # 64-bits architectures
    ctypedef long long INTEGER64
    ctypedef float FLOAT32
    ctypedef double FLOAT64
    #ctypedef ComplexFloat32 COMPLEXF32
    #ctypedef ComplexFloat64 COMPLEXF64      
    #ctypedef ComplexFloatDAG XDAG

    ctypedef enum MapleID:
        pass

    
    #--------------------------------------------------------------------------
    #
    # Maple Kernel Functions
    #
    ctypedef struct MKernelVectorDesc:
        pass
        
    ctypedef struct MCallBackVectorDesc:
        void textCallBack(void *data, int tag, char *output)
        void errorCallBack(void *data, M_INT offset, char *msg)
        void statusCallBack(void *data, long kilobytesUsed, long kilobytesAlloc, double cpuTime)
        char* readLineCallBack(void *data, M_BOOL debug)
        M_BOOL redirectCallBack(void *data, char *name, char *mode)
        char* streamCallBack(void *data, char *stream, int nargs, char **args)
        M_BOOL queryInterrupt(void *data)
        char* callBackCallBack(void *data, char *output)
        
    ctypedef MKernelVectorDesc* MKernelVector
    ctypedef MCallBackVectorDesc* MCallBackVector


cdef extern from "maplec.h" nogil:
    # ---------------------------------------------------------------------- #
    #                        Maple Kernel and Initializers                   #
    # ---------------------------------------------------------------------- #        
    MKernelVector StartMaple(int argc, char *argv, MCallBackVector cb, void *user_data, void *info, char *errstr)
    void StopMaple(MKernelVector kv)
    M_BOOL RestartMaple(MKernelVector kv, char* errstr)
    
    # ---------------------------------------------------------------------- #
    #                       Memory Management                                #
    # ---------------------------------------------------------------------- #

    # Allocate Using Maple's Allocator #
    void* MapleAlloc(MKernelVector kv, M_INT nbytes)

    # Allocate a new Maple Object #
    ALGEB MapleNew(MKernelVector kv, MapleID id, M_INT len)

    # Free Memory Allocated By Maple's Allocator # 
    void MapleDispose(MKernelVector kv, ALGEB s)

    # Allow a to be garbage collected #
    void MapleGcAllow(MKernelVector kv, ALGEB a)

    # Prevent a from being garbage collected #
    void MapleGcProtect(MKernelVector kv, ALGEB a)

    # Check if an object is protected from being garbage collected #
    M_BOOL MapleGcIsProtected(MKernelVector kv, ALGEB a)

    # Apply to all stored Maple objects during a gc sweep #
    void MapleGcMark(MKernelVector kv, ALGEB a)
    
    # ---------------------------------------------------------------------- #
    #                     Conversion from Maple Objects                      #
    # ---------------------------------------------------------------------- #

#    COMPLEXF32 MapleToComplexFloat32(MKernelVector kv, ALGEB s) 

#    COMPLEXF64 MapleToComplexFloat64(MKernelVector kv, ALGEB s) 

#    void MapleToComplexSingle(MKernelVector kv, ALGEB s, COMPLEXF32 *c) 

#    void MapleToComplexDouble(MKernelVector kv, ALGEB s, COMPLEXF64 *c)

#    CXDAG MapleToComplexFloatDAG(MKernelVector kv, ALGEB s)

    FLOAT32 MapleToFloat32(MKernelVector kv, ALGEB s)

    FLOAT64 MapleToFloat64(MKernelVector kv, ALGEB s)

#    INTEGER8 MapleToInteger8(MKernelVector kv, ALGEB s)

#    INTEGER16 MapleToInteger16(MKernelVector kv, ALGEB s)

    INTEGER32 MapleToInteger32(MKernelVector kv, ALGEB s)

    INTEGER64 MapleToInteger64(MKernelVector kv, ALGEB s)

#    mpz_ptr MapleToGMPInteger(MKernelVector kv, ALGEB s)

    M_BOOL MapleToM_BOOL(MKernelVector kv, ALGEB s)

    M_INT MapleToM_INT(MKernelVector kv, ALGEB s)

    void* MapleToPointer(MKernelVector kv, ALGEB s)

    char* MapleToString(MKernelVector kv, ALGEB s)

#    void MapleTohfData(MKernelVector kv, ALGEB s, hfdata *d)
    
#    void DoubleTohfData(MKernelVector kv, double re, double im, hfdata *d)

#    double RealhfData(MKernelVector kv, hfdata d)

    # Determine the number of arguments in a Maple object #
    M_INT MapleNumArgs(MKernelVector kv, ALGEB expr)
    
    # ---------------------------------------------------------------------- #
    #                        Conversion to Maple Objects                     #
    # ---------------------------------------------------------------------- #

    ALGEB ToMapleBoolean(MKernelVector kv, long b)

    ALGEB ToMapleChar(MKernelVector kv, long c)

    ALGEB ToMapleComplex(MKernelVector kv, double re, double im)

    ALGEB ToMapleComplexFloat(MKernelVector kv, ALGEB re, ALGEB im)

#    ALGEB ToMapleExpressionSequence(MKernelVector kv, int nargs, ALGEB ...)

    ALGEB ToMapleInteger(MKernelVector kv, long i) 

    ALGEB ToMapleInteger64(MKernelVector kv, INTEGER64 i) 

#    ALGEB GMPIntegerToMaple(MKernelVector kv, mpz_ptr g)

    ALGEB ToMapleFloat(MKernelVector kv, double f) 

#    ALGEB ToMapleFunction(MKernelVector kv, ALGEB fn, int nargs, ...)
 
    ALGEB ToMapleFunc(MKernelVector kv, ALGEB fn, ALGEB expseq)

    ALGEB ToMapleName(MKernelVector kv, char* n, M_BOOL is_global) 

    ALGEB ToMapleNULL(void*) 

    ALGEB ToMapleNULLPointer(void*) 

    ALGEB ToMaplePointer(MKernelVector kv, void* v, M_INT type)

    ALGEB ToMapleRelation(MKernelVector kv, char* rel, ALGEB lhs, ALGEB rhs)

    ALGEB ToMapleString(MKernelVector kv, char* s) 

    ALGEB ToMapleUneval(MKernelVector kv, ALGEB s) 

#    ALGEB ToMaplehfData(MKernelVector kv, hfdata *d) 

    # ---------------------------------------------------------------------- #
    #                Foreign Object (MaplePointer) Management                #
    # ---------------------------------------------------------------------- #

    # query the user-supplied pointer type marker #
    M_INT MaplePointerType(MKernelVector kv, ALGEB a)

    # set the pointer type marker #
    void MaplePointerSetType(MKernelVector kv, ALGEB a, M_INT type)

    # Set the function to be called during a gc mark sweep.
    #   MapleGcMark can then be called on all Maple objects contained
    #   in the foreign data-structure so they won't be collected. 
    #
    void MaplePointerSetMarkFunction(MKernelVector kv, ALGEB a, void markfn(ALGEB a))

    # Set a function to call when a Pointer object is about to be
    #   garbage collected.
    #
    void MaplePointerSetDisposeFunction(MKernelVector kv, ALGEB a, void disposefn(ALGEB a))

    # set the function to be called in order to convert a Pointer object
    #   into a printable Maple object during printing 
    void MaplePointerSetPrintFunction(MKernelVector kv, ALGEB a, ALGEB printfn(ALGEB a))


    # ---------------------------------------------------------------------- #
    #                 Evaluate a Maple Procedure or statement                #
    # ---------------------------------------------------------------------- #

    ALGEB EvalMapleProc(MKernelVector kv, ALGEB fn, int nargs, ...)

    ALGEB EvalMapleProcedure(MKernelVector kv, ALGEB fn, ALGEB args)

    ALGEB EvalMapleStatement(MKernelVector kv, char* statement)

    ALGEB MapleEval(MKernelVector kv, ALGEB s)

    # returns the value assigned to the given name 's' #
    ALGEB MapleNameValue(MKernelVector kv, ALGEB s)
    
    # ---------------------------------------------------------------------- #
    #                   Expression Sequence Manipulation                     #
    # ---------------------------------------------------------------------- #

    ALGEB NewMapleExpressionSequence(MKernelVector kv, int nargs)

    void MapleExpseqAssign(MKernelVector kv, ALGEB expseq, M_INT i, ALGEB val)

    ALGEB MapleExpseqSelect(MKernelVector kv, ALGEB expseq, M_INT i)
    

    # ---------------------------------------------------------------------- #
    #                          Data Queries                                  #
    # ---------------------------------------------------------------------- #

    M_BOOL IsMapleAssignedName(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleComplexNumeric(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleNumeric(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleInteger(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleInteger8(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleInteger16(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleInteger32(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleInteger64(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleList(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleExpressionSequence(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleName(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleNULL(MKernelVector kv, ALGEB s)

    M_BOOL IsMaplePointer(MKernelVector kv, ALGEB s)

    M_BOOL IsMaplePointerNULL(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleProcedure(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleRTable(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleSet(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleStop(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleString(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleTable(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleUnassignedName(MKernelVector kv, ALGEB s)

    M_BOOL IsMapleUnnamedZero(MKernelVector kv, ALGEB s)
    
    
    # ---------------------------------------------------------------------- #
    #        Evaluate a Maple Procedure or DAG using hardware floats         #
    # ---------------------------------------------------------------------- #

    double MapleEvalhf(MKernelVector kv, ALGEB s)

    # first argument here is args[1] #
    double EvalhfMapleProc(MKernelVector kv, ALGEB fn, int nargs, double *args)
    
    # first argument here is args[1] #
    #hfdata EvalhfDataProc(MKernelVector kv, ALGEB fn, int nargs, hfdata *args)
