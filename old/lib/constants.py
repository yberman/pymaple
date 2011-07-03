from maple.core import maple as _maple

Pi = _maple.Pi
"""
The following names are known, either as global or environment variables under user control or as names of constants known to certain functions. 
Catalan    Catalan's constant = sum((-1)^i/(2*i+1)^2,i=0..infinity)      
           evalf(Catalan) is approximately 0.915965594...                
constants  See constants ( default is the sequence:                      
           false, gamma, infinity, true, Catalan, FAIL, Pi )             
Digits     number of digits carried in floats (default is 10).           
           Digits is an environment variable.                            
FAIL       used by boolean evaluation as unknown truth for               
           3-valued logic.                                               
false      the value false (false) in the context of Boolean evaluation. 
gamma      Euler's constant = limit(sum(1/i,i=1..n) - ln(n),             
           n=infinity). evalf(gamma) is approximately 0.5772156649...    
gamma(n)   a series of constants such that gamma(n)  =                   
           limit(sum(ln(k)^n/k, k=1..m) - ln(m)^(n+1)/(n+1),             
           m=infinity). gamma(0) = gamma, Euler's constant.              
I          complex number such that I^2 = -1 (i).                        
           Internally, I is represented as Complex(1).                   
infinity   name for infinity used by some library functions (infinity)   
integrate  initially assigned the function name int                      
lasterror  See lasterror                                                 
libname    path name which is the root of the standard Maple library     
`mod`      initially assigned the function name modp; for symmetric      
           representation, assign `mod` := mods; (mod is an operator).   
           Mod is an environment variable.                               
NULL       initialized to the null expression sequence                   
Order      truncation order for series (default is 6); see also Order.   
           Order is an environment variable.                             
Pi         math constant pi (pi); use Pi for calculations,               
           evalf(Pi) is approximately 3.14159265...                      
printlevel See printlevel (default is 1).  Printlevel is an              
           environment variable.                                         
true       the value true (true) in the context of Boolean evaluation    
undefined  name for undefined used by some library functions        
"""