import tkinter as tk
from tkinter import ttk

from ClWxSim.utils.logging import Logger

# Pages
from ClWxSim.ui.SimControlPage import SimControlPage
from ClWxSim.ui.SimDataPage import SimDataPage
from ClWxSim.ui.SimTestsPage import SimTestsPage

LARGE_FONT= ("Verdana", 12)

class ClWxSimGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        # Initial Config
        tk.Tk.__init__(self, *args, **kwargs)

        self.wm_title("ClWxSim")

        self.logger = Logger(log_ID="GUI")

        self.fig_ref = None

        # Main container
        main_container = tk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        #main_container.grid_rowconfigure(1, weight=1)

        # Add bottom info bar
        self.info_ribbon_frame = tk.Frame(main_container, relief="sunken", borderwidth=1)
        self.info_ribbon_frame.grid(row=1, column=0, sticky="nsew")

        self.info_ribbon_frame.grid_columnconfigure(0, weight=1)
        self.info_ribbon_frame.grid_columnconfigure(1, weight=1)
        self.info_ribbon_frame.grid_columnconfigure(2, weight=1)
        self.info_ribbon_frame.grid_rowconfigure(0, weight=1)

        self.info_ribbon_tick = tk.Label(self.info_ribbon_frame, text="Current Tick: Null", anchor=tk.W)
        self.info_ribbon_tick.grid(row=0, column=0)

        self.info_ribbon_wld = tk.Label(self.info_ribbon_frame, text="Current World: Null", anchor=tk.W)
        self.info_ribbon_wld.grid(row=0, column=1)

        self.info_ribbon_status = tk.Label(self.info_ribbon_frame, text="No Sim Controller", fg="red", anchor=tk.W)
        self.info_ribbon_status.grid(row=0, column=2)

        # Frames setup
        page_container = tk.Frame(main_container)
        page_container.grid(row=0, column=0, sticky="nsew")
        page_container.grid_rowconfigure(0, weight=1)
        page_container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (SimDataPage, SimControlPage, SimTestsPage):
            frame = F(page_container, self)

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
        viewMenu.add_command(label="Data Page", command=self.onViewData)
        viewMenu.add_command(label="Control Page", command=self.onViewControl)
        viewMenu.add_command(label="Debug Page", command=self.onViewDebug)
        viewMenu.add_command(label="Refresh Graphs", command=self.frames[SimDataPage].refresh)

                    # Sim dropdown
        simMenu = tk.Menu(menubar)
        simMenu.add_command(label="Prepare Sim", command=self.frames[SimControlPage].setup_sim)
        simMenu.add_command(label="Start Sim", command=self.frames[SimControlPage].start_sim)
        simMenu.add_command(label="Next Tick", command=self.frames[SimControlPage].next_tick)
        simMenu.add_command(label="Pause/Resume Sim", command=self.frames[SimControlPage].pause_resume_sim)

                    # Add dropdowns to menu bar
        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label="View", menu=viewMenu)
        menubar.add_cascade(label="Sim", menu=simMenu)

        # Intercept close window
        self.protocol('WM_DELETE_WINDOW', self.onExit)

        # Prepare for and show first frame
        self.frames[SimTestsPage].onFirstShow()
        self.frames[SimDataPage].onFirstShow()
        self.frames[SimControlPage].dataPage_ref = self.frames[SimDataPage]
        self.show_frame(SimDataPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Commands
    def onExit(self):
        self.quit()
        self.destroy()

    def onViewControl(self):
        self.show_frame(SimControlPage)

    def onViewDebug(self):
        self.show_frame(SimTestsPage)

    def onViewData(self):
        self.show_frame(SimDataPage)
