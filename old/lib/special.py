#TODO: special initially known functions
"""

AiryAi,                                                                          
AiryAiZeros,                                                                     
AiryBi,                                                                          
AiryBiZeros           - Airy wave functions and their negative real zeros        
AngerJ                - Anger J function                                         
BesselI               - modified Bessel function of the 1st kind                 
BesselJ               - Bessel function of the 1st kind                          
BesselJZeros          - non negative real zeros of Bessel J                      
BesselK               - modified Bessel function of the 2nd kind                 
BesselY               - Bessel function of the 2nd kind                          
BesselYZeros          - positive real zeros of Bessel Y                          
Beta                  - Beta function                                            
ChebyshevT            - Chebyshev function of the 1st kind                       
ChebyshevU            - Chebyshev function of the 2nd kind                       
Chi                   - hyperbolic cosine integral                               
Ci                    - cosine integral                                          
CoulombF              - regular Coulomb wave function                            
CylinderD             - Whittaker's parabolic function                           
CylinderU,                                                                       
CylinderV             - Parabolic cylinder functions                             
Dirac                 - Dirac delta function                                     
Ei                    - exponential integrals                                    
EllipticCE            - complementary complete elliptic integral of the 2nd kind 
EllipticCK            - complementary complete elliptic integral of the 1st kind 
EllipticCPi           - complementary complete elliptic integral of the 3rd kind 
EllipticE             - incomplete or complete elliptic integral of the 2nd kind 
EllipticF             - incomplete elliptic integral of the 1st kind             
EllipticK             - complete elliptic integral of the 1st kind               
EllipticModulus       - Modulus elliptic function                                
EllipticNome          - Nome elliptic function                                   
EllipticPi            - incomplete or complete elliptic integral of the 3rd kind 
FresnelC              - Fresnel cosine integral                                  
Fresnelf              - Fresnel f auxiliary function                             
Fresnelg              - Fresnel g auxiliary function                             
FresnelS              - Fresnel sine integral                                    
GAMMA                 - Gamma and incomplete Gamma functions                     
GaussAGM              - Gauss arithmetic geometric mean                          
GegenbauerC           - Gegenbauer (ultraspherical) function                     
HankelH1,                                                                        
HankelH2              - Hankel functions (Bessel functions of the 3rd kind)      
Heaviside             - Heaviside step function                                  
HermiteH              - Hermite function                                         
HeunB,                                                                           
HeunC,                                                                           
HeunD,                                                                           
HeunG,                                                                           
HeunT                 - Heun functions                                           
HeunBPrime,                                                                      
HeunCPrime,                                                                      
HeunDPrime,                                                                      
HeunGPrime,                                                                      
HeunTPrime            - derivatives of Heun functions                            
InverseJacobiAM       - inverse Jacobi amplitude function                        
InverseJacobiCD,                                                                 
InverseJacobiCN,                                                                 
InverseJacobiCS,                                                                 
InverseJacobiDC,                                                                 
InverseJacobiDN,                                                                 
InverseJacobiDS,                                                                 
InverseJacobiNC,                                                                 
InverseJacobiND,                                                                 
InverseJacobiNS,                                                                 
InverseJacobiSC,                                                                 
InverseJacobiSD,                                                                 
InverseJacobiSN       - inverse Jacobi elliptic functions                        
JacobiP               - Jacobi function                                          
JacobiAM              - Jacobi amplitude function                                
JacobiCD,                                                                        
JacobiCN,                                                                        
JacobiCS,                                                                        
JacobiDC,                                                                        
JacobiDN,                                                                        
JacobiDS,                                                                        
JacobiNC,                                                                        
JacobiND,                                                                        
JacobiNS,                                                                        
JacobiSC,                                                                        
JacobiSD,                                                                        
JacobiSN              - Jacobi elliptic functions                                
JacobiTheta1,                                                                    
JacobiTheta2,                                                                    
JacobiTheta3,                                                                    
JacobiTheta4          - Jacobi theta functions                                   
JacobiZeta            - Jacobi Zeta function                                     
KelvinBei,                                                                       
KelvinBer,                                                                       
KelvinHei,                                                                       
KelvinHer,                                                                       
KelvinKei,                                                                       
KelvinKer             - Kelvin functions                                         
KummerM,                                                                         
KummerU               - Kummer functions                                         
LaguerreL             - Laguerre function                                        
LambertW              - Lambert W function                                       
LegendreP             - associated Legendre function of the 1st kind             
LegendreQ             - associated Legendre function of the 2nd kind             
LerchPhi              - Lerch's Phi function                                     
Li                    - logarithmic integral                                     
LommelS1              - Lommel function s                                        
LommelS2              - Lommel function S                                        
MathieuA              - Mathieu characteristic function                          
MathieuB              - Mathieu characteristic function                          
MathieuC              - even general Mathieu function                            
MathieuCPrime         - 1st derivative of MathieuC                               
MathieuCE             - even 2*Pi-periodic Mathieu function                      
MathieuCEPrime        - 1st derivative of MathieuCE                              
MathieuExponent       - Mathieu characteristic exponent                          
MathieuFloquet        - Floquet solution of Mathieu's equation                   
MathieuFloquetPrime   - 1st derivative of MathieuFloquet                         
MathieuS              - odd general Mathieu function                             
MathieuSPrime         - 1st derivative of MathieuS                               
MathieuSE             - odd 2*Pi-periodic Mathieu function                       
MathieuSEPrime        - 1st derivative of MathieuSE                              
MeijerG               - MeijerG function                                         
ModifiedMeijerG       - a modified MeijerG function                              
Psi                   - polygamma function                                       
RiemannTheta          - Riemann theta function                                   
Shi                   - hyperbolic sine integral                                 
Si                    - sine integral                                            
SphericalY            - spherical harmonic function                                                               
Ssi                   - shifted sine integral                                    
StruveH               - Struve function                                          
StruveL               - modified Struve function                                 
WeberE                - Weber E function                                         
WeierstrassP          - Weierstrass P-function                                   
WeierstrassPPrime     - Derivative of Weierstrass P-function                     
WeierstrassSigma      - Weierstrass sigma-function                               
WeierstrassZeta       - Weierstrass zeta-function                                
WhittakerM,                                                                      
WhittakerW            - Whittaker functions                                      
Wrightomega           - Wright omega function                                    
Zeta                  - Riemann and Hurwitz zeta functions  
"""