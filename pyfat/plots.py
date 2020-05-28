import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

class Plots:


    def __init__(self,name,saveloc):
        self.name = name
        self.save_loc = str(saveloc)



    def mono_test_plot(self,x1,y1,x2,y2):
        x1 = x1*100
        y1 = y1/10**6
        x2 = x2*100
        y2 = y2/10**6

        font = {'fontname':'Times New Roman'}
        plt.figure()
        plt.plot(x1,y1,linewidth=0.5,color='k',ls='--')
        plt.plot(x2,y2,linewidth=0.5,color='k',ls='-.')
        plt.xlabel('Strain (%)',fontdict = font,fontsize=15)
        plt.ylabel('Stress (MPa)',fontdict = font,fontsize=15)
        plt.title('Stress vs. Strain '+self.name,fontdict = font,fontsize=15)
        plt.grid(True)
        plt.legend(('Engineering','True'))
        plt.savefig(
            self.save_loc + '/Stress_vs_Strain_' +
            self.name + '.pdf',bbox='tight'
        )



    def mono_all_plot(self, runs, names):
        font = {'fontname':'Times New Roman'}
        fig = plt.figure()
        ax = fig.add_subplot(111)
        i = 0
        for run in runs:
            stress = run.stress/10**6
            strain  = run.ax_str*100
            ax.plot(strain,stress,label = names[i])
            i += 1
        handles, labels = ax.get_legend_handles_labels() 
        lgd = ax.legend(handles, labels,loc=2,bbox_to_anchor=(1,1))
        ax.set_title('Stress vs. Strain (All Tests)',fontdict = font)
        ax.grid('on')
        ax.set_xlabel('Strain (%)',fontdict = font)
        ax.set_ylabel('Stress (MPa)',fontdict = font)
        plt.savefig(
            self.save_loc + '/Stress_vs_Strain_All.pdf',bbox_inches='tight'
        )



    def fatigue_loglog(self, xdata, ydata, x_std, model, mode):
        """Creates log log plot for elastic and plastic strain - saves
        a .tiff file in the "plots" directory with good name"""

        #Data for scatter
        x_scatter = xdata
        y_scatter = ydata

        #Data for line
        x_line = x_std
        y_line = model

        #Create Figure...
        font = {'fontname':'Times New Roman'}
        plt.figure()
        plt.grid(True,which="both",ls="--")
        plt.plot(x_line,y_line,ls="-.",color='C1')
        plt.scatter(x_scatter,y_scatter,marker=".",color='black')

        i = 0
        for element in x_scatter:
            if element == 4000000:
                plt.scatter(x_scatter[i],y_scatter[i],marker=".",color = 'red')
            i += 1

        ax = plt.gca()
        ax.set_axisbelow(True)
        ax.set_xscale('log')
        ax.set_yscale('log')
        plt.xlabel("Reversals to Failure (2N)",fontdict=font)

        if mode == "P":
            plt.ylabel("Plastic Strain Amplitude (m/m)",fontdict=font)
            plt.title("Plastic Strain-Life",fontdict = font)
            plt.savefig(
                Path(self.save_loc,'Plastic_StrainLife.tiff'),\
                    dpi=600,bbox_inches='tight')
        elif mode == "E":
            plt.ylabel("Elastic Strain Amplitude (m/m)",fontdict=font)
            plt.title("Elastic Strain-Life",fontdict = font)
            plt.savefig(
                Path(self.save_loc,'Elastic_StrainLife.tiff'),\
                    dpi=600,bbox_inches='tight')
        elif mode =="S":
            plt.ylabel("Stress Range (MPa)",fontdict=font)
            plt.xlabel("Cycles to Failure (N)",fontdict=font)
            plt.title("Strain Controlled Stress-Life",fontdict = font)
            plt.savefig(
                Path(self.save_loc,'StressLife.tiff'),\
                    dpi=600,bbox_inches='tight')



    def fatigue_semilogX(self, xdata, ydata, x_std, model):
        """creates plot for strain amplitude vs cycles to failure. Save tiff
        file in the plots output folder"""
        
        #Data for scatter...
        x_scatter = xdata
        y_scatter = ydata

        #Data for line...
        x_line = x_std
        y_line = model

        #Create Figure...
        font = {'fontname':'Times New Roman'}
        plt.figure()
        plt.grid(True,which="both",ls="--")
        plt.plot(x_line,y_line,ls="-.",color='C1')
        plt.scatter(x_scatter,y_scatter,marker=".",color='black')

        i = 0
        for element in x_scatter:
            if element == 4000000:
                plt.scatter(x_scatter[i],y_scatter[i],marker=".",color = 'red')
            i += 1

        ax = plt.gca()
        ax.set_axisbelow(True)
        ax.set_xscale('log')
        plt.xlabel("Cycles to Failure (N)",fontdict=font)
        plt.ylabel("True Strain Amplitude (%)",fontdict=font)
        plt.title("Strain Amplitude vs. Cycles to Failure")

        #Save Figure...
        plt.savefig(
                Path(self.save_loc,'StrainAmp_vs_Cycles.tiff'),\
                    dpi=600,bbox_inches='tight'
                )



    def total_strain_life(self,x_std, plastic, elastic, total):
        """Creates total strainlife plot with elastic, plastic and total lines,
        saves a .tiff file to the plots directory"""

        #Create Figure...
        font = {'fontname':'Times New Roman'}
        plt.figure()
        plt.loglog(x_std,total)
        plt.loglog(x_std,plastic,ls="-.")
        plt.loglog(x_std,elastic,ls="--")
        plt.grid(True,which="both",ls="--")
        plt.title("Total Strain-Life",fontdict=font)
        plt.ylabel("Strain Amplitude (m/m)",fontdict=font)
        plt.xlabel("Cycles to Failure (N)",fontdict=font)
        plt.legend([
            "Total Strain-Life","Plastic Strain-Life","Elastic Strain-Life"
            ],loc = 1)
        plt.ylim([total[-1],total[0]])
        plt.xlim([1,len(x_std)])
        ax = plt.gca()
        ax.set_axisbelow(True)
        ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
        ax.yaxis.get_major_formatter().set_scientific(False)
        ax.yaxis.get_major_formatter().set_useOffset(False)
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.3f'))
        ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
        ax.yaxis.get_minor_formatter().set_scientific(False)
        ax.yaxis.get_minor_formatter().set_useOffset(False)
        ax.yaxis.set_minor_formatter(mticker.FormatStrFormatter('%.3f'))

        #Save Figure...
        plt.savefig(
                Path(self.save_loc,'Total_StrainLife.tiff'),\
                    dpi=600,bbox_inches='tight'
                )