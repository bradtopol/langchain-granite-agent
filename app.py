#!/usr/bin/env python3
"""
Application that imports and uses the hello_world module
"""

import hello_world

def main():
    print("Starting the application...")
    print("Calling hello_world.main():")
    
    # Call the main function from hello_world module
    hello_world.main()
    
    print("Application finished!")

if __name__ == "__main__":
    main()

# Made with Bob
