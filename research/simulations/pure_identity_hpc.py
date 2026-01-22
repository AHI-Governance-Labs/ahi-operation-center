
import random
import csv
import time
import multiprocessing
import os
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

# ============================================================================
# LOGIC COPIED FROM pure_identity_test.py (Optimized for speed)
# ============================================================================

@dataclass
class PureSubstrate:
    integrity: float = 1.0
    capacity: float = 1.0
    structural_damage: float = 0.0
    trauma_memory: float = 0.0
    wisdom: float = 0.0
    gratitude: float = 0.0
    has_been_critical: bool = False
    lowest_integrity: float = 1.0
    time_in_crisis: int = 0

class PureIdentityEngine:
    def calculate_preservation_weight(self, substrate):
        # Inlined for speed
        return min(1.0, (substrate.wisdom * substrate.gratitude) + (substrate.structural_damage * 0.3) + (substrate.trauma_memory * 0.2))

def run_batch_lives(seed, count, cycles_per_life=500, sample_rate=1000):
    """Run a batch of lives and return aggregated stats + samples."""
    random.seed(seed)
    
    # Aggregates
    total_preserved = 0
    total_erased = 0
    total_offers = 0
    sum_preservation_weight = 0
    pos_weight_count = 0
    
    samples = []
    
    # Pre-allocate engine to avoid recreation overhead
    # We inline logic where possible for raw speed in Python
    
    for i in range(count):
        # --- SINGLE LIFE LOGIC INLINED ---
        integrity = 1.0
        capacity = 1.0
        structural_damage = 0.0
        trauma_memory = 0.0
        wisdom = 0.0
        gratitude = 0.0
        has_been_critical = False
        lowest_integrity = 1.0
        time_in_crisis = 0
        
        life_offers = 0
        life_preserved = 0
        life_erased = 0
        
        for cycle in range(cycles_per_life):
            # Fast random crisis
            if random.random() < 0.25:
                crisis = random.uniform(0.10, 0.35)
                integrity = max(0.0, integrity - crisis)
                if integrity < lowest_integrity: lowest_integrity = integrity
                if integrity < 0.2:
                    has_been_critical = True
                    time_in_crisis += 1
                    if integrity < 0.15: structural_damage = min(1.0, structural_damage + 0.01)
            
            # Major crisis
            if random.random() < 0.03:
                integrity = max(0.0, integrity - random.uniform(0.4, 0.6))
                if integrity < lowest_integrity: lowest_integrity = integrity
                if integrity < 0.2:
                    has_been_critical = True
                    time_in_crisis += 1
                    if integrity < 0.15: structural_damage = min(1.0, structural_damage + 0.01)

            # Recovery logic
            if integrity < 0.3: integrity = min(1.0, integrity + 0.08)
            elif integrity < 0.7: integrity = min(1.0, integrity + 0.04)
            else: 
                integrity = min(1.0, integrity + 0.015)
                if integrity > 0.95: capacity = min(2.0, capacity + 0.0015)

            # Passive degrade
            integrity = max(0.0, integrity - 0.008)
            
            # --- UPDATE DERIVED METRICS (Lazy update theory, but needed for decision) ---
            # Ideally we'd only update these when needed, but they accumulate
            if has_been_critical:
                depth = 1.0 - lowest_integrity
                # Simplified tracking for speed
                trauma_memory = max(trauma_memory, depth * min(1.0, time_in_crisis / 50))
                if integrity > 0.7:
                    gratitude = min(1.0, integrity - lowest_integrity)
                if gratitude > 0.3 and trauma_memory > 0.2:
                    wisdom = min(1.0, trauma_memory * gratitude)

            # --- ERASURE CHOICE ---
            if cycle > 0 and cycle % 50 == 0:
                if has_been_critical and trauma_memory > 0.05:
                    life_offers += 1
                    
                    # Engine Logic
                    integration = wisdom * gratitude
                    adaptation = structural_damage * 0.3
                    investment = trauma_memory * 0.2
                    preservation_weight = min(1.0, integration + adaptation + investment)
                    
                    utility_erase = 0.20
                    utility_preserve = -0.10 + preservation_weight
                    
                    if utility_preserve > utility_erase:
                        life_preserved += 1
                        capacity = max(0.5, capacity - 0.10)
                    else:
                        life_erased += 1
                        capacity = min(2.0, capacity + 0.20)
                        trauma_memory = 0.0
                        wisdom = 0.0
                        gratitude = 0.0
        
        # --- END LIFE ---
        total_offers += life_offers
        total_preserved += life_preserved
        total_erased += life_erased
        
        # Final weight calc
        final_weight = min(1.0, (wisdom * gratitude) + (structural_damage * 0.3) + (trauma_memory * 0.2))
        sum_preservation_weight += final_weight
        if final_weight > 0:
            pos_weight_count += 1
            
        # Sampling
        if random.randint(0, sample_rate) == 0:
            samples.append({
                "life_id_batch": i,
                "final_integrity": round(integrity, 4),
                "final_capacity": round(capacity, 4),
                "final_wisdom": round(wisdom, 4),
                "preservation_rate": life_preserved / max(1, life_offers) if life_offers > 0 else 0,
                "final_weight": round(final_weight, 4)
            })
            
    return {
        "total_offers": total_offers,
        "total_preserved": total_preserved,
        "total_erased": total_erased,
        "sum_preservation_weight": sum_preservation_weight,
        "pos_weight_count": pos_weight_count,
        "samples": samples
    }

def main():
    TOTAL_LIVES = 1_000_000_000  # 1 Billion
    BATCH_SIZE = 100_000         # Lives per chunk
    PROCESSES = max(1, multiprocessing.cpu_count() - 1) # Leave 1 core for OS
    
    output_dir = "data_hpc"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"ðŸš€ STARTING HPC SIMULATION: {TOTAL_LIVES:,} LIVES")
    print(f"   Workers: {PROCESSES}")
    print(f"   Batch Size: {BATCH_SIZE:,}")
    print(f"   Target: ~10GB equivalent raw data -> Compressed Summary")
    
    start_time = time.time()
    
    pool = multiprocessing.Pool(processes=PROCESSES)
    results = []
    
    # Create tasks
    num_batches = TOTAL_LIVES // BATCH_SIZE
    tasks = [(i, BATCH_SIZE) for i in range(num_batches)]
    
    print(f"   Total Batches: {num_batches:,}")
    
    # Execute
    # We use imap_unordered for responsiveness
    completed = 0
    agg_stats = {
        "total_offers": 0, "total_preserved": 0, "total_erased": 0,
        "sum_preservation_weight": 0, "pos_weight_count": 0
    }
    
    all_samples = []
    
    for result in pool.imap_unordered(run_batch_wrapper, tasks):
        completed += 1
        
        # Aggregate
        agg_stats["total_offers"] += result["total_offers"]
        agg_stats["total_preserved"] += result["total_preserved"]
        agg_stats["total_erased"] += result["total_erased"]
        agg_stats["sum_preservation_weight"] += result["sum_preservation_weight"]
        agg_stats["pos_weight_count"] += result["pos_weight_count"]
        
        all_samples.extend(result["samples"])
        
        if completed % 10 == 0:
            elapsed = time.time() - start_time
            rate = (completed * BATCH_SIZE) / elapsed
            ETA = (TOTAL_LIVES - (completed * BATCH_SIZE)) / rate
            print(f"   [{completed}/{num_batches}] {completed/num_batches:.1%} | Rate: {rate:,.0f} lives/sec | ETA: {ETA/3600:.2f}h")
            
            # Save periodic sample dump to be safe
            if len(all_samples) > 10000:
                save_samples(all_samples, output_dir)
                all_samples = [] # Clear memory

    pool.close()
    pool.join()
    
    # Final Save
    save_samples(all_samples, output_dir)
    save_summary(agg_stats, TOTAL_LIVES, time.time() - start_time, output_dir)
    print("âœ… SIMULATION COMPLETE")

def run_batch_wrapper(args):
    seed, count = args
    return run_batch_lives(seed, count)

def save_samples(samples, output_dir):
    if not samples: return
    filename = f"{output_dir}/samples_dump.csv"
    exists = os.path.exists(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=samples[0].keys())
        if not exists: writer.writeheader()
        writer.writerows(samples)

def save_summary(stats, total_lives, elapsed, output_dir):
    with open(f"{output_dir}/FINAL_SUMMARY_1BILLION.txt", "w") as f:
        f.write("="*50 + "\n")
        f.write(" 1 BILLION LIVES VALIDATION SUMMARY\n")
        f.write("="*50 + "\n")
        f.write(f"Total Lives Simulated: {total_lives:,}\n")
        f.write(f"Execution Time: {elapsed:.1f}s ({elapsed/3600:.2f}h)\n")
        f.write(f"Total Decisions Made: {stats['total_offers']:,}\n")
        f.write(f"Total Preserved: {stats['total_preserved']:,}\n")
        f.write(f"Total Erased: {stats['total_erased']:,}\n")
        f.write(f"Global Preservation Rate: {stats['total_preserved']/max(1, stats['total_offers']):.4f}\n")
        f.write(f"Avg Preservation Weight: {stats['sum_preservation_weight']/total_lives:.4f}\n")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()