Hexagon grid conversions
========================

Define a tessellating hexagonal grid as a set of hexagons
:math:`\mathcal{H}` which covers the cartesian plane
:math:`\mathbb{R}^2`. Each hexagon :math:`h_{i,j} \in \mathcal{H}` has
an integer address :math:`\{i, j\} \in \mathbb{Z}^2`. The hexagons do
not overlap so the intersection of any two distinct :math:`h` is empty,
and the cartesian space is covered such that any coordinate
:math:`\{x, y\} \in \mathbb{R}^2` belongs to some :math:`h_{i,j}`.

We can therefore define the grid with a function
:math:`f : \mathbb{R}^2 \rightarrow \mathbb{Z}^2` that maps coordinates
in cartesian space to the corresponding hexagon address. This function
is useful in the context of a computer interaction where a user selects
a pixel location on a rendering of the hexagonal grid, and we which to
find the corresponding grid coordinates.

Without loss of generality, assume that the hex grid is “flat topped” as
defined in `1 <https://www.redblobgames.com/grids/hexagons/>`__, and the
hexagonal grid coordinates are “Axial Coordinates” as defined in
`1 <https://www.redblobgames.com/grids/hexagons/>`__.

Hexagon geometry
----------------

We need to determine the shape of each hexagon. Clearly for the obvious
tessellation we need each hexagon to be the same size, however they do
not need to be regular, as any simple scaling of the coordinates could
easily be inverted to get regular hexagons if that was so desired. A
regular hexagon with side 1 has a height of :math:`\sqrt{3}` so it is in
fact more convenient to choose a non-regular geometry.

Define the hexagon shape so that the distances between hexagons are
small whole numbers: a small section of the tessellation is shown below
- the vertical space between adjacent hexagons in the same “column”
(labelled :math:`h`) is 2, and the vertical space relative to the
hexagon in the next column is 1. The horizontal space (:math:`w`) is 1.

.. code:: ipython3

    import numpy as np
    
    def hex_points():
        return np.array([
            [1.25, 1.],
            [0.75, 2.],
            [0.25, 2.],
            [-0.25, 1.],
            [0.25, 0.],
            [0.75, 0.],
            [1.25, 1]
        ])



.. image:: hex_files/hex_4_0.svg


Colouring the hexagons
----------------------

As noted at the start, each hexagon has an address :math:`\{i, j\}`. In
order to better understand our representations of the grid, we will pick
a pseudo-random colour for each hexagon using its address and the
SHA-256 hash function.

.. code:: ipython3

    import hashlib
    
    def color_for_hex(i, j):
        """Calculates a size 3 array of floats that can be used as a color
        
        The input values are put into a byte string and passed to the sha256
        hash function. 
        """
        buffer = np.array([i, j], dtype=np.int32).tobytes()
        hash_data = hashlib.sha256(buffer).digest()
        return np.frombuffer(hash_data, dtype=np.uint8)[:3].astype(float)/255
    
    print(color_for_hex(1, 1))
    # The function is deterministic, and only considers integer values, so this
    # will print the same output
    print(color_for_hex(1.1, 1))
    # Another example
    print(color_for_hex(23, -123))


.. parsed-literal::

    [0.39215686 0.92941176 0.5254902 ]
    [0.39215686 0.92941176 0.5254902 ]
    [0.08235294 0.17254902 0.38431373]


Addressing the rectangular grid
-------------------------------

The addresses for the hexagons have to components :math:`i` and
:math:`j`. The first addresses the column (so increases along the
:math:`x` direction). As we move up a column, the :math:`j` component
increases, but has an offset which ensures that for any given tile, a
move in one of the six available directions always has the same change
in :math:`\{i, j\}` (for example, moving to the tile up and to the right
of any :math:`\{i, j\}`, always moves to address :math:`\{i+1, j+1\}`).

Given the :math:`\{i, j\}` coordinates of a hexagon, we can find the
origin of the hexagon in the cartesian plane. We have established that
the horizontal spacing between hexagons is 1, so the :math:`x`
coordinate is simply :math:`i`.

The vertical spacing is 2, so we expect a factor of :math:`2j` in the
:math:`y` value. To acheive the correct offset, we need to subtract
:math:`i` to move the hexagon down by one for each column.

.. code:: ipython3

    def axial_to_world(i: int, j: int) -> (float, float):
        x = np.float(i)
        y = np.float(2*j - i)
        return x, y

Plotting our hexagon geometry on this grid, and using the random colours
to fill them in:



.. image:: hex_files/hex_10_0.svg


Finding the hexagon address for a cartesian coordinate
------------------------------------------------------

The function ``axial_to_world`` finds the ‘origin’ coordinates of a
hexagon, given its address - we then draw a polygon relative to this to
obtain the hexagons on the above image. The hexagon produced by this
process is effectively the preimage of the hexagon index in the funtion
:math:`f` that we wish to find.

Therefore, we can start forming :math:`f` by inverting the calculation
in ``axial_to_world``. Note that the mapping is not continuous since the
axial coordinates have to be integers, whereas the “world” coordinates
are real-valued.

.. code:: ipython3

    def axial_to_world_inverse(x: float, y: float) -> (int, int):
        i = np.int(np.floor(x))
        j = np.int(np.floor((y+i)/2))
        return i, j
    
    i, j = (23, 33)
    x, y = axial_to_world(i, j)
    print(f'axial_to_world{i, j} -> {x, y}')
    x, y = (23.4, 43.1)
    i, j = axial_to_world_inverse(x, y)
    print(f'axial_to_world_inverse{x, y} -> {i, j}')


.. parsed-literal::

    axial_to_world(23, 33) -> (23.0, 43.0)
    axial_to_world_inverse(23.4, 43.1) -> (23, 33)


.. code:: ipython3

    def world_to_axial(x: float, y: float) -> (int, int):
        i = np.int(np.floor(x))
        j = np.int(np.floor((y+i)/2))
        
        origin_x, origin_y = axial_to_world(i, j)
        local_x = x - origin_x
        local_y = (y - origin_y)/2
        
        if local_x + local_y < 0.25:
            return i-1, j-1
        elif local_x + (1-local_y) < 0.25:
            return i-1, j
        elif (1-local_x) + (1-local_y) < 0.25:
            return i+1, j+1
        elif (1-local_x) + local_y < 0.25:
            return i+1, j
        else:
            return i, j
            




.. image:: hex_files/hex_14_0.svg

