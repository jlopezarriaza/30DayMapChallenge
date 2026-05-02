import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os

def generate_bird_call(duration=3.0, fs=44100):
    """Synthesize a complex bird call (e.g., Northern Cardinal-like sweeps)."""
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    # Base signal
    y = np.zeros_like(t)
    
    # Note 1: Downward sweep (cheer)
    t1_mask = (t > 0.2) & (t < 0.6)
    t1 = t[t1_mask] - 0.2
    # Freq drops from 4000 to 2000
    f1 = 4000 - 5000 * t1
    y[t1_mask] += np.sin(2 * np.pi * f1 * t1)
    
    # Note 2: Downward sweep (cheer)
    t2_mask = (t > 0.8) & (t < 1.2)
    t2 = t[t2_mask] - 0.8
    f2 = 4000 - 5000 * t2
    y[t2_mask] += np.sin(2 * np.pi * f2 * t2)
    
    # Note 3: Fast trill
    t3_mask = (t > 1.5) & (t < 2.5)
    t3 = t[t3_mask] - 1.5
    # Freq modulates rapidly around 3000
    f3 = 3000 + 500 * np.sin(2 * np.pi * 15 * t3)
    y[t3_mask] += np.sin(2 * np.pi * f3 * t3)
    
    # Add some harmonics safely
    y_harmonic = np.zeros_like(t)
    y_harmonic[t1_mask] = 0.4 * np.sin(2 * np.pi * (f1 * 2) * t1)
    y_harmonic[t2_mask] = 0.4 * np.sin(2 * np.pi * (f2 * 2) * t2)
    y_harmonic[t3_mask] = 0.2 * np.sin(2 * np.pi * (f3 * 2.5) * t3)
    
    y += y_harmonic
    
    # Add some natural noise (wind, distant sounds)
    noise = np.random.normal(0, 0.05, len(t))
    
    # Filter noise to be mostly low frequency (wind)
    b, a = signal.butter(4, 1000 / (fs / 2), 'low')
    wind_noise = signal.filtfilt(b, a, noise) * 2
    
    return t, y + wind_noise, fs

def main():
    print("Generating simulated acoustic data (BirdCLEF style)...")
    t, audio, fs = generate_bird_call()
    
    print("Computing Short-Time Fourier Transform (STFT)...")
    # Compute spectrogram
    f, t_spec, Zxx = signal.stft(audio, fs, nperseg=1024, noverlap=768)
    
    # Convert amplitude to Decibels for visualization
    Zxx_db = 20 * np.log10(np.abs(Zxx) + 1e-10)
    
    # Filter out very high frequencies we didn't generate just to make it look clean
    freq_mask = f <= 10000
    f = f[freq_mask]
    Zxx_db = Zxx_db[freq_mask, :]
    
    print("Plotting acoustic raster (Spectrogram)...")
    fig, ax = plt.subplots(figsize=(15, 8))
    fig.patch.set_facecolor('#09090b')
    ax.set_facecolor('#09090b')
    
    # Use a vibrant colormap popular in audio analysis
    im = ax.pcolormesh(t_spec, f, Zxx_db, vmin=-80, vmax=0, shading='gouraud', cmap='magma')
    
    # Style the axes
    ax.set_ylabel('Frequency (Hz)', color='#94a3b8', fontsize=12)
    ax.set_xlabel('Time (s)', color='#94a3b8', fontsize=12)
    ax.tick_params(colors='#94a3b8')
    for spine in ax.spines.values():
        spine.set_color('#1e293b')
        
    ax.set_title("Day 29: Raster - Acoustic Spectrogram (Vocal Visualization)", color='white', fontsize=24, pad=20, fontweight='bold')
    
    # Add a colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label('Power (dB)', color='#94a3b8')
    cbar.ax.yaxis.set_tick_params(color='#94a3b8')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#94a3b8')
    
    ax.text(0.01, 0.95, "Simulated Cardinal Call | Inspired by BirdCLEF 2026", 
            transform=ax.transAxes, ha='left', color='#e2e8f0', fontsize=10, bbox=dict(facecolor='#020617', alpha=0.5, edgecolor='none'))
    
    output_path = os.path.join('2025', 'day_29', 'visualization', 'acoustic_spectrogram.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#09090b')
    print(f"Saved to {output_path}")
    
    # Update README
    readme_content = f"""# Day 29: Raster
Pushing the boundaries of the challenge, this is an **Acoustic Raster**—a spectrogram visualizing the vocalizations of a bird over time. This approach, heavily utilized in machine learning competitions like **BirdCLEF 2026**, represents time on the X-axis, frequency on the Y-axis, and amplitude via color intensity (magma colormap). The signal features simulated frequency sweeps and a rapid trill characteristic of many songbirds, superimposed over low-frequency background noise.

## Visualization
![Acoustic Spectrogram](visualization/acoustic_spectrogram.png)
"""
    with open(os.path.join('2025', 'day_29', 'README.md'), 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
