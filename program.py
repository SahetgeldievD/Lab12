import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Slider

class ZBufferAlgorithm:
    def __init__(self, objects):
        self.objects = objects

    def z_buffer_render(self, ax, angle, scale):
        ax.cla()
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_zlim(-10, 10)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.view_init(elev=angle, azim=angle)
        ax.set_box_aspect([1, 1, 1])

        for obj in self.objects:
            obj.render(ax, scale)

    def move_object(self, obj_idx, dx, dy, dz):
        obj = self.objects[obj_idx]
        obj.move(dx, dy, dz)

class Prism:
    def __init__(self, base_center, height):
        self.base_center = np.array(base_center)
        self.height = height

    def render(self, ax, scale):
        base = self.base_center
        height = self.height
        base_vertices = [
            base + [-scale, -scale, 0],
            base + [scale, -scale, 0],
            base + [scale, scale, 0],
            base + [-scale, scale, 0]
        ]
        top_vertices = [
            v + [0, 0, height] for v in base_vertices
        ]
        vertices = np.vstack([base_vertices, top_vertices])

        faces = [
            [base_vertices[0], base_vertices[1], top_vertices[1], top_vertices[0]],
            [base_vertices[1], base_vertices[2], top_vertices[2], top_vertices[1]],
            [base_vertices[2], base_vertices[3], top_vertices[3], top_vertices[2]],
            [base_vertices[3], base_vertices[0], top_vertices[0], top_vertices[3]],
            [base_vertices[0], base_vertices[1], base_vertices[2], base_vertices[3]],
            [top_vertices[0], top_vertices[1], top_vertices[2], top_vertices[3]]
        ]

        ax.add_collection3d(Poly3DCollection(faces, facecolors='orange', linewidths=1, edgecolors='r', alpha=0.6))
     
class Cuboid:
    def __init__(self, center, dimensions):
        self.center = np.array(center)
        self.dimensions = np.array(dimensions)

    def render(self, ax, scale):
        width, depth, height = self.dimensions

        center = self.center

        vertices = [
            center + [ width / 2,  depth / 2,  height / 2],
            center + [-width / 2,  depth / 2,  height / 2],
            center + [-width / 2, -depth / 2,  height / 2],
            center + [ width / 2, -depth / 2,  height / 2],
            center + [ width / 2,  depth / 2, -height / 2],
            center + [-width / 2,  depth / 2, -height / 2],
            center + [-width / 2, -depth / 2, -height / 2],
            center + [ width / 2, -depth / 2, -height / 2]
        ]

        faces = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],
            [vertices[4], vertices[5], vertices[6], vertices[7]],
            [vertices[0], vertices[1], vertices[5], vertices[4]],
            [vertices[1], vertices[2], vertices[6], vertices[5]],
            [vertices[2], vertices[3], vertices[7], vertices[6]],
            [vertices[3], vertices[0], vertices[4], vertices[7]]
        ]

        ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=0.6))


class Sphere:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def render(self, ax, scale):
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = self.center[0] + self.radius * np.outer(np.cos(u), np.sin(v))
        y = self.center[1] + self.radius * np.outer(np.sin(u), np.sin(v))
        z = self.center[2] + self.radius * np.outer(np.ones(np.size(u)), np.cos(v))

        ax.plot_surface(x, y, z, color='green', alpha=0.6)

        u_edge = np.linspace(0, 2 * np.pi, 100)
        v_edge = np.linspace(0, np.pi, 50)
        x_edge = self.center[0] + self.radius * np.outer(np.cos(u_edge), np.sin(v_edge))
        y_edge = self.center[1] + self.radius * np.outer(np.sin(u_edge), np.sin(v_edge))
        z_edge = self.center[2] + self.radius * np.outer(np.ones(np.size(u_edge)), np.cos(v_edge))

        ax.plot_wireframe(x_edge, y_edge, z_edge, color='r', linewidth=0.5)

    def move(self, dx, dy, dz):
        self.center = (self.center[0] + dx, self.center[1] + dy, self.center[2] + dz)

if __name__ == "__main__":
    prism = Prism([0, 0, 0], 5)
    cuboid = Cuboid([2, 2, 2], [2, 2, 2])
    sphere = Sphere([4, -3, 3], 1)
    
    objects = [prism, cuboid, sphere]
    
    zbuffer = ZBufferAlgorithm(objects)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    angle = 30
    scale = 3
    
    zbuffer.z_buffer_render(ax, angle, scale)
    
    def update(val):
        angle = slider_angle.val
        scale = slider_scale.val
        zbuffer.z_buffer_render(ax, angle, scale)
        fig.canvas.draw_idle()

    slider_angle = Slider(plt.axes([0.25, 0.01, 0.65, 0.03]), 'Angle', 0, 360, valinit=angle)
    slider_scale = Slider(plt.axes([0.25, 0.06, 0.65, 0.03]), 'Scale', 0.5, 5, valinit=scale)
    
    slider_angle.on_changed(update)
    slider_scale.on_changed(update)
    
    plt.show()
