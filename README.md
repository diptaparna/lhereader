# lhereader
A Python module to read LHE (Les Houches Event) file and access the event information in an object oriented way.
Requires [vector](https://github.com/scikit-hep/vector), [awkward](https://github.com/scikit-hep/awkward) and [uproot](https://github.com/scikit-hep/uproot5) (`pip install -r requirements.txt`). No ROOT installation is needed.

Sample code to use this module -

    from lhereader import readLHEF
    import numpy as np
    import uproot

    data=readLHEF('unweighted_events.lhe')
    parts=data.getParticlesByIDs([5,-5]) # collect all bottom and anti-bottom quarks
    hist=np.histogram([p.pt for p in parts],bins=100,range=(0,1000))
    with uproot.recreate("pt_b_bbar.root") as f:
      f["pt"]=hist # write the histogram as a ROOT TH1

The events can also be converted to an awkward array or written out as a ROOT TTree -

    arrays=data.toArrays() # awkward array of particle records, one list per event
    data.writeROOT('events.root') # TTree "events" with branches nparticle, particle_px, particle_pdgid, ...
