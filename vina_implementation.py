# from vina import Vina


# v = Vina(sf_name='vina')

# v.set_receptor('1iep_receptor.pdbqt')

# v.set_ligand_from_file('1iep_ligand.pdbqt')
# v.compute_vina_maps(center=[15.190, 53.903, 16.917], box_size=[20, 20, 20])

# # Score the current pose
# energy = v.score()
# print('Score before minimization: %.3f (kcal/mol)' % energy[0])

# # Minimized locally the current pose
# energy_minimized = v.optimize()
# print('Score after minimization : %.3f (kcal/mol)' % energy_minimized[0])
# v.write_pose('1iep_ligand_minimized.pdbqt', overwrite=True)

# # Dock the ligand
# v.dock(exhaustiveness=32, n_poses=20)
# v.write_poses('1iep_ligand_vina_out.pdbqt', n_poses=5, overwrite=True)


import subprocess


class RunVina:
    def __init__(self, receptor, ligand, x, y, z, exh, sx, sy, sz, output_file) -> None:

        self.receptor = receptor
        self.ligand = ligand
        self.x = x
        self.y = y
        self.z = z
        self.exh = exh
        self.sx = sx
        self.sy = sy
        self.sz = sz
        self.output_file = output_file

    def run_process(self):
        proc = subprocess.Popen(
            rf'vina --receptor "docking/{self.receptor}" --ligand "docking/{self.ligand}" --center_x {self.x} --center_y {self.y} --center_z {self.z} --exhaustiveness {self.exh} --size_x {self.sx} --size_y {self.sy} --size_z {self.sz} --out "docking/outputs/{self.output_file}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output, err = proc.communicate()

        print(output)
        print(err)
        return (output, err)
