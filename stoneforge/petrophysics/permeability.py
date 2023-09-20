import numpy as np
import numpy.typing as npt


def permeability_sdr(a1: float , phit: npt.ArrayLike, m1: float, 
                     t2_lm: npt.ArrayLike, n1: float) -> np.ndarray:
    
    """Estimate the permeability from the SDR (Schlumberger-Doll-Research).

    Parameters
    ----------
    a1 : array_like
        Tortuosity coefficient.
    phit : array_like
        Total Porosity.
    m1: array_like
        Cementation coefficient.
    t2_lm: array_like
        Logarithmic spectrum of T2 cutoff (in ms).
    n1: array_like
        Saturation exponent.
    
    Returns
    -------
    k_sdr
        Estimated permeability by SDR(Schlumberger-Doll-Research)."""
    
    k_sdr = (a1 * (phit ** m1) * (t2_lm) ** n1) * 1000
    
    
    return k_sdr


def permeability_tim(phit: npt.ArrayLike, a2: npt.ArrayLike , m2: npt.ArrayLike, 
                    bvm : npt.ArrayLike, bvi: npt.ArrayLike, n2: npt.ArrayLike) -> np.ndarray:
    
    """Estimate the permeability from Timur-Coates.

    Parameters
    ----------
    phit : array_like
        Total Porosity.
    c2 : array_like
        Tortuosity coefficient.
    m2: array_like
        Cementation coefficient.
    bvm: array_like (It can be called Free Fluid)
        Bulk Volume Movable.
    bvi: array_like
        Bulk Volume Irreducible
    n2: array_like
        Saturation exponent.
    
    Returns
    -------
    k_tim
        Estimated permeability by Timur-Coates."""

    k_tim = (phit / a2) ** m2 * (bvm / bvi) ** n2
    

    return k_tim

_permeability_methods = {
    "sdr": permeability_sdr,
    "tim": permeability_tim
}


def permeability(method: str = "linear", **kwargs) -> np.ndarray:
    """Compute the shale volume from gamma ray log.

    This is a façade for the methods:
        - sdr
        - tim
    

    Parameters
    ----------
    a1 & a2 : array_like
        Tortuosity coefficient.
    phit : array_like
        Total Porosity.
    m1 & m2: array_like
        Cementation coefficient.
    t2_lm: array_like
        Logarithmic spectrum of T2 cutoff (in ms).
    n1 & n2: array_like
        Saturation exponent.
    bvm: array_like (It can be called Free Fluid)
        Bulk Volume Movable.
    bvi: array_like
        Bulk Volume Irreducible
        Name of the method to be used.  Should be one of
            - 'sdr'
            - 'tim'
        If not given, default method is 'linear'

    Returns
    -------
    permeability_sdr : array_like
        Estimated permeability by SDR(Schlumberger-Doll-Research);
    permeability_tim : array_like
        Estimated permeability by Timur-Coates.
    """
    options = {}

    required = []
    if method == "sdr":
        required = ["a1","phit","m1","t2_lm","n1"]
    elif method == "tim":
        required = ["phit","a2","m2","bvm","bvi","n2"]

    for arg in required:
        if arg not in kwargs:
            msg = f"Missing required argument for method '{method}': '{arg}'"
            raise TypeError(msg)
        options[arg] = kwargs[arg]

    fun = _permeability_methods[method]

    return fun(**options)
