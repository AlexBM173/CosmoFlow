import tracers
import numpy as np

def generate_redshifts(n) -> np.ndarray:
    """
    Generates an array of sampled redshifts using the ELG tracer.

    :param n: Number of redshift samples to generate
    :return: Array of sampled redshifts
    """
    edge_1 = np.random.randint(0, n + 1)
    edge_2 = np.random.randint(0, n + 1)
    edge_3 = np.random.randint(0, n + 1)
    n_lrg = edge_1
    n_elg = edge_2 - edge_1
    n_qso = edge_3 - edge_2
    n_bgs = n - edge_3
    lrg_tracer = tracers.LRG()
    elg_tracer = tracers.ELG()
    qso_tracer = tracers.QSO()
    bgs_tracer = tracers.BGS()
    redshifts = []
    if n_lrg > 0:
        redshifts.extend(lrg_tracer.sample_redshifts(n_lrg))
    if n_elg > 0:
        redshifts.extend(elg_tracer.sample_redshifts(n_elg))
    if n_qso > 0:
        redshifts.extend(qso_tracer.sample_redshifts(n_qso))
    if n_bgs > 0:
        redshifts.extend(bgs_tracer.sample_redshifts(n_bgs))
    return np.array(redshifts)