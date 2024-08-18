AminoAcidMass = {
    'G': 57,
    'A': 71,
    'S': 87,
    'P': 97,
    'V': 99,
    'T': 101,
    'C': 103,
    'I': 113,
    'L': 113,
    'N': 114,
    'D': 115,
    'K': 128,
    'Q': 128,
    'E': 129,
    'M': 131,
    'H': 137,
    'F': 147,
    'R': 156,
    'Y': 163,
    'W': 186
}

def LinearSpectrum(Peptide, AminoAcidMass):
    PrefixMass = {}
    PrefixMass[0] = 0
    for i in range(1,len(Peptide)+1):
        for aa in AminoAcidMass.keys():
            if Peptide[i-1] == aa:
                PrefixMass[i] = PrefixMass[i-1] + AminoAcidMass[aa]
    LinearSpectrum = [0]
    for i in range(len(Peptide)):
        for j in range(i+1,len(Peptide)+1):
            LinearSpectrum.append(PrefixMass[j]-PrefixMass[i])
    LinearSpectrum.sort()
    print(*LinearSpectrum)




Peptide = 'GWQYRISALDVCCILFAVFHEQGGRLKMPRMLAKD'
LinearSpectrum(Peptide, AminoAcidMass)
