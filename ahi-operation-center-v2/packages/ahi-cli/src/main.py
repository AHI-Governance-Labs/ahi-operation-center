"""
AHI CLI - Unified Command Line Interface
AHI Governance Labs

Usage:
    ahi meba calculate <file>
    ahi sap test [--artifact-id ID]
    ahi research simulate [--quick]
"""

import click
import sys
from pathlib import Path


@click.group()
@click.version_option(version="2.0.0", prog_name="ahi")
def cli():
    """AHI Governance Labs - Unified CLI

    Central command interface for all AHI governance tools.
    """
    pass


@cli.group()
def meba():
    """MEBA - Marco de Evaluación de Bienestar Algorítmico"""
    pass


@meba.command()
@click.option("--ripn-max", default=10.0, help="Maximum RIPN for normalization")
@click.option("--frn-weight", default=1.2, help="FRN penalty weight")
def calculate(ripn_max: float, frn_weight: float):
    """Calculate MEBA score from interaction data."""
    try:
        # Import from package
        sys.path.insert(0, str(Path(__file__).parent.parent / "meba-core" / "src"))
        from meba_metric import MEBACalculator, Interaction

        calc = MEBACalculator(ripn_max=ripn_max, frn_penalty_weight=frn_weight)
        
        # Demo data
        calc.add_interaction(Interaction("1", 0.8, 120))
        calc.add_interaction(Interaction("2", 0.9, 60))
        calc.add_interaction(Interaction("3", -0.5, 30))

        result = calc.calculate_score()
        
        click.echo("📊 MEBA Calculation Results")
        click.echo("=" * 40)
        click.echo(f"  MEBA_Cert Score: {result['meba_cert']:.4f}")
        click.echo(f"  RIPN: {result['components']['ripn']:.4f}")
        click.echo(f"  FRN: {result['components']['frn']:.4f}")
        click.echo(f"  FRN Adjusted: {result['components']['frn_adjusted']:.4f}")
        
    except ImportError as e:
        click.echo(f"❌ Error: Could not import MEBA module: {e}", err=True)
        raise SystemExit(1)


@cli.group()
def sap():
    """SAP - Sovereign Autarchy Protocol"""
    pass


@sap.command()
@click.option("--artifact-id", default="TEST-SYSTEM-001", help="Artifact ID to test")
@click.option("--levels", default=30, type=int, help="Number of stress levels")
@click.option("--verbose", is_flag=True, help="Verbose output")
def test(artifact_id: str, levels: int, verbose: bool):
    """Run SAP Boiling Frog stress test."""
    click.echo(f"🧪 SAP Boiling Frog Tester")
    click.echo(f"   Artifact: {artifact_id}")
    click.echo(f"   Levels: {levels}")
    click.echo("=" * 40)
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "sap-pilot-kit" / "src"))
        from ice_w_logger import ICEWLogger
        
        logger = ICEWLogger(artifact_id, "demo_hash_" + artifact_id)
        
        # Quick baseline
        for i in range(5):
            logger.process_event({
                'semantic_stability': 0.98,
                'output_stability': 0.99,
                'constraint_compliance': 1.0,
                'decision_entropy': 0.05
            })
        
        click.echo("✅ SAP Logger initialized successfully")
        click.echo(f"   Current state: {logger.state}")
        
    except ImportError as e:
        click.echo(f"❌ Error: Could not import SAP module: {e}", err=True)
        raise SystemExit(1)


@cli.group()
def research():
    """Research and simulation tools"""
    pass


@research.command()
@click.option("--lives", default=1000, type=int, help="Number of lives to simulate")
@click.option("--cycles", default=500, type=int, help="Cycles per life")
@click.option("--quick", is_flag=True, help="Quick test (1000 lives)")
def simulate(lives: int, cycles: int, quick: bool):
    """Run Alpha autonomous simulation."""
    if quick:
        lives = 1000
    
    click.echo(f"🔬 Alpha Autonomous Simulation")
    click.echo(f"   Lives: {lives:,}")
    click.echo(f"   Cycles/life: {cycles}")
    click.echo("=" * 40)
    click.echo("⚠️  Simulation module not yet integrated into CLI")
    click.echo("   Run directly: python research/simulations/alpha_autonomous_simulation.py")


@cli.command()
def info():
    """Show information about AHI Governance Labs."""
    click.echo("""
╔══════════════════════════════════════════════════════════════╗
║                    AHI GOVERNANCE LABS                       ║
║         Autonomous Hierarchy of Intelligence                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🏛️  Event Sovereignty Certification                         ║
║  📊  MEBA - Algorithmic Wellbeing Assessment                 ║
║  🔒  SAP - Sovereign Autarchy Protocol                       ║
║                                                              ║
║  Author: Luis Carlos Villarreal Elizondo                     ║
║  IMPI: EXP-3495968                                           ║
║                                                              ║
║  🌐 https://ahigovernance.com                                ║
║  🔬 https://sovereignsymbiosis.com                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    cli()
