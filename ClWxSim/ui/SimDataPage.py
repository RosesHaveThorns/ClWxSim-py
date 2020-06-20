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

    quiver_w_scale = 100.
    quiver_c_scale = 100.
    quiver_g_scale = 100.

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

                # Show Coriolis Tickbox
        cori_style = ttk.Style()
        cori_style.configure("tur.TCheckbutton", foreground="turquoise")

        self.show_coriolis = tk.IntVar()
        show_coriolis_chkbox = ttk.Checkbutton(self, text="View Coriolis Effect", variable=self.show_coriolis)
        show_coriolis_chkbox.configure(style="tur.TCheckbutton")
        show_coriolis_chkbox.pack()

                # Show Wind Tickbox
        self.show_wind = tk.IntVar()
        show_wind_chkbox = ttk.Checkbutton(self, text="View Wind Speed", variable=self.show_wind)
        show_wind_chkbox.pack()

                # Show PGF Tickbox
        pgf_style = ttk.Style()
        pgf_style.configure("red.TCheckbutton", foreground="red")

        self.show_pgf = tk.IntVar()
        show_pgf_chkbox = ttk.Checkbutton(self, text="View Pressure Gradient Force", variable=self.show_pgf)
        show_pgf_chkbox.configure(style="red.TCheckbutton")
        show_pgf_chkbox.pack()

    def onFirstShow(self):
        # Create graph widget
        self.wld_ref = self.cont.frames[SimControlPage].wld

        self.createGraph()
        plt.close(self.fig)
        self.cont.fig_ref = self.fig

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
        self.graph_contour = self.axar.contour(X, Y, np.transpose(self.wld_ref.air_pressure), 16, colors='black', alpha=0.5)
        plt.clabel(self.graph_contour, inline=True, fontsize=8)

        # Background Img
        self.graph_img = self.axar.imshow(self.wld_ref.air_pressure, cmap='coolwarm', alpha=0.5, origin='lower', norm=DivergingNorm(self.wld_ref.starting_pressure))
        plt.colorbar(self.graph_img, ax=self.axar)
        self.graph_img.set_clim([self.wld_ref.air_pressure.min(), self.wld_ref.air_pressure.max()])

        # Wind quiver (remove zero vals and scale down)
        data_u = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))
        data_v = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))

        data_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.air_vel_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_w_scale
        data_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.air_vel_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_w_scale

        for i in range(self.wld_ref.grid_size):
            for j in range(self.wld_ref.grid_size):
                if data_u[i, j] == 0:
                    data_u[i, j] = 0.0000000000000000000000000000001 * self.quiver_w_scale

                if data_v[i, j] == 0:
                    data_v[i, j] = 0.0000000000000000000000000000001 * self.quiver_w_scale

        self.graph_w_arrows = self.axar.quiver(X, Y, np.transpose(data_u), np.transpose(data_v), scale=5, scale_units='inches', alpha=0.5)

        # Coriolis quiver (remove zero vals and scale down)
        data_u = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))
        data_v = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))

        data_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.dbg_coriolis_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_c_scale
        data_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.dbg_coriolis_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_c_scale

        for i in range(self.wld_ref.grid_size):
            for j in range(self.wld_ref.grid_size):
                if data_u[i, j] == 0:
                    data_u[i, j] = 0.0000000000000000000000000000001 * self.quiver_c_scale

                if data_v[i, j] == 0:
                    data_v[i, j] = 0.0000000000000000000000000000001 * self.quiver_c_scale

        self.graph_c_arrows = self.axar.quiver(X, Y, np.transpose(data_u), np.transpose(data_v), color="c", scale=5, scale_units='inches', alpha=0.5)

        # PGF quiver (remove zero vals and scale down)
        data_u = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))
        data_v = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))

        data_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.air_pressure_grad_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_g_scale
        data_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.air_pressure_grad_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_g_scale

        for i in range(self.wld_ref.grid_size):
            for j in range(self.wld_ref.grid_size):
                if data_u[i, j] == 0:
                    data_u[i, j] = 0.0000000000000000000000000000001 * self.quiver_g_scale

                if data_v[i, j] == 0:
                    data_v[i, j] = 0.0000000000000000000000000000001 * self.quiver_g_scale

        self.graph_g_arrows = self.axar.quiver(X, Y, np.transpose(data_u), np.transpose(data_v), color="r", scale=5, scale_units='inches', alpha=0.5)


# Commands
    def refresh(self):
        # Replace old contour with updated contour
        for tp in self.graph_contour.collections:
            tp.remove()

        X, Y = np.mgrid[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size]
        X[0:self.wld_ref.grid_size] = X[0:self.wld_ref.grid_size] + 0.5
        Y[0:self.wld_ref.grid_size] = Y[0:self.wld_ref.grid_size] + 0.5
        self.graph_contour = self.axar.contour(X, Y, np.transpose(self.wld_ref.air_pressure), 16, colors='black', alpha=0.5)

        # Update img
        self.graph_img.set_array(self.wld_ref.air_pressure)
        self.graph_img.set_clim([self.wld_ref.air_pressure.min(), self.wld_ref.air_pressure.max()])

        # Update wind quiver (remove zero vals and scale down)
        data_u = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))
        data_v = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))

        data_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.air_vel_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_w_scale
        data_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.air_vel_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_w_scale

        for i in range(self.wld_ref.grid_size):
            for j in range(self.wld_ref.grid_size):
                if data_u[i, j] == 0:
                    data_u[i, j] = 0.0000000000000000000000000000001 * self.quiver_w_scale

                if data_v[i, j] == 0:
                    data_v[i, j] = 0.0000000000000000000000000000001 * self.quiver_w_scale

        if self.show_wind.get():
            self.graph_w_arrows.set_visible(True)
        else:
            self.graph_w_arrows.set_visible(False)

        self.graph_w_arrows.set_UVC(np.transpose(data_u), np.transpose(data_v))

        # Update coriolis quiver (remove zero vals and scale down)
        data_u = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))
        data_v = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))

        data_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.dbg_coriolis_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_c_scale
        data_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.dbg_coriolis_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_c_scale

        for i in range(self.wld_ref.grid_size):
            for j in range(self.wld_ref.grid_size):
                if data_u[i, j] == 0:
                    data_u[i, j] = 0.0000000000000000000000000000001 * self.quiver_c_scale

                if data_v[i, j] == 0:
                    data_v[i, j] = 0.0000000000000000000000000000001 * self.quiver_c_scale

        if self.show_coriolis.get():
            self.graph_c_arrows.set_visible(True)
        else:
            self.graph_c_arrows.set_visible(False)

        self.graph_c_arrows.set_UVC(np.transpose(data_u), np.transpose(data_v))

        # Update PGF quiver (remove zero vals and scale down)
        data_u = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))
        data_v = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))

        data_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.air_pressure_grad_u[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_c_scale
        data_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] = self.wld_ref.air_pressure_grad_v[0:self.wld_ref.grid_size, 0:self.wld_ref.grid_size] * self.quiver_c_scale

        for i in range(self.wld_ref.grid_size):
            for j in range(self.wld_ref.grid_size):
                if data_u[i, j] == 0:
                    data_u[i, j] = 0.0000000000000000000000000000001 * self.quiver_g_scale

                if data_v[i, j] == 0:
                    data_v[i, j] = 0.0000000000000000000000000000001 * self.quiver_g_scale

        if self.show_pgf.get():
            self.graph_g_arrows.set_visible(True)
        else:
            self.graph_g_arrows.set_visible(False)

        self.graph_g_arrows.set_UVC(np.transpose(data_u), np.transpose(data_v))
