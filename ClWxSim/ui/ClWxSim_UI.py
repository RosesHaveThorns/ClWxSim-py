import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import ttk

import numpy as np

LARGE_FONT= ("Verdana", 12)

class ClWxSimGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        # Initial Config
        tk.Tk.__init__(self, *args, **kwargs)

        self.wm_title("ClWxSim")
        self.geometry("400x300")

        # Frames setup
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (SimTrackingPage, SimControlPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        # Top Menu Setup
        menubar = tk.Menu(self)
        self.config(menu=menubar)

                    # File dropdown
        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Exit", command=self.onExit)

                    # View dropdown
        viewMenu = tk.Menu(menubar)
        viewMenu.add_command(label="Refresh Graphs", command=self.frames[SimTrackingPage].refresh)

                    # Sim dropdown
        simMenu = tk.Menu(menubar)
        simMenu.add_command(label="Start Sim", command=self.onNewSim)

                    # Add dropdowns to menu bar
        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label="View", menu=viewMenu)
        menubar.add_cascade(label="Sim", menu=simMenu)

        # Intercept close window
        self.protocol('WM_DELETE_WINDOW', self.onExit)

        # Show first frame
        self.show_frame(SimTrackingPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Commands
    def onExit(self):
        self.quit()
        self.destroy()

    def onNewSim(self):
        self.show_frame(SimControlPage)


class SimTrackingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller

        # Create Parts:
            # Heading
        label = tk.Label(self, text="Data", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

            # Load graph
        plt.ion()
        self.fig, self.axar = plt.subplots(1,1)

###---         LINK TO SIM SCRIPTS             ---###
        self.wld_ref = self.cont.frames[SimControlPage].wld
        #self.cont.frames[SimControlPage].sim
        self.N = self.cont.frames[SimControlPage].sim.world
        self.PRESSURE_ARRAY = np.ones((self.N+2,self.N+2))
        self.WIND_U = np.ones((self.N+2,self.N+2))
        self.WIND_V = np.ones((self.N+2,self.N+2))

        self.PRESSURE_ARRAY[20:30, 5:20] = 10
        self.WIND_U[2:10, 10:20] = 10
        self.WIND_V[5:40, 15:50] = 10
###---         REPLACE ABOVE VARIABLES         ---###

        self.createGraph()

        canvas = FigureCanvasTkAgg(self.fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

            # Refresh Button
        refresh_btn = ttk.Button(self, text="Refresh Graphs", command=self.refresh)
        refresh_btn.pack()

    def createGraph(self):
        self.axar.set_title('Pressure (mbar) and Wind Map')

        self.axar.xaxis.set_ticks([])
        self.axar.yaxis.set_ticks([])
        self.axar.set_aspect('equal')

        X, Y = np.mgrid[0:self.wld_ref.wld_grid_size + 2, 0:self.wld_ref.wld_grid_size + 2]
        X[0:self.wld_ref.wld_grid_size + 2] = X[0:self.wld_ref.wld_grid_size + 2] + 0.5
        Y[0:self.wld_ref.wld_grid_size + 2] = Y[0:self.wld_ref.wld_grid_size + 2] + 0.5
        self.graph_contour = self.axar.contour(X, Y, self.wld_ref.air_pressure, 3, colors='black')
        plt.clabel(self.graph_contour, inline=True, fontsize=8)

        self.graph_img = self.axar.imshow(self.wld_ref.air_pressure, cmap='hot', alpha=0.5, origin='lower')
        plt.colorbar(self.graph_img, ax=self.axar)
        self.graph_img.set_clim([self.wld_ref.air_pressure.min(), self.wld_ref.air_pressure.max()])

        self.graph_arrows = self.axar.quiver(X, Y, self.wld_ref.air_vel_u, self.wld_ref.air_vel_v)

        plt.pause(0.00001)

# Commands
    def refresh(self):
        # Replace old contour with updated contour
        for tp in self.graph_contour.collections:
            tp.remove()

        X, Y = np.mgrid[0:self.wld_ref.wld_grid_size + 2, 0:self.wld_ref.wld_grid_size + 2]
        X[0:self.wld_ref.wld_grid_size + 2] = X[0:self.wld_ref.wld_grid_size + 2] + 0.5
        Y[0:self.wld_ref.wld_grid_size + 2] = Y[0:self.wld_ref.wld_grid_size + 2] + 0.5
        self.graph_contour = self.axar.contour(X, Y, self.wld_ref.air_pressure, 3, colors='black')

        # Update img
        self.graph_img.set_array(self.wld_ref.air_pressure)
        self.graph_img.set_clim([self.wld_ref.air_pressure.min(), self.wld_ref.air_pressure.max()])

        # Update quiver
        self.graph_arrows.set_UVC(self.wld_ref.air_vel_u, self.wld_ref.air_vel_v)


class SimControlPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller

        label = tk.Label(self, text="Simulation Control", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        setting_field_names = "World Name", "Array Size (Width and Height)", "Standard Pressure", "Angular Velocity"

        self.wld = World(world_name="default-world", wld_grid_size=100)

    def sim_tick_loop(self):
        pass

# Commands
    def update_wld_settings(self):
        for entry in self.setting_fields:
            field = entry[0]
            text  = entry[1].get()
            # set wld values
