#!/usr/bin/env python3
"""
NemoClaw Example - Text Analysis Orchestration
Demonstrates how two agents collaborate to summarize and analyze text
"""

import sys
from orchestrator import NemoClawOrchestrator


# Sample texts for examples
SAMPLE_TEXT_AI = """
Artificial intelligence is rapidly transforming the healthcare industry through 
innovative applications in diagnostics, treatment planning, and patient care. 
Machine learning algorithms can now analyze medical images with accuracy that 
rivals or exceeds human radiologists, detecting subtle patterns that might be 
missed by the human eye. In treatment planning, AI systems help oncologists 
design personalized cancer treatment protocols by analyzing vast amounts of 
patient data, genetic information, and clinical research. These systems can 
predict which treatments are most likely to be effective for individual patients, 
reducing trial-and-error approaches and improving outcomes.

Beyond diagnostics and treatment, AI is revolutionizing patient care through 
predictive analytics that can identify patients at risk of complications before 
symptoms appear. Natural language processing enables AI assistants to help 
doctors by automatically extracting relevant information from medical records, 
saving valuable time and reducing administrative burden. Remote monitoring 
systems powered by AI can track patients' vital signs and alert healthcare 
providers to concerning changes, enabling early intervention.

However, the integration of AI in healthcare also raises important questions 
about data privacy, algorithmic bias, and the role of human judgment in medical 
decision-making. As these technologies continue to evolve, healthcare 
organizations must balance innovation with ethical considerations and ensure 
that AI systems augment rather than replace the human touch that is essential 
to quality patient care.
"""

SAMPLE_TEXT_CLIMATE = """
Climate change represents one of the most pressing challenges facing humanity 
in the 21st century. Rising global temperatures, driven primarily by greenhouse 
gas emissions from human activities, are causing widespread environmental 
disruption. The effects are already visible: melting polar ice caps, rising sea 
levels, more frequent and severe weather events, and shifting ecosystems that 
threaten biodiversity.

The scientific consensus is clear: without significant action to reduce carbon 
emissions, the planet will face catastrophic consequences. However, addressing 
climate change requires coordinated global effort across multiple sectors. 
Renewable energy technologies like solar and wind power have become increasingly 
cost-competitive with fossil fuels, offering a viable path toward decarbonization. 
Electric vehicles are gaining market share, and innovations in battery technology 
promise to make them even more practical and affordable.

Beyond technology, addressing climate change requires changes in policy, 
business practices, and individual behavior. Governments must implement carbon 
pricing mechanisms and regulations that incentivize clean energy adoption. 
Businesses need to embrace sustainable practices and transparent reporting of 
their environmental impact. Individuals can contribute through conscious 
consumption choices, energy conservation, and support for climate-friendly 
policies. While the challenge is immense, the combination of technological 
innovation, policy action, and social change offers hope for a sustainable future.
"""

SAMPLE_TEXT_REMOTE_WORK = """
The COVID-19 pandemic accelerated a workplace transformation that was already 
underway: the shift to remote and hybrid work models. What began as an emergency 
response has evolved into a fundamental rethinking of how and where work gets 
done. Many organizations have discovered that remote work can maintain or even 
improve productivity while offering employees greater flexibility and work-life 
balance.

The benefits of remote work extend beyond individual convenience. Companies can 
access talent from anywhere in the world, reducing geographic constraints on 
hiring. Office space costs can be reduced, and employees save time and money 
on commuting. Environmental benefits include reduced carbon emissions from 
transportation. Digital collaboration tools have matured to support effective 
remote teamwork, with video conferencing, project management platforms, and 
cloud-based document sharing becoming standard.

However, remote work also presents challenges. Maintaining company culture and 
fostering innovation can be more difficult when teams are distributed. Some 
employees struggle with isolation or difficulty separating work from personal 
life. Not all jobs can be performed remotely, raising questions about equity. 
Organizations are experimenting with hybrid models that combine remote work 
with periodic in-office collaboration, seeking to capture the benefits of both 
approaches. As this workplace evolution continues, success will depend on 
thoughtful policies, robust technology infrastructure, and a focus on outcomes 
rather than physical presence.
"""


def example_1_ai_healthcare():
    """Example 1: Analyze AI in healthcare text"""
    print("\n" + "="*70)
    print("EXAMPLE 1: AI in Healthcare Analysis")
    print("="*70)
    
    orchestrator = NemoClawOrchestrator(model="granite4:micro")
    
    result = orchestrator.analyze_text(SAMPLE_TEXT_AI)
    
    if result.success:
        print("\n" + "="*70)
        print("COMPLETE ANALYSIS REPORT")
        print("="*70)
        print("\n--- SUMMARY ---")
        print(result.summary)
        print("\n--- ANALYSIS ---")
        print(result.analysis)
        print("\n" + "="*70)
        print(f"✓ Analysis completed in {result.execution_time:.2f}s")
        print("="*70)
    else:
        print(f"\n❌ Analysis failed: {result.error}")
    
    return result


def example_2_climate_change():
    """Example 2: Analyze climate change text"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Climate Change Analysis")
    print("="*70)
    
    orchestrator = NemoClawOrchestrator(model="granite4:micro")
    
    result = orchestrator.analyze_text(SAMPLE_TEXT_CLIMATE)
    
    if result.success:
        print("\n" + "="*70)
        print("COMPLETE ANALYSIS REPORT")
        print("="*70)
        print("\n--- SUMMARY ---")
        print(result.summary)
        print("\n--- ANALYSIS ---")
        print(result.analysis)
        print("\n" + "="*70)
        print(f"✓ Analysis completed in {result.execution_time:.2f}s")
        print("="*70)
    else:
        print(f"\n❌ Analysis failed: {result.error}")
    
    return result


def example_3_remote_work():
    """Example 3: Analyze remote work text"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Remote Work Analysis")
    print("="*70)
    
    orchestrator = NemoClawOrchestrator(model="granite4:micro")
    
    result = orchestrator.analyze_text(SAMPLE_TEXT_REMOTE_WORK)
    
    if result.success:
        print("\n" + "="*70)
        print("COMPLETE ANALYSIS REPORT")
        print("="*70)
        print("\n--- SUMMARY ---")
        print(result.summary)
        print("\n--- ANALYSIS ---")
        print(result.analysis)
        print("\n" + "="*70)
        print(f"✓ Analysis completed in {result.execution_time:.2f}s")
        print("="*70)
    else:
        print(f"\n❌ Analysis failed: {result.error}")
    
    return result


def interactive_mode():
    """Interactive mode - user provides text to analyze"""
    print("\n" + "="*70)
    print("NemoClaw Interactive Analysis Mode")
    print("="*70)
    print("\nEnter text to analyze, and the orchestrator will:")
    print("  1. Extract key points and create a summary (Summarizer Agent)")
    print("  2. Provide insights and recommendations (Analyzer Agent)")
    print("\nType 'quit' to exit")
    print("Type 'paste' to enter multi-line text (end with a line containing only 'END')")
    print("="*70)
    
    orchestrator = NemoClawOrchestrator(model="granite4:micro")
    
    # Show agent info
    orchestrator.print_agent_info()
    
    while True:
        try:
            print("\n" + "-"*70)
            text_input = input("\nText to analyze (or 'paste'/'quit'): ").strip()
            
            if not text_input:
                continue
            
            if text_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋\n")
                break
            
            # Handle multi-line paste mode
            if text_input.lower() == 'paste':
                print("\nPaste your text below. Type 'END' on a new line when done:")
                lines = []
                while True:
                    line = input()
                    if line.strip() == 'END':
                        break
                    lines.append(line)
                text_input = '\n'.join(lines)
                
                if not text_input.strip():
                    print("No text provided. Please try again.")
                    continue
            
            # Run analysis
            result = orchestrator.analyze_text(text_input)
            
            if result.success:
                print("\n" + "="*70)
                print("COMPLETE ANALYSIS REPORT")
                print("="*70)
                print("\n--- SUMMARY ---")
                print(result.summary)
                print("\n--- ANALYSIS ---")
                print(result.analysis)
                print("\n" + "="*70)
                print(f"✓ Analysis completed in {result.execution_time:.2f}s")
                print("="*70)
                
                # Ask if user wants to see individual agent outputs
                show_details = input("\nShow individual agent outputs? (y/n): ").strip().lower()
                if show_details == 'y':
                    print("\n" + "="*70)
                    print("SUMMARIZER OUTPUT")
                    print("="*70)
                    print(result.summary)
                    
                    print("\n" + "="*70)
                    print("ANALYZER OUTPUT")
                    print("="*70)
                    print(result.analysis)
            else:
                print(f"\n❌ Analysis failed: {result.error}")
        
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
            example_2_climate_change()
        elif mode == "example3":
            example_3_remote_work()
        elif mode == "interactive" or mode == "-i":
            interactive_mode()
        else:
            print(f"Unknown mode: {mode}")
            print("\nUsage:")
            print("  python example_analysis.py example1      # AI in Healthcare")
            print("  python example_analysis.py example2      # Climate Change")
            print("  python example_analysis.py example3      # Remote Work")
            print("  python example_analysis.py interactive   # Interactive mode")
    else:
        # Default: run interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()


# Made with Bob