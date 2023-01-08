import numpy as np

from Dataclasses.s2p import S2P


def compare_s2p(snp1, snp2, freq_tol=None):
    if not isinstance(snp1, S2P) or not isinstance(snp2, S2P):
        raise TypeError('Both comparable objects must be S2P class')
    s2p_com = S2P()
    freq1 = snp1.freq
    freq2 = snp2.freq
    if freq1.nop == freq2.nop:
        if freq_tol is None:
            atol1 = (np.max(freq1) - np.min(freq1)) / (freq1.nop * 2)
            atol2 = (np.max(freq2) - np.min(freq2)) / (freq2.nop * 2)
            freq_tol = np.min(atol1, atol2)
        if np.allclose(freq1, freq2, atol=freq_tol):
            freq = freq1.freqs
            s11 = snp1

