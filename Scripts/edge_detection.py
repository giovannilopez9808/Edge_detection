from Class_list import *
parameters = {
    "path graphics": "../Graphics/",
    "kernel name": "feldman_5",
    "path data": "../Data/",
}
edge_detection = edge_detection_algorithm(parameters=parameters)
edge_detection.run()
edge_detection.create_animation()
