import sys,glob,os 
import numpy as np

def main(split):

    xpisumdirlist = []


    for file in glob.glob('XPISUM*'):
        xpisumdirlist.append(file)

    num_files = len(xpisumdirlist)

    bound_states_headers = []
    energies_headers = []

    file_1 = xpisumdirlist[0]
    file1FILE = open(file_1,'r') 

    file1 = file1FILE.readlines()
    length_of_file = len(file1)


    bound_states_headers.append(file1[0])
    energies_headers.append(file1[1]) 

    num_energy_points_per_bound = int(file1[1].split()[1]) 

    num_bound_states = int(length_of_file) / int((num_energy_points_per_bound + 2))


    if int(num_bound_states) != num_bound_states:
        print("possible problem with file")
        sys.exit() 

    total_energy_piunts = num_energy_points_per_bound * len(xpisumdirlist)

    num_bound_states = int(num_bound_states) 

    offset = 2 + num_energy_points_per_bound
    for jj in range(1,num_bound_states):
        bound_states_headers.append(file1[offset])
        energies_headers.append(file1[offset+1])
        offset = offset + 2 + num_energy_points_per_bound

    zeros_PI = np.zeros([num_bound_states,num_files*num_energy_points_per_bound,2])
    print(np.shape(zeros_PI))
    file1FILE.close()

    file_offset = 0

    for file in xpisumdirlist:
        current_file_file = open(file,'r')
        current_file = current_file_file.readlines()
        assert(len(current_file) == length_of_file), 'files not same length ! '
        offset = 0
        for jj in range(0,num_bound_states):
            x = []
            for line in current_file[(offset+(jj+1)*2):offset+num_energy_points_per_bound+(jj+1)*2]:
                x.append(line.replace('\n','').split())
            #x = np.array(x).astype(float)
            #x = file1[offset:offset+num_energy_points_per_bound]
            x = np.array(x).astype(float)
            #print(x)

            #print((offset),(offset+num_energy_points_per_bound))
            zeros_PI[jj,file_offset:num_energy_points_per_bound+file_offset,:] = x

            offset = offset + num_energy_points_per_bound
        file_offset = file_offset + num_energy_points_per_bound

        current_file_file.close()


    if not split:
        outfile = open('XPIzSUM_ARRANGED.OUT','w')

    for jj in range(0,num_bound_states):

        if split:
            outfile = open('XPIZSUM_ARRANGEDbound'+str(jj)+'.OUT','w')
            outfile.write('#'+bound_states_headers[jj])
            outfile.write('#'+energies_headers[jj].replace(str(num_energy_points_per_bound),str(total_energy_piunts)))
        else:
            outfile.write(bound_states_headers[jj])
            outfile.write(energies_headers[jj].replace(str(num_energy_points_per_bound),str(total_energy_piunts)))
        #current = zeros_PI[jj,:,:]

        energies = zeros_PI[jj,:,0]
        csa = zeros_PI[jj,:,1]

        order = np.argsort(energies)
        energies = energies[order]
        csa = csa[order]

        for ii in range(0,total_energy_piunts):
            string_format = '{:14.8E} {:9.3E}\n'.format(energies[ii],csa[ii])
            outfile.write(string_format)



import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--split',  help='splits into a file for each found state (default false)',action="store_true")
args = parser.parse_args()

split = False
if args.split:
    split = True

main(split)




#print(zeros_PI)