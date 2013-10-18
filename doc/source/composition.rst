Composability
=============

Toolz functions interoperate because they consume and produce only a small
set of common, core data structures.  Each `toolz` function consumes iterables,
dictionaries, and functions and produces iterables, dictionaries, and
functions.  This standardized interface enables us to compose several general
purpose functions to solve custom problems.

Standard interfaces enable us to use many tools together, even if those tools
were not designed with each other in mind.  We call this "using together"
composition.


Standard Interface
------------------

This is best explained by a two examples; the automobile industry and LEGOs.

Automobile pieces are not composable because they do not adhere to a standard
interface.  You can't connect a Porsche engine to the body of a Volkswagen
Beetle but include the safety features of your favorite luxury car.  As a
result when something breaks you need to find a specialist who understands
exactly your collection of components and, depending on the popularity of your
model, replacement parts may be hard to find.  While the customization provides
a number of efficiencies important for automobiles, it limits the ability of
downstream tinkerers.  This ability for future developers to tinker is
paramount in good software design.

Contrast this with LEGO toys.  With LEGOs you *can* connect a rocket engine and
skis to a rowboat.  This is a perfectly natural thing to do because every piece
adheres to a simple interface - those simple and regular 8mm circular bumps.
This freedom to connect pieces at will lets children unleash their imagination
in such varied ways (like going arctic shark hunting with a rocket-ski-boat).

The abstractions in programming make it far more like LEGO than like building
cars.  This breaks down a little when we start to be constrained by performance
or memory issues but this affects only a very small fraction of applications.
Most of the time we have the freedom to operate in the LEGO model if we choose
to give up customization and embrace simple core standards.

This principle of standard interfaces is what separates XML (customizable) from JSON (standardized.)
