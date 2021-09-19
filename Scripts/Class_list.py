import moviepy.video.io.ImageSequenceClip as Movie_maker
from scipy import fftpack, signal
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from functions import *
import numpy as np
import cv2
import os


class edge_detection_algorithm:
    def __init__(self, parameters):
        """
        Algoritmo para la deteccion de bordes a través de las imagenes satelitales proporcionadas por Google Earth
        #### Inputs
        paramters -> diccionario que debe contener los siguientes elementos:
        +  path graphics ->  direccion donde seran guardadas las graficas y la animación.
        + kernel name -> nombre del kernel que se usara para la deteccion de bordes.
        + path data" -> direccion donde se encuentran las imagenes satelitales.
        """
        self.images_names = listdir_sorted(parameters["path data"])
        self.kernel = egde_kernels(parameters["kernel name"])
        self.parameters = parameters

    def run(self):
        """
        Ejecucion del algoritmo de deteccion de bordes con los parametros dados.
        """
        print("Deteccion de bordes iniciando")
        # Inicializacion del entorno gráfico
        plots = plot()
        for image in self.images_names:
            """
            Inicializacion dde la lista de imagenes, al final la lista contendra dos imagenes, la original y la procesada con los bordes marcados.
            """
            self.final_images = []
            # Lectura de la imagen de Google Earth
            images = obtain_images(path=self.parameters["path data"],
                                   name=image)
            # Ingreso de la imagen
            self.final_images.append(images.img_original)
            # Convolucion con el kernel seleccionado y la imagen con alto contraste
            self.convolve_image(img=images.img)
            # Ingreso de la imagen procesada
            self.final_images.append(self.img_edge)
            # Grafica de la imagen original y la procesada
            plots.plot_image(path=self.parameters["path graphics"],
                             name=image,
                             images=self.final_images,)

    def convolve_image(self, img=cv2.imread("")):
        """
        Convolucion de la imagen en la direccion XY utilizando el kernel seleccionado

        #### Input
        img -> imagen de Google Earth 

        #### Return
        img_edge -> Imagen procesada para el resaltado de bordes
        """
        img_edge_x = signal.convolve2d(img,
                                       self.kernel.kernel,
                                       boundary='symm',
                                       mode='same')
        img_edge_y = signal.convolve2d(img,
                                       self.kernel.kernel.transpose(),
                                       boundary='symm',
                                       mode='same')
        self.img_edge = np.sqrt(img_edge_x**2+img_edge_y**2)

    def create_animation(self):
        animation = animation_algorithm(path=self.parameters["path graphics"])
        animation.create(delete=False)


class egde_kernels:
    def __init__(self, name=""):
        """
        Selecciona un kernel para el analisis de bordes en una imagen:
        Opciones posibles:
        + sobel_5
        + scharr_5
        + feldman_5
        + sobel_3
        + scharr_3
        + feldman_3
        """
        self.name = name
        self.kernels = {"sobel_5": np.array([[2, 2, 4, 2, 2],
                                             [1,  1,  2,  1, -1],
                                             [0,  0,  0,  0, -0],
                                             [-1,  -1,  -2,  -1, -1],
                                             [-2, -2, -4, -2, -2], ]),
                        "scharr_5":  np.array([[162, 162, 324, 162, 162],
                                               [47, 47, 162, 47, 47],
                                               [0, 0, 0, 0, 0],
                                               [-47, -47, -162, -47, -47],
                                               [-162, -162, -324, -162, -162], ]),
                        "feldman_5": np.array([[10, 10, 20, 10, 10],
                                               [3, 3, 10, 3, 3],
                                               [0, 0, 0, 0, 0],
                                               [-3, -3, -10, -3, -3],
                                               [-10, -10, -20, -10, -10], ]),
                        "sobel_3": np.array([[1,  2,  1],
                                             [0,  0,  0],
                                             [-1, -2, 1], ]),
                        "scharr_3": np.array([[47, 162, 47],
                                              [0, 0, 0],
                                              [-47, -162, -47], ]),
                        "feldman_3": np.array([[3, 10, 3],
                                               [0, 0, 0],
                                               [-3, -10, -3], ]),
                        }
        self.select_kernel()

    def select_kernel(self):
        """
        Selecciona el kernel en base al nombre introducido
        """
        self.kernel = self.kernels[self.name]


class obtain_images:
    def __init__(self, path="", name=""):
        """
        Lectura de la imagen proporcionada por Google Earth
        #### inputs
        + path -> direccion donde se encuentra la imagen
        + name -> nombre de la imagen
        """
        self.path = path
        self.name = name
        # Lectura de la imagen
        self.read_image()

    def read_image(self):
        """
        Ejecucion de la lectura de la imagen, a esta se le aplicara un filtro de alto contraste
        """
        # Direccion con le nombre de la imagen
        path_image = "{}{}".format(self.path,
                                   self.name)
        # Lectura de la imagen
        img_original = cv2.imread(path_image,
                                  1)
        # Filtro de alto contraste a la imagen
        self.img = self.high_contrast_image(img_original)[:, :, 0]
        # Lectura de la imagen con el formato RGB
        self.img_original = Image.open(path_image).convert("RGB")

    def high_contrast_image(self, img=cv2.imread("")):
        """
        Filtro de alto contraste a la imagen
        """
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8, 8))
        # convert from BGR to LAB color space
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        # split on 3 different channels
        l, a, b = cv2.split(lab)
        # apply CLAHE to the L-channel
        l2 = clahe.apply(l)
        # merge channels
        lab = cv2.merge((l2, a, b))
        # convert from LAB to BGR
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        return img


class plot:
    def __init__(self):
        """
        Ploteo de la imagen original y el procesamiento de bordes en una sola imagen
        """
        # Inicializacion del entorno grafico
        self.init_figure_plot()

    def init_figure_plot(self):
        """
        Inicializacion del entorno grafico, si no se realiza aqui puede causar problemas de meoria al estar abriendo un entorno gráfico por cada imagen.
        """
        self.fig = plt.figure(figsize=(10, 5))

    def plot_image(self, path="", name="", images=[]):
        """
        Ploteo de la imagen original y la analizada
        #### inputs
        + path -> direccion donde se guardara la grafica
        + name -> nombre de la grafica a guardar
        + images -> lista con las dos imagenes a plotear en ella
        """
        # Crea la carpeta donde se guardaran las imagenes
        self.create_movie_folder(path=path)
        path = path+"Movie/"
        # Cambio el nombre de jpg a png
        name = jpg2png(name)
        # Crea el entorno de cada imagen
        axs = [self.fig.add_subplot(1, 2, i+1) for i in range(2)]
        # Grafica de las imageness en sus entornos correspondientes
        for ax, image in zip(axs, images):
            self.individual_plots(ax, image)
        # Obtiene la fecha del nombre de la grafica
        date = name.replace(".png", "")
        self.fig.text(0.415,
                      0.85,
                      date,
                      fontsize=20)
        plt.subplots_adjust(left=0,
                            bottom=0,
                            right=1,
                            top=0.91,
                            wspace=0,
                            hspace=0)
        # Guardado de la grafica
        plt.savefig("{}{}".format(path,
                                  name),
                    bbox_inches="tight",
                    pad_inches=0)
        # Limpieza del entorno gráfico
        plt.clf()

    def create_movie_folder(self, path=""):
        """
        Crea la carpeta donde se guardaran las graficas de cada dia
        """
        mkdir(path=path,
              name="Movie")

    def individual_plots(self, ax, image=cv2.imread("")):
        """
        Grafica cada imagen en su entorno grafico correspondiente
        """
        ax.axis("off")
        ax.imshow(image,
                  cmap="gray")


class animation_algorithm:
    def __init__(self, path="", outfile="animation"):
        """
        Encargado de realizar la animacion del analisis
        ### inputs
        + path -> direccion donde se guardara la animacion
        + outfile -> nombre que recibira el archivo
        """
        self.outfile = outfile
        self.path = path

    def create(self, delete=True, fps=3):
        """
        Ejecuta la creacion de la animacion
        """
        # Direccion donde se encuentran las imagenes individuales
        movie_path = self.path+"Movie/"
        # Nombre de las imagenes que se usaran en la animacion
        filenames = listdir_sorted(movie_path)
        # Union del nombre de cada imagen y su direccion
        filenames = [movie_path+filename for filename in filenames]
        # Creacion de la secuencia
        movie = Movie_maker.ImageSequenceClip(filenames,
                                              fps=fps,)
        # Creacion del archivo
        movie.write_videofile("{}{}.mp4".format(self.path,
                                                self.outfile),
                              logger=None)
        print("Creación del video en {}".format(self.path))
        if delete:
            os.system("rm -rf {}".format(movie_path))
