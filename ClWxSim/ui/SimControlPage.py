from ClWxSim.data.world import World
from ClWxSim.sim.controller import Controller as SimControl

import tkinter as tk
from tkinter import ttk

LARGE_FONT= ("Verdana", 12)

class SimControlPage(tk.Frame):

    def __init__(self, parent, controller):
         # Inital setup
        tk.Frame.__init__(self, parent)
        self.cont = controller

        self.dataPage_ref = None

        # Create world and sim vars
        self.wld = World(world_name="default-world", wld_grid_size=100)
        self.sim = None

        # Create Parts:
            # Heading
        label = tk.Label(self, text="Simulation Control", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

            # World settings fields [only editable before sim is setup]
        self.setting_field_names = "World Name", "World Size (Width/Height)", "Standard Pressure", "Angular Velocity"
        self.setting_fields = []

        settings_frame = tk.Frame(self)
        for i in range(len(self.setting_field_names)):
            lab = tk.Label(settings_frame, width=25, text=self.setting_field_names[i], anchor='w')
            ent = tk.Entry(settings_frame)
            lab.grid(column=0, row=i, sticky='w')
            ent.grid(column=1, row=i)
            self.setting_fields.append(ent)

        self.setting_fields[0].insert(0, self.wld.world_name)
        self.setting_fields[1].insert(0, self.wld.wld_grid_size)
        self.setting_fields[2].insert(0, self.wld.starting_pressure)
        self.setting_fields[3].insert(0, self.wld.angular_vel)

        settings_frame.pack()

            # Update World Settings buttons [only selectable before sim is setup]
        self.update_btn = ttk.Button(self, text="Set World Settings", command=self.update_wld_settings)
        self.update_btn.pack(pady=5)

            # Frame for 'sim is not running' buttons
        prep_sim_frame = tk.Frame(self)

                # Prepare sim button [only selectable if sim is not setup]
        self.setup_btn = ttk.Button(prep_sim_frame, text="Prepare Sim Controller", command=self.setup_sim)
        self.setup_btn.grid(row=0, column=0, padx=5)

                # Clear sim button [only selectable is sim is paused and setup]
        self.clear_sim_btn = ttk.Button(prep_sim_frame, text="Delete Sim Controller", command=self.clear_sim, state='disabled')
        self.clear_sim_btn.grid(row=0, column=1,padx=5)

        prep_sim_frame.pack(padx=5, pady=10)

            # Frame for sim control buttons
        ctrl_sim_frame = tk.Frame(self)

                # Start sim button [only selectable if sim is not running and is setup]
        self.start_sim_btn = ttk.Button(ctrl_sim_frame, text="Start Sim", command=self.start_sim, state='disabled')
        self.start_sim_btn.grid(row=0, column=0,padx=5)

                # Pause/Resume sim button [only selectable if sim is setup, change text based on if sim is running]
        self.pau_res_sim_btn = ttk.Button(ctrl_sim_frame, text="Pause Sim", command=self.pause_resume_sim, state='disabled')
        self.pau_res_sim_btn.grid(row=0, column=1,padx=5)

                # Clear world data button [only selectable is sim is paused]
        self.clear_world_btn = ttk.Button(ctrl_sim_frame, text="Clear World Data", command=self.clear_wld, state='disabled')
        self.clear_world_btn.grid(row=0, column=2,padx=5)

        ctrl_sim_frame.pack(padx=5, pady=10)

            # Frame for img saving controls
        save_imgs_frame = tk.Frame(self)

                # Save ticks tickbox
        self.store_imgs = tk.IntVar()
        store_imgs_chkbox = ttk.Checkbutton(save_imgs_frame, text="Store ticks:", variable=self.store_imgs)
        store_imgs_chkbox.grid(row=0, column=0)

                # Text boxes
        self.img_setting_field_names = "Save an iamge every X ticks:", "File Location (relative to scripts):"
        self.img_setting_fields = []

        for i in range(len(self.img_setting_field_names)):
            lab = tk.Label(save_imgs_frame, width=25, text=self.img_setting_field_names[i], anchor='w')
            ent = tk.Entry(save_imgs_frame)
            lab.grid(column=0, row=i+1, sticky='w')
            ent.grid(column=1, row=i+1)
            self.img_setting_fields.append(ent)

        self.img_setting_fields[0].insert(0, "1")
        self.img_setting_fields[1].insert(0, "image_out/")

        save_imgs_frame.pack(padx=5, pady=10)

        # Update info ribbon
        self.cont.info_ribbon_wld.config(text="Current World: {}".format(self.wld.world_name))

    def sim_tick_loop(self):
        if self.sim != None:
            if self.sim.running:
            # Run tick calculations
                try:
                    self.sim.tick()

                    # Store img
                    try:
                        store_on_tick = int(self.img_setting_fields[0].get())
                        if self.store_imgs.get() and self.sim.tickNum % store_on_tick == 0:
                            self.save_fig_img()
                    except Exception as e:
                        print("Error saveing image, was the given time between ticks an integer and the image address correct? [{}]".format(e))

                    # Update info ribbon
                    self.cont.info_ribbon_tick.config(text="Current Tick: {}".format(self.sim.tickNum))

                except Exception as e:
                    print("Error during tick {}: [{}]".format(self.sim.tickNum, e))
                    self.sim.running = False

                # check running again, possible error above
                if self.sim.running:
                    self.cont.after(10, self.sim_tick_loop)

    def save_fig_img(self):
        self.dataPage_ref.refresh()
        self.cont.fig_ref.savefig(self.img_setting_fields[1].get() + "{}_{}.png".format(self.wld.world_name, self.sim.tickNum))

# Commands
    def clear_sim(self):
        # Clear sim reference
        self.sim = None

        # Update info ribbon
        self.cont.info_ribbon_status.config(text="No Sim Controller", fg="red")
        self.cont.info_ribbon_tick.config(text="Current Tick: Null")

        # Unlock setup sim button, lock clear sim button
        self.clear_sim_btn.config(state='disabled')
        self.setup_btn.config(state='normal')

        # Unlock world settings fields
        for entry in self.setting_fields:
            entry.config(state='normal')
        self.update_btn.config(state='normal')

        # Lock sim control buttons
        self.start_sim_btn.config(state='disabled')
        self.clear_world_btn.config(state='disabled')
        self.pau_res_sim_btn.config(state='disabled')

    def setup_sim(self):
        if self.sim == None:
            # Create a new sim class controller
            self.sim = SimControl(self.wld)

            # Update info ribbon
            self.cont.info_ribbon_status.config(text="Sim Ready", fg="yellow")

            # Lock setup sim button, unlock clear sim button
            self.clear_sim_btn.config(state='normal')
            self.setup_btn.config(state='disabled')

            # Lock world settings fields
            for entry in self.setting_fields:
                entry.config(state='disabled')
            self.update_btn.config(state='disabled')

            # Unlock sim control buttons
            self.start_sim_btn.config(state='normal')
            self.clear_world_btn.config(state='normal')

    def start_sim(self):
        if self.sim != None:
            # Update info ribbon
            self.cont.info_ribbon_status.config(text="Sim Running", fg="green")

            # Lock/Unlock buttons
            self.clear_sim_btn.config(state='disabled')

            self.start_sim_btn.config(state='disabled')
            self.clear_world_btn.config(state='disabled')
            self.pau_res_sim_btn.config(state='normal')

            self.pau_res_sim_btn.config(text="Pause Sim")

            # Start repeating sim tick loop after 10ms
            self.sim.running = True

            if self.store_imgs:
                loop_every = 50
            else:
                loop_every = 20
            self.cont.after(loop_every, self.sim_tick_loop)

    def next_tick(self):
        if self.sim != None:
            self.cont.info_ribbon_status.config(text="Sim Running", fg="green")
            self.sim.running = True
            self.sim.tick()
            self.cont.info_ribbon_tick.config(text="Current Tick: {}".format(self.sim.tickNum))
            self.sim.running = False
            self.cont.info_ribbon_status.config(text="Sim Paused", fg="yellow")

    def pause_resume_sim(self):
        # Check if sim.running, if true pause, if false resume. Update button text
        if self.sim != None:
            if self.sim.running:
                # Stop running sim
                self.sim.running = False

                # Update info ribbon
                self.cont.info_ribbon_status.config(text="Sim Paused", fg="yellow")

                # Lock/Unlock buttons
                self.pau_res_sim_btn.config(text="Resume Sim")
                self.clear_world_btn.config(state='normal')
                self.clear_sim_btn.config(state='normal')

            elif not self.sim.running:
                # Lock/Unlock buttons
                self.pau_res_sim_btn.config(text="Pause Sim")
                self.clear_world_btn.config(state='disabled')
                self.clear_sim_btn.config(state='disabled')

                # Update info ribbon
                self.cont.info_ribbon_status.config(text="Sim Running", fg="green")

                # Start running sim
                self.sim.running = True

                if self.store_imgs:
                    loop_every = 50
                else:
                    loop_every = 20
                self.cont.after(loop_every, self.sim_tick_loop)

    def clear_wld(self):
        self.sim.tickNum = 0
        self.cont.info_ribbon_tick.config(text="Current Tick: {}".format(self.sim.tickNum))
        self.wld.clear_data()

    def update_wld_settings(self):
        if self.sim == None:    # Only update world settings if the sim is not prepared
            # Reset background colours
            self.setting_fields[0].configure({"background": "white"})
            self.setting_fields[1].configure({"background": "white"})
            self.setting_fields[2].configure({"background": "white"})
            self.setting_fields[3].configure({"background": "white"})

            # Store old value in case of error
            old_world_name = self.wld.world_name
            old_wld_grid_size = self.wld.wld_grid_size
            old_grid_size = self.wld.grid_size
            old_starting_pressure = self.wld.starting_pressure
            old_angular_vel = self.wld.angular_vel

            # Set world values
            failed = False

                # World Name
            text = self.setting_fields[0].get()
            if text != "":
                self.wld.world_name = text
            else:
                self.cont.logger.log("Error setting world Name: [No text entered]")
                failed = True
                self.setting_fields[0].configure({"background": "red"})

                # Array Grid Size
            text = self.setting_fields[1].get()
            try:
                if int(text) > 0:
                    self.wld.wld_grid_size = int(text)
                    self.wld.grid_size = int(text)+2
                else:
                    self.cont.logger.log("Error setting world Array Size: [Value less than 1]")
                    failed = True
                    self.setting_fields[1].configure({"background": "red"})

            except Exception as e:
                self.cont.logger.log("Error setting world Array Size: [{}]".format(e))
                failed = True
                self.setting_fields[1].configure({"background": "red"})

                # Starting Pressure
            text = self.setting_fields[2].get()
            try:
                if float(text) >= 0:
                    self.wld.starting_pressure = float(text)
                else:
                    self.cont.logger.log("Error setting world Starting Pressure: [Value less than 0]")
                    failed = True
                    self.setting_fields[2].configure({"background": "red"})

            except Exception as e:
                self.cont.logger.log("Error setting world Starting Pressure: [{}]".format(e))
                failed = True
                self.setting_fields[2].configure({"background": "red"})

                # Angular Velocity
            text = self.setting_fields[3].get()
            try:
                if float(text) > 0:
                    self.wld.angular_vel = float(text)
                else:
                    self.cont.logger.log("Error setting world Angular Velocity: [Value less than 1]")
                    failed = True
                    self.setting_fields[3].configure({"background": "red"})

            except Exception as e:
                self.cont.logger.log("Error setting world Angular Velocity: [{}]".format(e))
                failed = True
                self.setting_fields[3].configure({"background": "red"})

            # If failed, reset all values, if not, reset the world
            if failed:
                self.wld.world_name = old_world_name
                self.wld.wld_grid_size = old_wld_grid_size
                self.wld.grid_size = old_grid_size
                self.wld.starting_pressure = old_starting_pressure
                self.wld.angular_vel = old_angular_vel
            else:
                self.wld.clear_data()

            # Update info ribbon
            self.cont.info_ribbon_wld.config(text="Current World: {}".format(self.wld.world_name))
