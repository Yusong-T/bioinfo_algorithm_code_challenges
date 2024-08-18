# C1_W4

import random

def CreateProfile(motifs):
    num = len(motifs)
    profile = []
    for i in range(k):
        A_count = 0
        C_count = 0
        G_count = 0
        T_count = 0
        for j in range(num):
            if motifs[j][i] == 'A':
                A_count += 1
            elif motifs[j][i] == 'C':
                C_count += 1
            elif motifs[j][i] == 'G':
                G_count += 1
            elif motifs[j][i] == 'T':
                T_count += 1
        profile.append([(A_count+1)/(num+4),(C_count+1)/(num+4),(G_count+1)/(num+4),(T_count+1)/(num+4)])       # with pseudocounts
    return profile

# def ProfileMostProbable(string,k,profile):
#     probability = 0
#     position = 0                                # set the default position to prevent error
#     for i in range(len(string)-k+1):            # also means selecting the first kmer if all the probabilities equal to 0
#         prob = 1
#         for j in range(k):
#             if string[i+j] == 'A':
#                 prob *= float(profile[j][0])
#             elif string[i+j] == 'C':
#                 prob *= float(profile[j][1])
#             elif string[i+j] == 'G':
#                 prob *= float(profile[j][2])
#             elif string[i+j] == 'T':
#                 prob *= float(profile[j][3])
#         if prob > probability:
#             probability = prob
#             position = i
#     return string[position:position+k]

def hammingdis(p,q):
    count = []
    for i in range(0,len(p)):
        if p[i] == q[i]:
            continue
        else:
            count.append(i)
    return len(count)

def Score(motifs):
    num = len(motifs)
    consensus = []
    for i in range(k):
        tcount = {'A':0,'C':0,'G':0,'T':0}
        for j in range(num):
            if motifs[j][i] == 'A':
                tcount['A'] += 1
            elif motifs[j][i] == 'C':
                tcount['C'] += 1
            elif motifs[j][i] == 'G':
                tcount['G'] += 1
            elif motifs[j][i] == 'T':
                tcount['T'] += 1
        for key,value in tcount.items():
            if value == max(tcount.values()):
                consensus.append(key)
                break                           # to prevent getting more than one character from one loop
    ConsensusString = "".join(consensus)
    result = 0
    for motif in motifs:
        result += hammingdis(ConsensusString,motif)
    return result

def ProfileRandomlyKmer(string,k,profile):
    ProbDistribution = {}
    for i in range(len(string)-k+1):
        prob = 1
        for j in range(k):
            if string[i+j] == 'A':
                prob *= float(profile[j][0])
            elif string[i+j] == 'C':
                prob *= float(profile[j][1])
            elif string[i+j] == 'G':
                prob *= float(profile[j][2])
            elif string[i+j] == 'T':
                prob *= float(profile[j][3])
        if string[i:i+k] not in ProbDistribution.keys():            # to avoid overwriting the probability of the same pattern
            ProbDistribution[string[i:i+k]] = prob
        else:
            ProbDistribution[string[i:i+k]] += prob
    space = {}                                                      # making a weighted choice
    current = 0                                                     # further explanation on notebook
    for choice,weight in ProbDistribution.items():                          # reference: https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
        space[current] = choice
        current += weight
    rand = random.uniform(0,current)
    space[current] = None
    for key in sorted(space.keys()):
        if rand < key:
            return choice
        choice = space[key]
    return None

def GibbsSampler(DnaString,k,t,N):
    Dna = DnaString.split(' ')
    length = len(Dna[0])
    Results = []
    CurrentScore = k * t
    Motifs = []
    BestMotifs = []
    Results = []
    for repeat in range(20):
        for i in range(t):
            ranpos = random.randint(0,length-k)             # note that both side-values are included
            Motifs.append(Dna[i][ranpos:ranpos+k])
            BestMotifs.append(Dna[i][ranpos:ranpos+k])
        for j in range(N):
            m = random.randint(0,t-1)
            motif_m = Motifs.pop(m)
            Profile = CreateProfile(Motifs)
            motif_m = ProfileRandomlyKmer(Dna[m],k,Profile)        ### !!! it's Dna[m] NOT motif_m!!!
            Motifs.insert(m,motif_m)
            if Score(Motifs) < Score(BestMotifs):
                for n in range(t):
                    BestMotifs[n] = Motifs[n]
        if Score(BestMotifs) < CurrentScore:
            Results.clear()
            for n in range(t):
                Results.append(BestMotifs[n])
            CurrentScore = Score(Results)
    print(Score(Results))
    return Results

k = 15
t = 20
N = 2000
DnaString = '''CGTCGTGATGTGAGCTGTTGGCGACTGGTGCGCGGTGACCCCTGTATAGCGTTAAGGCAGTGTACGCTCATGTGCTCCTCACACGTCCGAAACAGACCGTCCTCTACCACTTGTTGTCCGCTAGAGGGATTTCGAAAAGCTGGCAAGACGTAGAGATCACCCACTTGATCGTGAAGAAGTAGGAGGATAAGTATGAGACAACCCGGCATAGTAGTGGCCAAAATTTCAAGAAACCTGCGTCGCACGTGGTTCTAATACTTGGTCGAAATAGAGACCGGGATCTATGCTATTAATTTATGACACGTACGTTTTTCAACGTCGTGATGTGAGC TGTTGGAGAGACCTGGCTGTTCGACTGGTGCGCGGTGACCCCTGTATAGCGTTAAGGCAGTGTACGCTCATGTGCTCCTCACACGTCCGAAACAGACCGTCCTCTACCACTTGTTGTCCGCTAGAGGGATTTCGAAAAGCTGGCAAGACGTAGAGATCACCCACTTGATCGTGAAGAAGTAGGAGGATAAGTATGAGACAACCCGGCATAGTAGTGGCCAAAATTTCAAGAAACCTGCGTCGCACGTGGTTCTAATACTTGGTCGAAATAGAGACCGGGATCTATGCTATTAATTTATGACACGTACGTTTTTCAACGTCGTGATGTGAGC GTGGCCACTCTTCGATGTCGAAATCAGGGACGTCCTCGCTAACATCGATCACATCGCTCAATTCTGATGTGTTTCGTTTTCGTCAGTGTGAGGAAGCCGTATTTTCCAGTGTGAGACGGGTAATCTTGTGCTTACGGTAAGACGTTCTCGGCTTTGTTCGGTCAGTAACATCTACATTCGTCTTATCTGTTATTCAATCGGTGGCACGACCGAGCCTAGCCACAGAACGGATGGGGATTAAGGGTTTACCGTATTCGAGATCACTGGGGTTTGTATCCCCTAAAATAACCACCCTCTATACTAATACGATGCTTTATAAGTACTAAACCGT CGACGACAGTTGTCCACACTCCGGAATCCACTGGCTGTTCTGCCACACAGAGAGCTGCATAACACAACTACAGGGATATCCATCTCCTGACGTCAGTCTGCTCTTTTTGGGTATCGTGTTCCGCACACGAGACCGCGCGTAGGGTCTATTTCAGACTGTTACACTTTCAAAAGTGAGTTATCTTATCAGCGAGTGTCTGAAAACGTCAGGGACTATGCGTCCCGATTTTGAAGACTTCAGTTTTCGCGCCGGTGTGAGGTGACTAGCAGGTTGGGTTAATAAATTAGACAGGCCAGCTACAAGTACTCGGTGTTTCGTCCCGCTAGGTTTC GTGCAGAAAACAACCGATTTAGAAGGTCAGAGCGGGGTATCTATGGGAAGGTTTTGACACTTGTTATTGTCTTTTCGTCTGATCAAGCTCCCGATTCCAGACCTTATTTCACTTAGTGTTTACCCTCCTTAAGGCAAAATTGCGCCACATGGGTAACAAATATCGTGAGTCCCGCACAAAGCGCCCGTCCGCAAGAATCGGTGAAGACTTAACTTTAACACGCAGAATGCGTACTTCCTATCCTGGGAAACTCAATCAAAGTGGCAGAGTTTCACTCTAAGGCCTGTCTGCACTTCAAAGATCACTGGCTTCGCTACAAACCGCTGGTTCG TCTTCCGCGTGAAATGCTGGATGCGAACGGGCCTCATCCATAGGCCGATGTCCTTCCACGATAGCTGTGCGCGTATGTGGTTAGATCACGTACTGTTATACGGCTCCATACGTCTCACACATCGCCGTTCTCTCTTGGGCAGTCGTTCGTACAACGGCATTCGTATTCTGCTAAGGTGAGGTCAATACAGTCCAGAACCCGTGCAAGCAACGAGTGAATGGACCGAGATTTATCACACCTTAGGTTAACGTAACTGATAGAAATATCAATGTAGCTCTTGTGCCCATCAATCGAAGACCCTGAGGCAACCGATGATTCGGGTTCATACGGT GCCGCAGGCGCGCGGGCTAACTGCTATACCATCCCACTAAGATAGAGTCTCCGGGATCAAGACTTTAGTGCATATAATGCCATCTAGAAAGATACCCTCCCCCTCCATTTATAATTCATACTCGCGTCTAGGCGGCAACATTTGTCAGAACAACCTTGTACCCGCTGGGCCTGCTCAAGTCATATTCAGAGTCCAGTGCAGGCTTAAACCATTGTCTAACGGCAGGGTGGGGCGTGGCCTAGACGTCAACCGCGATCACTGGCTGACCTTAGCTCTATCGCACTCGTAGGAGATCCACTGGTGGTTCTTTGATACTAGCTAGACTCGCAGT CCCGTCCCTGAGCAGAGTGGCCAGTCTGCTCCTACCTGGGACATGCAGAGCGGTAATCTATGTCAAGATGCAGATTTATGGCTGTTTTTTGGGTCGATAAGCATGAGTAACGCTCTGTATGGTGAATCCGAGGATGTAACTCTCGAACCGAATAAGGTTTTCAATCGACGCACTTCACCCGTCCGACTGAAGGCACGTATTAACGCGCAGGAGTTAGCTCATCTCAAACGCCTCCAGAGGTAATGCCGTCCGCGCGGATGAATAGGAAACAACGGTAAGTATGCTTCTGGCATTGCATGCAGTCACGGCCACACGGTGAGGTATAGGTGAG TCTCTCACAAGGATGGAACGTGTTACGTTTCCGATAAATGTAGCGCCATGATTAGCAAGCCGGAAAGTACTCATTACGCCTTCCGAAAATATCCCGTACTAATCATAGAGCAGCCGGTTAAGGTCAAGGAACTATGATAAAGAATGGCACGCCTCTTCGCGCGCCCTCCGGCAGTCCCCTAGTTATCGGGCTCTAAAGGGTAGGTTCAACGGATCGGCTATCCTAACGTAGGTCTCCGCTTGAAGGAGAGTGTTACACTCGTGTATTCTAGATCAACAGCTGTTGCATAACGAGCTGACTGATATTCAGTATGACCAAGAAGACGTGTGGC AGACAAGTGGGGACTTCTAATACAAGTTTTACCTAAGCCCGAAGGGAATGCGCGTAGGAAGTCCCCGGGCCCCGTTCCTGGTTACTATGCGAATCTGAGTGCTTAAAAAGCTCAAGGACTACAGTGATGTAGAACTGAGGTAAGGCAGATTTTTGGCTGTTGTTGCAGATCGTCCTGCATTATAGTGTCTTAGTTCACGACAGAGAACAACATCTATTACTCGTGGCGTTTAACCGTACTTGATACAGTCAGCACATACTCTTGAATGGGAATTACACAGGATGTTACCCACGCGTTGCTAATCGCCCCGCGCACACTGGCTGCCTGGGGA TTTCGGTTCCTCCTACTCTGCATGAAGGCCCCCTAGAATTTGGCTGTGCCCGCCCAGGTCCGTCTCCATAGTAAATCGACATCACACCCACGGTCTGACCGTGCGTGAAAGCGCGGGCCAAAGCGATCGGACCGCCAACTTGCTACTTTAAGCCCTCTCGAACTACAACATCGTGTAGACAGAGTCGTTCGTTCTGATGCATGTTCTCATCTGTATGCAAAATTAAGTAATGTATATTGCACATTGTAGATCACTTCTTGTTGCACCGCGGGCTTGAATATCTCTACACTTACGTAGATCCGGACGCCCTTTCGGGGTTGTCCAGGCATCC GTGACTACTCCTGTACGCATGGGTATAAAGGGGCGAGTATTCGATACCCGGTGGTCCGCTGTGCTATCAACGGCCTACGTTAGCGCGCAAAATAAAGGATTTAGGAGTAACAGCGATTTTTATAGCTCTTCGTGGGCCGCGCCGTTCGATCAGGGGGGTCCGTGAACGACGGGTAACCGGCGGTACCTCATGACGTCGAAAGATTGCTGCGTTTTTTTATCGGCGTTGGCCGGGTGTAGCTGCCTACAGAGAGGTAGATCACTGTTCGTTGAGGACGATGGACGTAAATTGGTCCTTTCGGGTACGATGAGACCCAAGCAGGTTGTATAAT TTGCCATGCAAAACTCCAATTTTAAATTTAGGAGGAGGAAGTTACTAGGATAGTCGTACGAATACCTAGATCGTAGATCGTGGGCTGTTGAGCGGGACTATGTCGCGTACACTGTCTGCTAGCGACAGATGCTGGGGTCCTTTCTCGTCTACAGTACCTGCTCTTCGAGAGTCACAATATACGATCCGCGGGTGTCTTCGCGGGAGCTAATCCCTTGTAATGGAGGTCTTACCAAAGCCCCCCGTAAGCTTCCCTCCTCGCATCTCCTGGTCCCGCGAACCTCGAGAGTGCAACGGGTTAATAATGCGAGAATACCTCGGCTTCTTATTTT TTATTTCAGCCTACCGTCCGATGTAATCCCTCCCTTCAGCACGATCGGTCCCCAACTTCCCGCTTCCATGATTAGTGGGTATCTCAGGGTTTAGGAGCTGCTGAGAGGTGCACGAGTGTCTCGCCAACGGGAATCGATCTGGTGGTGTGCTCTAGTCAGTGTTTACAATCAACGAAACGACGTAGCAGATAAGGTACCCGCGGAGGTCGATCGCAATCTCCTATCACTGGCTGTCTGTCACCATGTCGGCGTCAGAATATGTACTACGTTAGTTAGTCCAACATCAGACTTCGTCAACGGTTACAGACACTCAACGACACTGGTCAACAAT GTGGCGACTGACAATACGGTGGAGAGGCGCAGGAGCTCGTCAGCGGCTGCGGGCTAACGTTTCACCTACAAGCGTTCCATACTAACAAGACTCAATCGTGACGGCGGTCCCCTTCCCTGTGCCGAGCTAGTAGCAGACTTCTGGCTGTTTAGTTAACAAGATCACAATGGATGTGGTCTAGCTTATAAGTGCTCCGGGCTCCCGAGAGGTCAACGAAGGCGTCACTAGTCTCGGATTTTCGAGAGAAAGTGGTGACGGTGTCCTGATTACGCAACGAGTATGCGTTAGAGTCATCTTGGTGTCAGCTAATCCTGGTTAACCCGCATATCAG ACAGAGCATATTGCCACACTGTGCCGGCCACACGAGTCCGTTACGCTTTGTATGCAAGACTTTCCGGGATTCACCGATTGGAGCTTAAGGGGAGGGACCAAGGGGAAGACCTCAACTATGAACAATTCTCACCGCATTGGCCCTGGTTGGGCGGGAAACCACTAGTGATGCAGTGTTAAAACCTGTGGTCGGGTAGATCACTGGCATCTATCATTCGCACCGGACTTTGGAGATTGAATTAGCGCTCCTAGTGACATTTATTGGTGAATTCGCCAGCCCGGGATCGCCTTGGATTAATCTATAGGTTGAATACGTGGGACGTACGCACTAA AATATGTAAACAGAGAATCCTGTCTCAAGGGTGTTGGGAATACAATTCGCCTGGCCAGCGGGATGAGATATGAGGATGCCTAAAAGATTGCTAAGTTGACTATTAATCTCGCTACCAGATAGTTGACGAGAGCGCTTTTCACTGGCTGTTAAGCTCATAACTCGCCAACAACCCGTGTAAACGGACTGTGGCTCAAGGATAACTCCCAAGTCGCGACGATATCCGGAATGCCAGGTCGAATGAGCAAATAAAACTCTTACACTCCTCTGCGACAGCGTAAGAAACCCATCTACTACTTGCCTTTCACGGGAGTGTGCCGGGTTTGCAGATG TCAGATAATGGGAGACGCCACCACGTTTCTAATTCGTAGGATGTGGGTTGCGGCGCCGACGTACATCGCAGGGAACAAACTGCTTCCGCTATCATCATAATACAAGACTGTAATTTGGATGATTCGAGCAGACTGGACCCTTGGCTGTACACTGGTGTTAAACAAGACTCTTGATAGATCGACGGCTGTTCACCAGCTAGCGTTGTGTGGTTCCGGAGAAAACCGGGGACTGTAACGTTATAGAGCGCACCGATAGCTTTTCAGGCTCGGGCGCTAACGAGCAAATTGGCATTGTGGACGACCGTTGCTCGGACTTCACAGGGGCTTGTCA ACTTACGCTAATAAGAGATCAGGAGCTGTTCAACCTATCGAATCTTAGAGTTGAAGCAACCCTACCGCTGTGGCTAGTGAGTGGCGCTCTTAGTACATTGTGCTAATATTCGCCTTACGGGAGCTGGGCACGTTGCTGATACCCTCTTGGACGCTGTATGTTGAGTCGCCCGTGGAGCCCGGTTCATCGTCTATCCACGGTTTGCCTACCACTCGCTTCCGATAAGTGGCGCTTTACTTGCCACAGTCGCGTAATTTGTTCCATAACGTCATTTACGGCCAACAGGTCACAGCGAAAGTCCGACAGGTAGGAGACCGTAGTATTCAGATGA TATACATTAGTGCCCTTTGGCTTACCCCGTTTGGGACCGTAGGTTGTCTCGCTTGCACAGAGGTGTGCGTTAACGCAAGAGCTCCCAGACGCACTAGCTCTGTGGTTCTTTTAGCCACGGGACAGTAACCGCACGCAACCTCCAGCGGAACGGCGGCCAATGACAGGCCGACACTTCTCCATAGTACGGGATAGAATCCGTGCTCAGGAAACTGGCTGTTCAAGTTGCGCAACAACGGAGCCATAGAATGCCTCACACATAAGTTGGTGCCAGTTCCCCAGACGTGAAGAACCGCTATGATAGCTTTCCCCTACGGTAGCCCATACTGCGG'''
print(*GibbsSampler(DnaString,k,t,N))
