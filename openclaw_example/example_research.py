#!/usr/bin/env python3
"""
OpenClaw Example - Research Orchestration
Demonstrates how multiple agents collaborate on a research task
"""

import sys
from orchestrator import OpenClawOrchestrator


def example_1_ai_healthcare():
    """Example 1: Research AI in healthcare"""
    print("\n" + "="*70)
    print("EXAMPLE 1: AI in Healthcare")
    print("="*70)
    
    orchestrator = OpenClawOrchestrator(model="granite4:micro")
    
    result = orchestrator.run_research(
        topic="The impact of artificial intelligence on healthcare"
    )
    
    if result.success:
        print("\n" + "="*70)
        print("FINAL RESEARCH REPORT")
        print("="*70)
        print(result.final_output)
        print("\n" + "="*70)
        print(f"✓ Research completed in {result.execution_time:.2f}s")
        print("="*70)
    else:
        print(f"\n❌ Research failed: {result.error}")
    
    return result


def example_2_quantum_computing():
    """Example 2: Research quantum computing"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Quantum Computing")
    print("="*70)
    
    orchestrator = OpenClawOrchestrator(model="granite4:micro")
    
    result = orchestrator.run_research(
        topic="Quantum computing and its potential applications"
    )
    
    if result.success:
        print("\n" + "="*70)
        print("FINAL RESEARCH REPORT")
        print("="*70)
        print(result.final_output)
        print("\n" + "="*70)
        print(f"✓ Research completed in {result.execution_time:.2f}s")
        print("="*70)
    else:
        print(f"\n❌ Research failed: {result.error}")
    
    return result


def example_3_climate_change():
    """Example 3: Research climate change solutions"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Climate Change Solutions")
    print("="*70)
    
    orchestrator = OpenClawOrchestrator(model="granite4:micro")
    
    result = orchestrator.run_research(
        topic="Innovative solutions to combat climate change"
    )
    
    if result.success:
        print("\n" + "="*70)
        print("FINAL RESEARCH REPORT")
        print("="*70)
        print(result.final_output)
        print("\n" + "="*70)
        print(f"✓ Research completed in {result.execution_time:.2f}s")
        print("="*70)
    else:
        print(f"\n❌ Research failed: {result.error}")
    
    return result


def interactive_mode():
    """Interactive mode - user provides research topic"""
    print("\n" + "="*70)
    print("OpenClaw Interactive Research Mode")
    print("="*70)
    print("\nEnter a research topic, and the orchestrator will:")
    print("  1. Create a research plan (Planner Agent)")
    print("  2. Conduct research on each subtask (Researcher Agent)")
    print("  3. Write a comprehensive report (Writer Agent)")
    print("\nType 'quit' to exit")
    print("="*70)
    
    orchestrator = OpenClawOrchestrator(model="granite4:micro")
    
    # Show agent info
    orchestrator.print_agent_info()
    
    while True:
        try:
            topic = input("\nResearch Topic: ").strip()
            
            if not topic:
                continue
            
            if topic.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋\n")
                break
            
            # Run research
            result = orchestrator.run_research(topic)
            
            if result.success:
                print("\n" + "="*70)
                print("FINAL RESEARCH REPORT")
                print("="*70)
                print(result.final_output)
                print("\n" + "="*70)
                print(f"✓ Research completed in {result.execution_time:.2f}s")
                print("="*70)
                
                # Ask if user wants to see individual agent outputs
                show_details = input("\nShow individual agent outputs? (y/n): ").strip().lower()
                if show_details == 'y':
                    print("\n" + "="*70)
                    print("PLANNER OUTPUT")
                    print("="*70)
                    print(result.plan)
                    
                    print("\n" + "="*70)
                    print("RESEARCHER OUTPUT")
                    print("="*70)
                    print(result.research)
            else:
                print(f"\n❌ Research failed: {result.error}")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def main():
    """Main function"""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "example1":
            example_1_ai_healthcare()
        elif mode == "example2":
            example_2_quantum_computing()
        elif mode == "example3":
            example_3_climate_change()
        elif mode == "interactive" or mode == "-i":
            interactive_mode()
        else:
            print(f"Unknown mode: {mode}")
            print("\nUsage:")
            print("  python example_research.py example1      # AI in Healthcare")
            print("  python example_research.py example2      # Quantum Computing")
            print("  python example_research.py example3      # Climate Change")
            print("  python example_research.py interactive   # Interactive mode")
    else:
        # Default: run interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()


# Made with Bob