from IPython import get_ipython
get_ipython().run_line_magic('reset', '-f')
import numpy as np
import matplotlib.pyplot as plt

loadAbsorption = np.load('totalAbsorption_1.npz')
for name, value in (loadAbsorption.items()):
    globals()[name] = value
particleStepsAbs = particleSteps
loadDegradation = np.load('degradation_1.npz')
for name, value in (loadDegradation.items()):
    globals()[name] = value
particleStepsDeg = particleSteps

# Plot section #########################################################################
if plotCharts and recordTrajectories:
    # Trajectories
    plt.figure(figsize=(8, 8))
    plt.rcParams.update({'font.size': 20})
    for i in range(num_particles):
        plt.plot(xPath[i][:][xPath[i][:]!=0], yPath[i][:][xPath[i][:]!=0], lw=0.5)
    plt.axhline(y=uby, color='r', linestyle='--', linewidth=2)
    plt.axhline(y=lby, color='r', linestyle='--', linewidth=2)
    if cpxOn:
        plt.axvline(x=cpx, color='b', linestyle='--', linewidth=2)
        plt.axvline(x=-cpx, color='b', linestyle='--', linewidth=2)
    plt.axvline(x=x0, color='yellow', linestyle='--', linewidth=2)
    if lbxOn:
        plt.axvline(x=lbx, color='black', linestyle='-', linewidth=2)
    plt.title("2D Diffusion Process (Langevin Equation)")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.grid(True)
    plt.tight_layout()
    # plt.savefig("/home/eugenio/Github/IDAEA/Overleaf/WeeklyMeetingNotes/images/trajectoriesInfinite.png", format="png", bbox_inches="tight")
    # plt.savefig("/home/eugenio/Github/IDAEA/Overleaf/WeeklyMeetingNotes/images/trajectoriesSemiInfinite.png", format="png", bbox_inches="tight")
    # plt.savefig("/home/eugenio/Github/IDAEA/Overleaf/WeeklyMeetingNotes/images/trajectoriesDegradation.png", format="png", bbox_inches="tight")
    plt.show()

if plotCharts and cpxOn:
    # PDF
    plt.figure(figsize=(8, 8))
    plt.plot(Time, pdf_part/num_particles)
    plt.xscale('log')
    plt.title("PDF")

    # CDF
    plt.figure(figsize=(8, 8))
    plt.plot(Time, np.cumsum(pdf_part)/num_particles)
    plt.xscale('log')
    plt.title("CDF")

    # 1-CDF
    plt.figure(figsize=(8, 8))
    plt.plot(Time, 1-np.cumsum(pdf_part)/num_particles)
    plt.xscale('log')
    plt.yscale('log')
    plt.title("1-CDF")

    # Binning for plotting the pdf from a Lagrangian vector
    countsLog, binEdgesLog = np.histogram(particleRT, timeLogSpaced, density=True)
    binCentersLog = (binEdgesLog[:-1] + binEdgesLog[1:]) / 2
    plt.figure(figsize=(8, 8))
    plt.plot(binCentersLog[countsLog!=0], countsLog[countsLog!=0], 'r*')
    plt.xscale('log')
    plt.yscale('log')
    plt.title("Lagrangian PDF of the BTC")

if plotCharts and lbxOn:
    plt.figure(figsize=(8, 8))
    plt.rcParams.update({'font.size': 20})
    plt.plot(timeBinsLog, countsSemiInfLog, 'b*')
    plt.plot(timeBinsLog, analPdfSemiInf, 'r-')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('PDF of BTC - Simulated vs analytical solution')
    plt.xlabel('Time step')
    plt.ylabel('Normalised number of particles')
    plt.tight_layout()
    # plt.savefig("/home/eugenio/Github/IDAEA/Overleaf/WeeklyMeetingNotes/images/verificationInfinite.png", format="png", bbox_inches="tight")

# Spatial concentration profile at 'recordSpatialConc' time
if plotCharts and np.logical_not(lbxOn):
    plt.figure(figsize=(8, 8))
    plt.rcParams.update({'font.size': 20})
    plt.plot(binCenterSpace, countsSpace, 'b-')
    plt.plot(binCenterSpace, yAnalytical, color='red', linestyle='-')
    plt.axvline(x=x0, color='yellow', linestyle='--', linewidth=2)
    if cpxOn:
        plt.axvline(x=cpx, color='b', linestyle='--', linewidth=2)
        plt.axvline(x=-cpx, color='b', linestyle='--', linewidth=2)
    plt.title("Simulated vs analytical solution")
    plt.tight_layout()
    # plt.savefig("/home/eugenio/Github/IDAEA/Overleaf/WeeklyMeetingNotes/images/verificationInfinite.png", format="png", bbox_inches="tight")

if plotCharts and degradation:
    # Distribution of survival times for particles
    plt.figure(figsize=(8, 8))
    plt.plot(np.arange(0, num_particles, 1), np.sort(particleStepsDeg)[::-1], 'b*')
    plt.plot(np.arange(0, num_particles, 1), np.sort(survivalTimeDist)[::-1], 'k-')
    plt.title("Survival time distribution")

    # Distribution of live particles in time
    plt.figure(figsize=(8, 8))
    survDistWm = np.array([sum(particleStepsDeg>float(Time[i])) for i in range(len(Time))])
    survDistWmNorm = survDistWm/survDistWm.sum()
    plt.plot(Time, exp_prob, 'r-')
    plt.plot(Time, survDistWmNorm, 'b*')
    plt.title("Live particle distribution in time")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Time step')
    plt.ylabel('PDF of live particles')
    plt.tight_layout()
    # plt.savefig("/home/eugenio/Github/IDAEA/Overleaf/WeeklyMeetingNotes/images/liveParticleInTime.png", format="png", bbox_inches="tight")

if plotCharts and recordTrajectories and np.logical_not(reflection):
    # Final particles's positions
    plt.figure(figsize=(8, 8))
    plt.plot(xPath[:, -1], yPath[:, -1], 'b*')
    plt.axvline(x=x0, color='yellow', linestyle='--', linewidth=2)
    plt.axhline(y=uby, color='r', linestyle='--', linewidth=1)
    plt.axhline(y=lby, color='r', linestyle='--', linewidth=1)
    for val in vInterval:
        plt.axvline(x=val, color='black', linestyle='--', linewidth=2)
    for val in hInterval:
        plt.axhline(y=val, color='black', linestyle='--', linewidth=2)
    plt.tight_layout()
    # plt.savefig("/home/eugenio/Github/IDAEA/Overleaf/WeeklyMeetingNotes/images/finalPositions.png", format="png", bbox_inches="tight")

    # Vertical distribution
    plt.figure(figsize=(8, 8))
    plt.bar(vBins[:-1], vDist, width=np.diff(vBins), edgecolor="black", align="edge")
    plt.title('Particles distribution at the end of the simulation')
    plt.xlabel('Distance along Y')
    plt.ylabel('Number of particles EXCLUDING THOSE ON BOUNDARIES')
    plt.tight_layout()
    # plt.savefig("/home/eugenio/Github/IDAEA/Overleaf/WeeklyMeetingNotes/images/verticalFinalDist.png", format="png", bbox_inches="tight")

    # Horizontal distribution
    plt.figure(figsize=(8, 8))
    plt.bar(hBins[:-1], hDist, width=np.diff(hBins), edgecolor="black", align="edge")
    plt.title('Particles distribution at the end of the simulation')
    plt.xlabel('Distance along X')
    plt.ylabel('Number of particles')
    plt.tight_layout()
    # plt.savefig("/home/eugenio/Github/IDAEA/Overleaf/WeeklyMeetingNotes/images/horizontalFinalDist.png", format="png", bbox_inches="tight")

if plotCharts and len(particleStepsAbs)>0:
    # Distribution of non-absorbed particles in time
    plt.figure(figsize=(8, 8))
    # pathLegnth = np.array([np.count_nonzero((row != lby) & (row != uby)) for row in yPath])
    nonAbsorbedParticles = np.array([sum(particleStepsAbs>float(Time[i])) for i in range(len(Time))])
    plt.plot(Time, nonAbsorbedParticles, 'b*')
    plt.title("Non-absorbed particles in time")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Time step')
    plt.ylabel('Number of non-absorbed particles')
    plt.grid(True, which="major", linestyle='-', linewidth=0.7, color='black')
    plt.grid(True, which="minor", linestyle=':', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.savefig("/home/eugenio/Github/IDAEA/Overleaf/WeeklyMeetingNotes/images/nonAbsParticles.png", format="png", bbox_inches="tight")

    # Normalised distribution of non-absorbed particles in time
    plt.figure(figsize=(8, 8))
    nonAbsorbedParticlesNorm = nonAbsorbedParticles/nonAbsorbedParticles.sum()
    plt.plot(Time, nonAbsorbedParticlesNorm, 'b*')
    plt.title("Non-absorbed particle normalised in time")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Time step')
    plt.ylabel('Non-absorbed particles normalised')
    plt.grid(True, which="major", linestyle='-', linewidth=0.7, color='black')
    plt.grid(True, which="minor", linestyle=':', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.savefig("/home/eugenio/Github/IDAEA/Overleaf/WeeklyMeetingNotes/images/nonAbsParticlesNorm.png", format="png", bbox_inches="tight")

# Well-mixed vs diffusion-limited survival time distributions ###########################################################

if len(loadAbsorption.files)>0 and len(loadDegradation.files)>0:
    # Distribution of live particles in time
    plt.figure(figsize=(8, 8))
    plt.rcParams.update({'font.size': 20})    
    tau = (uby-lby)**2/Df
    plt.plot(Time[:-1]/tau, survDistWmNorm[:-1], 'b*')
    plt.plot(Time[:-1]/tau, exp_prob[:-1], 'r-')
    plt.plot(Time[:-1]/tau, nonAbsorbedParticlesNorm[:-1], 'g*')
    plt.title("Live particle distribution in time")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('(Time step)/tau')
    plt.ylabel('PDF of live particles')
    plt.tight_layout()
    plt.savefig("/home/eugenio/Github/IDAEA/Overleaf/WeeklyMeetingNotes/images/survTimeDistCompare.png", format="png", bbox_inches="tight")

    # Rates of particles decay
    plt.figure(figsize=(8, 8))
    plt.rcParams.update({'font.size': 20})
    dt = np.diff(Time)
    dSurvPart = np.diff(survDistWmNorm)
    dExpProb = np.diff(exp_prob)
    dNonAbsPart = np.diff(nonAbsorbedParticlesNorm)
    dSurvdt = dSurvPart/dt
    dExpProbdt = dExpProb/dt
    dNonAbsdt = dNonAbsPart/dt
    midTimes = (Time[:-1] + Time[1:]) / 2
    plt.plot(midTimes[:-1], dSurvdt[:-1], 'b*')
    plt.plot(midTimes[:-1], dExpProbdt[:-1], 'r-')
    #plt.axhline(y=k_deg, color='r', linestyle='-', linewidth=1)
    plt.plot(midTimes[:-1], dNonAbsdt[:-1], 'g-')
    plt.title("Effective reaction rate")
    plt.xlabel('Time step')
    plt.ylabel('k(t)')
    plt.tight_layout()
    plt.savefig("/home/eugenio/Github/IDAEA/Overleaf/WeeklyMeetingNotes/images/survTimeDistRateCompare.png", format="png", bbox_inches="tight")