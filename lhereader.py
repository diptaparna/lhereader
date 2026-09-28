import xml.etree.ElementTree as ET
import vector

class Particle:
    def __init__(self,pdgid,spin,px=0,py=0,pz=0,energy=0,mass=0):
        self.pdgid=pdgid
        self.px=px
        self.py=py
        self.pz=pz
        self.energy=energy
        self.mass=mass
        self.spin=spin    
    
    @property
    def p4(self):
        return vector.obj(px=self.px,py=self.py,pz=self.pz,E=self.energy)
    
    @p4.setter
    def p4(self,value):
        self.px=value.px
        self.py=value.py
        self.pz=value.pz
        self.energy=value.E
        self.mass=value.mass
    
    @property
    def p(self):
        return self.p4.p
    
    @property
    def eta(self):
        return self.p4.eta
    
    @property
    def pt(self):
        return self.p4.pt
    
    
class Event:
    def __init__(self,num_particles):
        self.num_particles=num_particles
        self.particles=[]
    
    def __addParticle__(self,particle):
        self.particles.append(particle)
        
    def getParticlesByIDs(self,idlist):
        partlist=[]
        for pdgid in idlist:
            for p in self.particles:
                if p.pdgid==pdgid:
                    partlist.append(p)
        return partlist

class LHEFData:
    def __init__(self,version):
        self.version=version
        self.events=[]
    
    def __addEvent__(self,event):
        self.events.append(event)
        
    def getParticlesByIDs(self,idlist):
        partlist=[]
        for event in self.events:
            partlist.extend(event.getParticlesByIDs(idlist))
        return partlist
    
    def toArrays(self):
        import awkward as ak
        fields=['pdgid','spin','px','py','pz','energy','mass']
        return ak.zip({f:[[getattr(p,f) for p in e.particles] for e in self.events] for f in fields})
    
    def writeROOT(self,filename,treename='events'):
        import uproot
        arrays=self.toArrays()
        with uproot.recreate(filename) as f:
            f.mktree(treename,{'particle':arrays.type.content})
            f[treename].extend({'particle':arrays})
        

def readLHEF(name):
    tree = ET.parse(name)
    root=tree.getroot()
    lhefdata=LHEFData(float(root.attrib['version']))
    for child in root:
        if(child.tag=='event'):
            lines=child.text.strip().split('\n')
            event_header=lines[0].strip()
            num_part=int(event_header.split()[0].strip())
            e=Event(num_part)
            for i in range(1,num_part+1):
                part_data=lines[i].strip().split()
                p=Particle(int(part_data[0]), float(part_data[12]), float(part_data[6]), float(part_data[7]), float(part_data[8]), float(part_data[9]), float(part_data[10]))
                e.__addParticle__(p)
            lhefdata.__addEvent__(e)
    
    return lhefdata
