"""
FDMNES tkinter GUI windows
"""

import sys, os
import matplotlib.pyplot as plt # Plotting
if sys.version_info[0] < 3:
    import Tkinter as tk
    import tkFileDialog as filedialog
else:
    import tkinter as tk
    from tkinter import filedialog
from ..classes_fdmnes import Fdmnes, FdmnesAnalysis
from .basic_widgets import (TF, BF, SF, LF, HF, TTF, TTFG, TTBG,
                            bkg, ety, btn, opt, btn2,
                            btn_active, opt_active, txtcol,
                            btn_txt, ety_txt, opt_txt)


class RunFDMNESgui:
    """
    Create FDMNES indata files and run them
    """

    def __init__(self, xtl):
        """Initialise"""
        self.xtl = xtl
        self.fdm = Fdmnes(xtl)
        # Create Tk inter instance
        self.root = tk.Tk()
        self.root.wm_title('FDMNES %s' % xtl.name)
        # self.root.minsize(width=640, height=480)
        self.root.maxsize(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.root.tk_setPalette(
            background=bkg,
            foreground=txtcol,
            activeBackground=opt_active,
            activeForeground=txtcol)
        default_width = 60
        default_height = 30

        frame = tk.Frame(self.root)
        frame.pack(side=tk.LEFT, anchor=tk.N, fill=tk.BOTH, expand=tk.YES)

        # Available x-ray edges
        self.xr_edges, self.xr_energies = self.xtl.Properties.xray_edges()
        # Polarisations
        poltypes = [u'\u03c3-\u03c3', u'\u03c3-\u03c0', u'\u03c0-\u03c3', u'\u03c0-\u03c0']

        # Variables
        if hasattr(xtl, 'P'):
            # Superstructure with parent
            pass
        else:
            # Not superstructure
            pass
        self.calculation_name = tk.StringVar(frame, self.fdm.output_name)
        self.calculation_path = tk.StringVar(frame, self.fdm.generate_input_path())
        self.calc_comment = tk.StringVar(frame, self.fdm.comment)
        self.calc_range = tk.StringVar(frame, self.fdm.range)
        self.calc_radius = tk.DoubleVar(frame, self.fdm.radius)
        self.calc_edge = tk.StringVar(frame, self.xr_edges[0])
        self.calc_green = tk.BooleanVar(frame, self.fdm.green)
        self.calc_scf = tk.BooleanVar(frame, self.fdm.scf)
        self.calc_quad = tk.BooleanVar(frame, self.fdm.quadrupole)
        self.calc_aziref = tk.StringVar(frame, str(self.fdm.azi_ref).strip('[]'))
        self.calc_reflist = tk.StringVar(frame, str(self.fdm.hkl_reflections))
        self.calc_addref = tk.StringVar(frame, '1, 0, 0')
        self.calc_addpol = tk.StringVar(frame,  poltypes[1])

        # ---Line 0---
        line = tk.Frame(frame, bg=TTBG)
        line.pack(expand=tk.YES, fill=tk.X)
        var = tk.Label(line, text='FDMNES Code, by Y. Joly and O. Bunau', font=TTF, fg=TTFG, bg=TTBG)
        var.pack(fill=tk.X, expand=tk.YES)

        # ---Line 0---
        line = tk.Frame(frame)
        line.pack(expand=tk.YES, fill=tk.X)
        var = tk.Label(line, text='FDMNES Path: %s' % self.fdm.exe_path, font=SF)
        var.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        # ---Line 1---
        line = tk.Frame(frame)
        line.pack(expand=tk.YES, fill=tk.X)
        var = tk.Label(line, text='Path:', font=SF)
        var.pack(side=tk.LEFT)
        var = tk.Entry(line, textvariable=self.calculation_path, font=HF, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
        var = tk.Button(line, text='Select', font=BF, bg=btn, activebackground=btn_active,
                        command=self.fun_loadpath)
        var.pack(side=tk.LEFT, padx=5)

        # ---Line 2---
        line = tk.Frame(frame)
        line.pack(expand=tk.YES, fill=tk.X)
        var = tk.Label(line, text='Calculation Name:', font=SF)
        var.pack(side=tk.LEFT)
        var = tk.Entry(line, textvariable=self.calculation_name, font=HF, width=10, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        var = tk.Label(line, text='Comment:', font=SF)
        var.pack(side=tk.LEFT, padx=5)
        var = tk.Entry(line, textvariable=self.calc_comment, font=HF, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X, padx=5)

        # ---Line 3---
        line = tk.Frame(frame)
        line.pack(fill=tk.BOTH, expand=tk.YES)

        # LLLLeftLLL
        left = tk.Frame(line)
        left.pack(side=tk.LEFT)

        # |||Parameters box|||
        box = tk.LabelFrame(left, text='Calculation Parameters', font=SF)
        box.pack(padx=4, pady=6)

        # ---Line B1---
        bline = tk.Frame(box)
        bline.pack(side=tk.TOP, fill=tk.X, pady=5)
        var = tk.Label(bline, text='Range (eV)', font=SF)
        var.pack(side=tk.LEFT, padx=5)
        var = tk.Entry(bline, textvariable=self.calc_range, font=HF, width=15, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT, padx=5)

        # ---Line B2---
        bline = tk.Frame(box)
        bline.pack(side=tk.TOP, fill=tk.X, pady=5)
        var = tk.Label(bline, text='Radius (A)', font=SF)
        var.pack(side=tk.LEFT, padx=5)
        var = tk.Entry(bline, textvariable=self.calc_radius, font=HF, width=5, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT, padx=5)

        # ---Line B3---
        bline = tk.Frame(box)
        bline.pack(side=tk.TOP, fill=tk.X, pady=5)
        var = tk.Label(bline, text='Edge:', font=SF)
        var.pack(side=tk.LEFT, padx=5)
        var = tk.OptionMenu(bline, self.calc_edge, *self.xr_edges)
        var.config(font=SF, width=5, bg=opt, activebackground=opt_active)
        var["menu"].config(bg=opt, bd=0, activebackground=opt_active)
        var.pack(side=tk.LEFT, padx=5)

        # ---Line B4---
        bline = tk.Frame(box)
        bline.pack(side=tk.TOP, fill=tk.X, pady=5)
        var = tk.Checkbutton(bline, text='Muffin-Tin', variable=self.calc_green, font=SF)
        var.pack(side=tk.LEFT, padx=6)
        var = tk.Checkbutton(bline, text='SCF', variable=self.calc_scf, font=SF)
        var.pack(side=tk.LEFT, padx=6)

        # ---Line B5---
        bline = tk.Frame(box)
        bline.pack(side=tk.TOP, fill=tk.X, pady=5)
        var = tk.Checkbutton(bline, text='Quadrupole', variable=self.calc_quad, font=SF)
        var.pack(side=tk.LEFT, padx=6)

        # ---Line B6---
        bline = tk.Frame(box)
        bline.pack(side=tk.TOP, fill=tk.X, pady=5)
        var = tk.Label(bline, text='Azimuthal Reference:', font=SF)
        var.pack(side=tk.LEFT)
        var = tk.Entry(bline, textvariable=self.calc_aziref, font=SF, width=6, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT, expand=tk.YES, padx=6)

        # ---Line B7---
        bline = tk.Frame(box)
        bline.pack(side=tk.TOP, fill=tk.X, pady=5)
        var = tk.Label(bline, text='h,k,l:', font=SF)
        var.pack(side=tk.LEFT)
        var = tk.Entry(bline, textvariable=self.calc_addref, font=SF, width=6, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT, expand=tk.YES, padx=6)
        """
        var = tk.OptionMenu(bline, self.calc_addpol, *poltypes)
        var.config(font=SF, width=5, bg=opt, activebackground=opt_active)
        var["menu"].config(bg=opt, bd=0, activebackground=opt_active)
        var.pack(side=tk.LEFT)
        """
        var = tk.Button(bline, text='Add Ref', font=BF, bg=btn, activebackground=btn_active,
                        command=self.fun_addref)
        var.pack(side=tk.LEFT)

        # ---Line B8---
        bline = tk.Frame(box)
        bline.pack(side=tk.TOP, fill=tk.X, pady=5)
        var = tk.Label(bline, text='Reflections:', font=SF)
        var.pack(side=tk.LEFT)
        var = tk.Label(bline, textvariable=self.calc_reflist, font=SF)
        var.pack(side=tk.LEFT)
        var = tk.Button(bline, text='Clear', font=BF, bg=btn, activebackground=btn_active,
                        command=self.fun_clearref)
        var.pack(side=tk.LEFT)

        # ---Line  B9---
        bline = tk.Frame(box)
        bline.pack(fill=tk.X)
        var = tk.Button(bline, text='Update input text', font=BF, bg=btn, activebackground=btn_active,
                        command=self.fun_update)
        var.pack(side=tk.RIGHT)

        # LLLLine 2LLL
        lline = tk.Frame(left)
        lline.pack()
        var = tk.Button(lline, text='Create Directory + input files', font=BF, bg=btn, activebackground=btn_active,
                        command=self.fun_writefiles)
        var.pack()
        var = tk.Button(lline, text='Write fdm start file', font=BF, bg=btn, activebackground=btn_active,
                        command=self.fun_writefdmfile)
        var.pack()
        var = tk.Button(lline, text='Write Files & Run FDMNES', font=BF, bg=btn2, activebackground=btn_active,
                        command=self.fun_runfdmnes)
        var.pack()
        var = tk.Button(lline, text='Plot Results', font=BF, bg=btn, activebackground=btn_active,
                        command=self.fun_analyse)
        var.pack()

        # |||Text Box|||
        box = tk.LabelFrame(line, text='FDMNES Input File')
        box.pack(side=tk.LEFT, padx=4, fill=tk.BOTH, expand=tk.YES)

        # Scrollbars
        scanx = tk.Scrollbar(box, orient=tk.HORIZONTAL)
        scanx.pack(side=tk.BOTTOM, fill=tk.X)

        scany = tk.Scrollbar(box)
        scany.pack(side=tk.RIGHT, fill=tk.Y)

        # Editable string box
        self.text = tk.Text(box, width=default_width, height=default_height, font=HF, wrap=tk.NONE, bg=ety)
        self.text.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.gentxt()

        self.text.config(xscrollcommand=scanx.set, yscrollcommand=scany.set)
        scanx.config(command=self.text.xview)
        scany.config(command=self.text.yview)

    def update(self):
        """Updates the internal fdm object"""

        filepath, filename = os.path.split(self.calculation_path.get())
        self.fdm.output_path = filepath
        self.fdm.input_name = filename
        self.fdm.output_name = self.calculation_name.get()
        self.fdm.comment = self.calc_comment.get()
        self.fdm.range = self.calc_range.get()
        self.fdm.radius = self.calc_radius.get()
        absedge = self.calc_edge.get()
        self.fdm.absorber, self.fdm.edge = absedge.split()
        self.fdm.green = self.calc_green.get()
        self.fdm.scf = self.calc_scf.get()
        self.fdm.quadrupole = self.calc_quad.get()
        self.fdm.azi_ref = [float(n) for n in self.calc_aziref.get().replace(',', ' ').split()]

    def gentxt(self):
        """Generate input file text"""
        parstr = self.fdm.generate_parameters_string()
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, parstr)

    def write_reflections(self):
        """ Write reflections string"""
        self.calc_reflist.set('%s'%self.fdm.hkl_reflections)

    def fun_loadpath(self, event=None):
        """Select folder"""
        filepath, filename = os.path.split(self.calculation_path.get())
        filepath = filedialog.askdirectory(initialdir=filepath)
        self.fdm.input_name = filename
        self.fdm.output_path = filepath
        self.calculation_path.set(self.fdm.generate_input_path())

    def fun_addref(self, event=None):
        """Add reflection to list"""
        newhkl = [int(n) for n in self.calc_addref.get().replace(',', ' ').split()]
        newpol = self.calc_addpol.get()
        self.fdm.hkl_reflections += [newhkl]
        self.write_reflections()

    def fun_clearref(self, event=None):
        """Clear reflection list"""
        self.fdm.hkl_reflections = []
        self.write_reflections()

    def fun_update(self, event=None):
        """Update values and generate text"""
        self.update()
        self.gentxt()

    def fun_writefiles(self, event=None):
        """Create FDMNES files"""
        self.update()
        text_string = self.text.get(1.0, tk.END)
        self.fdm.create_files(param_string=text_string)

    def fun_writefdmfile(self, event=None):
        """Create FDMNES files"""
        self.update()
        self.fdm.write_fdmfile()

    def fun_runfdmnes(self, event=None):
        """Run FDMNES"""
        self.update()
        text_string = self.text.get(1.0, tk.END)
        self.fdm.create_files(param_string=text_string)
        self.fdm.write_fdmfile()
        self.fdm.run_fdmnes()  # This will take a few mins, output should be printed to the console
        #self.fdm.info()

    def fun_analyse(self, event=None):
        """Start Analysis GUI"""
        self.update()
        AnaFDMNESgui(self.fdm.output_path, self.fdm.output_name)


class AnaFDMNESgui:
    """
    Read files from a completed FDMNES calculation folder
    """

    def __init__(self, output_path=None, output_name='out'):
        """Initialise"""
        # Create Tk inter instance
        self.root = tk.Tk()
        self.root.wm_title('FDMNES %s' % output_path)
        # self.root.minsize(width=640, height=480)
        self.root.maxsize(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.root.tk_setPalette(
            background=bkg,
            foreground=txtcol,
            activeBackground=opt_active,
            activeForeground=txtcol)
        default_width = 60
        default_height = 30

        if output_path is None or not os.path.isfile(os.path.join(output_path, output_name + '.txt')):
            self.fun_loadpath()

        self.fdm = FdmnesAnalysis(output_path, output_name)

        frame = tk.Frame(self.root)
        frame.pack(side=tk.LEFT, anchor=tk.N)

        # ---Line 1---
        line = tk.Frame(frame)
        line.pack(expand=tk.YES, fill=tk.X)
        var = tk.Label(line, text='Calculation Path: %s' % self.fdm.output_path, font=SF)
        var.pack(side=tk.LEFT, expand=tk.YES)
        var = tk.Button(line, text='Select', font=BF, bg=btn, activebackground=btn_active,
                        command=self.fun_loadpath)
        var.pack(side=tk.LEFT, padx=5)

        # LLLLeftLLL
        left = tk.Frame(frame)
        left.pack(side=tk.LEFT)

        # ---Line 1---
        line = tk.Frame(left)
        line.pack(expand=tk.YES, fill=tk.X)
        var = tk.Button(line, text='XANES', font=BF, bg=btn, activebackground=btn_active,
                        command=self.fun_xanes)
        var.pack(side=tk.LEFT, padx=5)
        var = tk.Button(line, text='DoS', font=BF, bg=btn, activebackground=btn_active,
                        command=self.fun_dos)
        var.pack(side=tk.LEFT, padx=5)

        # ---Line 2---
        line = tk.Frame(left)
        line.pack(side=tk.TOP, fill=tk.X, pady=5)
        var = tk.Label(line, text='Reflections:', font=SF)
        var.pack(side=tk.LEFT)
        self.reflist = [ref.replace('(', '').replace(')', '').replace('-', '_') for ref in self.fdm.refkeys]
        self.reflection = tk.StringVar(frame, self.reflist[0])
        var = tk.OptionMenu(line, self.reflection, *self.reflist)
        var.config(font=SF, width=10, bg=opt, activebackground=opt_active)
        var["menu"].config(bg=opt, bd=0, activebackground=opt_active)
        var.pack(side=tk.LEFT)

        # ---Line 3---
        line = tk.Frame(left)
        line.pack(side=tk.TOP, fill=tk.X, pady=5)
        var = tk.Button(line, text='Plot All Azi/Energy', font=BF, bg=btn, activebackground=btn_active,
                        command=self.fun_ref3d)
        var.pack(side=tk.LEFT, padx=5)
        # DoS projection button if sph_signal_rxs files available
        if any(['sph' in key for key in self.fdm.__dict__.keys()]):
            var = tk.Button(line, text='Plot DoS Projection', font=BF, bg=btn, activebackground=btn_active,
                            command=self.fun_refdos)
            var.pack(side=tk.LEFT, padx=5)

        # ---Line 4---
        line = tk.Frame(left)
        line.pack(side=tk.TOP, fill=tk.X, pady=5)
        var = tk.Label(line, text='Angle (Deg):', font=SF)
        var.pack(side=tk.LEFT)
        self.cutangle = tk.StringVar(frame, 'max')
        var = tk.Entry(line, textvariable=self.cutangle, font=SF, width=10, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT, expand=tk.YES, padx=6)
        var = tk.Button(line, text='Plot Energy', font=BF, bg=btn, activebackground=btn_active, width=15,
                        command=self.fun_refenergy)
        var.pack(side=tk.LEFT, padx=6)

        # ---Line 5---
        line = tk.Frame(left)
        line.pack(side=tk.TOP, fill=tk.X, pady=5)
        var = tk.Label(line, text='Energy (keV):', font=SF)
        var.pack(side=tk.LEFT)
        self.cutenergy = tk.StringVar(frame, 'max')
        var = tk.Entry(line, textvariable=self.cutenergy, font=SF, width=10, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT, expand=tk.YES, padx=6)
        var = tk.Button(line, text='Plot Azimuth', font=BF, bg=btn, activebackground=btn_active, width=15,
                        command=self.fun_refazim)
        var.pack(side=tk.LEFT, padx=6)

        # ---Line 6---
        var = tk.Label(left, text='Number of cycles: %d' % self.fdm.bavfile.cycles(), font=SF)
        var.pack(anchor=tk.W)
        var = tk.Label(left, text='Final Cycle Charge state:', font=SF)
        var.pack(anchor=tk.W)
        var = tk.Label(left, text=self.fdm.bavfile.potrmt_str(), font=HF)
        var.pack(anchor=tk.W)

        # RRRRightRRR
        right = tk.Frame(frame)
        right.pack(side=tk.LEFT, expand=tk.YES)

        # ---Search box---
        line = tk.Frame(right)
        line.pack(side=tk.TOP, fill=tk.X, pady=5)
        var = tk.Label(line, text='Search:', font=SF)
        var.pack(side=tk.LEFT)
        self.bavsearch = tk.StringVar(frame, '')
        var = tk.Entry(line, textvariable=self.bavsearch, font=SF, width=30, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT, expand=tk.YES, padx=6)
        var.bind('<Return>', self.fun_search_next)
        var.bind('<KP_Enter>', self.fun_search_next)
        var = tk.Button(line, text='Next', font=BF, bg=btn, activebackground=btn_active, width=5,
                        command=self.fun_search_next)
        var.pack(side=tk.LEFT, padx=6)
        var = tk.Button(line, text='Prev', font=BF, bg=btn, activebackground=btn_active, width=5,
                        command=self.fun_search_prev)
        var.pack(side=tk.LEFT, padx=6)

        # |||Text Box|||
        box = tk.LabelFrame(right, text='FDMNES _bav.txt File')
        box.pack(side=tk.LEFT, padx=4, fill=tk.BOTH, expand=tk.YES)

        # Scrollbars
        scanx = tk.Scrollbar(box, orient=tk.HORIZONTAL)
        scanx.pack(side=tk.BOTTOM, fill=tk.X)

        scany = tk.Scrollbar(box)
        scany.pack(side=tk.RIGHT, fill=tk.Y)

        # Editable string box
        self.text = tk.Text(box, width=default_width, height=default_height, font=HF, wrap=tk.NONE, bg=ety)
        self.text.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, self.fdm.bavfile.text)
        self.text.config(state=tk.DISABLED)

        self.text.config(xscrollcommand=scanx.set, yscrollcommand=scany.set)
        scanx.config(command=self.text.xview)
        scany.config(command=self.text.yview)

        # Set cursor
        self.text.mark_set(tk.INSERT, "1.0")

    def fun_loadpath(self, event=None):
        """Button Select - Open new folder"""
        filename = filedialog.askopenfilename(filetypes=[('FDMNES output file', '.txt'),
                                                         ('All files', '.*')])  # from tkFileDialog
        if filename:
            filepath, filename = os.path.split(filename)
            self.root.destroy()
            AnaFDMNESgui(filepath)

    def fun_xanes(self, event=None):
        """Button XANES"""
        self.fdm.xanes.plot()
        plt.show()

    def fun_dos(self, event=None):
        """Button DOS"""
        self.fdm.density.plot()
        plt.show()

    def fun_ref3d(self, event=None):
        """Button Plot all Azim/energy"""
        refn = self.reflection.get()
        refob = self.fdm.__getattribute__(refn)
        refob.plot3D()
        plt.show()

    def fun_refdos(self, event=None):
        """Button spherical tensors"""
        refn = self.reflection.get()
        sphrefname = 'sph_' + refn
        if sphrefname in self.fdm.__dict__.keys():
            refob = self.fdm.__getattribute__(sphrefname)
            refob.plot()
            plt.show()
        else:
            print('Spherical tensor file not available')

    def fun_refenergy(self, event=None):
        """Button Plot Energy"""
        refn = self.reflection.get()
        azim = self.cutangle.get()
        try:
            azim = float(azim)
        except ValueError:
            pass
        refob = self.fdm.__getattribute__(refn)
        refob.plot_eng(azim)
        plt.show()

    def fun_refazim(self, event=None):
        """Button Plot Azimuth"""
        refn = self.reflection.get()
        energy = self.cutenergy.get()
        try:
            energy = float(energy)
        except ValueError:
            pass
        refob = self.fdm.__getattribute__(refn)
        refob.plot_azi(energy)
        plt.show()

    def fun_search_next(self, event=None):
        """Button Next"""
        search_text = self.bavsearch.get()
        if search_text == '': return

        searchpos = self.text.index(tk.INSERT) + "+1c"

        res = self.text.search(search_text, searchpos, stopindex=tk.END)
        if res == '': return
        self.text.focus_set()
        self.text.mark_set(tk.INSERT, res)
        self.text.see(tk.INSERT)

    def fun_search_prev(self, event=None):
        """Button Prev"""
        search_text = self.bavsearch.get()
        if search_text == '': return

        searchpos = self.text.index(tk.INSERT) + "-1c"

        res = self.text.search(search_text, searchpos, stopindex=None, backwards=True)
        if res == '': return
        self.text.focus_set()
        self.text.mark_set(tk.INSERT, res)
        self.text.see(tk.INSERT)

