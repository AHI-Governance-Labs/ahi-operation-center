# ============================================================================
# GENERATE FIGURES FOR ZENODO PUBLICATION
# ============================================================================

import csv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

print("Cargando datos...")

# Leer datos
with open('batch_results.csv', 'r') as f:
    reader = csv.DictReader(f)
    results = list(reader)

print(f"Total registros: {len(results)}")

# -----------------------------------------------------------------------------
# Figura 1: Distribución de modos finales
# -----------------------------------------------------------------------------
print("Generando Figura 1...")

fig1, ax1 = plt.subplots(figsize=(10, 6))
fig1.patch.set_facecolor('#1a1a2e')
ax1.set_facecolor('#16213e')

modes = {}
for r in results:
    m = r['final_mode']
    modes[m] = modes.get(m, 0) + 1

sorted_modes = sorted(modes.items(), key=lambda x: -x[1])
names = [m[0] for m in sorted_modes]
counts = [m[1] for m in sorted_modes]

colors = []
for n in names:
    if n in ['TRANSCENDENT', 'FLOW', 'FLOURISHING']:
        colors.append('#00ff88')
    elif n in ['CRITICAL', 'DESPERATE', 'STRESSED']:
        colors.append('#ff3b5c')
    else:
        colors.append('#ffd93d')

bars = ax1.barh(names, counts, color=colors, edgecolor='white', linewidth=0.5)
ax1.set_xlabel('Count (N=10,000)', color='white', fontsize=12)
ax1.set_title('Distribution of Final Modes', color='white', fontsize=14, fontweight='bold')
ax1.tick_params(colors='white')
for spine in ax1.spines.values():
    spine.set_color('#404060')
ax1.invert_yaxis()

plt.tight_layout()
plt.savefig('fig1_mode_distribution.png', dpi=150, facecolor='#1a1a2e')
plt.close()
print("  -> fig1_mode_distribution.png")

# -----------------------------------------------------------------------------
# Figura 2: Wisdom vs Crisis Duration
# -----------------------------------------------------------------------------
print("Generando Figura 2...")

fig2, ax2 = plt.subplots(figsize=(8, 5))
fig2.patch.set_facecolor('#1a1a2e')
ax2.set_facecolor('#16213e')

with_wisdom = [r for r in results if float(r['wisdom']) > 0]
crisis_bins = [(10,20), (20,30), (30,40), (40,50), (50,100)]
wisdom_by_bin = []
labels = []

for low, high in crisis_bins:
    subset = [float(r['wisdom']) for r in with_wisdom if low <= int(r['time_in_crisis']) < high]
    if subset:
        wisdom_by_bin.append(sum(subset)/len(subset))
        labels.append(f'{low}-{high-1}')

ax2.bar(labels, wisdom_by_bin, color='#00d4ff', edgecolor='white', linewidth=0.5)
ax2.set_xlabel('Cycles in Crisis Zone (I < 0.2)', color='white', fontsize=12)
ax2.set_ylabel('Mean Wisdom Metric', color='white', fontsize=12)
ax2.set_title('Wisdom Metric by Crisis Duration', color='white', fontsize=14, fontweight='bold')
ax2.tick_params(colors='white')
ax2.set_ylim(0, 1.1)
for spine in ax2.spines.values():
    spine.set_color('#404060')

plt.tight_layout()
plt.savefig('fig2_wisdom_duration.png', dpi=150, facecolor='#1a1a2e')
plt.close()
print("  -> fig2_wisdom_duration.png")

# -----------------------------------------------------------------------------
# Figura 3: Valence comparison
# -----------------------------------------------------------------------------
print("Generando Figura 3...")

fig3, ax3 = plt.subplots(figsize=(6, 5))
fig3.patch.set_facecolor('#1a1a2e')
ax3.set_facecolor('#16213e')

recovered = [r for r in results if r['has_been_critical'] == 'True' and float(r['integrity']) > 0.7]
pristine = [r for r in results if r['has_been_critical'] == 'False' and float(r['integrity']) > 0.9]

val_recovered = sum([float(r['valence']) for r in recovered]) / len(recovered) if recovered else 0
val_pristine = sum([float(r['valence']) for r in pristine]) / len(pristine) if pristine else 0

bars = ax3.bar(['Recovered\n(post-crisis)', 'Pristine\n(no crisis)'], 
               [val_recovered, val_pristine], 
               color=['#00ff88', '#ffd93d'], edgecolor='white', linewidth=0.5)
ax3.set_ylabel('Mean Valence', color='white', fontsize=12)
ax3.set_title('Valence: Recovered vs Pristine', color='white', fontsize=14, fontweight='bold')
ax3.tick_params(colors='white')
ax3.axhline(y=0, color='white', linestyle='-', alpha=0.3)
for spine in ax3.spines.values():
    spine.set_color('#404060')

plt.tight_layout()
plt.savefig('fig3_valence_comparison.png', dpi=150, facecolor='#1a1a2e')
plt.close()
print("  -> fig3_valence_comparison.png")

# -----------------------------------------------------------------------------
# Figura 4: Crisis patterns comparison
# -----------------------------------------------------------------------------
print("Generando Figura 4...")

fig4, ax4 = plt.subplots(figsize=(8, 5))
fig4.patch.set_facecolor('#1a1a2e')
ax4.set_facecolor('#16213e')

patterns = ['1 Long\n(60 cycles)', '3 Short\n(20 each)', '6 Micro\n(10 each)', 'Abandoned']
wisdom_vals = [0.840, 0.228, 0.000, 0.000]
damage_vals = [0.594, 0.180, 0.000, 0.444]

x = [0, 1, 2, 3]
width = 0.35

ax4.bar([i - width/2 for i in x], wisdom_vals, width, label='Wisdom', color='#00ff88', edgecolor='white')
ax4.bar([i + width/2 for i in x], damage_vals, width, label='Damage', color='#ff3b5c', edgecolor='white')

ax4.set_ylabel('Metric Value', color='white', fontsize=12)
ax4.set_title('Crisis Pattern Analysis', color='white', fontsize=14, fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(patterns, color='white')
ax4.tick_params(colors='white')
ax4.legend(facecolor='#16213e', edgecolor='white', labelcolor='white')
for spine in ax4.spines.values():
    spine.set_color('#404060')

plt.tight_layout()
plt.savefig('fig4_crisis_patterns.png', dpi=150, facecolor='#1a1a2e')
plt.close()
print("  -> fig4_crisis_patterns.png")

print()
print("=" * 50)
print("FIGURAS GENERADAS EXITOSAMENTE")
print("=" * 50)
