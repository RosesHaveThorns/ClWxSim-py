import tkinter as tk
from tkinter import ttk

import numpy as np

import ClWxSim.sim.fluid_solver as solver

# Pages
from ClWxSim.ui.SimControlPage import SimControlPage

LARGE_FONT= ("Verdana", 12)

class SimTestsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller

        self.wld_ref = None

        # Create Parts:
            # Heading
        label = tk.Label(self, text="Debug Commands", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

            # Heading
        label = tk.Label(self, text="Add Source:", font=("Verdana", 8))
        label.pack(pady=10,padx=10)

            # Add Source Options Frame
        add_source_frame = tk.Frame(self)

                # Source Option Entries
        self.source_field_names = "Value", "Centre X", "Centre Y", "Radius"
        self.source_fields = []

        for i in range(len(self.source_field_names)):
            lab = tk.Label(add_source_frame, width=25, text=self.source_field_names[i], anchor='w')
            ent = tk.Entry(add_source_frame)
            lab.grid(column=0, row=i, sticky='w')
            ent.grid(column=1, row=i)
            self.source_fields.append(ent)

        self.source_fields[0].insert(0, "0")
        self.source_fields[1].insert(0, "0")
        self.source_fields[2].insert(0, "0")
        self.source_fields[3].insert(0, "0")

        add_source_frame.pack(padx=5, pady=10)

            # Add Source Buttons Frame
        add_source_btns_frame = tk.Frame(self)

                # Add Pressure Button
        add_p_btn = ttk.Button(add_source_btns_frame, text="Add Pressure", command=self.add_pressure_cmd)
        add_p_btn.grid(row=0, column=0)

                # Add Wind U Vector Button
        add_wu_btn = ttk.Button(add_source_btns_frame, text="Add Wind U Vector", command=self.add_wind_u_cmd)
        add_wu_btn.grid(row=0, column=1)

                # Add Wind V Vector Button
        add_wv_btn = ttk.Button(add_source_btns_frame, text="Add Wind V Vector", command=self.add_wind_v_cmd)
        add_wv_btn.grid(row=0, column=2)

        add_source_btns_frame.pack(padx=5, pady=10)

            # Heading
        label = tk.Label(self, text="Get Cell Data:", font=("Verdana", 8))
        label.pack(pady=10,padx=10)

            # Add Cell Data Entries Frame
        cell_data_entries_frame = tk.Frame(self)

                # Cell Data Entries
        self.cell_data_field_names = "Cell X", "Cell Y"
        self.cell_data_fields = []

        for i in range(len(self.cell_data_field_names)):
            lab = tk.Label(cell_data_entries_frame, width=25, text=self.cell_data_field_names[i], anchor='w')
            ent = tk.Entry(cell_data_entries_frame)
            lab.grid(column=0, row=i, sticky='w')
            ent.grid(column=1, row=i)
            self.cell_data_fields.append(ent)

        self.cell_data_fields[0].insert(0, "0")
        self.cell_data_fields[1].insert(0, "0")

        cell_data_entries_frame.pack(padx=5, pady=10)

            # Add Cell Data View Frame
        cell_data_frame = tk.Frame(self)

                # Show cell data
        self.p_data_label = tk.Label(cell_data_frame, text="Pressure: Null")
        self.p_data_label.grid(row=0, column=0)

        self.u_data_label = tk.Label(cell_data_frame, text="Wind U: Null")
        self.u_data_label.grid(row=0, column=1)

        self.v_data_label = tk.Label(cell_data_frame, text="Wind V: Null")
        self.v_data_label.grid(row=0, column=2)

                # Create get cell data button
        get_data_btn = ttk.Button(cell_data_frame, text="View Cell Data", command=self.view_cell_data)
        get_data_btn.grid(row=0, column=3)

        cell_data_frame.pack(padx=5, pady=10)

            # Add Presets Frame
        presets_frame = tk.Frame(self)

                # Heading
        self.p_data_label = tk.Label(presets_frame, text="Presets:")
        self.p_data_label.grid(row=0, column=1)

                # Preset Buttons
        preset_A_btn = ttk.Button(presets_frame, text="Add Preset A", command=self.preset_A)
        preset_A_btn.grid(row=1, column=0)

        preset_B_btn = ttk.Button(presets_frame, text="Add Preset B", command=self.preset_B)
        preset_B_btn.grid(row=1, column=1)

        preset_C_btn = ttk.Button(presets_frame, text="Add Preset C", command=self.preset_C)
        preset_C_btn.grid(row=1, column=2)

        presets_frame.pack(padx=5, pady=10)

    def onFirstShow(self):
        # Create world reference
        self.wld_ref = self.cont.frames[SimControlPage].wld

    def add_to_wld(self, arr, val, cx, cy, r):
        # Calculate source array
        src = np.zeros((self.wld_ref.grid_size, self.wld_ref.grid_size))

        x = np.arange(0, self.wld_ref.grid_size)
        y = np.arange(0, self.wld_ref.grid_size)

        mask = (x[np.newaxis,:] - cx) ** 2 + (y[:,np.newaxis] - cy) ** 2 < r ** 2
        src[mask] = val

        # Add source array to pressure
        solver.add_source(self.wld_ref.wld_grid_size, arr, src, self.wld_ref.dt)

# Commands
    def preset_A(self):
        # Add high p center in northern hemisphere, low p center in southern hemisphere
        self.add_to_wld(self.wld_ref.air_pressure, 5., 50, 25, 5)
        self.add_to_wld(self.wld_ref.air_pressure, -5., 50, 75, 5)

    def preset_B(self):
        # Add a high and a low p center to each hemisphere
        self.add_to_wld(self.wld_ref.air_pressure, 5., 25, 25, 5)
        self.add_to_wld(self.wld_ref.air_pressure, -5., 25, 75, 5)
        self.add_to_wld(self.wld_ref.air_pressure, -5., 75, 25, 5)
        self.add_to_wld(self.wld_ref.air_pressure, 5., 75, 75, 5)

    def preset_C(self):
        # Add a u and v wind hotspot to each hemisphere
        self.add_to_wld(self.wld_ref.air_vel_u, 0.002, 25, 25, 5)
        self.add_to_wld(self.wld_ref.air_vel_u, 0.002, 25, 75, 5)
        self.add_to_wld(self.wld_ref.air_vel_v, 0.002, 75, 25, 5)
        self.add_to_wld(self.wld_ref.air_vel_v, 0.002, 75, 75, 5)

    def view_cell_data(self):
        x = int(self.cell_data_fields[1].get())
        y = int(self.cell_data_fields[0].get())

        self.p_data_label.config(text=self.wld_ref.air_pressure[x, y])
        self.u_data_label.config(text=self.wld_ref.air_vel_u[x, y])
        self.v_data_label.config(text=self.wld_ref.air_vel_v[x, y])

    def add_pressure_cmd(self):
        # Get entry vals
        val = float(self.source_fields[0].get())
        cx = int(self.source_fields[1].get())
        cy = int(self.source_fields[2].get())
        r = int(self.source_fields[3].get())

        self.add_to_wld(self.wld_ref.air_pressure, val, cx, cy, r)

    def add_wind_u_cmd(self):
        # Get entry vals
        val = float(self.source_fields[0].get())
        cx = int(self.source_fields[1].get())
        cy = int(self.source_fields[2].get())
        r = int(self.source_fields[3].get())

        self.add_to_wld(self.wld_ref.air_vel_u, val, cx, cy, r)

    def add_wind_v_cmd(self):
        # Get entry vals
        val = float(self.source_fields[0].get())
        cx = int(self.source_fields[1].get())
        cy = int(self.source_fields[2].get())
        r = int(self.source_fields[3].get())

        self.add_to_wld(self.wld_ref.air_vel_v, val, cx, cy, r)
