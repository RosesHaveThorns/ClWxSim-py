import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
from matplotlib.colors import DivergingNorm

import numpy as np

# Pages
from ClWxSim.ui.SimControlPage import SimControlPage

LARGE_FONT= ("Verdana", 12)

class SimDataPage(tk.Frame):

    quiver_scale = 500.

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller

        # Create Parts:
            # Heading
        label = tk.Label(self, text="Data", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

            # Prepare for graph
        plt.ion()
        self.fig, self.axar = plt.subplots(1,1)

        self.wld_ref = None

            # Refresh Button
        refresh_btn = ttk.Button(self, text="Refresh Graphs", command=self.refresh)
        refresh_btn.pack()

    def onFirstShow(self):
        # Create graph widget
        self.wld_ref = self.cont.frames[SimControlPage].wld

        self.createGraph()

        canvas = FigureCanvasTkAgg(self.fig, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def createGraph(self):
        # Setup graph
        self.axar.set_title('Pressure (mbar) and Wind Map')

        self.axar.xaxis.set_ticks([])
        self.axar.yaxis.set_ticks([])
        #self.axar.set_aspect('equal')

        # Contour
        X, Y = np.mgrid[0:self.wld_ref.wld_grid_size + 2, 0:self.wld_ref.wld_grid_size + 2]
        X[0:self.wld_ref.wld_grid_size + 2] = X[0:self.wld_ref.wld_grid_size + 2] + 0.5
        Y[0:self.wld_ref.wld_grid_size + 2] = Y[0:self.wld_ref.wld_grid_size + 2] + 0.5
        self.graph_contour = self.axar.contour(X, Y, self.wld_ref.air_pressure, 8, colors='black', alpha=0.5)
        plt.clabel(self.graph_contour, inline=True, fontsize=8)

        # Background Img
        self.graph_img = self.axar.imshow(np.transpose(self.wld_ref.air_pressure), cmap='coolwarm', alpha=0.5, origin='lower', norm=DivergingNorm(self.wld_ref.starting_pressure))
        plt.colorbar(self.graph_img, ax=self.axar)
        self.graph_img.set_clim([self.wld_ref.air_pressure.min(), self.wld_ref.air_pressure.max()])

        # Update quiver (remove zero vals and scale down)
        data_u = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))
        data_v = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))

        data_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.air_vel_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_scale
        data_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.air_vel_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_scale

        for i in range(self.wld_ref.grid_size):
            for j in range(self.wld_ref.grid_size):
                if data_u[i, j] == 0:
                    data_u[i, j] = 0.0000000001 * self.quiver_scale

                if data_v[i, j] == 0:
                    data_v[i, j] = 0.0000000001 * self.quiver_scale

        self.graph_arrows = self.axar.quiver(X, Y, data_u, data_v, scale=5, scale_units='inches', alpha=0.5)


# Commands
    def refresh(self):
        # Replace old contour with updated contour
        for tp in self.graph_contour.collections:
            tp.remove()

        X, Y = np.mgrid[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size]
        X[0:self.wld_ref.grid_size] = X[0:self.wld_ref.grid_size] + 0.5
        Y[0:self.wld_ref.grid_size] = Y[0:self.wld_ref.grid_size] + 0.5
        self.graph_contour = self.axar.contour(X, Y, self.wld_ref.air_pressure, 8, colors='black', alpha=0.5)

        # Update img
        self.graph_img.set_array(np.transpose(self.wld_ref.air_pressure))
        self.graph_img.set_clim([self.wld_ref.air_pressure.min(), self.wld_ref.air_pressure.max()])

        # Update quiver (remove zero vals and scale down)
        data_u = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))
        data_v = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))

        data_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.air_vel_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_scale
        data_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.air_vel_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_scale

        for i in range(self.wld_ref.grid_size):
            for j in range(self.wld_ref.grid_size):
                if data_u[i, j] == 0:
                    data_u[i, j] = 0.0000000001 * self.quiver_scale

                if data_v[i, j] == 0:
                    data_v[i, j] = 0.0000000001 * self.quiver_scale

        self.graph_arrows.set_UVC(data_u, data_v)
