from scipy.integrate import quad

def pdf_to_cdf(pdf):
    """
    Takes a probability density function pdf(x)
    and returns a function representing the CDF.
    """

    # The CDF at a point x is the integral of the PDF from -infinity to x.
    def cdf(x):
        # quad returns a tuple (result, error), where result is the value of the integral
        # and error is an estimate of the absolute error in the result.
        # We only care about the result, so we ignore the error.
        # quad(function, a, b) computes the integral of the function from a to b.
        # floats are how computers represent real numbers
        # the decimal point floats depending on the exponent
        # if we wrote quad(pdf(x),...,...) instead,
        # it would try to evaluate pdf(x) immediately, which is not what we want.
        result, _ = quad(pdf, -float("inf"), x)
        return result
        # alternatively could write return quad(pdf, -float("inf"), x)[0] to get the result directly

    return cdf

import math

def normal_pdf(x):
    return (1 / math.sqrt(2 * math.pi)) * math.exp(-x**2 / 2)

# now python has created a function that behaves like
# def normal_cdf(x):
# return quad(normal_pdf, -float("inf"), x)[0]
normal_cdf = pdf_to_cdf(normal_pdf)

print(normal_cdf(0))    # ≈ 0.5
print(normal_cdf(1))    # ≈ 0.8413
print(normal_cdf(-1))   # ≈ 0.1587