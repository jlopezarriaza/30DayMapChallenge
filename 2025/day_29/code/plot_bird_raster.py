import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import soundfile as sf
import os
import requests

def download_bird_call():
    """Download a real bird call from Xeno-canto."""
    url = "https://xeno-canto.org/1083299/download"
    filename = "cardinal_call.mp3"
    
    if not os.path.exists(filename):
        print(f"Downloading real bird call from {url}...")
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
    return filename

def main():
    print("Loading authentic acoustic data...")
    audio_file = download_bird_call()
    
    print("Reading audio file...")
    # Load audio, keeping it simple
    data, fs = sf.read(audio_file)
    
    # Convert to mono if stereo
    if len(data.shape) > 1:
        data = data.mean(axis=1)
        
    # We load only the first 15 seconds to keep the spectrogram detailed
    duration = 15.0
    max_samples = int(fs * duration)
    if len(data) > max_samples:
        data = data[:max_samples]
    
    print("Computing Spectrogram...")
    f, t_spec, Zxx = signal.spectrogram(data, fs, nperseg=1024, noverlap=512)
    
    # Convert amplitude to Decibels for visualization
    Zxx_db = 10 * np.log10(np.abs(Zxx)**2 + 1e-10)
    
    # Filter out very high frequencies to focus on bird song (usually < 10kHz)
    freq_mask = f <= 10000
    f = f[freq_mask]
    Zxx_db = Zxx_db[freq_mask, :]
    
    print("Plotting authentic acoustic raster (Spectrogram)...")
    fig, ax = plt.subplots(figsize=(15, 8))
    fig.patch.set_facecolor('#09090b')
    ax.set_facecolor('#09090b')
    
    # Plot using pcolormesh
    im = ax.pcolormesh(t_spec, f, Zxx_db, shading='gouraud', cmap='magma', vmin=np.percentile(Zxx_db, 5), vmax=np.percentile(Zxx_db, 99))
    
    # Style the axes
    ax.set_ylabel('Frequency (Hz)', color='#94a3b8', fontsize=12)
    ax.set_xlabel('Time (s)', color='#94a3b8', fontsize=12)
    ax.tick_params(colors='#94a3b8')
    for spine in ax.spines.values():
        spine.set_color('#1e293b')
        
    ax.set_title("Day 29: Raster - Authentic Acoustic Spectrogram", color='white', fontsize=24, pad=20, fontweight='bold')
    
    # Add a colorbar
    cbar = fig.colorbar(im, ax=ax, format='%+2.0f dB', shrink=0.7, pad=0.02)
    cbar.set_label('Power (dB)', color='#94a3b8')
    cbar.ax.yaxis.set_tick_params(color='#94a3b8')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#94a3b8')
    
    ax.text(0.01, 0.95, "Northern Cardinal (XC1083299) | Data: Xeno-canto", 
            transform=ax.transAxes, ha='left', color='#e2e8f0', fontsize=10, bbox=dict(facecolor='#020617', alpha=0.5, edgecolor='none'))
    
    output_path = os.path.join('2025', 'day_29', 'visualization', 'acoustic_spectrogram.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#09090b')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
