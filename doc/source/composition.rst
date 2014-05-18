Composability
=============

Toolz functions interoperate because they consume and produce only a small
set of common, core data structures.  Each ``toolz`` function consumes
just iterables, dictionaries, and functions and each ``toolz`` function produces
just iterables, dictionaries, and functions.  This standardized interface
enables us to compose several general purpose functions to solve custom
problems.

Standard interfaces enable us to use many tools together, even if those tools
were not designed with each other in mind.  We call this "using together"
composition.


Standard Interface
------------------

This is best explained by two examples; the automobile industry and LEGOs.

Autos
^^^^^

Automobile pieces are not widely composable because they do not adhere to a
standard interface.  You can't connect a Porsche engine to the body of a
Volkswagen Beetle but include the safety features of your favorite luxury car.
As a result when something breaks you need to find a specialist who understands
exactly your collection of components and, depending on the popularity of your
model, replacement parts may be difficult to find.  While the customization
provides a number of efficiencies important for automobiles, it limits the
ability of downstream tinkerers.  This ability for future developers to tinker
is paramount in good software design.

Lego
^^^^

Contrast this with Lego toys.  With Lego you *can* connect a rocket engine and
skis to a rowboat.  This is a perfectly natural thing to do because every piece
adheres to a simple interface - those simple and regular 5mm circular bumps.
This freedom to connect pieces at will lets children unleash their imagination
in such varied ways (like going arctic shark hunting with a rocket-ski-boat).

The abstractions in programming make it far more like Lego than like building
cars.  This breaks down a little when we start to be constrained by performance
or memory issues but this affects only a very small fraction of applications.
Most of the time we have the freedom to operate in the Lego model if we choose
to give up customization and embrace simple core standards.


Other Standard Interfaces
-------------------------

The Toolz project builds off of a standard interface -- this choice is not
unique.  Other standard interfaces exist and provide immeasurable benefit to
their application areas.

The NumPy array serves as a foundational object for numeric and scientific
computing within Python.  The ability of any project to consume and produce
NumPy arrays is largely responsible for the broad success of the
various SciPy projects.  We see similar development today with the Pandas
DataFrame.

The UNIX toolset relies on files and streams of text.

JSON emerged as the standard interface for communication over the web.  The
virtues of standardization become glaringly apparent when we contrast JSON with
its predecessor, XML.  XML was designed to be extensible/customizable, allowing
each application to design its own interface.  This resulted in a sea of
difficult to understand custom data languages that failed to develop a common
analytic and data processing infrastructure.  In contrast JSON is very
restrictive and allows only a fixed set of data structures, namely lists,
dictionaries, numbers, strings.  Fortunately this set is common to most modern
languages and so JSON is extremely widely supported, perhaps falling second
only to CSV.

Standard interfaces permeate physical reality as well.  Examples range
from supra-national currencies to drill bits and electrical circuitry.  In all
cases the interoperation that results becomes a defining and invaluable feature
of each solution.
