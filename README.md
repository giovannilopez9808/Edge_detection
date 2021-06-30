# Edge detection

Herramienta desarrollada para analizar los bordes de una imagen satelital por medio de diferentes kernels dependiendo la resolucion.

Los kernels disponibles son los siguientes:

- Sobel 3
  $$
  \begin{pmatrix}
    1&  2&  1\\
    0&  0&  0\\
    -1& -2& 1\\
  \end{pmatrix}
  $$
- Scharr 3

  $$
  \begin{pmatrix}
    47& 162& 47\\
    0& 0& 0\\
    -47& -162& -47\\
  \end{pmatrix}
  $$

- Feldman 3
  $$
  \begin{pmatrix}
    3& 10& 3\\
    0& 0& 0\\
    -3& -10& -3\\
  \end{pmatrix}
  $$
- Sobel 5
  $$
  \begin{pmatrix}
  2&2& 4& 2& 2\\
  1& 1&  2&  1& -1 \\
  0& 0&  0&  0& -0\\
  -1&  -1&  -2&  -1& -1\\
  -2& -2& -4& -2& -2\\
  \end{pmatrix}
  $$
- Scharr 5
  $$
  \begin{pmatrix}
    162& 162& 324& 162& 162\\
    47& 47& 162& 47& 47\\
    0& 0& 0& 0& 0\\
    -47& -47& -162& -47& -47\\
    -162& -162& -324& -162& -162\\
  \end{pmatrix}
  $$
- feldman 5

  $$
  \begin{pmatrix}
    10& 10& 20& 10& 10\\
    3& 3& 10& 3& 3\\
    0& 0& 0& 0& 0\\
    -3& -3& -10& -3& -3\\
    -10& -10& -20& -10& -10\\
  \end{pmatrix}
  $$
