'''

generate plots for the mock challenge paper 


'''
import os 
import h5py 
import numpy as np 
# --- gqp_mc ---
from gqp_mc import util as UT 
from gqp_mc import data as Data 
from gqp_mc import fitters as Fitters
# --- plotting --- 
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['axes.linewidth'] = 1.5
mpl.rcParams['axes.xmargin'] = 1
mpl.rcParams['xtick.labelsize'] = 'x-large'
mpl.rcParams['xtick.major.size'] = 5
mpl.rcParams['xtick.major.width'] = 1.5
mpl.rcParams['ytick.labelsize'] = 'x-large'
mpl.rcParams['ytick.major.size'] = 5
mpl.rcParams['ytick.major.width'] = 1.5
mpl.rcParams['legend.frameon'] = False


dir_fig = os.path.join(UT.dat_dir(), 'mini_mocha') 


def mock_challenge_photo(noise='none', dust=False, method='ifsps'): 
    ''' Compare properties inferred from forward modeled photometry to input properties
    '''
    # read Lgal input input properties
    _, meta = Data.Photometry(sim='lgal', noise=noise, lib='bc03', sample='spectral_challenge') 
    Mstar_input = meta['logM_total'] # total mass 
    Z_MW_input  = meta['Z_MW'] # mass-weighted metallicity
    tage_input  = meta['t_age_MW'] # mass-weighted age
    
    theta_inf = [] 
    for igal in range(97): 
        # read best-fit file and get inferred parameters
        _fbf = Fbestfit_photo(igal, noise=noise, dust=dust, method=method) 
        fbf = h5py.File(_fbf, 'r')  

        theta_inf_i = np.array([
            fbf['theta_2sig_minus'][...], 
            fbf['theta_1sig_minus'][...], 
            fbf['theta_med'][...], 
            fbf['theta_1sig_plus'][...], 
            fbf['theta_2sig_plus'][...]])
        theta_inf.append(theta_inf_i) 
    theta_inf = np.array(theta_inf) 
    
    # inferred properties
    Mstar_inf   = theta_inf[:,:,0]
    Z_MW_inf    = 10**theta_inf[:,:,1]
    tage_inf    = theta_inf[:,:,2]
    
    fig = plt.figure(figsize=(15,4))
    # compare total stellar mass 
    sub = fig.add_subplot(131) 
    sub.errorbar(Mstar_input, Mstar_inf[:,2], 
            yerr=[Mstar_inf[:,2]-Mstar_inf[:,1], Mstar_inf[:,3]-Mstar_inf[:,2]], fmt='.C0')
    sub.plot([9., 12.], [9., 12.], c='k', ls='--') 
    sub.set_xlabel(r'input $\log~M_{\rm tot}$', fontsize=25)
    sub.set_xlim(9., 12.) 
    sub.set_ylabel(r'inferred $\log~M_{\rm tot}$', fontsize=25)
    sub.set_ylim(9., 12.) 
    
    # compare metallicity
    sub = fig.add_subplot(132)
    sub.errorbar(Z_MW_input, Z_MW_inf[:,2], 
            yerr=[Z_MW_inf[:,2]-Z_MW_inf[:,1], Z_MW_inf[:,3]-Z_MW_inf[:,2]], fmt='.C0')
    sub.plot([1e-3, 1], [1e-3, 1.], c='k', ls='--') 
    sub.set_xlabel(r'input MW $Z$', fontsize=20)
    sub.set_xscale('log') 
    sub.set_xlim(1e-3, 5e-2) 
    sub.set_ylabel(r'inferred MW $Z$', fontsize=20)
    sub.set_yscale('log') 
    sub.set_ylim(1e-3, 5e-2) 

    # compare age 
    sub = fig.add_subplot(133)
    sub.errorbar(tage_input, tage_inf[:,2], 
            yerr=[tage_inf[:,2]-tage_inf[:,1], tage_inf[:,3]-tage_inf[:,2]], fmt='.C0')
    sub.plot([0, 13], [0, 13.], c='k', ls='--') 
    sub.set_xlabel(r'input MW $t_{\rm age}$', fontsize=20)
    sub.set_xlim(0, 13) 
    sub.set_ylabel(r'inferred MW $t_{\rm age}$', fontsize=20)
    sub.set_ylim(0, 13) 

    fig.subplots_adjust(wspace=0.4)
    _ffig = os.path.join(dir_fig, 'mock_challenge.photofit.%s.noise_%s.dust_%s.png' % (method, noise, ['no', 'yes'][dust]))
    fig.savefig(_ffig, bbox_inches='tight') 
    return None 


def mini_mocha_spec(noise='bgs0', method='ifsps'): 
    ''' Compare properties inferred from forward modeled photometry to input properties
    '''
    # read noiseless Lgal spectra of the spectral_challenge mocks
    specs, meta = Data.Spectra(sim='lgal', noise=noise, lib='bc03', sample='mini_mocha') 

    Mstar_input = meta['logM_fiber'][:97] # total mass 
    Z_MW_input  = meta['Z_MW'][:97]  # mass-weighted metallicity
    tage_input  = meta['t_age_MW'][:97]  # mass-weighted age
    
    theta_inf = [] 
    for igal in range(97): 
        # read best-fit file and get inferred parameters
        _fbf = Fbestfit_spec(igal, noise=noise, method=method) 
        fbf = h5py.File(_fbf, 'r')  

        theta_inf_i = np.array([
            fbf['theta_2sig_minus'][...], 
            fbf['theta_1sig_minus'][...], 
            fbf['theta_med'][...], 
            fbf['theta_1sig_plus'][...], 
            fbf['theta_2sig_plus'][...]])

        if sfr == '1gyr': 
            sfr_inf = ifsps._SFR_MCMC(fbf['mcmc_chain'][...], dt=1.)
        elif sfr == '100myr': 
            sfr_inf = ifsps._SFR_MCMC(fbf['mcmc_chain'][...], dt=0.1)
        theta_inf_i = np.concatenate([theta_inf_i, np.atleast_2d(sfr_inf).T], axis=1) 

        theta_inf.append(theta_inf_i) 
    theta_inf = np.array(theta_inf) 
    
    # inferred properties
    Mstar_inf   = theta_inf[:,:,0]
    Z_MW_inf    = 10**theta_inf[:,:,1]
    tage_inf    = theta_inf[:,:,2]
    
    fig = plt.figure(figsize=(15,4))
    # compare total stellar mass 
    sub = fig.add_subplot(131) 
    sub.errorbar(Mstar_input, Mstar_inf[:,2], 
            yerr=[Mstar_inf[:,2]-Mstar_inf[:,1], Mstar_inf[:,3]-Mstar_inf[:,2]], fmt='.C0')
    sub.plot([9., 12.], [9., 12.], c='k', ls='--') 
    sub.set_xlabel(r'input $\log~M_{\rm fib.}$', fontsize=25)
    sub.set_xlim(9., 12.) 
    sub.set_ylabel(r'inferred $\log~M_{\rm fib.}$', fontsize=25)
    sub.set_ylim(9., 12.) 
    
    # compare metallicity
    sub = fig.add_subplot(132)
    sub.errorbar(Z_MW_input, Z_MW_inf[:,2], 
            yerr=[Z_MW_inf[:,2]-Z_MW_inf[:,1], Z_MW_inf[:,3]-Z_MW_inf[:,2]], fmt='.C0')
    sub.plot([1e-3, 1], [1e-3, 1.], c='k', ls='--') 
    sub.set_xlabel(r'input MW $Z$', fontsize=20)
    sub.set_xscale('log') 
    sub.set_xlim(1e-3, 5e-2) 
    sub.set_ylabel(r'inferred MW $Z$', fontsize=20)
    sub.set_yscale('log') 
    sub.set_ylim(1e-3, 5e-2) 

    # compare age 
    sub = fig.add_subplot(133)
    sub.errorbar(tage_input, tage_inf[:,2], 
            yerr=[tage_inf[:,2]-tage_inf[:,1], tage_inf[:,3]-tage_inf[:,2]], fmt='.C0')
    sub.plot([0, 13], [0, 13.], c='k', ls='--') 
    sub.set_xlabel(r'input MW $t_{\rm age}$', fontsize=20)
    sub.set_xlim(0, 13) 
    sub.set_ylabel(r'inferred MW $t_{\rm age}$', fontsize=20)
    sub.set_ylim(0, 13) 

    fig.subplots_adjust(wspace=0.4)
    _ffig = os.path.join(dir_fig, 'mini_mocha.%s.specfit.vanilla.noise_%s.png' % (method, noise)) 
    fig.savefig(_ffig, bbox_inches='tight') 
    fig.savefig(UT.fig_tex(_ffig, pdf=True), bbox_inches='tight') 
    return None 


def mini_mocha_photo(noise='legacy', method='ifsps'): 
    ''' Compare properties inferred from forward modeled photometry to input properties
    '''
    # read noiseless Lgal spectra of the spectral_challenge mocks
    photo, meta = Data.Photometry(sim='lgal', noise=noise, lib='bc03', sample='mini_mocha')

    Mstar_input = meta['logM_total'][:97] # total mass 
    Z_MW_input  = meta['Z_MW'][:97]  # mass-weighted metallicity
    tage_input  = meta['t_age_MW'][:97]  # mass-weighted age
    
    theta_inf = [] 
    for igal in range(97): 
        # read best-fit file and get inferred parameters
        _fbf = Fbestfit_photo(igal, noise=noise, method=method) 
        fbf = h5py.File(_fbf, 'r')  

        theta_inf_i = np.array([
            fbf['theta_2sig_minus'][...], 
            fbf['theta_1sig_minus'][...], 
            fbf['theta_med'][...], 
            fbf['theta_1sig_plus'][...], 
            fbf['theta_2sig_plus'][...]])
        theta_inf.append(theta_inf_i) 
    theta_inf = np.array(theta_inf) 
    
    # inferred properties
    Mstar_inf   = theta_inf[:,:,0]
    Z_MW_inf    = 10**theta_inf[:,:,1]
    tage_inf    = theta_inf[:,:,2]
    
    fig = plt.figure(figsize=(15,4))
    # compare total stellar mass 
    sub = fig.add_subplot(131) 
    sub.errorbar(Mstar_input, Mstar_inf[:,2], 
            yerr=[Mstar_inf[:,2]-Mstar_inf[:,1], Mstar_inf[:,3]-Mstar_inf[:,2]], fmt='.C0')
    sub.plot([9., 12.], [9., 12.], c='k', ls='--') 
    sub.set_xlabel(r'input $\log~M_{\rm tot.}$', fontsize=25)
    sub.set_xlim(9., 12.) 
    sub.set_ylabel(r'inferred $\log~M_{\rm tot.}$', fontsize=25)
    sub.set_ylim(9., 12.) 
    
    # compare metallicity
    sub = fig.add_subplot(132)
    sub.errorbar(Z_MW_input, Z_MW_inf[:,2], 
            yerr=[Z_MW_inf[:,2]-Z_MW_inf[:,1], Z_MW_inf[:,3]-Z_MW_inf[:,2]], fmt='.C0')
    sub.plot([1e-3, 1], [1e-3, 1.], c='k', ls='--') 
    sub.set_xlabel(r'input MW $Z$', fontsize=20)
    sub.set_xscale('log') 
    sub.set_xlim(1e-3, 5e-2) 
    sub.set_ylabel(r'inferred MW $Z$', fontsize=20)
    sub.set_yscale('log') 
    sub.set_ylim(1e-3, 5e-2) 

    # compare age 
    sub = fig.add_subplot(133)
    sub.errorbar(tage_input, tage_inf[:,2], 
            yerr=[tage_inf[:,2]-tage_inf[:,1], tage_inf[:,3]-tage_inf[:,2]], fmt='.C0')
    sub.plot([0, 13], [0, 13.], c='k', ls='--') 
    sub.set_xlabel(r'input MW $t_{\rm age}$', fontsize=20)
    sub.set_xlim(0, 13) 
    sub.set_ylabel(r'inferred MW $t_{\rm age}$', fontsize=20)
    sub.set_ylim(0, 13) 

    fig.subplots_adjust(wspace=0.4)
    _ffig = os.path.join(dir_fig, 'mini_mocha.%s.photofit.vanilla.noise_%s.png' % (method, noise)) 
    fig.savefig(_ffig, bbox_inches='tight') 
    fig.savefig(UT.fig_tex(_ffig, pdf=True), bbox_inches='tight') 
    return None 


def mini_mocha_specphoto(noise='bgs0_legacy', method='ifsps'): 
    ''' Compare properties inferred from forward modeled photometry to input properties
    '''
    if noise != 'none':
        noise_spec = noise.split('_')[0]
        noise_photo = noise.split('_')[1]
    else:
        noise_spec = 'none'
        noise_photo = 'none'
    # read noiseless Lgal spectra of the spectral_challenge mocks
    specs, meta = Data.Spectra(sim='lgal', noise=noise_spec, lib='bc03', sample='mini_mocha') 
    # read Lgal photometry of the mini_mocha mocks
    photo, _ = Data.Photometry(sim='lgal', noise=noise_photo, lib='bc03', sample='mini_mocha')

    Mstar_input = meta['logM_total'][:97] # total mass 
    Z_MW_input  = meta['Z_MW'][:97]  # mass-weighted metallicity
    tage_input  = meta['t_age_MW'][:97]  # mass-weighted age
    
    theta_inf = [] 
    for igal in range(97): 
        # read best-fit file and get inferred parameters
        _fbf = Fbestfit_specphoto(igal, noise=noise, method=method) 
        fbf = h5py.File(_fbf, 'r')  

        theta_inf_i = np.array([
            fbf['theta_2sig_minus'][...], 
            fbf['theta_1sig_minus'][...], 
            fbf['theta_med'][...], 
            fbf['theta_1sig_plus'][...], 
            fbf['theta_2sig_plus'][...]])
        theta_inf.append(theta_inf_i) 
    theta_inf = np.array(theta_inf) 
    
    # inferred properties
    Mstar_inf   = theta_inf[:,:,0]
    Z_MW_inf    = 10**theta_inf[:,:,1]
    tage_inf    = theta_inf[:,:,2]
    
    fig = plt.figure(figsize=(15,4))
    # compare total stellar mass 
    sub = fig.add_subplot(131) 
    sub.errorbar(Mstar_input, Mstar_inf[:,2], 
            yerr=[Mstar_inf[:,2]-Mstar_inf[:,1], Mstar_inf[:,3]-Mstar_inf[:,2]], fmt='.C0')
    sub.plot([9., 12.], [9., 12.], c='k', ls='--') 
    sub.set_xlabel(r'input $\log~M_{\rm tot}$', fontsize=25)
    sub.set_xlim(9., 12.) 
    sub.set_ylabel(r'inferred $\log~M_{\rm tot}$', fontsize=25)
    sub.set_ylim(9., 12.) 
    
    # compare metallicity
    sub = fig.add_subplot(132)
    sub.errorbar(Z_MW_input, Z_MW_inf[:,2], 
            yerr=[Z_MW_inf[:,2]-Z_MW_inf[:,1], Z_MW_inf[:,3]-Z_MW_inf[:,2]], fmt='.C0')
    sub.plot([1e-3, 1], [1e-3, 1.], c='k', ls='--') 
    sub.set_xlabel(r'input MW $Z$', fontsize=20)
    sub.set_xscale('log') 
    sub.set_xlim(1e-3, 5e-2) 
    sub.set_ylabel(r'inferred MW $Z$', fontsize=20)
    sub.set_yscale('log') 
    sub.set_ylim(1e-3, 5e-2) 

    # compare age 
    sub = fig.add_subplot(133)
    sub.errorbar(tage_input, tage_inf[:,2], 
            yerr=[tage_inf[:,2]-tage_inf[:,1], tage_inf[:,3]-tage_inf[:,2]], fmt='.C0')
    sub.plot([0, 13], [0, 13.], c='k', ls='--') 
    sub.set_xlabel(r'input MW $t_{\rm age}$', fontsize=20)
    sub.set_xlim(0, 13) 
    sub.set_ylabel(r'inferred MW $t_{\rm age}$', fontsize=20)
    sub.set_ylim(0, 13) 

    fig.subplots_adjust(wspace=0.4)
    _ffig = os.path.join(dir_fig, 'mini_mocha.%s.specphotofit.vanilla.noise_%s.png' % (method, noise)) 
    fig.savefig(_ffig, bbox_inches='tight') 
    fig.savefig(UT.fig_tex(_ffig, pdf=True), bbox_inches='tight') 
    return None 


def photo_vs_specphoto(noise_photo='legacy', noise_specphoto='bgs0_legacy', method='ifsps', sfr='1gyr'):  
    ''' Compare properties inferred from photometry versus spectrophotometry to see how much
    information is gained from adding spectra
    '''
    assert noise_specphoto.split('_')[1] == noise_photo
    # read noiseless Lgal spectra of the spectral_challenge mocks
    specs, meta = Data.Spectra(sim='lgal', noise=noise_specphoto.split('_')[0], lib='bc03', sample='mini_mocha') 
    # read Lgal photometry of the mini_mocha mocks
    photo, _ = Data.Photometry(sim='lgal', noise=noise_specphoto.split('_')[1], lib='bc03', sample='mini_mocha')

    Mstar_input = np.array(meta['logM_total'][:97]) # total mass 
    logSFR_input= np.log10(np.array(meta['sfr_%s' % sfr][:97])) 
    Z_MW_input  = meta['Z_MW'][:97]  # mass-weighted metallicity
    tage_input  = meta['t_age_MW'][:97]  # mass-weighted age
    
    theta_inf_photo, theta_inf_specphoto = [], []
    for igal in range(97): 
        # read best-fit file and get inferred parameters from photometry
        _fbf = Fbestfit_photo(igal, noise=noise_photo, method=method) 
        fbf = h5py.File(_fbf, 'r')  

        theta_inf_i = np.array([
            fbf['theta_2sig_minus'][...], 
            fbf['theta_1sig_minus'][...], 
            fbf['theta_med'][...], 
            fbf['theta_1sig_plus'][...], 
            fbf['theta_2sig_plus'][...]])

        # calculate average SFR
        if method == 'ifsps': 
            ifsps = Fitters.iFSPS()
            if sfr == '1gyr': 
                sfr_inf = ifsps._SFR_MCMC(fbf['mcmc_chain'][...], dt=1.)
            elif sfr == '100myr': 
                sfr_inf = ifsps._SFR_MCMC(fbf['mcmc_chain'][...], dt=0.1)
            theta_inf_i = np.concatenate([theta_inf_i, np.atleast_2d(sfr_inf).T], axis=1) 

        theta_inf_photo.append(theta_inf_i) 

        # read best-fit file and get inferred parameters from spectrophoto
        _fbf = Fbestfit_specphoto(igal, noise=noise_specphoto, method=method) 
        fbf = h5py.File(_fbf, 'r')  

        theta_inf_i = np.array([
            fbf['theta_2sig_minus'][...], 
            fbf['theta_1sig_minus'][...], 
            fbf['theta_med'][...], 
            fbf['theta_1sig_plus'][...], 
            fbf['theta_2sig_plus'][...]])
        
        if method == 'ifsps': 
            ifsps = Fitters.iFSPS()
            if sfr == '1gyr': 
                sfr_inf = ifsps._SFR_MCMC(fbf['mcmc_chain'][...], dt=1.)
            elif sfr == '100myr': 
                sfr_inf = ifsps._SFR_MCMC(fbf['mcmc_chain'][...], dt=0.1)
            theta_inf_i = np.concatenate([theta_inf_i, np.atleast_2d(sfr_inf).T], axis=1) 

        theta_inf_specphoto.append(theta_inf_i) 
    theta_inf_photo = np.array(theta_inf_photo) 
    theta_inf_specphoto = np.array(theta_inf_specphoto) 
    
    # inferred properties
    Mstar_inf_photo = theta_inf_photo[:,:,0]
    Mstar_inf_specphoto = theta_inf_specphoto[:,:,0]

    Mbins = np.linspace(9., 12., 16) 
    Mbin_mid = [] 
    dMstar_photo, sig_dMstar_photo = [], []
    dMstar_specphoto, sig_dMstar_specphoto = [], [] 
    for i_m in range(len(Mbins)-1): 
        inmbin = ((Mstar_input > Mbins[i_m]) & (Mstar_input <= Mbins[i_m+1])) 
        if np.sum(inmbin) == 0: continue 
        Mbin_mid.append(0.5 * (Mbins[i_m] + Mbins[i_m+1])) 

        dMstar_photo.append(np.average(Mstar_inf_photo[:,2][inmbin] - Mstar_input[inmbin])) 
        dMstar_specphoto.append(np.average(Mstar_inf_specphoto[:,2][inmbin] - Mstar_input[inmbin])) 

        sig_dMstar_photo.append(
                np.sqrt(np.sum(
                    np.max([Mstar_input[inmbin] - Mstar_inf_photo[inmbin,1], 
                        Mstar_inf_photo[inmbin,3] - Mstar_input[inmbin]], axis=1)
                    ))/np.float(np.sum(inmbin)))
        sig_dMstar_specphoto.append(
                np.sqrt(np.sum(
                    np.max([Mstar_input[inmbin] - Mstar_inf_specphoto[inmbin,1], 
                        Mstar_inf_specphoto[inmbin,3] - Mstar_input[inmbin]], axis=1)
                    ))/np.float(np.sum(inmbin)))
    dMstar_photo = np.array(dMstar_photo) 
    sig_dMstar_photo = np.array(sig_dMstar_photo) 
    dMstar_specphoto = np.array(dMstar_specphoto) 
    sig_dMstar_specphoto = np.array(sig_dMstar_specphoto) 
    
    # inferred SFRs
    logSFR_inf_photo        = np.log10(theta_inf_photo[:,:,-1]) 
    logSFR_inf_specphoto    = np.log10(theta_inf_specphoto[:,:,-1]) 

    # calculate delta log SFR 
    logSFRbins = np.linspace(-3., 3., 25) 
    logSFRbin_mid = [] 
    dlogSFR_photo, sig_dlogSFR_photo = [], []
    dlogSFR_specphoto, sig_dlogSFR_specphoto = [], [] 
    for i_m in range(len(Mbins)-1): 
        inbin = ((logSFR_input > logSFRbins[i_m]) & (logSFR_input <= logSFRbins[i_m+1])) 
        if sfr == '1gyr': 
            inbin = inbin & (np.array(tage_input) > 1.0) 
        elif sfr == '100myr': 
            inbin = inbin & (np.array(tage_input) > 0.1)
        if np.sum(inbin) == 0: continue 
        logSFRbin_mid.append(0.5 * (logSFRbins[i_m] + logSFRbins[i_m+1])) 

        dlogSFR_photo.append(np.average(logSFR_inf_photo[:,2][inbin] - logSFR_input[inbin])) 
        dlogSFR_specphoto.append(np.average(logSFR_inf_specphoto[:,2][inbin] - logSFR_input[inbin])) 

        sig_dlogSFR_photo.append(
                np.sqrt(np.sum(
                    np.max([logSFR_input[inbin] - logSFR_inf_photo[inbin,1], 
                        logSFR_inf_photo[inbin,3] - logSFR_input[inbin]], axis=1)
                    ))/np.float(np.sum(inbin)))
        sig_dlogSFR_specphoto.append(
                np.sqrt(np.sum(
                    np.max([logSFR_input[inbin] - logSFR_inf_specphoto[inbin,1], 
                        logSFR_inf_specphoto[inbin,3] - logSFR_input[inbin]], axis=1)
                    ))/np.float(np.sum(inbin)))
    dlogSFR_photo = np.array(dlogSFR_photo) 
    sig_dlogSFR_photo = np.array(sig_dlogSFR_photo) 
    dlogSFR_specphoto = np.array(dlogSFR_specphoto) 
    sig_dlogSFR_specphoto = np.array(sig_dlogSFR_specphoto) 


    fig = plt.figure(figsize=(12,5))
    # compare total stellar mass 
    sub = fig.add_subplot(121) 
    sub.plot([9., 12.], [0., 0.], c='k', ls='--')
    sub.fill_between(Mbin_mid, dMstar_photo - sig_dMstar_photo, dMstar_photo + sig_dMstar_photo, 
            fc='C0', ec='none', alpha=0.5, label='Photometry only') 
    sub.scatter(Mbin_mid, dMstar_photo, c='C0', s=2) 
    sub.plot(Mbin_mid, dMstar_photo, c='C0') 
    sub.fill_between(Mbin_mid, dMstar_specphoto - sig_dMstar_specphoto, dMstar_specphoto + sig_dMstar_specphoto, 
            fc='C1', ec='none', alpha=0.5, label='Photometry+Spectroscopy') 
    sub.scatter(Mbin_mid, dMstar_specphoto, c='C1', s=1) 
    sub.plot(Mbin_mid, dMstar_specphoto, c='C1') 
    #sub.scatter(Mstar_input, (Mstar_inf_photo[:,2]-Mstar_input), c='C0')
    #sub.scatter(Mstar_input, (Mstar_inf_specphoto[:,2]-Mstar_input), c='C1')
    sub.set_xlabel(r'$\log(~M_{\rm tot}~[M_\odot]~)$', fontsize=25)
    sub.set_xlim(9., 12.) 
    sub.set_ylabel(r'$\log(~\widehat{M}_{\rm tot} / M_{\rm tot}~)$', fontsize=25)
    sub.set_ylim(-1., 1.) 
    sub.legend(loc='upper right', fontsize=20, handletextpad=0.2) 
    
    # compare SFR 
    sub = fig.add_subplot(122) 
    sub.plot([-3., 3.], [0., 0.], c='k', ls='--')
    sub.fill_between(logSFRbin_mid, dlogSFR_photo - sig_dlogSFR_photo, dlogSFR_photo + sig_dlogSFR_photo, 
            fc='C0', ec='none', alpha=0.5, label='Photometry only') 
    sub.scatter(logSFRbin_mid, dlogSFR_photo, c='C0', s=2) 
    sub.plot(logSFRbin_mid, dlogSFR_photo, c='C0') 
    sub.fill_between(logSFRbin_mid, dlogSFR_specphoto - sig_dlogSFR_specphoto, dlogSFR_specphoto + sig_dlogSFR_specphoto, 
            fc='C1', ec='none', alpha=0.5, label='Photometry+Spectroscopy') 
    sub.scatter(logSFRbin_mid, dlogSFR_specphoto, c='C1', s=1) 
    sub.plot(logSFRbin_mid, dlogSFR_specphoto, c='C1') 
    
    if sfr == '1gyr': lbl_sfr = '1Gyr'
    elif sfr == '100myr': lbl_sfr = '100Myr'
    sub.set_xlabel(r'$\log(~{\rm SFR}_{%s}~[M_\odot/yr]~)$' % lbl_sfr, fontsize=25)
    sub.set_xlim(-3., 1.) 
    sub.set_ylabel(r'$\log(~\widehat{\rm SFR}_{%s} / {\rm SFR}_{%s}~)$' % (lbl_sfr, lbl_sfr), fontsize=25)
    sub.set_ylim(-3., 3.) 
    #sub.legend(loc='upper right', fontsize=20, handletextpad=0.2) 
    
    fig.subplots_adjust(wspace=0.3)
    _ffig = os.path.join(dir_fig, 'photo_vs_specphoto.%s.sfr_%s.vanilla.noise_%s_%s.png' % (method, sfr, noise_photo, noise_specphoto)) 
    fig.savefig(_ffig, bbox_inches='tight') 
    fig.savefig(UT.fig_tex(_ffig, pdf=True), bbox_inches='tight') 
    return None 


def Fbestfit_spec(igal, noise='none', method='ifsps'): 
    ''' file name of best-fit of spectra of spectral_challenge galaxy #igal 

    :param igal: 
        index of spectral_challenge galaxy 

    :param noise:
        noise of the spectra. If noise == 'none', no noise. If noise =='bgs0' - 'bgs7', 
        then BGS like noise. (default: 'none') 

    :param dust: 
        spectra has dust or not. 
    
    :param method: 
        fitting method. (default: ifsps)

    '''
    model = 'vanilla'
    if method == 'ifsps': 
        f_bf = os.path.join(UT.dat_dir(), 'mini_mocha', 'ifsps', 'lgal.spec.noise_%s.%s.%i.hdf5' % (noise, model, igal))
    elif method == 'pfirefly': 
        f_bf = os.path.join(UT.dat_dir(), 'mini_mocha', 'pff', 'lgal.spec.noise_%s.%s.%i.hdf5' % (noise, model, igal))
    return f_bf


def Fbestfit_photo(igal, noise='none', method='ifsps'): 
    ''' file name of best-fit of photometry of spectral_challenge galaxy #igal

    :param igal: 
        index of spectral_challenge galaxy 

    :param noise:
        noise of the spectra. If noise == 'none', no noise. If noise =='legacy', 
        then legacy like noise. (default: 'none') 

    :param dust: 
        spectra has dust or not. 
    
    :param method: 
        fitting method. (default: ifsps)
    '''
    model = 'vanilla'

    if method == 'ifsps': 
        f_bf = os.path.join(UT.dat_dir(), 'mini_mocha', 'ifsps', 'lgal.photo.noise_%s.%s.%i.hdf5' % (noise, model, igal))
    elif method == 'pfirefly': 
        f_bf = os.path.join(UT.dat_dir(), 'mini_mocha', 'pff', 'lgal.photo.noise_%s.%s.%i.hdf5' % (noise, model, igal))
    return f_bf


def Fbestfit_specphoto(igal, noise='bgs0_legacy', method='ifsps'): 
    ''' file name of best-fit of photometry of spectral_challenge galaxy #igal

    :param igal: 
        index of spectral_challenge galaxy 

    :param noise:
        noise of the spectra. If noise == 'none', no noise. If noise =='legacy', 
        then legacy like noise. (default: 'none') 

    :param dust: 
        spectra has dust or not. 
    
    :param method: 
        fitting method. (default: ifsps)
    '''
    model = 'vanilla'   
    f_bf = os.path.join(UT.dat_dir(), 'mini_mocha', 'ifsps', 'lgal.specphoto.noise_%s.%s.%i.hdf5' % (noise, model, igal))
    return f_bf


if __name__=="__main__": 
    #mock_challenge_photo(noise='none', dust=False, method='ifsps')
    #mock_challenge_photo(noise='none', dust=True, method='ifsps')
    #mock_challenge_photo(noise='legacy', dust=False, method='ifsps')
    #mock_challenge_photo(noise='legacy', dust=True, method='ifsps')

    #mini_mocha_spec(noise='bgs0', method='ifsps')
    #mini_mocha_spec(noise='bgs0', method='pfirefly')
    #mini_mocha_photo(noise='legacy', method='ifsps')
    #mini_mocha_specphoto(noise='bgs0_legacy', method='ifsps')
    
    #photo_vs_specphoto(noise_photo='legacy', noise_specphoto='bgs0_legacy', method='ifsps', sfr='1gyr')
    #photo_vs_specphoto(noise_photo='legacy', noise_specphoto='bgs0_legacy', method='ifsps', sfr='100myr')
