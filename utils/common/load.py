class Load(object):

    def __init__(self, axial_force=0.0, shear_force=0.0, moment=0.0):
        if axial_force is not None:
            self.axial_force = float(axial_force)
        else:
            self.axial_force = None
        if shear_force is not None:
            self.shear_force = float(shear_force)
        else:
            self.shear_force = None
        if moment is not None:
            self.moment = float(moment)
        else:
            self.moment = None

    def __repr__(self):
        repr = "Load\n"
        repr += "Axial Force: {}\n".format(self.axial_force)
        repr += "Shear Force: {}\n".format(self.shear_force)
        repr += "Moment: {}\n".format(self.moment)
        return repr