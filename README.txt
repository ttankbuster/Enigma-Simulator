
  ______ _   _ _____ _____ __  __          
 |  ____| \ | |_   _/ ____|  \/  |   /\    
 | |__  |  \| | | || |  __| \  / |  /  \   
 |  __| | . ` | | || | |_ | |\/| | / /\ \  
 | |____| |\  |_| || |__| | |  | |/ ____ \ 
 |______|_| \_|_____\_____|_|  |_/_/    \_\
                                           
___________________________________________


ENIGMA SIMULATOR V1

CREATED 20/06/24 BY TEDDY SWINGLER

> LEGAL
all work for this enigma project is available under the creative commons licence "CC BY 4.0 ATTRIBUTION 4.0 INTERNATIONAL"
which can be found here: https://creativecommons.org/licenses/by/4.0/ and is repeated here:
- You are free to:
	Share — copy and redistribute the material in any medium or format for any purpose, even commercially.
	Adapt — remix, transform, and build upon the material for any purpose, even commercially.
	The licensor cannot revoke these freedoms as long as you follow the license terms.
- Under the following terms:
	Attribution — You must give appropriate credit , provide a link to the license, and indicate if changes were made . You may do so in any reasonable 		manner, but not in any way that suggests the licensor endorses you or your use.
- No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.
- Notices:
	You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable exception or limitation .
No warranties are given. The license may not give you all of the permissions necessary for your intended use. For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.
> HOW TO USE
All enigma machine instantiations use a "seed", this seed represents how a real enigma machine would be setup (how its plugboard is wired, the order that the rotors are in and the initial rotor positions). A seed is by default, randomly generated. Although you can specify a seed to be used in runtime with a flag (see FLAGS). Any alphabetic key typed into the machine will simulate the internal circuitry of the enigma machine, When a key is pressed a lamp on the lapboard should illuminate the ciphered letter. The first rotor will then increment. Once any rotor to the right has fully cycled, the next rotor will also increment (so the first rotor will cycle every key press, the next every 26th keypress, and so on.)

The seed's format is as follows:
 - The seed is a continuous string of 32 characters in total.
 - The first 6 characters (rotor information) are in the pattern of digit-letter pairs.
 - The remaining 26 characters (plugboard information) are all uppercase letters.
- Rotor Information:
    - The first part of the seed consists of exactly 6 characters.
    - These 6 characters together represent the 3 rotors with a pair of characters.
    - Each pair contains:
        - A single digit which represents the rotor being used (0-4), eg. rotor2 or rotor5.
        - Followed immediately by a single uppercase letter (A-Z) representing the offset of the rotor in the machine, where A is no offset and Z is offset as much as possible before turning all the way back.
- Plugboard Information:
    - The second part of the seed consists of exactly 26 characters, all uppercase letters (A-Z). This is a different ordering of the alphabet, which gets compared to the normal order of the alphabet to substitute one letter with another, as was customary. In a randomly generated seed, a character can sit in the same position in the alphabet as it normally does, this means that it has not be substituted. The first letter will always be a remapping (or lack thereof) of the letter A, either back to itself (no substitution) or to another letter (substitution.)
>> KEYBINDS
- F1: Used to display help information (this section - KEYBINDS)
- Enter: used to reset the enigma machine back to its default settings, as the machine's seed describes. This is effectively resetting it to how it was when the        	program was launched.
- Escape: the escape key will close the program.
- Tab: the tab key can be used to copy the current seed to the clipboard, this action should be displayed by the UI by the seed flashing white.
>> LAUNCHING
the ASSET folder must be in the same directory for the program to run, see CONTENTS for a list of required assets.
>> FLAGS
--seed \<seed\>: used to specify the seed to start the enigma machine with eg. --seed "2E1Z0FZRULWOSNJIXDYHFTVBGPCQEKMA"
--historical_keyboard: used to set the keyboard to a historically accurate keyboard rather than the default QWERTY keyboard. eg. --historical_keyboard=True
> DESCRIPTION
The scope of this project is to simulate the workings of an enigma machine, using a pleasing user interface and an accurate reproduction of what the circuitry would do. The UI features a full QWERTY keyboard, though this is not faithful to the real life enigma machine it is done so as a stylistic choice. To access a historically accurate keyboard, see FLAGS. I will not go into detail about how the machine works, as this is documented extensively by others, (see "https://cryptomuseum.com/crypto/enigma/working.htm" for a detailed explanation) and the degree to which my project succeeds technically is how well it can reproduce the workings of a real enigma machine. I am unaware as of 20/06/24 of any inaccuracies in the simulation, if you find any please comment letting me know. Another thing, if anyone reading this knows how to compile a single file with all of the assets included in the executable so that the accompanying folder is not needed, please again, let me know. This simulates the Enigma model 1, used by the German army during WWII. As such I have implemented 5 rotors with cross-wiring as follows:
- ROTOR_CROSSWIRE1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
- ROTOR_CROSSWIRE2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
- ROTOR_CROSSWIRE3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
- ROTOR_CROSSWIRE4 = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
- ROTOR_CROSSWIRE5 = "VZBRGITYUPSDNHLXAWMJQOFECK"
This recreates the cross-wiring inside of each of the rotors. The offset of the rotor will also change how the rotor is involved in the cipher, this is displayed next to each rotor in the UI. The plugboard is also heavily involved in the final cipher.
>> CONTENTS
The ASSET folder should contain the following:
- ENIGMA_BACKGROUND.png
- icon.ico (the icon image used by the executable file and window)
- ROTOR.png (the image for a stationary rotor
- ROTOR_TURNING.png
- source.fig (a figma file containing all the work for the UI, yes I used figma to make the UI.)
- KEYS (a folder which contains all of the lamp images A-Z for ON and OFF folders respectively)
	- ON
	- OFF
- LAMPS (a folder which contains all of the lamp images A-Z for ON and OFF folders respectively)
	- ON
	- OFF